/* POST /api/chat: the Nora site chat (SSE). The logic lives in functions/_chat/chat-core.js, which is not a route. */
import { handleChat } from '../../_chat/chat-core.js';

export function onRequest({ request, env, waitUntil }) {
  return handleChat({ request, env, waitUntil });
}
