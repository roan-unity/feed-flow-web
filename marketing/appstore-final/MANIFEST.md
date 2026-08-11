# App Store screenshot sets — FINAL · 2026-08-11 (from b244)

Two complete 10-frame sets, captioned, App-Store-sized (1290×2796), Ocean theme,
one baby ("Nora"). Metric = ml/kg, imperial = oz/lb. Produced via
`Scripts/store_frame.py` (caption layer) + `Scripts/make_lockscreen.py` (frame 2)
over the RailV2 captures, plus the hand-built family split (frame 9).

## The 10 (both metric/ and imperial/)
1. safe window — Is that bottle still good?
2. **lock screen** — The countdown on your lock screen (real Live Activity)
3. log fast — Log any feed in three seconds
4. what's normal — What's normal, for your baby
5. **FlowCast** — The next feed and the gaps between  *(NEW — merged screen w/ braid)*
6. report — A feeding & growth report
7. growth — Where they land on the curve
8. allergens — Nine allergens, and where you are
9. **family split** — Everyone who helps, one shared story  *(NEW — lock notification + invite view)*
10. whole day — Your whole day, one calm screen

## Decisions made (easy to change)
- Dropped the "71% less waste" and "week journal" frames from the storyboard's 11 →
  swapped in the cleaner "log fast" frame to reach 10 and avoid a claim-sensitive number.
- Family frame = the split composite Robin described (not the plain family screen).

## Known caveats (minor)
- **growth (frame 7) is the metric capture in BOTH sets** — recapture with
  `-uitestUnits imperial` if the US set should show lb/in (percentile is unit-agnostic).
- Family-split lock panel reads 9:41 (others 8:58) — cosmetic.
- Caption ground on the family frame is ~1 shade lighter than the rail frames.

## NOT uploaded to ASC — app is mid-review; screenshot swap is Robin's call (do it
## deliberately, ideally right after approval).
