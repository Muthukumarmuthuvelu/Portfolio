// Cloudflare Worker: writes an answer from the passages sent by the chat page.
// Settings > Bindings: add Workers AI with the name AI.  Settings > Variables: ALLOWED_ORIGIN = https://muthukumarmuthuvelu.github.io
const MODEL = '@cf/meta/llama-3.1-8b-instruct'; // a smaller model stretches the free daily allowance
export default { async fetch(req, env) {
  const cors = {'Access-Control-Allow-Origin': env.ALLOWED_ORIGIN, 'Access-Control-Allow-Headers': 'content-type', 'Access-Control-Allow-Methods': 'POST, OPTIONS'};
  if (req.method === 'OPTIONS') return new Response(null, {headers: cors});
  if (req.method !== 'POST' || req.headers.get('Origin') !== env.ALLOWED_ORIGIN) return new Response('Forbidden', {status: 403, headers: cors});
  let b; try { b = await req.json(); } catch { return new Response('Bad request', {status: 400, headers: cors}); }
  const q = String(b.question || '').slice(0, 300);
  const ctx = (Array.isArray(b.chunks) ? b.chunks : []).slice(0, 4).map((c, i) => `[${i + 1}] ${String(c.title).slice(0, 100)}: ${String(c.text).slice(0, 1200)}`).join('\n\n');
  if (!q || !ctx) return new Response('Bad request', {status: 400, headers: cors});
  try {
    const r = await env.AI.run(MODEL, {max_tokens: 300, messages: [
      {role: 'system', content: 'You are a documentation assistant. Answer ONLY from the numbered documentation passages provided. Be concise and cite passage numbers like [1]. If the passages do not contain the answer, reply exactly: I could not find that in the documentation.'},
      {role: 'user', content: `Documentation:\n${ctx}\n\nQuestion: ${q}`}]});
    return new Response(JSON.stringify({answer: r.response}), {headers: {...cors, 'content-type': 'application/json'}});
  } catch (e) { return new Response('Model unavailable', {status: 503, headers: cors}); }
}};
