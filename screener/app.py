"""AuditBench Screener web app.   uvicorn screener.app:app --port 8000"""
from __future__ import annotations

import json
import time
from collections import defaultdict, deque
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .engine import ARTICLES, FAST, STRONG, screen

HERE = Path(__file__).parent
SAMPLES = json.loads((HERE / "samples" / "samples.json").read_text(encoding="utf-8"))
MAX_CHARS = 60_000
PER_HOUR = 12  # public demo: protects the Token Factory credits

app = FastAPI(title="AuditBench Screener")
app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
_hits: dict[str, deque] = defaultdict(deque)


class ScreenIn(BaseModel):
    documentation: str = Field(min_length=200, max_length=MAX_CHARS)
    system_outline: str = Field(default="", max_length=6000)
    articles: list[int] | None = None


def _rate_limit(ip: str):
    now, q = time.time(), _hits[ip]
    while q and now - q[0] > 3600:
        q.popleft()
    if len(q) >= PER_HOUR:
        raise HTTPException(429, f"Demo limit: {PER_HOUR} screenings per hour per visitor.")
    q.append(now)


@app.get("/")
def index():
    return FileResponse(HERE / "static" / "index.html")


@app.get("/api/samples")
def samples():
    return [{k: s[k] for k in ("id", "name", "source", "outline", "doc")} for s in SAMPLES]


@app.get("/api/info")
def info():
    return {"fast_model": FAST.split(":", 1)[1], "strong_model": STRONG.split(":", 1)[1], "articles": ARTICLES,
            "platform": "Nebius Token Factory"}


@app.post("/api/screen")
def do_screen(body: ScreenIn, request: Request):
    if body.articles and any(a not in ARTICLES for a in body.articles):
        raise HTTPException(422, f"articles must be among {ARTICLES}")
    _rate_limit(request.headers.get("x-forwarded-for", request.client.host if request.client else "?").split(",")[0])
    t = time.time()
    try:
        out = screen(body.documentation, body.system_outline, body.articles)
    except RuntimeError as e:
        raise HTTPException(502, f"Model call failed: {e}") from None
    out["seconds"] = round(time.time() - t, 1)
    return out
