# Website analytics — leads, clicks, and conversions

Privacy-first funnel tracking for tryfeedflow.app. Cookieless, no PII, no consent banner —
consistent with the brand ("your iCloud, not our servers") and the privacy policy §4.

## What's wired (in the pages already)

`index.html` and `beta.html` load two small scripts in `<head>`:
- **Plausible** (`script.outbound-links.tagged-events.js`) — cookieless pageviews + outbound-link +
  custom-event support, EU-hosted.
- **`analytics.js`** (first-party, in this repo) — captures the campaign source from the URL and
  fires custom events on the conversion clicks.

### Events it fires
| Event | When | Props |
|---|---|---|
| pageview | every page (Plausible automatic) | — |
| **Beta Apply** | click "Apply for free early access" / any `beta.html` link | `source`, `campaign` |
| **Affiliate Click** | click any `affiliate.html` link | `source` |
| **AppStore Click** | click any `apps.apple.com` link (fires once launched) | `source`, `campaign` |

`analytics.js` also **carries the campaign source into the beta page URL** (`?utm_source=…`) so a
lead's origin is known on the apply form, and remembers the source for the session.

## Turn it on (one-time, ~10 min)

1. Create a **Plausible** account and add the site **`tryfeedflow.app`** (plausible.io, or
   self-host). That's it — the script is already on the pages; it starts collecting on your next
   deploy. *(Until the account exists the script 404s harmlessly and events no-op — nothing breaks.)*
2. **Prefer free?** Swap Plausible for **Cloudflare Web Analytics** (also cookieless): replace the
   Plausible `<script>` with Cloudflare's beacon. `analytics.js` still runs; custom events are
   Plausible-specific, so on Cloudflare you'd rely on pageviews + the source in the beta URL.
3. Deploys happen on merge to `main` (Netlify auto-deploy).

## Tag your inbound links (so sources are legible)

Whenever you or the agent shares a link, add UTM params:
```
https://tryfeedflow.app/?utm_source=reddit&utm_medium=comment&utm_campaign=formula-savings
https://tryfeedflow.app/?utm_source=ig&utm_campaign=elise
https://tryfeedflow.app/?utm_source=babyverden&utm_campaign=safe-window
```
Then Plausible shows visits **and** Beta-Apply conversions **by source** — you see which channel
actually drives applications, not just clicks. Keep a short list of source names so they stay
consistent (reddit · ig · fb · tiktok · linkedin · babyverden · kvinneguiden · newsletter · partner-<name>).

## The full funnel (ties to the agent's `MEASUREMENT.md`)

```
outreach/social (UTM link)  →  site visit  →  Beta Apply  →  [at launch] AppStore Click  →  install
      Layer 2 source            Plausible      Plausible          Plausible            App Store Connect
```
- **Now (pre-launch):** the conversion that matters is **Beta Apply** — leads into early access.
  Watch Beta-Apply-by-source weekly; double down on the source that converts, not just the one that
  gets clicks.
- **At launch:** add the real App Store link. Attribution of the actual **install** is done with an
  **App Store Connect campaign link** (App Analytics → Acquisition → Campaigns) — Apple generates a
  URL per channel and attributes installs first-party. Use one per source. The `AppStore Click`
  event already fires on our side so you can compare click-through vs. installs. **No third-party
  attribution SDK** — consistent with the privacy policy.

## Reading it (weekly, 5 min)
1. Plausible → **Top Sources** + the **Beta Apply** goal → which channel converts best?
2. Plausible → **Top Pages** → where do people drop?
3. (Launch) App Store Connect → downloads per campaign link + promo-code redemptions.
4. Feed the winners back into the outreach segments; drop what doesn't convert.
