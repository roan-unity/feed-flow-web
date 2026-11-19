"""Images and videos for the home page (index.html hero, #how-it-works, structured-data screenshots).

Every frame is a real app capture (iPhone 17, 1206x2622, "Deep background" look, demo baby Theo, 2026-11-19,
tag v1.67.1-build.368). Nothing is drawn or retouched; this script only crops and resizes.

    /usr/bin/python3 scripts/prepare-how-it-works.py en    # screens/how/        from <captures>/en  (English, oz)
    /usr/bin/python3 scripts/prepare-how-it-works.py no    # screens/no/how/     from <captures>/nb  (Norwegian, ml)

<captures> defaults to ~/Developer/feedflow-web-captures (override: FEEDFLOW_WEB_CAPTURES). It holds en/ and nb/ with
start, today-before, bottle, today-after, flowcast, report-top, report-detail, growth, allergens, family, vitamin-d,
theme-ocean (+ theme-forest/lavender/midnight), the two flow-*.mp4 recordings and their *-poster-mid.png frames.

Slots (all written at 360 and 720 px wide, same aspect as before so the layout never shifts):
- pick-poster = poster of the "pick what to log" recording (the log menu: Pumped Milk, Breast, Formula, More)
- fill-poster = poster of the "fill the bottle and press" recording
  (start-*.webp, the older composite of the whole menu, is no longer made here: only the water guides still use it)
- before   = Today before the feed (the "from" frame of the day meter in step 04)
- log      = the bottle screen (also the hero phone)       - finish = Today after the feed
- flowcast, health (allergens), growth, family (activity feed), theme-ocean/forest/lavender/midnight
- hero-report = top of the Baby Report (hero's second phone)
- report-scroll = report-top stacked on the lower part of report-detail (two real scroll positions of the same
  report), so the section can scroll it inside a phone frame
- vitamin-d (900 px card crop, structured data only), report-detail (structured data only)
- <name>-bg.png = the plain phone background of a screen, used behind pieces that have not landed yet
- flow-pick.mp4 / flow-fill.mp4 = the two recordings at 540x1174, H.264, no audio, via scripts/transcode-video.swift:
    swiftc -O scripts/transcode-video.swift -o /tmp/transcode-video
"""
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
LANG = sys.argv[1] if len(sys.argv) > 1 else "en"
if LANG not in ("en", "no"):
    sys.exit("usage: prepare-how-it-works.py en|no")
CAPTURES = Path(os.environ.get("FEEDFLOW_WEB_CAPTURES", Path.home() / "Developer/feedflow-web-captures")) / ("en" if LANG == "en" else "nb")
OUT = ROOT / "screens" / ("how" if LANG == "en" else "no/how")
OUT.mkdir(parents=True, exist_ok=True)
TRANSCODER = Path(os.environ.get("TRANSCODE_VIDEO", "/tmp/transcode-video"))
REPORT_HEADER_PX = 480   # the pinned report header (Close / Baby Report / Doctor view / Share PDF) in the top frame
REPORT_TOP_END_Y = 2480   # the top frame stops above its "02 Feeding" heading, so the lower frame continues from there
REPORT_CROP_Y = 1040     # where the lower frame starts: the "Growth curves" heading, past the card hidden under its header


def load(name: str) -> Image.Image:
    return Image.open(CAPTURES / f"{name}.png").convert("RGB")


def save(image: Image.Image, name: str, widths=(360, 720), quality: int = 78) -> None:
    for width in widths:
        height = round(image.height * width / image.width)
        target = OUT / f"{name}-{width}.webp"
        image.resize((width, height), Image.Resampling.LANCZOS).save(target, "WEBP", quality=quality, method=6)
        print(f"Created {target.relative_to(ROOT)} ({width}x{height}, {target.stat().st_size // 1024} KB)")


def report_scroll() -> Image.Image:
    top, detail = load("report-top"), load("report-detail")
    body = detail.crop((0, REPORT_CROP_Y, detail.width, detail.height))
    sheet = Image.new("RGB", (top.width, REPORT_TOP_END_Y + body.height))
    sheet.paste(top.crop((0, 0, top.width, REPORT_TOP_END_Y)), (0, 0))
    sheet.paste(body, (0, REPORT_TOP_END_Y))
    print(f"report-scroll header fraction {REPORT_HEADER_PX} / {sheet.height}, travel ({sheet.height} - 2622) / {sheet.height}")
    return sheet


def background_strip(image: Image.Image, name: str, left_cols=(0.008, 0.03), right_cols=(0.97, 0.992)) -> None:
    """The plain phone background for a screen: the left and right edge of the capture (where nothing is drawn),
    median-filtered down its height and blended across the width. Shown behind pieces that have not landed yet, so
    an unrevealed area is the phone's own background and a landing piece has no box around it."""
    array = np.asarray(image.convert("RGB"), dtype=float)
    height, width, _ = array.shape
    window = max(9, height // 60) | 1
    pad = window // 2

    def edge(x0: float, x1: float):
        column = array[:, round(width * x0):max(round(width * x0) + 1, round(width * x1)), :].mean(axis=1)
        padded = np.pad(column, ((pad, pad), (0, 0)), mode="edge")
        return np.stack([np.median(padded[i:i + window], axis=0) for i in range(height)])

    left, right = edge(*left_cols), edge(*right_cols)
    mix = np.linspace(0, 1, 64).reshape(1, 64, 1)
    field = left[:, None, :] * (1 - mix) + right[:, None, :] * mix
    strip = Image.fromarray(field.round().astype("uint8")).filter(ImageFilter.GaussianBlur(2))
    strip = strip.resize((64, 262), Image.Resampling.BILINEAR)
    target = OUT / f"{name}-bg.png"
    strip.save(target)
    print(f"Created {target.relative_to(ROOT)}")


# Recordings: the poster is the frame that shows the point of the step (the picker; the bottle filling).
save(Image.open(CAPTURES / "flow-1-pick-poster-mid.png").convert("RGB"), "pick-poster")
save(Image.open(CAPTURES / "flow-2-fill-press-poster-mid.png").convert("RGB"), "fill-poster")
for source, name in (("flow-1-pick", "flow-pick"), ("flow-2-fill-press", "flow-fill")):
    target = OUT / f"{name}.mp4"
    if TRANSCODER.exists():
        subprocess.run([str(TRANSCODER), str(CAPTURES / f"{source}.mp4"), str(target), "540", "1174", "1200000"], check=True)
        for leftover in OUT.glob(f"{name}.mp4.sb-*"):
            leftover.unlink()
        print(f"Created {target.relative_to(ROOT)} ({target.stat().st_size // 1024} KB)")
    else:
        print(f"skipped {name}.mp4: build {TRANSCODER} first (see the header)")

log, finish, flowcast, growth, health, family = (load(n) for n in ("bottle", "today-after", "flowcast", "growth", "allergens", "family"))
save(load("today-before"), "before")
save(log, "log")
save(finish, "finish")
save(flowcast, "flowcast")
save(growth, "growth")
save(health, "health")
save(family, "family")
save(load("report-top"), "hero-report")
save(load("report-detail"), "report-detail", widths=(720,))
save(report_scroll(), "report-scroll", quality=74)
vitamin = load("vitamin-d")
save(vitamin.crop((0, 380, vitamin.width, 1740)), "vitamin-d", widths=(450, 900))
for theme in ("ocean", "forest", "lavender", "midnight"):
    if (CAPTURES / f"theme-{theme}.png").exists():
        save(load(f"theme-{theme}"), f"theme-{theme}", quality=74)
    else:
        print(f"no theme-{theme}.png in {CAPTURES}: the page keeps pointing at the English one")

# The growth strip is taken beside the plot and the health strip from INSIDE the card, because the animation holds
# back only the plot and the allergen rows, so the gap shows that card's own colour.
# how-it-works.js always loads them from /screens/how/ (a colour field, the same for every language), so only "en" makes them.
if LANG == "en":
    background_strip(log, "log")
    background_strip(finish, "finish")
    background_strip(flowcast, "flowcast")
    background_strip(growth, "growth", (0.06, 0.075), (0.91, 0.93))
    background_strip(health, "health", (0.05, 0.062), (0.94, 0.955))
    background_strip(family, "family")
