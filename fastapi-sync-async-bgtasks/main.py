"""
FastAPI demo: async vs threads (sync) vs BackgroundTasks

What you get:
1) /async-io        -> async endpoint doing NON-BLOCKING I/O (await asyncio.sleep) 
2) /sync-blocking   -> sync endpoint doing BLOCKING work (time.sleep) (FastAPI runs it in a threadpool)
3) /bg-email        -> BackgroundTasks: returns immediately, does work AFTER response
4) /cpu-async-bad   -> async endpoint doing CPU work (blocks event loop) (anti-pattern)
5) /cpu-to-thread   -> async endpoint offloading CPU work to a thread (recommended pattern)

Run:
  pip install fastapi uvicorn
  uvicorn main:app --reload

Test:
  Open 2 terminals and run curl requests in parallel to see blocking vs non-blocking effects.
"""

from fastapi import FastAPI, BackgroundTasks
import asyncio
import time
from typing import List, Any, Optional, Dict
from datetime import datetime

app = FastAPI(title="Async vs Threads vs BackgroundTasks Demo")

def now() -> str:
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]



@app.get("/")
def read_root():
    return f"{now()} - Root endpoint called"

# ----------------------------
# 1) ASYNC I/O (non-blocking)
# ----------------------------

@app.get("/async-io")
async def async_io(delay_s: float = 3.0) -> Dict[str, Any]:
    """
    Simulates I/O (DB/API/network) using await asyncio.sleep().
    While waiting, the event loop can serve other requests.
    """
    started = now()
    await asyncio.sleep(delay_s)  # non-blocking wait (simulates I/O)
    finished = now()
    return {
        "endpoint": "/async-io",
        "type": "async (non-blocking I/O)",
        "started": started,
        "finished": finished,
        "delay_s": delay_s,
    }


# ----------------------------
# 2) SYNC (runs in threadpool)
# ----------------------------
@app.get("/sync-blocking")
def sync_blocking(delay_s: float = 3.0) -> Dict[str, Any]:
    """
    Simulates blocking work using time.sleep().
    FastAPI will run this sync endpoint in a threadpool so the event loop isn't blocked,
    but each request occupies a thread while sleeping.
    """
    started = now()
    time.sleep(delay_s)  # blocking
    finished = now()
    return {
        "endpoint": "/sync-blocking",
        "type": "sync (blocking) - executed in a threadpool",
        "started": started,
        "finished": finished,
        "delay_s": delay_s,
    }


# ------------------------------------------
# 3) BACKGROUNDTASKS (after responding)
# ------------------------------------------
def fake_send_email(to: str, subject: str, body: str, delay_s: float = 5.0) -> None:
    """
    Pretend to send an email. This is intentionally blocking to demonstrate that
    BackgroundTasks runs after the response is returned.
    """
    print(f"[{now()}] [BG] Start sending email to={to!r} subject={subject!r}")
    time.sleep(delay_s)  # blocking work
    print(f"[{now()}] [BG] Finished sending email to={to!r}")

@app.post("/bg-email")
def bg_email(
    bg: BackgroundTasks,
    to: str = "emma@example.com",
    delay_s: float = 5.0,
) -> Dict[str, Any]:
    """
    Returns immediately. The 'email sending' runs after response is sent.
    NOTE: Not durable. If server crashes, task is lost.
    """
    started = now()
    bg.add_task(fake_send_email, to, "Welcome", "Hello from FastAPI", delay_s)
    returned = now()
    return {
        "endpoint": "/bg-email",
        "type": "BackgroundTasks (runs after response)",
        "started": started,
        "returned": returned,
        "bg_task": {"to": to, "delay_s": delay_s},
        "note": "Check server console logs for [BG] lines.",
    }


# -------------------------------------------------------
# 4) CPU-bound work in async endpoint (BAD: blocks loop)
# -------------------------------------------------------
def cpu_heavy(n: int = 30_000_000) -> int:
    """
    Pure CPU loop. This blocks whatever thread it runs on.
    """
    total = 0
    for i in range(n):
        total += (i % 7)
    return total

@app.get("/cpu-async-bad")
async def cpu_async_bad(n: int = 30_000_000) -> Dict[str, Any]:
    """
    Anti-pattern: CPU work inside async blocks the event loop.
    While this runs, other async requests get stuck.
    """
    started = now()
    total = cpu_heavy(n)  # blocks event loop
    finished = now()
    return {
        "endpoint": "/cpu-async-bad",
        "type": "async but CPU-bound (BAD: blocks event loop)",
        "started": started,
        "finished": finished,
        "n": n,
        "result": total,
    }


# -------------------------------------------------------
# 5) CPU-bound work offloaded to a thread (RECOMMENDED)
# -------------------------------------------------------
@app.get("/cpu-to-thread")
async def cpu_to_thread(n: int = 30_000_000) -> Dict[str, Any]:
    """
    Recommended: offload CPU work to a thread so the event loop stays responsive.
    """
    started = now()
    total = await asyncio.to_thread(cpu_heavy, n)
    finished = now()
    return {
        "endpoint": "/cpu-to-thread",
        "type": "async + asyncio.to_thread (CPU moved to thread)",
        "started": started,
        "finished": finished,
        "n": n,
        "result": total,
    }