from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
W, H = 1200, 630
image = Image.new("RGB", (W, H), "#eef7f8")
draw = ImageDraw.Draw(image)
draw.ellipse((760, -300, 1380, 320), fill="#d7edef")
draw.ellipse((-180, 470, 360, 910), fill="#e1f0f1")

baloo = str(ROOT / "assets/Baloo2-VF.ttf")
arial = "/System/Library/Fonts/Supplemental/Arial.ttf"
arial_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
font_logo = ImageFont.truetype(baloo, 48)
font_title = ImageFont.truetype(baloo, 66)
font_sub = ImageFont.truetype(arial, 27)
font_pill = ImageFont.truetype(arial_bold, 21)
font_caption = ImageFont.truetype(arial_bold, 16)

logo_x = 52
draw.text((logo_x, 42), "Feed", font=font_logo, fill="#102f38")
logo_x += draw.textlength("Feed", font=font_logo)
draw.text((logo_x, 42), "Flow", font=font_logo, fill="#2f7886")
logo_x += draw.textlength("Flow", font=font_logo)
draw.text((logo_x, 42), "!", font=font_logo, fill="#e87352")
draw.text((52, 132), "Feeding. Growth.", font=font_title, fill="#102f38")
draw.text((52, 208), "Baby health.", font=font_title, fill="#102f38")
draw.text((54, 309), "One calm app for your", font=font_sub, fill="#48636b")
draw.text((54, 347), "baby's whole day.", font=font_sub, fill="#48636b")
draw.rounded_rectangle((52, 430, 322, 484), radius=27, fill="#1c5e6b")
draw.text((75, 445), "Free to log on iPhone", font=font_pill, fill="#f3fbfc")
draw.text((54, 526), "Bottle countdown · FlowCast · Vitamin D · WHO reports", font=ImageFont.truetype(arial, 17), fill="#48636b")

shots = [
    (ROOT / "screens/formula/01-safe-bottle-720.webp", 610, 126, "Bottle"),
    (ROOT / "screens/flowcast-720.webp", 745, 66, "FlowCast"),
    (ROOT / "screens/store/vitamin-d.png", 880, 132, "Vitamin D"),
    (ROOT / "screens/formula/10-feeding-report-720.webp", 1015, 82, "Report"),
]
for source, x, y, caption in shots:
    with Image.open(source) as shot:
        shot = shot.convert("RGB")
        width = 132
        height = round(shot.height * width / shot.width)
        shot = shot.resize((width, height), Image.Resampling.LANCZOS)
        mask = Image.new("L", (width, height), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, width, height), radius=20, fill=255)
        shadow = Image.new("RGBA", (width + 34, height + 34), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle((17, 17, width + 17, height + 17), radius=22, fill=(15, 43, 53, 70))
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        image.paste(shadow, (x - 17, y - 12), shadow)
        image.paste(shot, (x, y), mask)
        tw = draw.textlength(caption, font=font_caption)
        draw.text((x + (width - tw) / 2, y + height + 16), caption, font=font_caption, fill="#1c5e6b")

image.save(ROOT / "og.png", optimize=True)
print(f"Created {ROOT / 'og.png'} ({W}x{H})")
