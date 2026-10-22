"""Minimal OpenJev (Codiv System One) client. Key is read from OPENJEV_API_KEY only."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

BASE = os.environ.get("OPENJEV_BASE_URL", "https://api.codiv.ai/v1")


def systemone(state, questions: dict, model: str = "openjev-latest", retries: int = 5, **extra) -> dict:
    return _post("systemone", {"model": model, "state": state, "questions": questions, **extra}, retries)


def chat(prompt: str, model: str = "diffusiongemma-26b", max_tokens: int = 700, retries: int = 5) -> dict:
    """OpenAI-compatible text generation (separate quota from System One)."""
    return _post("chat/completions", {"model": model, "max_tokens": max_tokens,
                                      "messages": [{"role": "user", "content": prompt}]}, retries)


def _post(path: str, payload: dict, retries: int) -> dict:
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{BASE}/{path}", data=body, method="POST",
        headers={"Authorization": f"Bearer {os.environ['OPENJEV_API_KEY']}", "Content-Type": "application/json",
                 "User-Agent": "auditbench/0.1"},  # Cloudflare rejects the default Python-urllib UA (error 1010)
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:300]
            # quota errors are final; rate-limit/overload are retried with backoff
            if e.code in (429, 529) and "quota" not in detail and attempt < retries - 1:
                time.sleep(float(e.headers.get("retry-after") or 2 ** attempt))
                continue
            raise RuntimeError(f"OpenJev HTTP {e.code}: {detail}") from None
        except (urllib.error.URLError, TimeoutError):
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
