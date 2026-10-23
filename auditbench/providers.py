"""Text-generation providers for the `generative` auditor (AIReg-Bench prompt), selected as provider:model.

    openjev:diffusiongemma-26b     nvidia:meta/llama-3.3-70b-instruct     openrouter:<id>:free
    groq:openai/gpt-oss-120b       gemini:gemini-2.5-flash                local:<model id>
    claude:haiku | claude:sonnet   (Claude Code subscription via `claude -p`, needs CLAUDE_CODE_OAUTH_TOKEN)

Keys are read with keys.get() (process env, then HKCU\\Environment) and never logged.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.request

from . import keys

# name: (base_url, key env var, requests per minute we allow ourselves)
OPENAI_COMPAT = {
    "nvidia": ("https://integrate.api.nvidia.com/v1", "NVIDIA_API_KEY", 25),
    "nebius": ("https://api.tokenfactory.nebius.com/v1", "NEBIUS_API_KEY", 120),  # Token Factory (hackathon)
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY", 18),
    "groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY", 25),
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai", "GEMINI_API_KEY", 9),
    "openjev": ("https://api.codiv.ai/v1", "OPENJEV_API_KEY", 55),
    "local": (None, None, 600),  # base URL from LOCAL_LLM_BASE_URL, default Atomic Chat
}
CLAUDE_RPM = 20

_pace: dict[str, tuple[threading.Lock, list[float]]] = {}


def _wait_turn(provider: str, rpm: int):
    """Space request starts at least 60/rpm seconds apart for this provider."""
    lock, last = _pace.setdefault(provider, (threading.Lock(), [0.0]))
    with lock:
        gap = 60.0 / rpm - (time.monotonic() - last[0])
        if gap > 0:
            time.sleep(gap)
        last[0] = time.monotonic()


def strip_reasoning(text: str) -> str:
    """Drop <think>…</think> so the template text a reasoning model repeats can't be parsed as its score."""
    return re.sub(r"(?s)<think>.*?</think>", "", text or "").strip()


def generate(spec: str, prompt: str, max_tokens: int = 4096, retries: int = 6) -> tuple[str, str, int]:
    """Return (text, model_id, prompt_tokens)."""
    provider, model = spec.split(":", 1)
    if provider == "claude":
        return _claude(model, prompt)
    base, key_name, rpm = OPENAI_COMPAT[provider]
    if provider == "local":  # Atomic Chat server (Server > Configuration shows port and API key)
        base = keys.get("LOCAL_LLM_BASE_URL") or "http://127.0.0.1:64303/v1"
        key_name = "LOCAL_LLM_API_KEY" if keys.get("LOCAL_LLM_API_KEY") else None
    headers = {"Content-Type": "application/json", "User-Agent": "auditbench/0.1"}
    if key_name:
        key = keys.get(key_name)
        if not key:
            raise RuntimeError(f"{key_name} is not set (setx {key_name} \"...\" in your own terminal)")
        headers["Authorization"] = f"Bearer {key}"
    body = {"model": model, "max_tokens": max_tokens, "temperature": 1.0,
            "messages": [{"role": "user", "content": prompt}]}
    if provider in ("nvidia", "nebius"):
        # NIM reasoning models (e.g. nemotron-3.5-lightning) otherwise spend >4k tokens thinking and return no answer;
        # thinking off for every NVIDIA model keeps the comparison like-for-like. Models without the switch ignore it.
        body["chat_template_kwargs"] = {"enable_thinking": False}
    for attempt in range(retries):
        _wait_turn(provider, rpm)
        req = urllib.request.Request(f"{base}/chat/completions", data=json.dumps(body).encode(), headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.loads(r.read())
            msg = d["choices"][0]["message"]
            text = strip_reasoning(msg.get("content") or "")
            return text, d.get("model", model), (d.get("usage") or {}).get("prompt_tokens", 0)
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:300]
            if e.code in (429, 500, 502, 503, 504, 529) and "quota" not in detail.lower() and attempt < retries - 1:
                time.sleep(float(e.headers.get("retry-after") or min(60, 2 ** (attempt + 1))))
                continue
            raise RuntimeError(f"{provider} HTTP {e.code}: {detail}") from None
        except (urllib.error.URLError, TimeoutError):
            if attempt == retries - 1:
                raise
            time.sleep(2 ** (attempt + 1))


# Claude Code subscription. The user's ~/.claude/settings.json routes the CLI to a local proxy (Atomic Chat), so
# user settings are skipped and every ANTHROPIC_* override is removed; auth comes from a `claude setup-token` token.
_CLAUDE_STRIP = ("ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_MODEL", "ANTHROPIC_DEFAULT_HAIKU_MODEL",
                 "ANTHROPIC_DEFAULT_SONNET_MODEL", "ANTHROPIC_DEFAULT_OPUS_MODEL", "ANTHROPIC_API_KEY", "CLAUDECODE",
                 "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH")
# Empty cwd *outside* the user's home: Claude Code also loads CLAUDE.md / .claude/CLAUDE.md from every ancestor
# directory, and C:\Users\<name>\.claude\CLAUDE.md is an ancestor of the temp dir.
# ProgramData subfolders inherit an ACL that lets any local user create files, and the judge loads *project*
# settings (hooks) from its cwd, so: fresh random dir per process, inheritance removed, current user only.
def _private_dir() -> str:
    if os.name != "nt":
        return tempfile.mkdtemp(prefix="auditbench-claude-")  # mode 0700
    d = tempfile.mkdtemp(prefix="auditbench-judge-", dir=os.environ.get("ProgramData", tempfile.gettempdir()))
    user = f"{os.environ['USERDOMAIN']}\\{os.environ['USERNAME']}"
    subprocess.run(["icacls", d, "/inheritance:r", "/grant:r", f"{user}:(OI)(CI)F"], check=True,
                   capture_output=True)
    return d


_CLAUDE_DIR = _private_dir()


def _claude(model: str, prompt: str) -> tuple[str, str, int]:
    token = keys.get("CLAUDE_CODE_OAUTH_TOKEN")
    if not token:
        raise RuntimeError("CLAUDE_CODE_OAUTH_TOKEN is not set (run `claude setup-token`, then setx it)")
    env = {k: v for k, v in os.environ.items() if k not in _CLAUDE_STRIP}
    env["CLAUDE_CODE_OAUTH_TOKEN"] = token
    # empty config dir: the user's global CLAUDE.md, memory, hooks and plugins must not reach the judge
    env["CLAUDE_CONFIG_DIR"] = os.path.join(_CLAUDE_DIR, "config")
    os.makedirs(env["CLAUDE_CONFIG_DIR"], exist_ok=True)  # inside the private dir created above
    env["USERPROFILE"] = env["HOME"] = _CLAUDE_DIR  # user-level CLAUDE.md is resolved from the home dir
    cmd = ["claude", "-p", "--model", model, "--setting-sources", "project", "--system-prompt",
           "You are a careful legal and technical compliance reviewer.", "--tools", "", "--strict-mcp-config",
           "--no-session-persistence", "--output-format", "json"]
    for attempt in range(4):
        _wait_turn("claude", CLAUDE_RPM)
        p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8", env=env,
                           cwd=_CLAUDE_DIR, timeout=300, shell=os.name == "nt")
        try:
            d = json.loads(p.stdout.strip().splitlines()[-1])
        except (IndexError, json.JSONDecodeError):
            d = {"is_error": True, "result": (p.stderr or p.stdout)[:300]}
        if not d.get("is_error"):
            used = next(iter(d.get("modelUsage") or {}), model)
            return strip_reasoning(d["result"]), used, (d.get("usage") or {}).get("input_tokens", 0)
        if "limit" in str(d.get("result", "")).lower() and attempt < 3:  # usage window hit: back off
            time.sleep(120 * (attempt + 1))
            continue
        raise RuntimeError(f"claude -p failed: {str(d.get('result'))[:300]}")
