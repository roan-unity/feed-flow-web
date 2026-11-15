#!/usr/bin/env python3
"""Tell Bing/Yandex/Seznam (IndexNow) which pages changed. ChatGPT search builds on Bing's index.
   python3 scripts/indexnow.py            -> submit every URL in sitemap.xml
   python3 scripts/indexnow.py /compare   -> submit given paths"""
import json, re, sys, urllib.request
from pathlib import Path
KEY = "8dfb129df75e44928a1735cee911c9ca"
ROOT = Path(__file__).resolve().parents[1]
urls = ["https://tryfeedflow.app" + p for p in sys.argv[1:]] or re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text())
body = json.dumps({"host": "tryfeedflow.app", "key": KEY, "keyLocation": f"https://tryfeedflow.app/{KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print(r.status, len(urls), "urls submitted")
