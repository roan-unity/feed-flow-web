# App Store screenshot sets — FINAL (in progress) · 2026-08-11

Captioned, App-Store-sized (1290×2796) marketing frames, produced from **b244** via
`Scripts/store_frame.py` (caption layer) over the RailV2 captures. Two unit systems.

## DONE — 7 of ~10 per set, metric + imperial
safeWindow · whatsNormal · report · **flowcast (NEW — merged screen w/ braid)** ·
allergens · **family (Everyone who helps)** · homeClean.
Metric = ml, imperial = oz. Fresh FlowCast is the big change vs the current ASC set.

## OWED — 3–4 frames (the tooling diverged; needs a focused finish + Robin's calls)
- **lessWaste** (waste/efficiency), **growth**, **lockscreen** (the safe-window Live
  Activity — build via `Scripts/make_lockscreen.py`), and **weekJournal** — the current
  rail capture tests don't shoot these to match the `store_frame` storyboard slots.
- **Canonical 10 is undecided.** The `store_frame` storyboard (11 slots), the rail
  capture tests, and the set already uploaded to ASC disagree. Robin picks the final 10.
- **Family frame — two options here:** the pipeline's plain captioned family frame
  (`store-10-family.png`) OR Robin's requested **split composite** (lock-screen
  notification + invite view — `store-XX-family-split-composite.png`, v1). If the split
  wins, it needs a caption band + an imperial (oz) variant of the "120 ml" notification.

## Reproduce / finish
Metric:   base `AppStoreRailV2CaptureTests` (now `-uitestUnits metric`) → store_frame --rail
Imperial: `AppStoreRailV2ImperialCaptureTests` → store_frame --rail
Lock frame: `Scripts/make_lockscreen.py`. NOT uploaded to ASC (app mid-review — Robin's call).
