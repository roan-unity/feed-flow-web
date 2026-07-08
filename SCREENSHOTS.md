# Screenshot capture brief — feed-flow-web

> The site uses **real app screens** (no mock-ups) as its art. These must be captured from the
> actual app on a Mac/simulator — they can't be produced from the web repo. Drop each file into
> `screens/` at the path below; the HTML already references them.

## App Store order & best practice (research-backed, 2026)

The **first 3 screenshots drive ~60–70% of installs** and the first 2 show in search results — so
order matters more than count. **Upload 6 (not fewer)** — 6–8 outperforms the minimum. Lead with the
benefit/outcome, not UI. Keep captions short + benefit-led + readable at thumbnail size (squint test).

**Canonical order (matches the website gallery `index.html#screens`):**
1. **Savings** — hero (the money hook + our ASO lead). "See the formula you're not wasting."
2. **Calm logging** — the heart. "One slider. One smart button."
3. **Food story** — the differentiator. "Introduce foods with confidence."
4. **FlowCast** — "Never miss a feed."
5. **Report** — "Doctor-ready in one tap."
6. **Themes** — personalization (users want to see it). "Calm, in your colour."

Sources: first-3 = ~60–70% of conversion, benefit heroes +45%, 6–8 shots +35% engagement, show
dark-mode/themes — apptweak / Screenhance / AppScreenshotStudio 2026.

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

## Design targets → real captures (match these)

The polished frames in `marketing/mockups/` are the **visual target** for the gallery section
(`index.html#screens`) and the App Store. They're representative mockups; the App Store should also
carry **real captures matched to each**. Map:

| Mockup (target) | Real capture to take | The one detail to match |
|---|---|---|
| `mockups/savings.png` | Savings/efficiency screen | money-saved hero + efficiency bars |
| `mockups/flowcast.png` | Today → Looking ahead | next-feed ring + day-ahead rows |
| `mockups/logging.png` | Home / Today | milk-today + live timeline + slider & button |
| `mockups/food-story.png` | Solids journal | smoothie meal + "X of 9" allergens + tastings |
| `mockups/report.png` | Growth + report | weight on WHO bands + Create Report |

When the real captures exist, swap the `<img src="marketing/mockups/…">` in the gallery for the real
files (or keep mockups as the polished App-Store set and use real ones in the device-frame beats).

## Not to capture / don't market (per POSITIONING decisions)
- **Family sharing** — postponed; site says "coming soon". No sharing screenshot.
- **Milestone photos** — not shipped; no photo screenshots.
- **Sleep** — not built.
- **Allergen premium history/export** — gate not wired yet; don't show a paywalled allergen state.
