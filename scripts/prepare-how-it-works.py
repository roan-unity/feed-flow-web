"""Images for the home page "How logging works" section (index.html #how-it-works).

Every frame is a real app capture. Nothing is drawn or retouched:
- start   = the log menu ("What do you want to log?") showing everything the app can log at once. The app
  shows three types and keeps the rest behind More; for the website the discs are laid out together in two
  rows. Every disc and every word is cut from a real 1206x2622 capture (see compose_picker below).
- press, log, finish = three frames of ONE real recording of a 2.5 oz bottle being logged
  (ff-167-livepolish scratch/livepolish/round3/attempt1/clip-i17.mp4, 1206x2622): Today before the
  feed at 14.5 s (17.5 oz so far), the bottle screen at 37.5 s (2.5 oz taken, 1.5 oz left) and Today
  after it at 44.1 s (the 2.5 oz row on top, 20 oz so far). So the amounts in the three phones agree
  because they are the same feed. Extract them with scripts/extract-frames.swift (see RECORDING below).
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


# Phone 1: the type picker ("What do you want to log?") with EVERYTHING the app logs on one screen (round 6).
# The app's own stage shows up to three feed types and opens the rest behind More, so no single capture holds
# them all. This composes one from real pixels, all Ocean, English, iPhone 17 (1206x2622), all at the app's
# own scale:
#   ground, title, Breast, Formula (selected), the blurred panel  = fill-menu-ocean-en-i17 (2026-11-15 fill run)
#   Solids as a large disc                                        = health-three-extras-en-i17 (health run r3)
#   Pumped Milk, Pumping, Vitamin D, Health as small discs        = health-six-extras-en-i17 (health run r3)
#   Water as a small disc = the large Water disc of fill-menu scaled 156/228 (no capture has it small); its
#   word is the capture's own, unscaled.
# A disc is moved as (its pixels minus the plain ground behind it) added onto the ground where it lands, so
# nothing is redrawn and no box shows. The ground is the capture's own edge columns, blended across.
PICKER_MENU = Path.home() / "Developer/ff-167-settings/scratch/fill/after/fill-menu-ocean-en-i17.png"
PICKER_HEALTH = Path.home() / "Developer/ff-167-health/scratch/health/r3"
LARGE_Y, SMALL_Y_SIX, LARGE_X = 1374.5, 792.5, (218.5, 602.5, 986.5)
BACK_Y, TITLE_SHIFT = 1019, -48
BACK_X = tuple(603 + 225 * i for i in range(-2, 3))


def compose_picker() -> Image.Image:
    import numpy as np
    from PIL import ImageFilter

    def load(path):
        return np.asarray(Image.open(path).convert("RGB"), dtype=float)

    def ground(a):
        left, right = a[:, 4:24].mean(axis=1), a[:, 1182:1202].mean(axis=1)
        mix = np.linspace(0, 1, a.shape[1])[None, :, None]
        return left[:, None, :] * (1 - mix) + right[:, None, :] * mix

    menu, three, six = load(PICKER_MENU), load(PICKER_HEALTH / "health-three-extras-en-i17.png"), load(PICKER_HEALTH / "health-six-extras-en-i17.png")
    delta = {"menu": menu - ground(menu), "three": three - ground(three), "six": six - ground(six)}

    def soft(height, width, feather=10):
        mask = Image.new("L", (width, height), 0)
        mask.paste(255, (feather, feather, width - feather, height - feather))
        return np.asarray(mask.filter(ImageFilter.GaussianBlur(feather / 2.5)), dtype=float)[..., None] / 255

    # The ground: the menu capture with its title, More and three discs taken out (x 40..1166, y 820..1600).
    out = menu.copy()
    y0, y1, x0, x1 = 820, 1600, 40, 1166
    out[y0:y1, x0:x1] -= delta["menu"][y0:y1, x0:x1] * soft(y1 - y0, x1 - x0, 14)

    def place(patch, cx, cy):
        """Add a ground-free patch (h x w x 3) centred on (cx, cy)."""
        h, w, _ = patch.shape
        top, left = round(cy - h / 2), round(cx - w / 2)
        out[top:top + h, left:left + w] += patch * soft(h, w)

    def cut(name, cx, cy, half_w, up, down):
        return delta[name][round(cy - up):round(cy + down), round(cx - half_w):round(cx + half_w)], (down - up) / 2

    def move(name, cx, cy, to_x, to_y, half_w, up, down):
        patch, offset = cut(name, cx, cy, half_w, up, down)
        place(patch, to_x, to_y + offset)

    move("menu", 603, 889, 603, 889 + TITLE_SHIFT, 420, 50, 50)                    # the title
    move("menu", LARGE_X[0], LARGE_Y, LARGE_X[0], LARGE_Y, 150, 152, 214)          # Breast
    move("menu", LARGE_X[1], LARGE_Y, LARGE_X[1], LARGE_Y, 156, 152, 214)          # Formula, with its ring
    move("three", LARGE_X[2], LARGE_Y, LARGE_X[2], LARGE_Y, 150, 152, 214)         # Solids
    # Back row, left to right: Water, Pumped Milk, Pumping, Vitamin D, Health.
    move("six", 484.5, SMALL_Y_SIX, BACK_X[1], BACK_Y, 112, 88, 138)
    move("six", 964.5, SMALL_Y_SIX, BACK_X[2], BACK_Y, 112, 88, 138)
    move("six", 244.5, SMALL_Y_SIX, BACK_X[3], BACK_Y, 112, 88, 138)
    move("six", 730.5, 546.5, BACK_X[4], BACK_Y, 112, 88, 138)
    disc, _ = cut("menu", LARGE_X[2], LARGE_Y, 126, 126, 126)
    size = round(252 * 156 / 228)
    small = np.stack([np.asarray(Image.fromarray(disc[..., c]).resize((size, size), Image.Resampling.LANCZOS)) for c in range(3)], axis=-1)
    place(small, BACK_X[0], BACK_Y)
    word, _ = cut("menu", LARGE_X[2], 1559.5, 80, 24, 24)
    place(word, BACK_X[0], BACK_Y + 111.5)
    return Image.fromarray(out.clip(0, 255).round().astype("uint8"))


# Without those two capture folders the committed start webps and start-bg.png stay as they are.
START = compose_picker() if PICKER_MENU.exists() and PICKER_HEALTH.exists() else None
if START is not None:
    save(START, "start")

# swiftc -O scripts/extract-frames.swift -o /tmp/extract-frames
# /tmp/extract-frames <clip-i17.mp4> <RECORDING dir> 14.5 37.5 44.1   (then rename as below)
RECORDING = Path.home() / "Developer/feed-flow-web-howitworks-frames/sources"
RECORDED = {"press": "home-before-t14.50.png", "log": "bottle-t37.50.png", "finish": "home-after-t44.10.png"}
RECORDED_FRAMES = {}
for name, filename in RECORDED.items():
    if (RECORDING / filename).exists():
        RECORDED_FRAMES[name] = Image.open(RECORDING / filename).convert("RGB")
        save(RECORDED_FRAMES[name], name)
save(report_scroll(), "report-scroll", quality=74)

# Step 02 lifts the action panel (type chip, amount slider, round log button) out of the Today frame
# and shows it sharp in the middle of the phone. Same pixels as the "press" frame, only cropped; the
# two sizes keep the scale of press-360 / press-720 so the panel can sit exactly on top of the frame.
PANEL_BOX_1206 = (16, 1630, 1190, 2390)
if "press" in RECORDED_FRAMES:
    panel = RECORDED_FRAMES["press"].crop(PANEL_BOX_1206)
    for width in (360, 720):
        size = (round(panel.width * width / 1206), round(panel.height * width / 1206))
        target = OUT / f"press-panel-{width}.webp"
        panel.resize(size, Image.Resampling.LANCZOS).save(target, "WEBP", quality=82, method=6)
        print(f"Created {target.relative_to(ROOT)} ({size[0]}x{size[1]}, {target.stat().st_size // 1024} KB)")


def background_strip(image: Image.Image, name: str, left_cols=(0.008, 0.03), right_cols=(0.97, 0.992)) -> None:
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
    left, right = edge(*left_cols), edge(*right_cols)
    mix = np.linspace(0, 1, 64).reshape(1, 64, 1)
    field = left[:, None, :] * (1 - mix) + right[:, None, :] * mix
    strip = Image.fromarray(field.round().astype("uint8")).filter(ImageFilter.GaussianBlur(2))
    strip = strip.resize((64, 262), Image.Resampling.BILINEAR)
    target = OUT / f"{name}-bg.png"
    strip.save(target)
    print(f"Created {target.relative_to(ROOT)}")


if START is not None:
    background_strip(START, "start")
for name, frame in RECORDED_FRAMES.items():
    background_strip(frame, name)
background_strip(Image.open(ROOT / "screens" / "flowcast-720.webp"), "flowcast")


# Cards added in round 3. Each is a real capture; nothing is drawn or retouched.
# - family: the phone screen cropped out of the 07-family store frame (the shared Activity Feed).
# - growth: the growth card ("Is Nora growing along the curve?") from the 2026-11 growth run
#   (ff-167-growth scratch/growth/pairs8), a 1206x2622 in-app capture. Skipped when that folder is missing.
# - health: screens/health-allergens is used as it is; only its background strip is made here.
# - themes: one capture of the same bottle screen in each of the four app themes, from the 2026-11-15
#   fill-stage run (ff-167 scratch/fill/r2/frames). Skipped when that folder is missing; the committed
#   webps stay as they are.
# The growth strip is taken just outside the plot (beside the axis labels) and the health strip from INSIDE the card / the allergen panel, because the animation
# holds back only the plot and the allergen rows, so the gap shows that card's own colour.
save(store_screen("07-family"), "family")
background_strip(store_screen("07-family"), "family")
background_strip(Image.open(ROOT / "screens" / "health-allergens-720.webp"), "health", (0.052, 0.066), (0.935, 0.952))

GROWTH_FRAME = Path.home() / "Developer/ff-167-growth/scratch/growth/pairs8/growth-along-ocean.png"
if GROWTH_FRAME.exists():
    GROWTH = Image.open(GROWTH_FRAME).convert("RGB")
    save(GROWTH, "growth")
    background_strip(GROWTH, "growth", (0.14, 0.155), (0.875, 0.89))

THEME_FRAMES = Path.home() / "Developer/ff-167/scratch/fill/r2/frames"
for theme in ("ocean", "forest", "lavender", "midnight"):
    frame = THEME_FRAMES / f"fill-pinned-{theme}-en-i17.png"
    if frame.exists():
        save(Image.open(frame).convert("RGB"), f"theme-{theme}", quality=74)
