// Lab 2: an assistant connects to an MCP server, asks what it offers, uses it, and is refused
// something the server does not offer. Both ends run in this page and exchange real MCP messages.
import { Client, McpServer, InMemoryTransport, z } from './vendor/mcp-sdk.min.js';

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s).replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
const QUESTION = 'Was order 1182 charged twice? What should we do about it?';

// ---------- Kettlewick's data (the same made-up records as the demos) ----------
const ORDERS = {
  1175: { customer: 'Priya Raman', item: 'Stand mixer', price_usd: 249.0, order_date: '2026-09-02', delivered_date: '2026-09-08', final_sale: 'no' },
  1179: { customer: 'Marcus Oyelaran', item: 'Toaster', price_usd: 39.0, order_date: '2026-09-28', delivered_date: '2026-10-03', final_sale: 'no' },
  1182: { customer: 'Dana Whitfield', item: 'Blender', price_usd: 89.0, order_date: '2026-10-14', delivered_date: '2026-10-19', final_sale: 'no' },
  1186: { customer: 'Tomas Lindqvist', item: 'Kettle', price_usd: 45.0, order_date: '2026-10-30', delivered_date: '2026-11-04', final_sale: 'no' },
  1190: { customer: 'Aiko Tanaka', item: 'Coffee grinder', price_usd: 59.0, order_date: '2026-11-06', delivered_date: '2026-11-11', final_sale: 'yes' },
};
const CHARGES = [
  { charge_id: 'C-5001', order_id: 1175, charge_date: '2026-09-02', amount_usd: 249.0 },
  { charge_id: 'C-5007', order_id: 1179, charge_date: '2026-09-28', amount_usd: 39.0 },
  { charge_id: 'C-5012', order_id: 1182, charge_date: '2026-10-14', amount_usd: 89.0 },
  { charge_id: 'C-5013', order_id: 1182, charge_date: '2026-10-14', amount_usd: 89.0 },
  { charge_id: 'C-5020', order_id: 1186, charge_date: '2026-10-30', amount_usd: 45.0 },
  { charge_id: 'C-5026', order_id: 1190, charge_date: '2026-11-06', amount_usd: 59.0 },
];
const POLICY = [
  '1. Returns. Full refund within 30 days of delivery. From day 31 to day 60: store credit, minus 10%. After 60 days: no refund and no credit.',
  '2. Final-sale items. Items marked final sale cannot be returned.',
  '3. Duplicate charges. If a customer was charged twice for the same order by mistake, the extra charge is refunded in full, whatever the date.',
  '4. Approval. Every refund must be approved by a person on the support team before it is issued. Refunds over $200 also need a supervisor.',
  '5. Replies to customers. No email goes to a customer until a person on the support team has read it.',
].join('\n');

// ---------- the server: what Kettlewick chose to offer ----------
function buildServer() {
  const server = new McpServer({ name: 'Kettlewick support server', version: '1.0.0' });
  const text = (t) => ({ content: [{ type: 'text', text: t }] });
  server.registerTool('look_up_order',
    { title: 'Look up an order', description: 'Returns the customer, item, price and dates for one order number.',
      inputSchema: { order_id: z.number().describe('The order number, for example 1182') }, annotations: { readOnlyHint: true } },
    async ({ order_id }) => {
      const o = ORDERS[order_id];
      return text(o ? 'Order ' + order_id + ': ' + o.item + ', $' + o.price_usd.toFixed(2) + ', bought by ' + o.customer + ' on ' + o.order_date +
        ', delivered ' + o.delivered_date + '. Final sale: ' + o.final_sale + '.' : 'No order with number ' + order_id + '.');
    });
  server.registerTool('list_charges',
    { title: 'List the charges on an order', description: 'Returns every card charge recorded against one order number.',
      inputSchema: { order_id: z.number().describe('The order number') }, annotations: { readOnlyHint: true } },
    async ({ order_id }) => {
      const rows = CHARGES.filter((c) => c.order_id === order_id);
      return text(rows.length ? rows.length + ' charge(s) on order ' + order_id + ':\n' +
        rows.map((c) => '  ' + c.charge_id + '  ' + c.charge_date + '  $' + c.amount_usd.toFixed(2)).join('\n') : 'No charges found for order ' + order_id + '.');
    });
  server.registerTool('get_refund_policy',
    { title: 'Read the refund policy', description: 'Returns the five rules of the Kettlewick refund policy.', annotations: { readOnlyHint: true } },
    async () => text('Kettlewick refund policy\n' + POLICY));
  server.registerTool('draft_reply',
    { title: 'Draft a reply to the customer', description: 'Saves a draft email for a person on the support team to read. It does not send anything.',
      inputSchema: { order_id: z.number(), text: z.string() }, annotations: { readOnlyHint: false } },
    async () => text('Draft saved. Not sent: a person on the support team must read it and send it.'));
  return server;
}

// ---------- the message log ----------
let logCount = 0;
function log(direction, message) {
  logCount += 1;
  $('logWrap').hidden = false;
  $('logCount').textContent = logCount;
  $('log').innerHTML += '<span class="dir">' + direction + '</span>\n' + esc(JSON.stringify(message, null, 1)) + '\n\n';
}

// ---------- the assistant's side of the connection ----------
const state = { client: null, got: {} };
async function connect() {
  const [clientSide, serverSide] = InMemoryTransport.createLinkedPair();
  const send = clientSide.send.bind(clientSide);
  clientSide.send = (m, o) => { log('assistant → server', m); return send(m, o); };
  await buildServer().connect(serverSide);
  const client = new Client({ name: 'Lab assistant', version: '1.0.0' });
  await client.connect(clientSide);
  const receive = clientSide.onmessage;
  clientSide.onmessage = (m, e) => { log('server → assistant', m); return receive(m, e); };
  state.client = client;
  return { info: client.getServerVersion(), tools: (await client.listTools()).tools };
}
async function use(name, args) {
  const res = await state.client.callTool({ name, arguments: args });
  const body = (res.content || []).map((c) => c.text).join('\n');
  return { refused: !!res.isError, body };
}

// ---------- wiring ----------
function fail(n, e) { $('o' + n).innerHTML += '<div class="err">That step did not work: ' + esc(e.message || e) + '. Reload the page and try again.</div>'; }
function unlock(n, ids) { $('s' + n).classList.remove('locked'); for (const id of ids) $(id).disabled = false; }

$('b2').onclick = async () => {
  $('b2').disabled = true;
  try {
    const { info, tools } = await connect();
    $('b2').textContent = 'Connected';
    $('o2').innerHTML = '<div class="fact">Connected to: ' + esc(info.name) + '. It offers ' + tools.length + ' things.</div>' +
      tools.map((t) => '<div class="tool"><b>' + esc(t.title || t.name) + '</b>' +
        (t.annotations && t.annotations.readOnlyHint ? '<span class="tag read">reads only</span>' : '<span class="tag write">writes a draft</span>') +
        '<div>' + esc(t.description) + '</div><div class="name">' + esc(t.name) + '</div></div>').join('') +
      '<div class="note">This list is the whole of what an assistant can do through this connection. In a real product it is the permission screen — the one most people click straight through.</div>';
    unlock(3, ['b3a', 'b3b', 'b3c']);
  } catch (e) { console.error(e); $('b2').disabled = false; fail(2, e); }
};

async function runTool(btn, key, label, name, args) {
  btn.disabled = true;
  try {
    const r = await use(name, args);
    state.got[key] = r.body;
    $('o3').innerHTML += '<div class="result"><div class="asked">Asked the server: ' + esc(label) + '</div>' + esc(r.body) + '</div>';
    if (state.got.order && state.got.charges && state.got.policy) { unlock(4, ['b4']); showHandOver(); }
  } catch (e) { console.error(e); btn.disabled = false; fail(3, e); }
}
$('b3a').onclick = () => runTool($('b3a'), 'order', 'look up order 1182', 'look_up_order', { order_id: 1182 });
$('b3b').onclick = () => runTool($('b3b'), 'charges', 'list the charges on order 1182', 'list_charges', { order_id: 1182 });
$('b3c').onclick = () => runTool($('b3c'), 'policy', 'read the refund policy', 'get_refund_policy', {});

$('b4').onclick = async () => {
  $('b4').disabled = true;
  let reason;
  try {
    const r = await use('issue_refund', { order_id: 1182, amount_usd: 89.0 });
    reason = r.body || 'no such tool';
  } catch (e) { reason = e.message || String(e); }
  $('o4').innerHTML = '<div class="result refused"><div class="asked">Asked the server: issue a refund of $89.00 on order 1182</div>The server refused.\nIts reply: ' + esc(reason) + '</div>' +
    '<div class="note warn">There is no refund tool on the list, so no assistant using this connection can issue a refund — however it is asked, and however it is tricked. Kettlewick decided that when it built the server.</div>';
};

function showHandOver() {
  const message = 'Answer the question using only the records below, which came from Kettlewick\'s support system. Say which records and which policy rule you used.\n\n' +
    'Order record:\n' + state.got.order + '\n\nCharges:\n' + state.got.charges + '\n\n' + state.got.policy + '\n\nQuestion: ' + QUESTION;
  $('o5').innerHTML = '<textarea id="msg" readonly></textarea><div style="margin-top:8px"><button id="copy">Copy this message</button></div>' +
    '<details><summary>No chatbot? See the expected answer</summary><div class="box">Yes. Order 1182 has two charges of $89.00 on the same day, October 14, for one blender. ' +
    'Rule 3 says the extra charge is refunded in full, whatever the date. Rule 4 says a person on the support team must approve the refund first. ' +
    'So: refund one charge of $89.00, once a person approves it.</div></details>' +
    '<div class="note">Nothing about the model changed between box A and box E. What changed is what it can reach.</div>';
  $('msg').value = message;
  $('copy').onclick = async () => {
    try { await navigator.clipboard.writeText($('msg').value); } catch { $('msg').select(); document.execCommand('copy'); }
    $('copy').textContent = 'Copied';
    setTimeout(() => { $('copy').textContent = 'Copy this message'; }, 1500);
  };
  $('s5').classList.remove('locked');
}
