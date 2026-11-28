// AI Demystified for Tech Leaders — the lab page (four labs, and three to try on your own).
// Answers are kept in this browser only (localStorage). Nothing is sent anywhere.
const KEY = 'tlsdemyst-answers-v1';
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

// ---------- rows that repeat ----------
const ACTIONS = ['Look up the order', 'List the charges on the order', 'Draft a reply', 'Send the reply', 'Refund $20', 'Refund $500', 'Change the customer’s email address'];
$('l4rows').innerHTML = ACTIONS.map((a, i) => `
  <div class="item"><div class="t">${i + 1}. ${a}</div>
    <div class="checks"><label><input type="checkbox" data-k="l4.list.${i}" data-label="${i + 1}. ${a}: on the server's list"><span>On the list</span></label></div>
    <div class="seg" data-label="${i + 1}. ${a}">
      <label><input type="radio" name="l4.act.${i}" value="Alone"><span>Alone</span></label>
      <label><input type="radio" name="l4.act.${i}" value="Person approves"><span>Person</span></label>
      <label><input type="radio" name="l4.act.${i}" value="Never"><span>Never</span></label>
    </div>
  </div>`).join('');

// Teach it your rules: the five tickets and Kettlewick's rule for each
const TICKETS = [['Cheaper at another shop (happy)', 'P1'], ['Dented $45 kettle (angry)', 'P4'], ['Change account email (polite)', 'P1'], ['Parcel 12 business days late', 'P2'], ['Charged $89 twice', 'P4']];
const prio = (name, label) => `<div class="seg" data-label="${label}">${[1, 2, 3, 4].map((n) => `<label><input type="radio" name="${name}" value="P${n}"><span>P${n}</span></label>`).join('')}</div>`;
$('l3rows').innerHTML = TICKETS.map(([t, rule], i) => `
  <div class="item"><div class="t">${i + 1}. ${t} · <span class="hint">Kettlewick’s rule: <b>${rule}</b></span></div>
    <div class="hint" style="margin-top:4px">What the AI said: Just ask <span id="l3m.plain.${i}"></span></div>${prio(`l3r.plain.${i}`, `Ticket ${i + 1}, just ask`)}
    <div class="hint">What the AI said: With examples <span id="l3m.ex.${i}"></span></div>${prio(`l3r.ex.${i}`, `Ticket ${i + 1}, with examples`)}
  </div>`).join('');

const QUESTIONS = [
  ['value', 'Value', 'Which number moves: time, cost, quality or revenue? Who has signed up to be measured on it?', false],
  ['feas', 'Feasibility', 'Is the data available and clean? Does a bought tool already do this? Can one team own all of it?', false],
  ['risk', 'Risk', 'What can it see? What can it do without approval? What is the worst it could do if it were tricked?', true],
  ['meas', 'Measurability', 'Is there a baseline today? Can we see a result inside 90 days, on one workflow? (A baseline is today’s number, measured before AI.)', true],
];
$('l9rows').innerHTML = QUESTIONS.map(([k, name, q, gate], i) => `
  <div class="item"><div class="t">${i + 1}. ${name}${gate ? ' <span style="color:var(--red)">(must pass)</span>' : ''}</div>
    <div>${q}</div>
    <div class="seg" data-label="${name}, score">
      <label><input type="radio" name="l9.${k}" value="1"${gate ? ' data-gate' : ''}><span>1</span></label>
      <label><input type="radio" name="l9.${k}" value="2"><span>2</span></label>
      <label><input type="radio" name="l9.${k}" value="3"><span>3</span></label>
    </div>
  </div>`).join('');

// ---------- save and restore ----------
let store = {};
try { store = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch { store = {}; }
let canSave = true;
function persist() {
  try { localStorage.setItem(KEY, JSON.stringify(store)); canSave = true; }
  catch { canSave = false; }
  $('status').textContent = canSave ? 'Saved on this device.' : 'This browser is not saving answers (private mode?). Copy or print them before you close the page.';
}
const fields = () => [...document.querySelectorAll('[data-k]')];
const radios = () => [...document.querySelectorAll('input[type=radio]')];
function grow(t) { if (t.tagName === 'TEXTAREA') { t.style.height = 'auto'; t.style.height = (t.scrollHeight + 2) + 'px'; } }

function restore() {
  for (const f of fields()) {
    const v = store[f.dataset.k];
    if (f.type === 'checkbox') f.checked = !!v; else f.value = v == null ? '' : v;
    grow(f);
  }
  for (const r of radios()) r.checked = store[r.name] === r.value;
  refresh();
}
function refresh() {
  // Estimate the tokens: the count button needs an estimate first
  for (const item of document.querySelectorAll('[data-line]')) {
    item.querySelector('.countbtn').disabled = item.querySelector('.guess').value === '';
  }
  // Lab 4, Score the proposal (fields named l9): a 1 on a question that must pass
  $('l9gate').hidden = !document.querySelector('input[data-gate]:checked');
  // Teach it your rules: marks and totals
  if (typeof l3score === 'function' && $('l3res')) l3score();
}
document.addEventListener('input', (e) => {
  const f = e.target;
  if (f.dataset && f.dataset.k) { store[f.dataset.k] = f.type === 'checkbox' ? f.checked : f.value; grow(f); persist(); }
  else if (f.type === 'radio') { store[f.name] = f.value; persist(); }
  refresh();
});

// ---------- Estimate the tokens: the counter ----------
let tokenizer = null;
async function loadTokenizer() {
  if (!tokenizer) tokenizer = import('./vendor/tokenizer.min.js');
  return tokenizer;
}
function showPieces(el, parts) {
  el.innerHTML = parts.map((p) => `<span>${esc(p.text).replace(/ /g, '·') || '&nbsp;'}</span>`).join('');
}
for (const item of document.querySelectorAll('[data-line]')) {
  const btn = item.querySelector('.countbtn');
  btn.addEventListener('click', async () => {
    const label = btn.textContent; btn.textContent = 'Counting…'; btn.disabled = true;
    try {
      const t = await loadTokenizer();
      const parts = t.pieces(item.querySelector('.sample').textContent);
      const c = item.querySelector('.count');
      c.value = parts.length; store[c.dataset.k] = String(parts.length); persist();
      showPieces(item.querySelector('.tok'), parts);
      $('tokErr').innerHTML = '';
    } catch (err) {
      tokenizer = null;
      $('tokErr').innerHTML = '<div class="note warn">The counter could not load. Use the tokenizer page linked below and type the count in yourself.</div>';
    }
    btn.textContent = label; refresh();
  });
}
let ownTimer = null;
$('ownText').addEventListener('input', () => {
  clearTimeout(ownTimer);
  ownTimer = setTimeout(async () => {
    const text = $('ownText').value;
    if (!text) { $('ownTok').innerHTML = ''; $('ownCount').textContent = ''; return; }
    try {
      const t = await loadTokenizer(); const parts = t.pieces(text);
      showPieces($('ownTok'), parts);
      $('ownCount').textContent = parts.length + (parts.length === 1 ? ' token' : ' tokens') + ' for ' + text.length + ' characters. A dot marks a space.';
    } catch { $('ownCount').textContent = 'The counter could not load.'; }
  }, 200);
});

// ---------- Teach it your rules, and Lab 3: copy the sample text ----------
async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return true; }
  catch {
    const ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select();
    let ok = false; try { ok = document.execCommand('copy'); } catch { ok = false; }
    ta.remove(); return ok;
  }
}
for (const b of document.querySelectorAll('[data-copy]')) {
  b.addEventListener('click', async () => {
    const ok = await copyText($(b.dataset.copy).textContent);
    $(b.dataset.msg || 'l5copied').textContent = ok ? 'Copied. Paste it into your chatbot.' : 'Could not copy. Press and hold the text to select it.';
  });
}

// ---------- Teach it your rules: read the AI's reply and show where it followed the rule ----------
// Finds the five priorities in a pasted reply. Handles tables (markdown, tab-separated,
// one cell per line) and "Ticket 1: P4" lines. Returns five values; null where not found.
function readPriorities(text) {
  const out = [null, null, null, null, null];
  for (const line of String(text).split(/\r?\n/)) {
    const m = line.match(/^[\s|*#>\-]*(?:ticket\s*(?:#|no\.?|number)?\s*)?\**\s*([1-5])\s*\**(?![\d$.,%]\d)(.*)$/i);
    if (!m) continue;
    const p = m[2].match(/\bP\s*([1-4])\b/i);
    if (p && !out[m[1] - 1]) out[m[1] - 1] = 'P' + p[1];
  }
  if (out.every(Boolean)) return out;
  const labelled = [...String(text).matchAll(/\bP\s*([1-4])\s*[-–—:(]?\s*(?:critical|high|medium|low)\b/gi)].map((x) => 'P' + x[1]);
  if (labelled.length === 5) return labelled;
  const bare = [...String(text).matchAll(/\bP([1-4])\b/g)].map((x) => 'P' + x[1]);
  if (bare.length === 5) return bare;
  return out;
}
for (const box of document.querySelectorAll('[data-l3paste]')) {
  box.addEventListener('input', () => {
    const kind = box.dataset.l3paste, msg = $('l3read_' + kind);
    grow(box);
    if (!box.value.trim()) { msg.innerHTML = ''; return; }
    const found = readPriorities(box.value);
    found.forEach((v, i) => { if (v) store[`l3r.${kind}.${i}`] = v; });
    for (const r of radios()) if (r.name.startsWith(`l3r.${kind}.`)) r.checked = store[r.name] === r.value;
    persist(); refresh();
    const n = found.filter(Boolean).length;
    msg.innerHTML = n === 5 ? '<span class="ok">Found all five.</span> They are in step 5.'
      : n ? `Found ${n} of 5. Tap the missing ones in step 5 (the P1–P4 buttons).`
      : 'Could not find the priorities in that. Tap the P1–P4 buttons in step 5 to enter what the AI said.';
  });
}
function l3score() {
  const line = (kind) => {
    let right = 0, done = 0;
    TICKETS.forEach(([, rule], i) => {
      const v = store[`l3r.${kind}.${i}`], mark = $(`l3m.${kind}.${i}`);
      if (v) { done++; if (v === rule) right++; }
      if (mark) mark.innerHTML = !v ? '' : v === rule ? '<span class="ok">✓ followed it</span>' : '<span class="no">✗ rule says ' + rule + '</span>';
    });
    return done ? `the AI followed the rule on <b>${right} of 5</b>` + (done < 5 ? ` <span class="hint">(${5 - done} not filled in)</span>` : '') : '<span class="hint">no reply yet</span>';
  };
  $('l3res').innerHTML = `Just ask: ${line('plain')} · With examples: ${line('ex')}`;
}

// ---------- keep your answers ----------
function answersAsText() {
  const out = ['AI Demystified for Tech Leaders — my lab answers', ''];
  for (const lab of document.querySelectorAll('section.lab')) {
    const lines = [];
    const seen = new Set();
    for (const el of lab.querySelectorAll('[data-k], .seg[data-label], .checks[data-label]')) {
      if (el.dataset.k) {
        if (el.type === 'checkbox') { if (el.checked) lines.push(el.dataset.label + ': yes'); }
        else if (el.value.trim()) lines.push(el.dataset.label + ': ' + el.value.trim().replace(/\n/g, '; '));
      } else {
        const r = el.querySelector('input[type=radio]:checked');
        if (r && !seen.has(r.name)) { seen.add(r.name); lines.push(el.dataset.label + ': ' + r.value); }
      }
    }
    if (lines.length) out.push(lab.dataset.lab, ...lines.map((l) => '  ' + l), '');
  }
  return out.length > 2 ? out.join('\n') : '';
}
let clearArmed = null;
document.addEventListener('click', async (e) => {
  const b = e.target.closest('[data-act]'); if (!b) return;
  const act = b.dataset.act;
  if (act === 'print') {
    document.querySelectorAll('textarea[data-k]').forEach(grow);
    window.print();
  } else if (act === 'copy') {
    const text = answersAsText();
    if (!text) { $('status').textContent = 'There are no answers to copy yet.'; $('status').scrollIntoView({ block: 'center' }); return; }
    const ok = await copyText(text);
    const box = $('copyBox'); box.value = text; box.style.display = 'block'; grow(box);
    $('status').textContent = ok ? 'Copied. Paste it into an email or note to yourself. The text is also shown below.' : 'Could not copy automatically. Select the text below and copy it.';
    box.scrollIntoView({ block: 'center' });
  } else if (act === 'clear') {
    if (clearArmed !== b) {
      clearArmed = b; b.textContent = 'Press again to erase every answer on this page';
      setTimeout(() => { if (clearArmed === b) { clearArmed = null; b.textContent = 'Clear my answers'; } }, 5000);
      return;
    }
    clearArmed = null; b.textContent = 'Clear my answers';
    store = {}; try { localStorage.removeItem(KEY); } catch { /* nothing to remove */ }
    restore();
    document.querySelectorAll('.tok, .res').forEach((el) => { el.innerHTML = ''; });
    document.querySelectorAll('[data-l3paste]').forEach((t) => { t.value = ''; grow(t); });
    l3score();
    $('copyBox').style.display = 'none';
    $('status').textContent = 'All answers cleared.';
  }
});

// If this page is open in two tabs, pick up answers typed in the other one,
// so an older copy cannot save over newer answers.
window.addEventListener('storage', (e) => {
  if (e.key !== KEY) return;
  try { store = JSON.parse(e.newValue || '{}') || {}; } catch { store = {}; }
  restore();
});

restore();
