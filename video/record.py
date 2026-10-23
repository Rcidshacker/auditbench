"""Record the demo clips of the live AuditBench Screener with Playwright (1920x1080, dark theme, visible cursor).

    python video/record.py            # writes video/clips/*.mp4
"""
from __future__ import annotations

import base64
import os
import shutil
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("SCREENER_URL", "https://auditbench-screener.vercel.app")
OUT = Path(__file__).parent / "clips"
CHROME = Path(os.environ["LOCALAPPDATA"]) / "ms-playwright" / "chromium-1243" / "chrome-win64" / "chrome.exe"
SIZE = {"width": 1920, "height": 1080}

# Playwright videos have no cursor; draw one so viewers can follow clicks.
CURSOR = """
addEventListener('DOMContentLoaded', () => {
  const c = document.createElement('div');
  c.style.cssText = 'position:fixed;left:0;top:0;width:22px;height:22px;border-radius:50%;z-index:2147483647;' +
    'pointer-events:none;background:rgba(240,105,61,.35);border:2px solid #f0693d;transform:translate(-50%,-50%);' +
    'transition:width .12s,height .12s';
  document.body.appendChild(c);
  addEventListener('mousemove', e => { c.style.left = e.clientX + 'px'; c.style.top = e.clientY + 'px'; });
  addEventListener('mousedown', () => { c.style.width = c.style.height = '14px'; });
  addEventListener('mouseup', () => { c.style.width = c.style.height = '22px'; });
});
"""


def glide_scroll(page, px: int, step: int = 40, pause: float = 0.025):
    for _ in range(max(1, px // step)):
        page.mouse.wheel(0, step)
        time.sleep(pause)


def move_to(page, selector: str):
    box = page.locator(selector).first.bounding_box()
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=30)
    time.sleep(0.4)


def reveal_all(page):
    page.evaluate("document.querySelectorAll('.reveal').forEach(e => e.classList.add('in'))")


def clip_landing(page):
    page.goto(URL, wait_until="networkidle")
    page.mouse.move(700, 500)
    time.sleep(3.5)
    glide_scroll(page, 900)
    time.sleep(3)
    glide_scroll(page, 1000)
    time.sleep(4)


def run_example(page, sample_id: str, scroll_results: int):
    page.goto(URL + "/#screen", wait_until="networkidle")
    page.evaluate("document.querySelector('#screen').scrollIntoView()")
    page.mouse.move(600, 400)
    time.sleep(1.5)
    move_to(page, "#sample")
    page.select_option("#sample", sample_id)
    time.sleep(1.5)
    move_to(page, "#go")
    page.click("#go")
    page.wait_for_selector("#out .meta", timeout=90_000)  # results rendered
    time.sleep(2)
    page.mouse.move(1350, 500, steps=25)
    glide_scroll(page, scroll_results, step=30, pause=0.03)
    time.sleep(5)


def clip_dossier(page):
    run_example(page, "dossier", 700)


def clip_injected(page):
    run_example(page, "injected", 250)


def clip_findings(page):
    page.goto(URL + "/#findings", wait_until="networkidle")
    reveal_all(page)
    page.mouse.move(900, 500)
    time.sleep(4)
    glide_scroll(page, 700)
    time.sleep(4)


CLIPS = {"1_landing": clip_landing, "2_dossier": clip_dossier, "3_injected": clip_injected, "4_findings": clip_findings}


def record(browser, name, fn):
    """Chrome DevTools screencast -> timestamped JPEG frames -> ffmpeg (variable frame durations) -> 30 fps MP4.

    Playwright's own recorder needs a browser/ffmpeg build we don't have locally; CDP works with any Chromium."""
    frames_dir = OUT / f"_{name}"
    shutil.rmtree(frames_dir, ignore_errors=True)
    frames_dir.mkdir(parents=True)
    ctx = browser.new_context(viewport=SIZE, color_scheme="dark")
    ctx.add_init_script(CURSOR)
    page = ctx.new_page()
    cdp = ctx.new_cdp_session(page)
    frames = []

    def on_frame(ev):
        path = frames_dir / f"{len(frames):05d}.jpg"
        path.write_bytes(base64.b64decode(ev["data"]))
        frames.append((path, ev["metadata"]["timestamp"]))
        cdp.send("Page.screencastFrameAck", {"sessionId": ev["sessionId"]})

    cdp.on("Page.screencastFrame", on_frame)
    cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 92, "maxWidth": SIZE["width"],
                                      "maxHeight": SIZE["height"], "everyNthFrame": 1})
    fn(page)
    end = time.time()
    cdp.send("Page.stopScreencast")
    ctx.close()
    # concat demuxer: each frame lasts until the next one arrives (screencast only sends frames on change)
    lines = []
    for i, (path, ts) in enumerate(frames):
        nxt = frames[i + 1][1] if i + 1 < len(frames) else max(ts + 0.04, end)
        lines += [f"file '{path.name}'", f"duration {max(nxt - ts, 0.001):.4f}"]
    lines.append(f"file '{frames[-1][0].name}'")
    (frames_dir / "list.txt").write_text("\n".join(lines), encoding="utf-8")
    out = OUT / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "list.txt",
                    "-vf", f"scale={SIZE['width']}:{SIZE['height']}:flags=lanczos,fps=30,format=yuv420p",
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium", str(out.resolve())],
                   cwd=frames_dir, check=True)
    shutil.rmtree(frames_dir, ignore_errors=True)
    print("recorded", name, len(frames), "frames")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=str(CHROME))
        for name, fn in CLIPS.items():
            record(browser, name, fn)
        browser.close()


if __name__ == "__main__":
    main()
