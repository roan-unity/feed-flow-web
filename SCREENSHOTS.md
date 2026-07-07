# Screenshot capture brief — feed-flow-web

> The site uses **real app screens** (no mock-ups) as its art. These must be captured from the
> actual app on a Mac/simulator — they can't be produced from the web repo. Drop each file into
> `screens/` at the path below; the HTML already references them.

## Capture specs (apply to all)
- **Device:** iPhone 17 simulator (matches current frames), portrait.
- **Content:** a realistic but tidy state — a baby named e.g. "Mila", a few days of data, no debug/placeholder text. Match the calm tone (no alarming numbers).
- **Format:** JPG, portrait phone aspect (~1179×2556 or the same ratio as the current `screens/*.jpg` ≈ 120–145 KB each). Keep file size reasonable.
- **Theme:** the current 5 screens are light-theme. Capture new ones **light** to match; optionally also capture a **dark** set later if we add theme-matched swaps.
- **No premium blur** on the free-tier screens noted below.

## Refresh (existing 5 — recapture from current build 96 UI)
| File | Section | State to show |
|---|---|---|
| `screens/home.jpg` | Hero | Home: milk-today range, live timeline (bottle/breast/solids), the one-tap slider. (Current one is already close.) |
| `screens/forecast.jpg` | Beat 1 · FlowCast | Next-feed countdown ring + Day-Ahead plan (noon/evening/night). |
| `screens/savings.jpg` | Beat 2 · Save | Bottle efficiency: baseline vs current, efficiency by feed type. |
| `screens/live-logging.jpg` | Beat 3 · Calm logging | A feed in progress: slider + smart button + live amount-left. |
| `screens/growth.jpg` | Beat 4 · Growth | Weight-for-age on WHO percentile bands + the feeding→growth link. |

## New captures needed (referenced/aspirational — P-ranked)
| Priority | File | Where it'd go | State to capture |
|---|---|---|---|
| **P0** | `og.png` | ✅ **DONE** — generated (1200×630 brand card). Replace later with a Baloo-font version if you want pixel-brand parity. | — |
| **P1** | `solids.jpg` | (optional) a device-frame beat for the Food Story section | Solids meal builder / food grid with a logged meal + tastings verdicts (loved/liked/meh/refused) + "new this week". |
| **P1** | `allergens.jpg` | (optional) Food Story section | Allergen journal: the big-9 "X of 9 introduced" checklist, a couple introduced, one gentle reaction note. **Free-teaser state, no blur.** |
| **P1** | `spectrum.jpg` | "Every feed, one place" card / a new beat | A day timeline with **mixed feed types in one log** — bottle · breast · pump · solids · water. Proves "not just bottles". |
| **P2** | `weight.jpg` | "Reassurance in the early days" card | Early weight tracking with a calm "within the expected early range" card. Frame as reassurance — **never** the word "monitor", no medical claim. |
| **P2** | `safe-window.jpg` | (promote safe-window to a beat later) | A prepared bottle with the safe-window countdown ring ("still good for 2h 40m"). |

> **Note on the Food Story section:** it currently uses a polished **HTML motif** (allergen chips +
> tastings), not a screenshot — so it looks complete today without any capture. `solids.jpg` /
> `allergens.jpg` are only needed if you later want to convert it (or add) a device-frame beat.

## Not to capture / don't market (per POSITIONING decisions)
- **Family sharing** — postponed; site says "coming soon". No sharing screenshot.
- **Milestone photos** — not shipped; no photo screenshots.
- **Sleep** — not built.
- **Allergen premium history/export** — gate not wired yet; don't show a paywalled allergen state.
