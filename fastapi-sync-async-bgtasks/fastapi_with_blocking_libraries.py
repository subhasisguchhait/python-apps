"""
FastAPI demo with REAL blocking dependencies:
- SQLite (sqlite3) -> blocking
- requests         -> blocking

Demonstrates:
1) Sync endpoint (def) using SQLite + requests (FastAPI runs it in a threadpool)
2) Async endpoint (async def) but incorrectly using blocking calls (BAD: blocks event loop)
3) Async endpoint that offloads blocking SQLite + requests to threads (GOOD)
4) BackgroundTasks to do "post-response" work (e.g., audit logging)

Install:
  pip install fastapi uvicorn requests

Run:
  uvicorn main:app --reload

Try:
  - Open two terminals and hit endpoints in parallel with curl to observe behavior.
"""

from __future__ import annotations

import sqlite3
import time
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional

import requests
from fastapi import FastAPI, BackgroundTasks, HTTPException

DB_PATH = "demo.db"

app = FastAPI(title="SQLite + requests: async vs threads vs BackgroundTasks")


def ts() -> str:
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


# ----------------------------
# SQLite helpers (blocking)
# ----------------------------
def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS hits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def insert_hit(endpoint: str) -> int:
    """
    Blocking DB write.
    Returns inserted row id.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "INSERT INTO hits(endpoint, created_at) VALUES(?, ?)",
            (endpoint, ts()),
        )
        conn.commit()
        return int(cur.lastrowid)


def count_hits() -> int:
    """
    Blocking DB read.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT COUNT(*) FROM hits")
        (n,) = cur.fetchone()
        return int(n)


# ----------------------------
# External call helper (blocking)
# ----------------------------
def call_httpbin(delay_s: float) -> Dict[str, Any]:
    """
    Blocking HTTP call using requests.
    httpbin.org/delay/<n> waits n seconds before responding.
    """
    delay_s = float(delay_s)
    if delay_s < 0 or delay_s > 10:
        raise ValueError("delay_s must be between 0 and 10")

    url = f"https://httpbin.org/delay/{int(delay_s)}"
    r = requests.get(url, timeout=15)  # blocking
    r.raise_for_status()
    return r.json()


# ----------------------------
# Background task (post-response)
# ----------------------------
def audit_log(message: str, delay_s: float = 2.0) -> None:
    """
    Simulate slow logging/audit work.
    Runs AFTER response when scheduled via BackgroundTasks.
    """
    print(f"[{ts()}] [BG] audit_log start: {message}")
    time.sleep(delay_s)  # blocking background work
    print(f"[{ts()}] [BG] audit_log done:  {message}")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


# ============================================================
# 1) SYNC endpoint: def (FastAPI runs it in a threadpool)
# ============================================================
@app.get("/sync")
def sync_endpoint(delay_s: float = 3.0) -> Dict[str, Any]:
    """
    This is the simplest "real world" approach with blocking libs:
    - sqlite3
    - requests

    FastAPI will execute 'def' endpoints using a threadpool.
    """
    started = ts()

    hit_id = insert_hit("/sync")           # blocking DB
    total = count_hits()                   # blocking DB
    http_data = call_httpbin(delay_s)      # blocking HTTP

    finished = ts()
    return {
        "endpoint": "/sync",
        "type": "sync (def) -> runs in FastAPI threadpool",
        "started": started,
        "finished": finished,
        "db": {"inserted_hit_id": hit_id, "total_hits": total},
        "httpbin": {"delay_s": delay_s, "url": http_data.get("url")},
        "note": "Under heavy load, threadpool size becomes the limiting factor.",
    }


# ============================================================
# 2) ASYNC endpoint but WRONG: blocking calls inside async def
# ============================================================
@app.get("/async-bad")
async def async_bad(delay_s: float = 3.0) -> Dict[str, Any]:
    """
    Anti-pattern:
    This blocks the event loop because it calls blocking sqlite3 + requests
    directly inside async def.

    Symptom:
    While this runs, OTHER async requests can get stuck behind it.
    """
    started = ts()

    # BAD: blocking DB + blocking HTTP inside async def
    hit_id = insert_hit("/async-bad")
    total = count_hits()
    http_data = call_httpbin(delay_s)

    finished = ts()
    return {
        "endpoint": "/async-bad",
        "type": "async but BLOCKING (bad)",
        "started": started,
        "finished": finished,
        "db": {"inserted_hit_id": hit_id, "total_hits": total},
        "httpbin": {"delay_s": delay_s, "url": http_data.get("url")},
        "warning": "This blocks the event loop. Avoid this in production.",
    }


# ============================================================
# 3) ASYNC endpoint done correctly: offload blocking work
# ============================================================
@app.get("/async-good")
async def async_good(delay_s: float = 3.0) -> Dict[str, Any]:
    """
    Recommended approach IF you want async endpoints but your libraries are blocking:
    - Use asyncio.to_thread(...) for blocking SQLite and requests calls

    This keeps the event loop responsive.
    """
    started = ts()

    hit_id = await asyncio.to_thread(insert_hit, "/async-good")
    total = await asyncio.to_thread(count_hits)
    http_data = await asyncio.to_thread(call_httpbin, delay_s)

    finished = ts()
    return {
        "endpoint": "/async-good",
        "type": "async + to_thread (good for blocking libs)",
        "started": started,
        "finished": finished,
        "db": {"inserted_hit_id": hit_id, "total_hits": total},
        "httpbin": {"delay_s": delay_s, "url": http_data.get("url")},
        "note": "This is still using threads, but the event loop stays free for other async work.",
    }


# ============================================================
# 4) BackgroundTasks: return immediately; do work after response
# ============================================================
@app.post("/bg")
def background_demo(
    bg: BackgroundTasks,
    message: str = "user_signup",
    delay_s: float = 2.0,
) -> Dict[str, Any]:
    """
    Use BackgroundTasks when you do NOT need to make the user wait.
    Example: audit log, metrics, sending a non-critical email, etc.

    Not durable: if the process crashes, task is lost.
    """
    started = ts()
    hit_id = insert_hit("/bg")
    total = count_hits()

    bg.add_task(audit_log, f"{message} (hit_id={hit_id})", delay_s)

    returned = ts()
    return {
        "endpoint": "/bg",
        "type": "BackgroundTasks (runs after response)",
        "started": started,
        "returned": returned,
        "db": {"inserted_hit_id": hit_id, "total_hits": total},
        "bg_task": {"message": message, "delay_s": delay_s},
        "note": "Watch server console for [BG] logs after response returns.",
    }
