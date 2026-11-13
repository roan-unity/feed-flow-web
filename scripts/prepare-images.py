from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = {
    "growth-report": ROOT / "screens/store/4-report.jpg",
    "health-allergens": ROOT / "screens/store/6-allergens.jpg",
    "flowcast": ROOT / "screens/store/5-flowcast.jpg",
    "report-detail": ROOT / "screens/store/report-detail.png",
}

for name, source in ASSETS.items():
    with Image.open(source) as image:
        image = image.convert("RGB")
        for width in (360, 720):
            height = round(image.height * width / image.width)
            resized = image.resize((width, height), Image.Resampling.LANCZOS)
            target = ROOT / "screens" / f"{name}-{width}.webp"
            resized.save(target, "WEBP", quality=84, method=6)
            print(f"Created {target.relative_to(ROOT)} ({width}x{height})")

# The vitamin D capture is intentionally cropped to its real Today-screen detail:
# header, full vitamin card and feed-gap summary. No UI content is altered.
with Image.open(ROOT / "screens/store/vitamin-d.png") as image:
    image = image.convert("RGB").crop((0, 0, image.width, 1100))
    for width in (450, 900):
        height = round(image.height * width / image.width)
        resized = image.resize((width, height), Image.Resampling.LANCZOS)
        target = ROOT / "screens" / f"vitamin-d-detail-{width}.webp"
        resized.save(target, "WEBP", quality=88, method=6)
        print(f"Created {target.relative_to(ROOT)} ({width}x{height})")
