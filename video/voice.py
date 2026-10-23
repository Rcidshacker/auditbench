"""Voice the narration with a free Microsoft Edge neural voice and check every line fits its slot.

    python video/voice.py          # writes video/voice/nXX.mp3; speeds up any line that would overrun
"""
from __future__ import annotations

import asyncio
import subprocess
import sys
from pathlib import Path

import edge_tts

sys.path.insert(0, str(Path(__file__).parent))
from narration import LINES  # noqa: E402

VOICE = "en-US-AriaNeural"
OUT = Path(__file__).parent / "voice"


def seconds(f: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                          "csv=p=0", str(f)], text=True))


async def speak(text: str, rate: int, f: Path):
    await edge_tts.Communicate(text, VOICE, rate=f"{rate:+d}%").save(str(f))


def main():
    OUT.mkdir(exist_ok=True)
    for name, _seg, _off, slot, text in LINES:
        f = OUT / f"{name}.mp3"
        rate = 0
        for _ in range(6):  # nudge the speaking rate up until the line fits (cap +25%)
            asyncio.run(speak(text, rate, f))
            d = seconds(f)
            if d <= slot - 0.2 or rate >= 25:
                break
            rate += 5
        flag = "" if d <= slot - 0.2 else "  OVERRUNS"
        print(f"{name}: {d:5.2f}s / slot {slot:4.1f}s  rate {rate:+d}%{flag}")


if __name__ == "__main__":
    main()
