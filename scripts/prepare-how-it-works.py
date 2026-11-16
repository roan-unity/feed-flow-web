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


save(Image.open(ROOT / "screens" / "logging.jpg").convert("RGB"), "start")
save(store_screen("01-safe-bottle"), "log")
save(store_screen("04-home"), "finish")
save(report_scroll(), "report-scroll", quality=74)
