// Model-tier routing. Pure functions, no I/O.
//
// Rule: the fast chain answers by default. A turn goes to the strong chain up
// front only for reasons we can see in the text (length, comparison / "why"
// wording, a long conversation). Billing, refund, bug and health wording does
// NOT pick the strong chain: handing over is a tool call, not intelligence.
//
// Each tier is a list of OpenRouter model slugs. OpenRouter tries them in order
// (its `models` fallback array) and reports which one answered.

export const DEFAULT_MODELS = {
  fast: ['nvidia/nemotron-3.5-super-vl:free', 'google/gemini-2.5-flash-lite', 'mistralai/mistral-small-2603'],
  strong: ['mistralai/mistral-medium-3.1', 'google/gemini-2.5-flash-lite'],
};

export const ROUTING = {
  LONG_MESSAGE_CHARS: 400, // latest user message longer than this -> strong
  STRONG_FROM_USER_TURN: 5, // user turn number >= this -> strong
};

export const HAND_OVER_TARGETS = ['support', 'founder'];
export const HAND_OVER_REASONS = ['billing', 'bug', 'account', 'request', 'unknown', 'feedback', 'important'];

// Word-edge match that also works for accented letters (\b does not).
const edge = (alternatives) =>
  new RegExp(`(?<![\\p{L}\\p{N}])(?:${alternatives.join('|')})(?![\\p{L}\\p{N}])`, 'iu');

const COMPLEX = edge([
  // English
  'compar(?:e|ed|es|ing|ison|isons)',
  'versus',
  'vs\\.?',
  'differences?\\s+between',
  "what(?:'s|\\s+is)\\s+the\\s+difference",
  'why',
  'explain\\s+how',
  // Spanish
  'comparar',
  'comparaci[oó]n',
  'compara',
  'diferencias?\\s+entre',
  'por\\s?qu[eé]',
  'expl[ií]ca(?:me)?\\s+c[oó]mo',
  // French
  'comparer',
  'comparaison',
  'compare',
  'diff[eé]rences?\\s+entre',
  'pourquoi',
  'expliqu(?:e|er)\\s+comment',
  // German
  'vergleich(?:e|en|t)?',
  'unterschied(?:e)?\\s+zwischen',
  'warum',
  'wieso',
  'weshalb',
  'erkl[aä]r(?:e|en)?\\s+(?:mir\\s+)?wie',
  // Norwegian, Swedish, Danish
  'sammenlign(?:e|er|ing)?',
  'forskjell(?:en)?\\s+(?:p[aå]|mellom)',
  'hvorfor',
  'forklar\\s+hvordan',
  'j[aä]mf[oö]r',
  'skillnaden?\\s+mellan',
  'varf[oö]r',
  'forskel(?:len)?\\s+p[aå]',
]);

export function userTurnCount(messages) {
  return Array.isArray(messages) ? messages.filter((m) => m && m.role === 'user').length : 0;
}

/** Why a tier was chosen: { tier, reason }. reason is 'default' for fast. */
export function explainTier(messages) {
  const list = Array.isArray(messages) ? messages : [];
  const turns = userTurnCount(list);
  const latest = [...list].reverse().find((m) => m && m.role === 'user');
  const text = typeof latest?.content === 'string' ? latest.content : '';
  if (text.length > ROUTING.LONG_MESSAGE_CHARS) return { tier: 'strong', reason: 'long_message' };
  if (COMPLEX.test(text)) return { tier: 'strong', reason: 'complex_keyword' };
  if (turns >= ROUTING.STRONG_FROM_USER_TURN) return { tier: 'strong', reason: 'long_conversation' };
  return { tier: 'fast', reason: 'default' };
}

/** 'fast' | 'strong' */
export function chooseTier(messages) {
  return explainTier(messages).tier;
}

function parseList(value) {
  if (typeof value !== 'string') return null;
  const list = value.split(',').map((s) => s.trim()).filter(Boolean);
  return list.length ? list : null;
}

/** The model chain for a tier, from CHAT_MODELS_FAST / CHAT_MODELS_STRONG (comma separated) or the defaults. */
export function modelsFor(env, tier) {
  const e = env || {};
  return tier === 'strong'
    ? parseList(e.CHAT_MODELS_STRONG) || [...DEFAULT_MODELS.strong]
    : parseList(e.CHAT_MODELS_FAST) || [...DEFAULT_MODELS.fast];
}

export const handOverTool = {
  type: 'function',
  function: {
    name: 'hand_over',
    description:
      'Pass this conversation to a person by showing the visitor an email form. to "support": bugs, billing, refunds, lost data, sharing or account trouble, or a how-to the knowledge does not cover. to "founder": you are unsure, or it seems important (partnerships, press, creators, feature ideas, complaints, anything about a baby\'s safety in the app). For the founder, offer first and call this only after the visitor says yes or has asked for a person. Call it alongside one short sentence for the visitor.',
    parameters: {
      type: 'object',
      properties: {
        to: { type: 'string', enum: HAND_OVER_TARGETS },
        reason: { type: 'string', enum: HAND_OVER_REASONS },
        summary: {
          type: 'string',
          description: 'One or two sentences in English: what the visitor needs. No personal details.',
        },
      },
      required: ['to', 'reason', 'summary'],
    },
  },
};

export const handUpTool = {
  type: 'function',
  function: {
    name: 'hand_up',
    description:
      'Call this, with no text, when the question needs more careful reasoning than you can give. A stronger assistant will answer instead.',
    parameters: { type: 'object', properties: {} },
  },
};

/** Fast gets hand_up + hand_over; strong only gets hand_over (it has nobody to hand up to). */
export function toolsFor(tier) {
  return tier === 'fast' ? [handUpTool, handOverTool] : [handOverTool];
}

/** Turn accumulated tool calls into { handUp, handOver }. */
export function interpretToolCalls(toolCalls) {
  let handUp = false;
  let handOver = null;
  for (const call of toolCalls || []) {
    if (call.name === 'hand_up') handUp = true;
    if (call.name === 'hand_over' && !handOver) {
      let args = {};
      try {
        args = JSON.parse(call.arguments || '{}');
      } catch {
        args = {};
      }
      handOver = {
        type: 'hand_over',
        to: HAND_OVER_TARGETS.includes(args.to) ? args.to : 'support',
        reason: HAND_OVER_REASONS.includes(args.reason) ? args.reason : 'unknown',
        summary: typeof args.summary === 'string' ? args.summary.slice(0, 300) : '',
      };
    }
  }
  return { handUp, handOver };
}
