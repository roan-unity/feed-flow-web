"""Printable feeding log (2026-11-16): one-day sheet in English, Norwegian and Swedish, A4 + US Letter.

Writes printables/feeding-log-<lang>-<size>.pdf and a PNG preview per language, using headless Chrome.
Run: python3 scripts/printables.py   (re-run after any wording change; PDFs are committed)
"""
import shutil, subprocess, tempfile
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "printables"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROWS = 12

T = {
    "en": {
        "title": "Newborn feeding log", "date": "Date", "baby": "Baby",
        "cols": ["Time", "Breast<br><small>L min / R min</small>", "Bottle made at", "Type<br><small>formula / breast milk</small>", "Offered", "Drank", "Pumped", "Wet", "Dirty", "Notes"],
        "type": "F &nbsp; BM", "unit": "ml / oz",
        "totals": "Day totals", "t": ["Feeds", "Drank", "Pumped", "Wet diapers", "Dirty diapers"],
        "tip": "Write the time you make each bottle. Use it within the time on the formula label or your local guidance, and make a fresh one if unsure.",
        "foot": "Free printable from tryfeedflow.app/printable-feeding-log &middot; A record, not medical advice. If you are worried about feeding, wet diapers or how your baby seems, contact your pediatrician or health nurse.",
    },
    "nb": {
        "title": "Matingslogg for nyfødt", "date": "Dato", "baby": "Barn",
        "cols": ["Klokka", "Amming<br><small>V min / H min</small>", "Flaske laget kl.", "Type<br><small>MME / morsmelk</small>", "Gitt", "Drukket", "Pumpet", "Våt", "Bæsj", "Notater"],
        "type": "MME &nbsp; MM", "unit": "ml",
        "totals": "Dagens sum", "t": ["Måltider", "Drukket", "Pumpet", "Våte bleier", "Bæsjebleier"],
        "tip": "Skriv ned når du lager hver flaske. Bruk den innen tiden som står på pakningen eller helsestasjonens råd, og lag en ny hvis du er usikker.",
        "foot": "Gratis utskrift fra tryfeedflow.app/no &middot; En logg, ikke medisinske råd. Er du bekymret for måltider, våte bleier eller hvordan barnet har det, kontakt helsestasjonen eller legen.",
    },
    "sv": {
        "title": "Matningslogg för nyfödd", "date": "Datum", "baby": "Barn",
        "cols": ["Tid", "Amning<br><small>V min / H min</small>", "Flaska gjord kl.", "Typ<br><small>ersättning / bröstmjölk</small>", "Erbjudet", "Drack", "Pumpat", "Blöt", "Bajs", "Anteckningar"],
        "type": "E &nbsp; BM", "unit": "ml",
        "totals": "Dagens summa", "t": ["Måltider", "Druckit", "Pumpat", "Blöta blöjor", "Bajsblöjor"],
        "tip": "Skriv upp när du gör varje flaska. Använd den inom tiden på förpackningen eller enligt BVC:s råd, och gör en ny om du är osäker.",
        "foot": "Gratis utskrift från tryfeedflow.app/sv &middot; En logg, inte medicinska råd. Är du orolig för måltider, blöta blöjor eller hur barnet mår, kontakta BVC eller läkare.",
    },
}
SIZES = {"a4": "A4", "letter": "letter"}


def sheet(lang, size):
    t = T[lang]
    head = "".join(f"<th>{c}</th>" for c in t["cols"])
    row = ("<tr><td></td><td class='lr'><span>/</span></td><td></td>"
           f"<td class='opt'>{t['type']}</td><td></td><td></td><td></td>"
           "<td class='box'>&#9744;</td><td class='box'>&#9744;</td><td></td></tr>")
    totals = "".join(f"<div><span>{x}</span><i></i></div>" for x in t["t"])
    return f"""<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8"><title>{t['title']}</title><style>
@page {{ size: {SIZES[size]}; margin: 11mm 10mm 10mm; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif; color: #102f38; font-size: 10pt; }}
.top {{ display: flex; align-items: flex-end; justify-content: space-between; border-bottom: 2.5pt solid #2f7886; padding-bottom: 6pt; margin-bottom: 8pt; }}
h1 {{ font-size: 21pt; margin: 0; letter-spacing: -.3pt; }}
.brand {{ font-weight: 800; color: #2f7886; font-size: 12pt; }} .brand b {{ color: #e87352; }}
.fields {{ display: flex; gap: 16pt; margin: 0 0 8pt; font-size: 10.5pt; }}
.fields div {{ flex: 1; border-bottom: .8pt solid #8fb3ba; padding-bottom: 3pt; }}
.unit {{ font-size: 8pt; color: #48636b; text-align: right; margin: -4pt 0 3pt; }}
table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
th {{ background: #e2f1f3; font-size: 8.4pt; font-weight: 700; padding: 4pt 2pt; border: .8pt solid #9cc0c6; line-height: 1.15; }}
th small {{ font-weight: 400; font-size: 6.8pt; color: #48636b; }}
td {{ border: .8pt solid #b7d2d6; height: {"15.6mm" if size == "a4" else "14.2mm"}; text-align: center; color: #9ab3b8; font-size: 8pt; }}
td.lr span {{ color: #b7d2d6; }} td.box {{ font-size: 13pt; color: #8fb3ba; }}
col.c0 {{ width: 9%; }} col.c1 {{ width: 12%; }} col.c2 {{ width: 10%; }} col.c3 {{ width: 11%; }} col.c4, col.c5, col.c6 {{ width: 8%; }} col.c7, col.c8 {{ width: 6%; }} col.c9 {{ width: 22%; }}
.totals {{ display: flex; gap: 6pt; margin-top: 8pt; align-items: center; }}
.totals strong {{ font-size: 10pt; margin-right: 2pt; white-space: nowrap; }}
.totals div {{ flex: 1; border: .8pt solid #9cc0c6; border-radius: 4pt; padding: 3pt 5pt; height: 34pt; }}
.totals span {{ font-size: 7.6pt; color: #48636b; }}
.tip {{ margin-top: 8pt; background: #f0f7f4; border-left: 3pt solid #e87352; padding: 5pt 8pt; font-size: 8.6pt; }}
.foot {{ margin-top: 6pt; font-size: 7.4pt; color: #48636b; }}
@media screen {{ body {{ padding: 10mm; }} }}
</style></head><body>
<div class="top"><h1>{t['title']}</h1><div class="brand">Feed Flow<b>!</b></div></div>
<div class="fields"><div>{t['date']}:</div><div>{t['baby']}:</div></div>
<div class="unit">{t['unit']}</div>
<table><colgroup>{''.join(f"<col class='c{i}'>" for i in range(10))}</colgroup><thead><tr>{head}</tr></thead><tbody>{row * ROWS}</tbody></table>
<div class="totals"><strong>{t['totals']}</strong>{totals}</div>
<div class="tip">{t['tip']}</div>
<div class="foot">{t['foot']}</div>
</body></html>"""


def main():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for lang in T:
            for size in SIZES:
                src = Path(tmp) / f"{lang}-{size}.html"
                src.write_text(sheet(lang, size), encoding="utf-8")
                pdf = OUT / f"feeding-log-{lang}-{size}.pdf"
                subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                                f"--print-to-pdf={pdf}", src.as_uri()], check=True, capture_output=True, timeout=90)
                print("Built", pdf.relative_to(ROOT), pdf.stat().st_size // 1024, "KB")
            # Preview image (A4 page at 2x), cropped by the window size.
            png = Path(tmp) / f"{lang}.png"
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                            "--window-size=794,1123", f"--screenshot={png}", (Path(tmp) / f"{lang}-a4.html").as_uri()],
                           check=True, capture_output=True, timeout=90)
            shutil.copy(png, OUT / f"feeding-log-{lang}-preview.png")
            print("Built", f"printables/feeding-log-{lang}-preview.png")


if __name__ == "__main__":
    main()
