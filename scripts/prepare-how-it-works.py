"""Images for the home page "How logging works" section (index.html #how-it-works).

Every frame is a real app capture. Nothing is drawn or retouched:
- start   = screens/logging.jpg (the log menu), resized.
- log     = the phone screen cropped out of the 01-safe-bottle store frame (bottle timer + Similac).
- finish  = the phone screen cropped out of the 04-home store frame (today's total + timeline).
- report-scroll = screens/report.jpg stacked on top of the lower part of
  screens/store/report-detail.png (two real scroll positions of the same Baby Report),
  so the section can scroll it inside a phone frame.

The store frames are read from the 1290x2796 App Store originals when that folder exists
(sharper), otherwise from the 720 px webps already in screens/formula/ (same image).
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "screens" / "how"
OUT.mkdir(exist_ok=True)
STORE_ORIGINALS = Path.home() / "Developer/ff-167-quicklog/specs/launch/cpp/formula/1290x2796"

# Phone-screen rectangle inside a 1290x2796 store frame (inside the drawn bezel).
SCREEN_BOX_1290 = (148, 541, 1142, 2711)


def store_screen(name: str) -> Image.Image:
    original = STORE_ORIGINALS / f"{name}.png"
    if original.exists():
        image = Image.open(original).convert("RGB")
        return image.crop(SCREEN_BOX_1290)
    image = Image.open(ROOT / "screens" / "formula" / f"{name}-720.webp").convert("RGB")
    scale = image.width / 1290
    return image.crop(tuple(round(v * scale) for v in SCREEN_BOX_1290))


def report_scroll() -> Image.Image:
    top = Image.open(ROOT / "screens" / "report.jpg").convert("RGB")
    detail = Image.open(ROOT / "screens" / "store" / "report-detail.png").convert("RGB")
    detail_body = detail.crop((0, 450, detail.width, detail.height))
    sheet = Image.new("RGB", (top.width, top.height + detail_body.height))
    sheet.paste(top, (0, 0))
    sheet.paste(detail_body, (0, top.height))
    return sheet


def save(image: Image.Image, name: str, quality: int = 78) -> None:
    for width in (360, 720):
        height = round(image.height * width / image.width)
        resized = image.resize((width, height), Image.Resampling.LANCZOS)
        target = OUT / f"{name}-{width}.webp"
        resized.save(target, "WEBP", quality=quality, method=6)
        print(f"Created {target.relative_to(ROOT)} ({width}x{height}, {target.stat().st_size // 1024} KB)")


# Phone 1: the current type picker ("What do you want to log?"), a 1206x2622 in-app capture from
# the 2026-11-15 fill-stage run. Falls back to the older radial menu when that folder is missing.
NEWER_PICKER = Path.home() / "Developer/ff-167-settings/scratch/fill/after/fill-menu-ocean-en-i17.png"
if NEWER_PICKER.exists():
    START = Image.open(NEWER_PICKER).convert("RGB")
else:
    START = Image.open(ROOT / "screens" / "logging.jpg").convert("RGB")
save(START, "start")
save(store_screen("01-safe-bottle"), "log")
save(store_screen("04-home"), "finish")
save(report_scroll(), "report-scroll", quality=74)


def background_strip(image: Image.Image, name: str) -> None:
    """The plain phone background for a screen: the left edge of the capture (where nothing is drawn),
    median-filtered down its height. Shown behind pieces that have not landed yet, so an unrevealed area
    is the phone's own background and a landing piece has no box around it."""
    import numpy as np
    from PIL import ImageFilter
    array = np.asarray(image.convert("RGB"), dtype=float)
    height, width, _ = array.shape
    window = max(9, height // 60) | 1
    pad = window // 2

    def edge(x0: float, x1: float):
        column = array[:, round(width * x0):max(round(width * x0) + 1, round(width * x1)), :].mean(axis=1)
        padded = np.pad(column, ((pad, pad), (0, 0)), mode="edge")
        return np.stack([np.median(padded[i:i + window], axis=0) for i in range(height)])

    # The screens carry a diagonal gradient, so take both edges and blend across the width.
    left, right = edge(0.008, 0.03), edge(0.97, 0.992)
    mix = np.linspace(0, 1, 64).reshape(1, 64, 1)
    field = left[:, None, :] * (1 - mix) + right[:, None, :] * mix
    strip = Image.fromarray(field.round().astype("uint8")).filter(ImageFilter.GaussianBlur(2))
    strip = strip.resize((64, 262), Image.Resampling.BILINEAR)
    target = OUT / f"{name}-bg.png"
    strip.save(target)
    print(f"Created {target.relative_to(ROOT)}")


background_strip(START, "start")
background_strip(store_screen("01-safe-bottle"), "log")
background_strip(store_screen("04-home"), "finish")
background_strip(Image.open(ROOT / "screens" / "flowcast-720.webp"), "flowcast")
