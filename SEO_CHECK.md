# SEO_CHECK.md: front page rewrite, 2026-11-01

Branch `site/rewrite-2026-11` (not merged, not deployed). Second pass 2026-11-01: sections now follow the message spine (`MESSAGE_SPINE_2026-11-01.md` §2). Brief from Robin: too much text, less slop, to the point, optimised for SEO.

Measured by a small script that parses the HTML (no browser): visible text is everything inside `<body>` except `<script>`, `<style>`, `<template>`, `<svg>` and `<noscript>`. "Tokens" counts every whitespace-separated token (this matches the ~1,367 Robin measured); "words" ignores tokens with no letter or digit (arrows, dots). Nav, footer and the health sentence are included. Alt text is not visible text.

## Before and after

| Measure | Before (`index.html` at branch start) | After |
|---|---|---|
| Visible words (tokens) | 1,375 (1,308 words only) | **442** (tokens; svg and comments excluded); limit 550 |
| Title tag | 57 chars, has an em dash: `Feed Flow! — The baby feeding app that watches the bottle` | **57 chars**, no dash: `Baby Feeding Tracker with a Bottle Countdown \| Feed Flow!` |
| Meta description | 280 chars | **150 chars**: `Feed Flow! is a baby feeding tracker for iPhone: a countdown on every bottle, a breastfeeding and pumping log, and a pediatrician report. Free to log.` |
| H1 | 1 | 1: `A baby feeding tracker that counts down every bottle` |
| H2 | 7 | **5** (and no H3; the old page had 13) |
| Images with alt | 12 of 12 | 6 of 6, each describing what the frame shows |
| Em dashes in the file | 54 (plus 1 en dash) | **0** (0 en dashes), including title, meta, JSON-LD, alts, `llms.txt` |
| Internal links | 5 page links (affiliate, privacy, support) + 10 same-page anchors | 7 page links (FAQ, Support, Privacy, Terms, Affiliates, home x2) + 0 anchors |
| External links | 7 | 6 (App Store x4 incl. review link, Reddit, Instagram) |
| HTML size | 67.4 KB | 25.1 KB |
| Image bytes, all images loaded | 2,595,709 (12 JPEGs, 7 are duplicates of each other under another path) | 100,414 at 1x, 244,786 if every image loads at 2x |
| Image bytes before the first scroll (hero) | 218,607 | 13,022 at 1x, 29,510 at 2x |
| Image formats and sizing | JPEG, no width/height attributes, 11 of 12 lazy | WebP 360 and 720 wide (1x/2x `srcset`), width and height on all 6 (no layout shift), 5 of 6 lazy, hero eager with `fetchpriority="high"` and a preload |
| Render-blocking tags in `<head>` | 1 stylesheet (Google Fonts, 3 weights) | **0**. The font stylesheet loads without blocking (preload + onload, with a `<noscript>` fallback), one weight (800, the wordmark only). Scripts are all `defer`. |
| Script on the page | theme toggle + slider demo + scroll reveal | theme toggle only |
| canonical, OpenGraph, Twitter, JSON-LD, robots, sitemap | present | all kept and updated (see below) |

Not measured (needs a browser): real Lighthouse scores, LCP time, contrast ratios. Checked by eye in the preview at 1280, 375 and in dark mode: no horizontal scroll at 375, all images render.

## What changed in the plumbing

- `<title>` and meta description: primary phrase "baby feeding tracker" first.
- `og:title`, `og:description`, `twitter:*` rewritten; `og:image:alt` added; `robots` meta with `max-image-preview:large` added; `theme-color` added.
- JSON-LD: WebSite and SoftwareApplication descriptions rewritten, `featureList` trimmed to what the page says, a `screenshot` array of the six WebP frames added, the offer text now names what is free and what is Premium. Organization node kept.
- `sitemap.xml`: home `lastmod` set to 2026-11-01. `robots.txt` unchanged. `llms.txt` rewritten to match the page (the unverified competitor comparison was dropped).

## Calls I made that Robin may want to overrule

0. **Spine order and the one-meter claim.** The five sections run: bottle you can trust, all her milk in one meter, learns her rhythm (FlowCast), everyone who feeds her, report. The one-meter section's frame (04 Today) has no by-source meter yet, so its copy says only "one total, in ml or oz" and no by-source split; an HTML comment `swap frame: milk-today meter, DEV355-4` marks it for the swap. Its H2 is "Every feed in one total, in ml or oz" until the meter ships, then "All her milk, one meter".
1. **Campaign link.** The brief said to keep the `pt=`/`ct=` values already on the page. The old page had none (every link was the bare `apps.apple.com/app/id6782075454`). I used the documented form `https://apps.apple.com/app/apple-store/id6782075454?pt=126898045&ct=website&mt=8` on all three Download buttons. If he wants the bare link back it is one find and replace. The review link in the footer stays bare.
2. **Health sentence.** The old front page never carried the in-app health-responsibility sentence. It only said "Feed Flow! is not a medical device" in a footnote of the removed "honest numbers" section. The website mirror lives in `privacy.html` section 7a. I put two sentences from the current site verbatim in a footnote above the footer: "Feed Flow! is not a medical device." and "Before you act on a number, check it against the label, the pack or your pediatrician: this is a record, not medical advice." ("health nurse" was replaced by "pediatrician" on 2026-11-01 for US readers; the in-app wording has an em dash, so the website v2 wording is the one used).
3. **Images come from the 1.65.8 build 354 store set, which is in App Review.** Frame 07 (activity feed) shows the owner's own feeds as "You" rows; that is new in 354. In the build that is live now, the feed lists other caregivers' feeds. The claim on the page ("shows who fed and when") is true in both. Hold the merge until 354 is live if he wants the pictures to match exactly.
4. **`og.png` still says** "Baby feeding, off your mind — and on record." with an em dash, drawn inside the image. It is a picture, so I left it. Sources are in `og-src/`.
5. **Not in the five H2s, left out on purpose:** savings/waste figures (the "~8 to 15 L" stat is an unsourced estimate and the waste story is not in his order of value), allergens and solids, twins, milestones, privacy as its own section (one sentence under the button instead), founder story (one footer line), the interactive slider demo, the gallery, pricing numbers (never on marketing surfaces).
6. **Target phrases in visible copy:** baby feeding tracker (title, meta, H1), formula feeding tracker (intro), bottle feeding (Home section), breastfeeding and pumping log (intro, meta). Each appears once or twice, inside normal sentences.
7. **Old files are still on disk**: `screens/*.jpg` and `screens/store/*.jpg`. Nothing on the front page references them now. Delete after Robin confirms. Separate from this rewrite: the Download buttons still carry the class `btn-primary`, which makes `analytics.js` send a stale "Beta Apply" event next to "AppStore Click". That was already so before; I left it.)
8. Every `.md` in the repo root, this one included, is served publicly by Netlify. Nothing here is secret, but he may not want the claims table public.

## Every claim on the page, and where in the app it is true

"Day 1" is what the parent sees before any feed is logged (rule: never sell a surface that will be empty).

| Claim on the page | Where in the app | Tier | Day 1 |
|---|---|---|---|
| A one-hour clock starts when you start a formula bottle | Home, log a Formula bottle: live feeding sheet with the ring, `STARTED`, `ENDS` (frame 01). Default formula window 60 minutes. | Free | Works from the first bottle |
| Change the hour for each kind of feed | Settings, the safe-window duration for each feed type (formula 1 h, pumped milk 2 h by default) | Free | Yes |
| The clock keeps running on the lock screen; time left and what is left show there | Live Activity on the lock screen while a bottle runs (frame 02: time left, bottle size, taken, left) | Free | Yes, while a bottle runs |
| When time is up it asks how much the baby took | Safe-window expiry prompt (also in the store description) | Free | Yes |
| After about four days of feeds it shows a likely time for the next feed | Home, `NEXT MEAL` chip; personalised predictions start after 4 logged days | Free (the time on Home) | Before day 4 the chip does not promise a time; the copy says "after about four days" |
| Premium shows the whole day ahead | Tap the chip: FlowCast screen (frame 03). Free users see the paywall there. | Premium | Needs the same four days |
| It's a guide, not a promise | FlowCast footer: "A guide from Nora's recent feeds, not a promise." | | |
| The day adds up to one total, in ml or oz | Today tab: the day meter and total (frame 04). By-source split is NOT claimed (meter in build, DEV355-4) | Free | Designed empty state with the log button |
| Log a bottle, a breastfeeding session or a pump in a few taps, one hand | Logging panel on Today; feed types radial picker | Free | Yes |
| Bottles, breastfeeding, pumping, solids and water in the same log | Five feed types in the picker | Free | Yes |
| Invite a partner, grandparent or sitter; up to five people, free, each on their own phone | Family tab, invite through iCloud sharing ("Free for up to 5 people") | Free | Yes (needs a connection to send the invite) |
| A feed can take a moment to show up | iCloud sync delay; honesty line from the store description | | |
| Premium adds an activity feed that shows who fed and when | Family, Activity Feed (frame 07) | Premium | Empty until a second caregiver logs; the copy sells it as Premium, not as free |
| Share a PDF of the feeds, amounts and weekly trend | Baby Report, Feeding scope, `Share PDF` (frame 10) | Premium | Thin until a few days are logged; the copy says "made from your own log" |
| Print it or send it before the visit | The share sheet on the PDF | Premium | |
| Vitamin D: log the drops, counted with what your formula's label lists (the block is now "Vitamin D and nutrition") | Vitamin D card, formula label vitamin D counted from the product's label | Full card is Premium and needs "Track vitamin D" on; no dosing or "enough" claim on the page | Hidden until switched on |
| Nutrition: energy, protein, fat, vitamin D and iron from the formula's label, added up for the day | Nutrition editor and analytics Macros card read `FormulaCatalog.json` per 100 ml (no vitamin C, no other nutrient) | Free to set; the analytics card is Premium | Needs a formula chosen |
| Formula finder: compare formulas using the numbers on each label | Compare formulas sheet (product picker) | Free | Yes |
| Free forever: logging, the bottle countdown, the next feed's time, caregiver sharing | See the rows above | Free tier | |
| Premium adds the day-ahead forecast, the activity feed, the vitamin D meter, the report and the full history | PREMIUM.md tier table | Premium | |
| Pay once if you prefer | Lifetime purchase on the paywall (no price on the page) | | |
| Your baby's data stays in your own iCloud | Settings, Account and data; no Feed Flow server holds the log | | |
| Made by a dad in Norway who's also a developer | Same wording as the previous footer story | | |
| Made by parents who know what tired is | Brand line (spine §1 #5), once, in the closing block, not a headline | | |
| Slide the bottle to what's left and the app works out how much your baby drank | Live bottle sheet slider (frame 01) | Free | Yes |
| Not a medical device; check the number against the label, the pack or your pediatrician | Same sentences as `privacy.html` 7a | | |
| Free to log, forever | Core logging is never paywalled | | |

Captions: the page has no visible captions. The store frames draw their own headline and sub-line, so the page copy, the one changed alt (hero) and the six JSON-LD `caption` values were rewritten to say something the frame does not (hero sub-line no longer repeats "Is that bottle still good?"; report H2 no longer repeats "Hand your pediatrician a clear report"). Section copy was also trimmed where it repeated a frame sub-line (lock screen, Today, FlowCast, family, report). Kept on purpose: "It's a guide, not a promise" (honesty line, also small print in frame 03).

What the page never says: savings or money, "AI", "only", "enough", "safe" as a verdict (it says the clock counts, not that the milk is fine), any number about the baby, any price, any comparison with other babies or apps.

## Preview

```
cd "/Users/robinandersson/Documents/FeedFlow Web" && python3 -m http.server 8787
```

Then open http://127.0.0.1:8787/ . Check 375 px wide and the theme toggle (top right).
