"""Generate the voiceover with ElevenLabs in Aria's voice; one MP3 per narration line.

    python video/tts.py --quota          # remaining characters
    python video/tts.py                  # writes video/voice/*.mp3 (skips lines already generated)

The key is read from the environment or ~/.claude/.env (where the Pulse voice server keeps it); it is never printed.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

VOICE = "21m00Tcm4TlvDq8ikWAM"  # Aria's voice (DA_IDENTITY)
MODEL = "eleven_multilingual_v2"
HERE = Path(__file__).resolve().parent
OUT = HERE / "voice"


def api_key() -> str:
    if os.environ.get("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"]
    for line in (Path.home() / ".claude" / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("ELEVENLABS_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ELEVENLABS_API_KEY not found")


def req(path: str, body: dict | None = None) -> bytes:
    r = urllib.request.Request(f"https://api.elevenlabs.io/v1/{path}", method="POST" if body else "GET",
                               data=json.dumps(body).encode() if body else None,
                               headers={"xi-api-key": api_key(), "Content-Type": "application/json",
                                        "Accept": "audio/mpeg" if body else "application/json"})
    with urllib.request.urlopen(r, timeout=120) as resp:
        return resp.read()


def main():
    if "--quota" in sys.argv:
        s = json.loads(req("user/subscription"))
        print(f"tier={s.get('tier')} used={s.get('character_count')} limit={s.get('character_limit')}")
        return
    from narration import LINES
    OUT.mkdir(exist_ok=True)
    for name, text in LINES:
        f = OUT / f"{name}.mp3"
        if f.exists():
            continue
        f.write_bytes(req(f"text-to-speech/{VOICE}?output_format=mp3_44100_128",
                          {"text": text, "model_id": MODEL,
                           "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.15}}))
        print("voiced", name)


if __name__ == "__main__":
    main()
