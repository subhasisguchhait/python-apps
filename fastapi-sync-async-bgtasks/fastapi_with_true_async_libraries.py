"""
FastAPI demo: TRUE async stack
- aiosqlite              -> async SQLite driver
- httpx.AsyncClient      -> async HTTP client

Demonstrates:
1) /async-true        -> fully async DB + HTTP (best for high concurrency I/O)
2) /bg-async          -> BackgroundTasks runs after response (uses sync wrapper + asyncio.run)
3) /cpu-async-bad     -> CPU-bound work inside async blocks event loop (anti-pattern)
4) /cpu-to-thread     -> CPU-bound work offloaded to thread (recommended)

Install:
  pip install fastapi uvicorn httpx aiosqlite

Run:
  uvicorn main:app --reload
"""

from __future__ import annotations

import asyncio
import time
from datetime import datetime
from typing import Any, Dict

import aiosqlite
import httpx
from fastapi import BackgroundTasks, FastAPI

DB_PATH = "demo_async.db"

app = FastAPI(title="TRUE async: aiosqlite + httpx.AsyncClient")


def ts() -> str:
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


# ----------------------------
# Async DB helpers (aiosqlite)
# ----------------------------
async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS hits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        await conn.commit()


async def insert_hit(endpoint: str) -> int:
    async with aiosqlite.connect(DB_PATH) as conn:
        cur = await conn.execute(
            "INSERT INTO hits(endpoint, created_at) VALUES(?, ?)",
            (endpoint, ts()),
        )
        await conn.commit()
        return int(cur.lastrowid)


async def count_hits() -> int:
    async with aiosqlite.connect(DB_PATH) as conn:
        cur = await conn.execute("SELECT COUNT(*) FROM hits")
        row = await cur.fetchone()
        return int(row[0])


# ----------------------------
# Async HTTP helper (httpx)
# ----------------------------
async def call_httpbin(delay_s: float) -> Dict[str, Any]:
    """
    Calls httpbin delay endpoint asynchronously.
    """
    delay_s = float(delay_s)
    if delay_s < 0 or delay_s > 10:
        raise ValueError("delay_s must be between 0 and 10")

    url = f"https://httpbin.org/delay/{int(delay_s)}"
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()


# ----------------------------
# Startup
# ----------------------------
@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


# ============================================================
# 1) TRUE ASYNC endpoint: aiosqlite + httpx.AsyncClient
# ============================================================
@app.get("/async-true")
async def async_true(delay_s: float = 3.0) -> Dict[str, Any]:
    """
    Fully async I/O:
    - DB insert/read via aiosqlite
    - External HTTP via httpx.AsyncClient

    While awaiting DB/HTTP, the event loop can serve other requests.
    """
    started = ts()

    hit_id = await insert_hit("/async-true")
    total = await count_hits()
    http_data = await call_httpbin(delay_s)

    finished = ts()
    return {
        "endpoint": "/async-true",
        "type": "true async (aiosqlite + httpx)",
        "started": started,
        "finished": finished,
        "db": {"inserted_hit_id": hit_id, "total_hits": total},
        "httpbin": {"delay_s": delay_s, "url": http_data.get("url")},
        "note": "This is the ideal pattern for high concurrency I/O APIs.",
    }


# ============================================================
# 2) BackgroundTasks with async work
# ============================================================
async def audit_log_async(message: str, delay_s: float = 2.0) -> None:
    """
    Example async background work:
    - async sleep
    - async DB insert
    """
    print(f"[{ts()}] [BG] audit_log_async start: {message}")
    await asyncio.sleep(delay_s)
    await insert_hit(f"/bg:{message}")
    print(f"[{ts()}] [BG] audit_log_async done:  {message}")


def run_async_bg_task(message: str, delay_s: float) -> None:
    """
    BackgroundTasks expects a regular callable.
    We wrap the async function so it can run.
    """
    asyncio.run(audit_log_async(message, delay_s))


@app.post("/bg-async")
def bg_async(bg: BackgroundTasks, message: str = "user_signup", delay_s: float = 2.0) -> Dict[str, Any]:
    """
    Returns immediately; background work runs after response.

    Note: For serious/critical background jobs, use Celery/RQ/etc.
    """
    started = ts()
    # You can still do sync work here, but we keep it minimal.
    bg.add_task(run_async_bg_task, message, delay_s)
    returned = ts()
    return {
        "endpoint": "/bg-async",
        "type": "BackgroundTasks (async work via wrapper)",
        "started": started,
        "returned": returned,
        "bg_task": {"message": message, "delay_s": delay_s},
        "note": "Check server console for [BG] logs. Task is not durable if process crashes.",
    }


# ============================================================
# 3) CPU-bound inside async (BAD)
# ============================================================
def cpu_heavy(n: int = 30_000_000) -> int:
    total = 0
    for i in range(n):
        total += (i % 7)
    return total


@app.get("/cpu-async-bad")
async def cpu_async_bad(n: int = 30_000_000) -> Dict[str, Any]:
    """
    Anti-pattern: CPU work blocks event loop.
    """
    started = ts()
    total = cpu_heavy(n)  # blocks event loop
    finished = ts()
    return {
        "endpoint": "/cpu-async-bad",
        "type": "async but CPU-bound (BAD: blocks event loop)",
        "started": started,
        "finished": finished,
        "n": n,
        "result": total,
    }


# ============================================================
# 4) CPU-bound offloaded to thread (GOOD)
# ============================================================
@app.get("/cpu-to-thread")
async def cpu_to_thread(n: int = 30_000_000) -> Dict[str, Any]:
    """
    Recommended: keep event loop responsive by moving CPU work to a thread.
    """
    started = ts()
    total = await asyncio.to_thread(cpu_heavy, n)
    finished = ts()
    return {
        "endpoint": "/cpu-to-thread",
        "type": "async + asyncio.to_thread (GOOD)",
        "started": started,
        "finished": finished,
        "n": n,
        "result": total,
    }
