# Nora, the site chat

`POST /api/chat` (`functions/api/chat/index.js`) streams Nora's answers (SSE: `delta`, `action`, `done`, `error`).
`POST /api/chat/escalate` emails a hand-over to support or the founder. Everything in `functions/_chat/` is
logic and data, not routes, and Cloudflare Pages does not publish the `functions/` folder.

## Run it locally (no wrangler)

    OPENROUTER_API_KEY="$(cat /path/to/key)" node scripts/chat-dev.mjs --port 7222

Open http://127.0.0.1:7222/ . Without a key `/api/chat` answers `503 not_configured` and the widget shows its contact form.
Pinned widget states for screenshots: `?chatdemo=bubbles`, `handsupport`, `handfounder`, `answered`, `escalate`, `closedform` and more (see the bottom of `chat.js`).

## Environment (Cloudflare Pages, production and preview)

| Name | Needed | What |
| --- | --- | --- |
| `OPENROUTER_API_KEY` | yes | Without it `/api/chat` answers `503 not_configured` and the widget falls back to the form. |
| `CHAT_MODELS_FAST` | no | Comma separated OpenRouter slugs, tried in order. Default `nvidia/nemotron-3.5-super-vl:free,google/gemini-2.5-flash-lite,mistralai/mistral-small-2603`. |
| `CHAT_MODELS_STRONG` | no | Default `mistralai/mistral-medium-3.1,google/gemini-2.5-flash-lite`. |
| `RESEND_API_KEY` | for the form | Sends the hand-over emails. |
| `FOUNDER_EMAIL` | no | Where `to: "founder"` goes. Falls back to support@tryfeedflow.app. |
| `ESCALATION_FROM` | no | Sender address. |
| `TURNSTILE_SECRET`, `CHAT_SESSION_SECRET` | no | The bot check. **Off unless `TURNSTILE_SECRET` is set.** |
| `AI_GATEWAY_URL` | no | Route OpenRouter calls through a gateway. |

The old behaviour, a hard failure when the Turnstile secret is missing, is gone on purpose. The money ceiling for now is the hard limit on the
OpenRouter key, plus a best-effort per-visitor counter in the edge cache (20 chat messages and 5 form sends an hour, then `429`). Also kept: 12 visitor
turns, 1,000 characters a message, 8 messages sent upstream, 16 KB body, `max_tokens` 350.

The `done` event carries the model that actually answered. It is logged server-side (`evt: chat`) and never shown to the visitor.

## Knowledge

    node scripts/build-chat-knowledge.mjs

Strips the English pages of the site and appends every `.md` in `functions/_chat/chat-knowledge/`. Writes `functions/_chat/knowledge.js` (commit it).
A test fails when it is out of date. Over 120,000 characters, the longest guides are dropped first and listed.

## Tests and evaluation

    node --test scripts/chat-function.test.mjs scripts/chat-escalate.test.mjs
    node scripts/chat-eval.mjs --key-file <file> --out <dir> [--chain]
