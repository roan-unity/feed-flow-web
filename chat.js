/* Feed Flow! site chat: Nora, the AI assistant. Vanilla, no dependencies, no cookies.
   The conversation lives in memory and sessionStorage only (gone when the tab closes).
   ?chatdemo=<state> renders a pinned state with no network at all (see the bottom of this file). */
(function () {
  'use strict';
  if (window.__ffChat) return;
  window.__ffChat = true;

  /* live: the chat answers. hours: null means always open; an object { tz, open, close } limits it to those hours,
     and the contact form takes over outside them. If the first message cannot be answered (not set up, a server
     error, a rate limit, no network) the widget also falls back to the contact form, which emails support. */
  var CHAT = { live: true, hours: null };

  var API = '/api/chat';
  var API_ESCALATE = '/api/chat/escalate';
  var STORE_KEY = 'ffc-v1';
  var OPENED_KEY = 'ffc-opened';
  var PILL_KEY = 'ffc-pill';
  var MAX_CHARS = 1000;
  var SUPPORT_EMAIL = 'support@tryfeedflow.app';
  var MIN_FILL_MS = 2600; /* the server silently drops anything faster than 2.5 s after the panel opened */
  var COUNT_FROM = 900;
  var STREAM_TIMEOUT_MS = 60000;
  var SVG_NS = 'http://www.w3.org/2000/svg';
  var NORA_LANE = { assistant: 1, card: 1, error: 1 };

  var COPY = {
    launcher: "Chat with Nora, Feed Flow's AI assistant",
    close: 'Close chat',
    pill: 'Questions? Ask Nora.',
    dismiss: 'Dismiss',
    role: 'Feed Flow assistant ',
    greeting: "Hi, I'm Nora, Feed Flow's AI assistant. Ask me anything about the app.",
    chips: ['What does Feed Flow track?', 'Is it free?', 'Can two parents log together?', 'Talk to a person'],
    person: 'Sure. Leave your email and a person on the team will write back.',
    placeholder: 'Write a message',
    send: 'Send message',
    foot: "Nora is an AI and can be wrong. No health advice. ",
    privacy: 'Privacy',
    failed: "That didn't go through.",
    retry: 'Retry',
    limited: 'Too many messages for now. Try again in a minute.',
    tooLong: 'That message is too long. Shorten it and send it again.',
    botCheck: "We couldn't check that you're a person. Reload the page and try again.",
    cardTitleSupport: 'Send to support',
    cardTitleFounder: 'Send to Robin, the founder',
    cardLineSupport: 'A person at Feed Flow will reply by email.',
    cardLineFounder: 'Robin will reply by email.',
    emailLabel: 'Your email',
    topicLabel: 'What is it about?',
    cardSend: 'Send',
    cardSending: 'Sending…',
    notNow: 'Not now',
    badEmail: "That email doesn't look right.",
    needTopic: 'Add a line about what you need.',
    sentTo: 'Sent. We’ll reply to ',
    /* closed mode: a contact form instead of the chat */
    closedLauncher: 'Leave a message for the Feed Flow team',
    closedPill: 'Questions? Leave us a message.',
    closedOff: "The chat isn't open right now. Leave a message here and a person at Feed Flow will reply by email.",
    closedHoursA: 'The chat is closed for now and opens again at ',
    closedHoursB: '. Leave a message here and a person at Feed Flow will reply by email.',
    closedFoot: 'Your message goes to the Feed Flow team by email. ',
    leaveTitle: 'Leave a message',
    messageLabel: 'Your message',
    needEmail: 'Add your email so we can reply.',
    needMessage: 'Write a short message first.',
    sentAnother: 'Send another message',
    mailLine: "Your email app should open with the message ready to send. If it doesn't, write to " + SUPPORT_EMAIL + '.',
    tryAgain: 'Try again',
    mailSubject: 'Question from the website'
  };

  var DEMO = false;
  var items = [];
  var busy = false;
  var open = false;
  var chipsEl = null;
  var pillTimer = null;
  var activeRequest = null;
  var closedMode = false;
  var launcherLabel = COPY.launcher;
  var openedAt = 0;
  var L = null; /* the contact form's state while in closed mode */
  var leaveCard = null;
  var mobileQuery = window.matchMedia ? window.matchMedia('(max-width: 519px)') : { matches: false };

  /* ---------- small helpers ---------- */
  function h(tag, cls, text) {
    var el = document.createElement(tag);
    if (cls) el.className = cls;
    if (text != null) el.textContent = text;
    return el;
  }
  function icon(paths) {
    var svg = document.createElementNS(SVG_NS, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('class', 'ffc-ic');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    paths.forEach(function (d) {
      var p = document.createElementNS(SVG_NS, 'path');
      p.setAttribute('d', d);
      svg.appendChild(p);
    });
    return svg;
  }
  var ICON_X = ['M6 6l12 12M18 6L6 18'];
  var ICON_SEND = ['M12 19V6M6 12l6-6 6 6'];
  var ICON_CHECK = ['M5 12.5l4.5 4.5L19 7.5'];
  function store(key, value) { if (DEMO) return; try { sessionStorage.setItem(key, value); } catch (e) {} }
  function load(key) { if (DEMO) return null; try { return sessionStorage.getItem(key); } catch (e) { return null; } }
  function avatar(cls, src) {
    var img = h('img', cls);
    img.src = src || '/assets/nora.svg';
    img.alt = '';
    img.width = 96;
    img.height = 96;
    return img;
  }
  function pagePath() { return location.pathname; }
  function track(name) { try { if (window.plausible) window.plausible(name); } catch (e) {} }

  /* Plain text into a node, with **bold**, https links and email addresses. Nothing is ever parsed as HTML. */
  function fill(el, text) {
    el.textContent = '';
    text = String(text).replace(/^[-*] (?!\*)/gm, '• ');
    var re = /(\*\*[^*\n]+\*\*)|(https?:\/\/[^\s<>]+)|([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})/g;
    var last = 0;
    var m;
    while ((m = re.exec(text))) {
      if (m.index > last) el.appendChild(document.createTextNode(text.slice(last, m.index)));
      var tok = m[0];
      var trail = '';
      if (m[1]) {
        el.appendChild(h('strong', '', tok.slice(2, -2)));
      } else {
        var t = tok.match(/[.,;:!?)\]]+$/);
        if (t) { trail = t[0]; tok = tok.slice(0, tok.length - trail.length); }
        var a = h('a', '', tok);
        a.href = m[2] ? tok : 'mailto:' + tok;
        if (m[2]) { a.target = '_blank'; a.rel = 'noopener noreferrer'; }
        el.appendChild(a);
        if (trail) el.appendChild(document.createTextNode(trail));
      }
      last = m.index + m[0].length;
    }
    if (last < text.length) el.appendChild(document.createTextNode(text.slice(last)));
  }

  /* ---------- opening hours (pure; scripts/chat-escalate.test.mjs evaluates this block) ---------- */
  /* time:start */
  function zoneParts(ms, tz) {
    var parts = new Intl.DateTimeFormat('en-US', {
      timeZone: tz, hour12: false, year: 'numeric', month: 'numeric', day: 'numeric',
      hour: 'numeric', minute: 'numeric', second: 'numeric'
    }).formatToParts(new Date(ms));
    var o = {};
    parts.forEach(function (p) { if (p.type !== 'literal') o[p.type] = parseInt(p.value, 10); });
    o.hour = o.hour % 24; /* some engines print midnight as 24 */
    return o;
  }
  function zoneOffsetMs(ms, tz) {
    var p = zoneParts(ms, tz);
    return Date.UTC(p.year, p.month - 1, p.day, p.hour, p.minute, p.second) - Math.floor(ms / 1000) * 1000;
  }
  /* The instant at which the wall clock in tz reads y-m-d h:00. Checked twice so a DST change on that day is honoured. */
  function zonedInstant(y, m, d, hour, tz) {
    var guess = Date.UTC(y, m - 1, d, hour, 0, 0);
    var off1 = zoneOffsetMs(guess, tz);
    var t = guess - off1;
    var off2 = zoneOffsetMs(t, tz);
    return off2 === off1 ? t : guess - off2;
  }
  function isOpenNow(nowMs, cfg) {
    if (!cfg.live) return false;
    if (!cfg.hours) return true;
    var hour = zoneParts(nowMs, cfg.hours.tz).hour;
    return hour >= cfg.hours.open && hour < cfg.hours.close;
  }
  function nextOpening(nowMs, cfg) {
    var p = zoneParts(nowMs, cfg.hours.tz);
    return zonedInstant(p.year, p.month, p.day + (p.hour < cfg.hours.open ? 0 : 1), cfg.hours.open, cfg.hours.tz);
  }
  /* "9:00 AM Eastern", plus "(15:00 your time)" when the visitor's clock differs at that moment. */
  function openingText(nowMs, cfg, opts) {
    opts = opts || {};
    var tz = cfg.hours.tz;
    var at = nextOpening(nowMs, cfg);
    var clean = function (str) { return String(str).replace(/[\s ]+/g, ' '); };
    var there = clean(new Intl.DateTimeFormat('en-US', { timeZone: tz, hour: 'numeric', minute: '2-digit' }).format(new Date(at)));
    var zone = '';
    try {
      new Intl.DateTimeFormat('en-US', { timeZone: tz, timeZoneName: 'long' }).formatToParts(new Date(at)).forEach(function (p) {
        if (p.type === 'timeZoneName') zone = p.value.replace(/\s+(Standard |Daylight |Summer )?Time$/, '');
      });
    } catch (e) {}
    if (!zone) zone = tz.split('/').pop().replace(/_/g, ' ');
    var text = there + ' ' + zone;
    var mine = opts.visitorTz || new Intl.DateTimeFormat().resolvedOptions().timeZone;
    if (mine && zoneOffsetMs(at, mine) !== zoneOffsetMs(at, tz)) {
      var local = clean(new Intl.DateTimeFormat(opts.locale, { timeZone: mine, hour: 'numeric', minute: '2-digit' }).format(new Date(at)));
      text += ' (' + local + ' your time)';
    }
    return text;
  }
  /* time:end */

  /* ---------- DOM ---------- */
  var root = h('div', 'ffc-root');
  var dock = h('div', 'ffc-dock');
  var pill = h('div', 'ffc-pill');
  var pillText = h('button', 'ffc-pill-text', COPY.pill);
  pillText.type = 'button';
  var pillX = h('button', 'ffc-pill-x');
  pillX.type = 'button';
  pillX.setAttribute('aria-label', COPY.dismiss);
  pillX.appendChild(icon(ICON_X));
  pill.appendChild(pillText);
  pill.appendChild(pillX);

  var launcher = h('button', 'ffc-launcher');
  launcher.type = 'button';
  launcher.id = 'ffc-launcher';
  launcher.setAttribute('aria-expanded', 'false');
  launcher.setAttribute('aria-controls', 'ffc-panel');
  launcher.setAttribute('aria-label', COPY.launcher);
  var launcherAv = avatar('ffc-l-av', '/assets/nora-face.svg');
  var launcherX = h('span', 'ffc-l-x');
  launcherX.appendChild(icon(ICON_X));
  launcher.appendChild(launcherAv);
  launcher.appendChild(launcherX);
  dock.appendChild(pill);
  dock.appendChild(launcher);

  var panel = h('div', 'ffc-panel');
  panel.id = 'ffc-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', COPY.launcher);
  var head = h('div', 'ffc-head');
  var headAv = h('div', 'ffc-head-av');
  headAv.appendChild(avatar(''));
  var headTxt = h('div', 'ffc-head-txt');
  headTxt.appendChild(h('div', 'ffc-name', 'Nora'));
  var role = h('div', 'ffc-role', COPY.role);
  role.appendChild(h('b', '', 'AI'));
  headTxt.appendChild(role);
  var closeBtn = h('button', 'ffc-close');
  closeBtn.type = 'button';
  closeBtn.setAttribute('aria-label', COPY.close);
  closeBtn.appendChild(icon(ICON_X));
  head.appendChild(headAv);
  head.appendChild(headTxt);
  head.appendChild(closeBtn);

  var log = h('div', 'ffc-log');
  log.setAttribute('role', 'log');
  log.setAttribute('aria-live', 'polite');
  log.setAttribute('aria-relevant', 'additions');

  var composer = h('form', 'ffc-composer');
  composer.setAttribute('novalidate', '');
  var field = h('div', 'ffc-field');
  var ta = h('textarea', 'ffc-ta');
  ta.rows = 1;
  ta.maxLength = MAX_CHARS;
  ta.placeholder = COPY.placeholder;
  ta.setAttribute('aria-label', COPY.placeholder);
  ta.setAttribute('enterkeyhint', 'send');
  field.appendChild(ta);
  var count = h('div', 'ffc-count');
  count.hidden = true;
  count.setAttribute('aria-live', 'polite');
  var sendBtn = h('button', 'ffc-send');
  sendBtn.type = 'submit';
  sendBtn.disabled = true;
  sendBtn.setAttribute('aria-label', COPY.send);
  sendBtn.appendChild(icon(ICON_SEND));
  composer.appendChild(count);
  composer.appendChild(field);
  composer.appendChild(sendBtn);

  var foot = h('div', 'ffc-foot', COPY.foot);
  var privacy = h('a', '', COPY.privacy);
  privacy.href = '/privacy.html';
  foot.appendChild(privacy);

  panel.appendChild(head);
  panel.appendChild(log);
  panel.appendChild(composer);
  panel.appendChild(foot);
  root.appendChild(dock);
  root.appendChild(panel);

  /* ---------- conversation model ---------- */
  function lastOf(list) { return list.length ? list[list.length - 1] : null; }

  function persist() {
    if (DEMO) return;
    var out = [];
    items.forEach(function (it) {
      if (it.typing) return;
      var c = {};
      for (var k in it) if (k !== 'el' && k !== 'bubble' && k !== 'typing') c[k] = it[k];
      out.push(c);
    });
    store(STORE_KEY, JSON.stringify(out.slice(-60)));
  }
  function restore() {
    var raw = load(STORE_KEY);
    if (!raw) return;
    try {
      var list = JSON.parse(raw);
      if (Object.prototype.toString.call(list) !== '[object Array]') return;
      list.forEach(function (it) {
        if (!it || typeof it.t !== 'string') return;
        if (it.t === 'card' && it.status === 'sending') it.status = 'form';
        items.push(it);
      });
    } catch (e) { items = []; }
  }
  /* Nora's reply shows as several bubbles; the API sees them as one assistant message. */
  function apiMessages() {
    var out = [];
    items.forEach(function (it) {
      if (it.t !== 'msg' || !it.text) return;
      var tail = out.length ? out[out.length - 1] : null;
      if (tail && tail.role === 'assistant' && it.role === 'assistant') tail.content += '\n\n' + it.text;
      else out.push({ role: it.role, content: it.text });
    });
    return out;
  }
  function side(it) { return it.role === 'user' ? 'user' : 'nora'; }
  function itemSide(it) { return it.t === 'msg' ? side(it) : 'nora'; }

  /* ---------- rendering ---------- */
  function nearBottom() { return log.scrollHeight - log.scrollTop - log.clientHeight < 90; }
  function toBottom() { log.scrollTop = log.scrollHeight; }

  function rowFor(it, index) {
    var s = itemSide(it);
    var prev = index > 0 ? items[index - 1] : null;
    var first = !prev || itemSide(prev) !== s;
    var row = h('div', 'ffc-row ffc-' + (s === 'user' ? 'user' : 'nora') + (first ? ' ffc-first' : ''));
    if (s === 'nora') row.appendChild(first ? avatar('ffc-av') : h('span', 'ffc-av-sp'));
    return row;
  }

  function buildMsg(it, index) {
    var row = rowFor(it, index);
    var bubble = h('div', 'ffc-bubble');
    if (it.typing) {
      setTyping(bubble);
    } else if (it.role === 'user') {
      bubble.textContent = it.text;
    } else {
      fill(bubble, it.text);
    }
    row.appendChild(bubble);
    it.el = row;
    it.bubble = bubble;
    return row;
  }
  function setTyping(bubble) {
    bubble.textContent = '';
    var dots = h('div', 'ffc-typing');
    dots.appendChild(h('i'));
    dots.appendChild(h('i'));
    dots.appendChild(h('i'));
    bubble.appendChild(dots);
    bubble.appendChild(h('span', 'ffc-sr', 'Nora is typing'));
  }

  function buildError(it, index) {
    var row = rowFor(it, index);
    var box = h('div', 'ffc-notice');
    var text = it.code === 'rate_limited' ? COPY.limited
      : it.code === 'too_long' ? COPY.tooLong
      : it.code === 'bot_check' ? COPY.botCheck
      : COPY.failed;
    box.appendChild(h('div', '', text));
    if (it.code !== 'rate_limited' && it.code !== 'too_long') {
      var retry = h('button', 'ffc-btn-link', COPY.retry);
      retry.type = 'button';
      retry.addEventListener('click', function () { retryLast(); });
      box.appendChild(retry);
    }
    row.appendChild(box);
    it.el = row;
    return row;
  }

  function buildCard(it, index) {
    var row = rowFor(it, index);
    var card = h('div', 'ffc-card');
    row.appendChild(card);
    it.el = row;
    paintCard(it, card);
    return row;
  }
  function paintCard(it, card) {
    card.textContent = '';
    if (it.status === 'sent') {
      var done = h('div', 'ffc-sent');
      done.appendChild(icon(ICON_CHECK));
      done.appendChild(h('div', '', COPY.sentTo + it.email + '.'));
      card.appendChild(done);
      return;
    }
    var founder = it.to === 'founder';
    card.appendChild(h('div', 'ffc-card-t', founder ? COPY.cardTitleFounder : COPY.cardTitleSupport));
    card.appendChild(h('div', 'ffc-card-p', founder ? COPY.cardLineFounder : COPY.cardLineSupport));
    var topic = null;
    if (it.needsTopic) {
      topic = h('textarea', 'ffc-input');
      topic.placeholder = COPY.topicLabel;
      topic.setAttribute('aria-label', COPY.topicLabel);
      topic.maxLength = MAX_CHARS;
      topic.value = it.topic || '';
      card.appendChild(topic);
    }
    var email = h('input', 'ffc-input');
    email.type = 'email';
    email.name = 'email';
    email.autocomplete = 'email';
    email.setAttribute('inputmode', 'email');
    email.placeholder = COPY.emailLabel;
    email.setAttribute('aria-label', COPY.emailLabel);
    email.value = it.email || '';
    card.appendChild(email);
    var err = h('div', 'ffc-err');
    err.setAttribute('role', 'alert');
    err.hidden = true;
    card.appendChild(err);
    var actions = h('div', 'ffc-actions');
    var go = h('button', 'ffc-btn', it.status === 'error' ? COPY.retry : COPY.cardSend);
    go.type = 'button';
    var no = h('button', 'ffc-btn-link', COPY.notNow);
    no.type = 'button';
    actions.appendChild(go);
    actions.appendChild(no);
    card.appendChild(actions);
    if (it.status === 'sending') { go.disabled = true; go.textContent = COPY.cardSending; }
    if (it.status === 'error') { err.hidden = false; err.textContent = COPY.failed; }

    no.addEventListener('click', function () { removeItem(it); persist(); });
    go.addEventListener('click', function () {
      var addr = email.value.replace(/^\s+|\s+$/g, '');
      it.email = addr;
      if (topic) it.topic = topic.value;
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(addr)) {
        err.hidden = false; err.textContent = COPY.badEmail; email.focus(); return;
      }
      if (topic && !topic.value.replace(/\s/g, '')) {
        err.hidden = false; err.textContent = COPY.needTopic; topic.focus(); return;
      }
      err.hidden = true;
      sendEscalation(it, card, go, err);
    });
  }

  function addItem(it, silent) {
    items.push(it);
    var index = items.length - 1;
    var node = it.t === 'msg' ? buildMsg(it, index) : it.t === 'error' ? buildError(it, index) : buildCard(it, index);
    log.appendChild(node);
    if (chipsEl && !silent) dropChips();
    if (!silent) toBottom();
    return it;
  }
  function removeItem(it) {
    var i = items.indexOf(it);
    if (i !== -1) items.splice(i, 1);
    if (it.el && it.el.parentNode) it.el.parentNode.removeChild(it.el);
  }
  function dropChips() {
    if (chipsEl && chipsEl.parentNode) chipsEl.parentNode.removeChild(chipsEl);
    chipsEl = null;
  }
  function renderAll() {
    log.textContent = '';
    var greet = h('div', 'ffc-row ffc-first ffc-nora');
    greet.appendChild(avatar('ffc-av'));
    greet.appendChild(h('div', 'ffc-bubble', COPY.greeting));
    log.appendChild(greet);
    chipsEl = null;
    if (!items.length) {
      chipsEl = h('div', 'ffc-chips');
      COPY.chips.forEach(function (label, i) {
        var b = h('button', 'ffc-chip', label);
        b.type = 'button';
        b.addEventListener('click', function () { onChip(i, label); });
        chipsEl.appendChild(b);
      });
      log.appendChild(chipsEl);
    }
    var list = items;
    items = [];
    list.forEach(function (it) { addItem(it, true); });
    toBottom();
  }

  /* ---------- sending ---------- */
  function setBusy(on) {
    busy = on;
    log.setAttribute('aria-busy', on ? 'true' : 'false');
    syncSend();
  }
  function syncSend() {
    sendBtn.disabled = busy || !ta.value.replace(/\s/g, '');
  }
  function submitText(text) {
    text = text.replace(/^\s+|\s+$/g, '').slice(0, MAX_CHARS);
    if (!text || busy) return;
    clearErrors();
    addItem({ t: 'msg', role: 'user', text: text });
    persist();
    run();
  }
  function clearErrors() {
    items.slice().forEach(function (it) { if (it.t === 'error') removeItem(it); });
  }
  function onChip(i, label) {
    if (busy) return;
    if (i === COPY.chips.length - 1) {
      addItem({ t: 'msg', role: 'user', text: label });
      addItem({ t: 'msg', role: 'assistant', text: COPY.person });
      addItem({ t: 'card', status: 'form', needsTopic: true, to: 'support', reason: 'request', summary: '' });
      persist();
      return;
    }
    submitText(label);
  }
  function retryLast() {
    if (busy) return;
    clearErrors();
    var tail = lastOf(items);
    while (tail && tail.t === 'msg' && tail.role === 'assistant') { removeItem(tail); tail = lastOf(items); }
    persist();
    run();
  }

  function run() {
    if (DEMO) { demoRun(); return; }
    setBusy(true);
    var firstMessage = !items.some(function (it) { return it.t === 'msg' && it.role === 'assistant'; });
    var reply = addItem({ t: 'msg', role: 'assistant', text: '', typing: true });
    var gotText = false;
    var pendingAction = null;
    var finished = false;
    var aborter = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { if (aborter) aborter.abort(); }, STREAM_TIMEOUT_MS);
    var token = {};
    activeRequest = token;

    function stuck() { return nearBottom(); }
    /* Each paragraph of the reply (a blank line between) is its own bubble. The stream decides when they arrive. */
    var current = reply;
    var carry = '';
    var breakNext = false;
    function put(text) {
      if (!text) return;
      if (breakNext) {
        if (!text.replace(/\s/g, '')) return;
        breakNext = false;
        current = addItem({ t: 'msg', role: 'assistant', text: '' }, true);
        text = text.replace(/^\s+/, '');
        if (stuck()) toBottom();
      }
      current.text += text;
      if (current.typing) current.typing = false;
      fill(current.bubble, current.text);
      gotText = true;
    }
    function onDelta(text) {
      if (!text) return;
      var stick = stuck();
      var s = carry + text;
      carry = '';
      var tailBreak = /[ \t]*\n\s*$/.exec(s);
      if (tailBreak) { carry = tailBreak[0]; s = s.slice(0, tailBreak.index); }
      var parts = s.split(/\n[ \t]*\n\s*/);
      parts.forEach(function (part, i) {
        if (i > 0) breakNext = true;
        put(part);
      });
      if (stick) toBottom();
    }
    function fallBackToForm() {
      var typed = '';
      items.forEach(function (it) { if (it.t === 'msg' && it.role === 'user') typed = it.text; });
      items = [];
      persist();
      activeRequest = null;
      setBusy(false);
      enterClosed(newLeave({ hours: false, message: typed }));
    }
    function finish(errCode, status) {
      if (finished) return;
      finished = true;
      clearTimeout(timer);
      if (activeRequest === token) activeRequest = null;
      /* First message and nothing came back (not set up, a server error, a rate limit, no network): show the form instead. */
      if (errCode && !gotText && firstMessage && (errCode === 'upstream' || errCode === 'rate_limited' || errCode === 'not_configured')) {
        removeItem(reply);
        fallBackToForm();
        return;
      }
      if (!gotText) removeItem(reply); else { reply.typing = false; current.typing = false; }
      if (errCode) {
        addItem({ t: 'error', code: errCode });
      } else if (pendingAction && !items.some(function (it) { return it.t === 'card' && it.status !== 'sent'; })) {
        addItem({ t: 'card', status: 'form', needsTopic: true, to: pendingAction.to === 'founder' ? 'founder' : 'support', reason: pendingAction.reason || 'request', summary: pendingAction.summary || '', topic: pendingAction.summary || '' });
      }
      setBusy(false);
      persist();
      toBottom();
    }
    function onEvent(name, data) {
      if (name === 'delta') onDelta(data && data.text);
      else if (name === 'action') { if (data && (data.type === 'hand_over' || data.type === 'escalate_form')) pendingAction = data; }
      else if (name === 'done') finish(null);
      else if (name === 'error') finish((data && data.code) || 'upstream');
    }

    getToken().then(function (tok) {
      return fetch(API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'text/event-stream' },
        body: JSON.stringify({ messages: apiMessages().slice(-20), page: pagePath(), turnstileToken: tok }),
        signal: aborter ? aborter.signal : undefined
      });
    }).then(function (res) {
      if (!res.ok) {
        return res.json().then(function (j) { return j && j.code; }, function () { return null; }).then(function (code) {
          /* 503, any 5xx and 429 on a first message mean the form takes over (see finish) */
          var c = res.status >= 500 ? 'upstream' : (code || codeForStatus(res.status));
          finish(c === 'not_configured' ? 'upstream' : c);
        });
      }
      return readStream(res, onEvent).then(function () {
        finish(gotText ? null : 'upstream');
      });
    }).catch(function () {
      finish('upstream');
    });
  }
  function codeForStatus(s) {
    return s === 429 ? 'rate_limited' : s === 413 ? 'too_long' : s === 403 ? 'bot_check' : s === 400 ? 'bad_request' : 'upstream';
  }
  function getToken() {
    var provider = window.FF_CHAT_TURNSTILE;
    if (typeof provider !== 'function') return Promise.resolve(null);
    try {
      return Promise.resolve(provider()).then(function (t) { return t || null; }, function () { return null; });
    } catch (e) { return Promise.resolve(null); }
  }

  /* Server-sent events, parsed by hand from the fetch body. */
  function readStream(res, onEvent) {
    var buffer = '';
    function consume(chunk, flush) {
      buffer += chunk;
      var parts = buffer.split(/\r?\n\r?\n/);
      buffer = flush ? '' : parts.pop();
      if (flush && parts.length && !parts[parts.length - 1]) parts.pop();
      parts.forEach(function (block) {
        var name = 'message';
        var data = [];
        block.split(/\r?\n/).forEach(function (line) {
          if (line.indexOf('event:') === 0) name = line.slice(6).replace(/^\s+/, '');
          else if (line.indexOf('data:') === 0) data.push(line.slice(5).replace(/^ /, ''));
        });
        if (!data.length) return;
        var parsed = null;
        try { parsed = JSON.parse(data.join('\n')); } catch (e) { return; }
        onEvent(name, parsed);
      });
    }
    if (!res.body || !res.body.getReader || !window.TextDecoder) {
      return res.text().then(function (t) { consume(t, true); });
    }
    var reader = res.body.getReader();
    var decoder = new TextDecoder('utf-8');
    function pump() {
      return reader.read().then(function (r) {
        if (r.done) { consume(decoder.decode(), true); return; }
        consume(decoder.decode(r.value, { stream: true }), false);
        return pump();
      });
    }
    return pump();
  }

  function sendEscalation(it, card, go, err) {
    if (DEMO) { it.status = 'sent'; paintCard(it, card); return; }
    it.status = 'sending';
    go.disabled = true;
    go.textContent = COPY.cardSending;
    var msgs = apiMessages().slice(-8).map(function (m) { return { role: m.role, content: m.content.slice(0, MAX_CHARS) }; });
    var question = it.needsTopic ? (it.topic || '') : (it.summary || '');
    if (!question) {
      for (var i = msgs.length - 1; i >= 0; i -= 1) { if (msgs[i].role === 'user') { question = msgs[i].content; break; } }
    }
    getToken().then(function (tok) {
      return fetch(API_ESCALATE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: it.email, question: question, transcript: msgs, page: pagePath(), to: it.to === 'founder' ? 'founder' : 'support', reason: it.reason || 'request', summary: it.summary || '', turnstileToken: tok })
      });
    }).then(function (res) {
      return res.json().then(function (j) { return { ok: res.ok && j && j.ok === true }; }, function () { return { ok: false }; });
    }).then(function (r) {
      it.status = r.ok ? 'sent' : 'error';
      paintCard(it, card);
      persist();
      if (r.ok) { card.setAttribute('tabindex', '-1'); card.focus({ preventScroll: true }); }
      else { var again = card.querySelector('.ffc-btn'); if (again) again.focus(); }
    }, function () {
      it.status = 'error';
      paintCard(it, card);
    });
  }

  /* ---------- closed mode: leave a message ---------- */
  var EMAIL_OK = /^[^\s@<>"',;:\\()[\]]+@[^\s@<>"',;:\\()[\]]+\.[^\s@<>"',;:\\()[\]]+$/;

  function newLeave(over) {
    var base = { status: 'form', email: '', message: '', company: '', errEmail: '', errMessage: '', errServer: '', hours: false, when: '' };
    for (var k in over) base[k] = over[k];
    return base;
  }
  function closedIntro() {
    return L.hours ? COPY.closedHoursA + L.when + COPY.closedHoursB : COPY.closedOff;
  }
  function enterClosed(state) {
    closedMode = true;
    L = state;
    root.classList.add('ffc-closed');
    launcherLabel = COPY.closedLauncher;
    launcher.setAttribute('aria-label', launcherLabel);
    pillText.textContent = COPY.closedPill;
    foot.textContent = COPY.closedFoot;
    var link = h('a', '', COPY.privacy);
    link.href = '/privacy';
    foot.appendChild(link);
    renderClosed();
  }
  function renderClosed() {
    log.textContent = '';
    chipsEl = null;
    var first = h('div', 'ffc-row ffc-first ffc-nora');
    first.appendChild(avatar('ffc-av'));
    first.appendChild(h('div', 'ffc-bubble', closedIntro()));
    log.appendChild(first);
    var second = h('div', 'ffc-row ffc-nora');
    second.appendChild(h('span', 'ffc-av-sp'));
    leaveCard = h('div', 'ffc-card');
    second.appendChild(leaveCard);
    log.appendChild(second);
    paintLeave();
  }
  function growMessage(box) {
    box.style.height = 'auto';
    box.style.height = Math.min(box.scrollHeight + 2, 160) + 'px';
  }
  function keepInView(el) {
    el.addEventListener('focus', function () {
      if (!mobileQuery.matches) return;
      setTimeout(function () { try { el.scrollIntoView({ block: 'center' }); } catch (e) {} }, 320);
    });
  }
  function lockForm(card) {
    var fields = card.querySelectorAll('input, textarea');
    for (var i = 0; i < fields.length; i += 1) fields[i].readOnly = true;
    var go = card.querySelector('.ffc-btn');
    if (go) { go.disabled = true; go.textContent = COPY.cardSending; }
  }
  function settleCard(card) {
    card.setAttribute('tabindex', '-1');
    card.focus({ preventScroll: true });
  }

  function paintLeave() {
    var card = leaveCard;
    card.textContent = '';
    if (L.status === 'sent') {
      var done = h('div', 'ffc-sent');
      done.appendChild(icon(ICON_CHECK));
      done.appendChild(h('div', '', COPY.sentTo + L.email + '.'));
      card.appendChild(done);
      var again = h('button', 'ffc-btn-link', COPY.sentAnother);
      again.type = 'button';
      again.addEventListener('click', function () {
        L.status = 'form'; L.message = ''; L.company = ''; L.errEmail = L.errMessage = L.errServer = '';
        paintLeave();
        var box = card.querySelector('textarea');
        if (box) box.focus({ preventScroll: true });
      });
      card.appendChild(again);
      return;
    }
    if (L.status === 'mailto') {
      var line = h('div', 'ffc-card-p ffc-mail');
      fill(line, COPY.mailLine);
      card.appendChild(line);
      var retry = h('button', 'ffc-btn-link', COPY.tryAgain);
      retry.type = 'button';
      retry.addEventListener('click', function () { openMailApp(); });
      card.appendChild(retry);
      return;
    }

    card.appendChild(h('div', 'ffc-card-t', COPY.leaveTitle));
    var form = h('form', 'ffc-leave');
    form.setAttribute('novalidate', '');

    var email = h('input', 'ffc-input');
    email.type = 'email';
    email.name = 'email';
    email.autocomplete = 'email';
    email.setAttribute('inputmode', 'email');
    email.placeholder = COPY.emailLabel;
    email.setAttribute('aria-label', COPY.emailLabel);
    email.setAttribute('aria-describedby', 'ffc-lv-email-err');
    email.value = L.email;
    var emailErr = h('div', 'ffc-err', L.errEmail);
    emailErr.id = 'ffc-lv-email-err';
    emailErr.hidden = !L.errEmail;
    if (L.errEmail) email.setAttribute('aria-invalid', 'true');
    form.appendChild(email);
    form.appendChild(emailErr);

    var box = h('textarea', 'ffc-input ffc-msg');
    box.rows = 3;
    box.name = 'message';
    box.maxLength = MAX_CHARS;
    box.placeholder = COPY.messageLabel;
    box.setAttribute('aria-label', COPY.messageLabel);
    box.setAttribute('aria-describedby', 'ffc-lv-msg-err ffc-lv-msg-count');
    box.value = L.message;
    var msgCount = h('div', 'ffc-msg-count');
    msgCount.id = 'ffc-lv-msg-count';
    msgCount.setAttribute('aria-live', 'polite');
    var msgErr = h('div', 'ffc-err', L.errMessage);
    msgErr.id = 'ffc-lv-msg-err';
    msgErr.hidden = !L.errMessage;
    if (L.errMessage) box.setAttribute('aria-invalid', 'true');
    form.appendChild(box);
    form.appendChild(msgCount);
    form.appendChild(msgErr);

    var trap = h('div', 'ffc-hp');
    trap.setAttribute('aria-hidden', 'true');
    var bait = h('input');
    bait.type = 'text';
    bait.name = 'company';
    bait.tabIndex = -1;
    bait.autocomplete = 'off';
    bait.value = L.company;
    trap.appendChild(bait);
    form.appendChild(trap);

    var srvErr = h('div', 'ffc-err', L.errServer);
    srvErr.setAttribute('role', 'alert');
    srvErr.hidden = !L.errServer;
    form.appendChild(srvErr);

    var actions = h('div', 'ffc-actions');
    var go = h('button', 'ffc-btn', COPY.cardSend);
    go.type = 'submit';
    actions.appendChild(go);
    form.appendChild(actions);
    card.appendChild(form);

    function syncCount() {
      var n = box.value.length;
      msgCount.hidden = n <= COUNT_FROM;
      msgCount.textContent = n > COUNT_FROM ? n.toLocaleString('en-US') + ' / ' + MAX_CHARS.toLocaleString('en-US') : '';
    }
    growMessage(box);
    syncCount();
    keepInView(email);
    keepInView(box);
    email.addEventListener('input', function () {
      L.email = email.value;
      if (L.errEmail) { L.errEmail = ''; emailErr.hidden = true; email.removeAttribute('aria-invalid'); }
    });
    box.addEventListener('input', function () {
      L.message = box.value;
      growMessage(box);
      syncCount();
      if (L.errMessage) { L.errMessage = ''; msgErr.hidden = true; box.removeAttribute('aria-invalid'); }
    });
    bait.addEventListener('input', function () { L.company = bait.value; });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (L.status === 'sending') return;
      var addr = email.value.replace(/^\s+|\s+$/g, '');
      var text = box.value.replace(/^\s+|\s+$/g, '');
      L.email = addr;
      L.message = box.value;
      L.errEmail = !addr ? COPY.needEmail : (addr.length > 254 || !EMAIL_OK.test(addr)) ? COPY.badEmail : '';
      L.errMessage = text ? '' : COPY.needMessage;
      L.errServer = '';
      if (L.errEmail || L.errMessage) {
        paintLeave();
        var bad = leaveCard.querySelector(L.errEmail ? 'input[name=email]' : 'textarea');
        if (bad) bad.focus();
        return;
      }
      L.message = text;
      srvErr.hidden = true;
      sendLeave();
    });
    if (L.status === 'sending') lockForm(card);
  }

  function mailtoUrl() {
    var body = (L.message + '\n\nPage: ' + pagePath()).replace(/\r?\n/g, '\r\n');
    return 'mailto:' + SUPPORT_EMAIL + '?subject=' + encodeURIComponent(COPY.mailSubject) + '&body=' + encodeURIComponent(body);
  }
  function openMailApp() {
    if (DEMO) return;
    window.location.href = mailtoUrl();
  }

  function sendLeave() {
    L.status = 'sending';
    lockForm(leaveCard);
    if (DEMO) { setTimeout(function () { L.status = 'sent'; paintLeave(); settleCard(leaveCard); }, 600); return; }

    function toMailto() {
      L.status = 'mailto';
      paintLeave();
      settleCard(leaveCard);
      openMailApp();
    }
    function post() {
      var payload = {
        email: L.email, question: L.message, transcript: [], page: pagePath(), reason: 'request',
        company: L.company || '', elapsedMs: Date.now() - openedAt
      };
      fetch(API_ESCALATE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (res) {
        return res.json().then(function (j) { return { res: res, body: j }; }, function () { return { res: res, body: null }; });
      }).then(function (r) {
        var code = r.body && r.body.code;
        if (r.res.ok && r.body && r.body.ok === true) {
          L.status = 'sent';
          paintLeave();
          settleCard(leaveCard);
        } else if (r.res.status === 503 && code === 'not_configured' || r.res.status === 404 || r.res.status === 405 || r.res.status === 501 || r.res.ok) {
          toMailto(); /* nothing on this host can send mail: hand the message to the visitor's email app */
        } else {
          L.status = 'form';
          L.errServer = (r.body && typeof r.body.message === 'string' && r.body.message) || COPY.failed;
          paintLeave();
          var msg = leaveCard.querySelector('.ffc-err[role=alert]');
          if (msg) msg.scrollIntoView({ block: 'nearest' });
        }
      }, toMailto);
    }
    var wait = Math.max(0, MIN_FILL_MS - (Date.now() - openedAt));
    if (wait) setTimeout(post, wait); else post();
  }

  /* ---------- open / close ---------- */
  function setOpen(next, opts) {
    opts = opts || {};
    open = next;
    root.classList.toggle('ffc-open', open);
    launcher.setAttribute('aria-expanded', open ? 'true' : 'false');
    launcher.setAttribute('aria-label', open ? COPY.close : launcherLabel);
    panel.setAttribute('aria-modal', open && mobileQuery.matches ? 'true' : 'false');
    document.documentElement.classList.toggle('ffc-lock', open && mobileQuery.matches);
    fitViewport();
    if (open) {
      hidePill(true);
      launcherAv.classList.remove('ffc-breathe');
      if (!DEMO && !load(OPENED_KEY)) { store(OPENED_KEY, '1'); track('Chat Open'); }
      if (!openedAt) openedAt = Date.now();
      if (closedMode) log.scrollTop = 0; else toBottom();
      if (opts.focus !== false) {
        window.requestAnimationFrame(function () {
          /* closed mode: on a phone, focusing a field would raise the keyboard over the Nora bubble, so wait for a tap */
          var target = !closedMode ? ta : (mobileQuery.matches ? closeBtn : (log.querySelector('input[name=email]') || closeBtn));
          target.focus({ preventScroll: true });
        });
      }
    } else if (opts.focus !== false) {
      launcher.focus({ preventScroll: true });
    }
  }
  function fitViewport() {
    var v = window.visualViewport;
    if (open && mobileQuery.matches && v) {
      panel.style.height = v.height + 'px';
      panel.style.top = v.offsetTop + 'px';
      panel.style.bottom = 'auto';
    } else {
      panel.style.height = panel.style.top = panel.style.bottom = '';
    }
  }
  function showPill() {
    if (open || items.length || load(PILL_KEY) || mobileQuery.matches) return;
    store(PILL_KEY, '1');
    pill.classList.add('ffc-show');
  }
  function hidePill(remember) {
    pill.classList.remove('ffc-show');
    if (remember) store(PILL_KEY, '1');
    if (pillTimer) { clearTimeout(pillTimer); pillTimer = null; }
  }

  /* ---------- events ---------- */
  launcher.addEventListener('click', function () { setOpen(!open); });
  closeBtn.addEventListener('click', function () { setOpen(false); });
  pillText.addEventListener('click', function () { setOpen(true); });
  pillX.addEventListener('click', function () { hidePill(true); launcher.focus({ preventScroll: true }); });
  document.addEventListener('keydown', function (e) {
    if (!open) return;
    if (e.key === 'Escape' || e.key === 'Esc') { e.preventDefault(); setOpen(false); return; }
    if (e.key === 'Tab' && mobileQuery.matches) {
      var nodes = panel.querySelectorAll('button:not([disabled]), a[href], input, textarea');
      var list = [];
      for (var i = 0; i < nodes.length; i += 1) if (nodes[i].offsetParent !== null) list.push(nodes[i]);
      if (!list.length) return;
      var first = list[0];
      var lastNode = list[list.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); lastNode.focus(); }
      else if (!e.shiftKey && document.activeElement === lastNode) { e.preventDefault(); first.focus(); }
      else if (!panel.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
    }
  });
  function growTextarea() {
    ta.style.height = 'auto';
    ta.style.height = Math.min(ta.scrollHeight, 110) + 'px';
    var n = ta.value.length;
    count.hidden = n <= COUNT_FROM;
    count.textContent = n.toLocaleString('en-US') + ' / ' + MAX_CHARS.toLocaleString('en-US');
    syncSend();
  }
  ta.addEventListener('input', growTextarea);
  ta.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); composer.requestSubmit ? composer.requestSubmit() : doSubmit(); }
  });
  function doSubmit() {
    var text = ta.value;
    if (busy || !text.replace(/\s/g, '')) return;
    ta.value = '';
    growTextarea();
    submitText(text);
  }
  composer.addEventListener('submit', function (e) { e.preventDefault(); doSubmit(); });
  if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', fitViewport);
    window.visualViewport.addEventListener('scroll', fitViewport);
  }
  if (mobileQuery.addEventListener) mobileQuery.addEventListener('change', function () { setOpen(open, { focus: false }); });

  /* ---------- start ---------- */
  function mount() {
    document.body.appendChild(root);
    var state = null;
    try { state = new URLSearchParams(location.search).get('chatdemo'); } catch (e) {}
    if (state) { startDemo(state); return; }
    var openNow = false;
    try { openNow = isOpenNow(Date.now(), CHAT); } catch (e) { openNow = false; }
    if (!openNow) {
      var hours = CHAT.live;
      var when = '';
      if (hours) { try { when = openingText(Date.now(), CHAT); } catch (e) { when = CHAT.hours.open + ':00'; } }
      enterClosed(newLeave({ hours: hours, when: when }));
      pillTimer = setTimeout(showPill, 4000);
      return;
    }
    restore();
    renderAll();
    if (!load(OPENED_KEY)) launcherAv.classList.add('ffc-breathe');
    pillTimer = setTimeout(showPill, 4000);
  }

  /* =================================================================
     Pinned demo states. ?chatdemo=<state> renders a fixed state with no
     network at all and no storage, for photographing the design.
     States: closed greeting open typing answered long escalate escalated bubbles handsupport handfounder
             error ratelimited escalate-error  (these force the open chat, whatever CHAT says)
     Closed-mode states (the contact form): closedform closedhours closedinvalid closedsending
             closedsent closedmailto closederror closedpill
     ================================================================= */
  var DEMO_TEXT = {
    track: 'Feeds first: bottle, breast, pumping and solids. Then the things around them: growth, vitamin D, medicines, vaccines and allergens.\n\nIt all stays on your phone and in your own iCloud.',
    free: 'Logging is free on iPhone. Premium adds the deeper views, like the full report and the analytics. The yearly plan starts with a 14-day free trial.',
    two: 'Yes. Family sharing lets both parents log to the same baby from their own phones.\n\nEach feed shows up on both phones, so nobody has to ask when she last ate.',
    german: 'Ja. Mit der Familienfreigabe können beide Eltern von ihrem eigenen iPhone aus dasselbe Baby eintragen. Jede Mahlzeit erscheint auf beiden Geräten, und Änderungen werden über iCloud abgeglichen, sodass niemand nachfragen muss, wann das Baby zuletzt getrunken hat. Die Kinderernährungsprotokollsynchronisierung läuft im Hintergrund, auch nachts.',
    url: 'Here is the guide: https://tryfeedflow.app/guides/how-to-keep-track-of-feeds-across-two-parents-and-a-grandparent-with-family-sharing-and-icloud-sync-2026 and you can also write to support@tryfeedflow.app.',
    unsure: "I can't answer that one reliably. I'd rather send it to the team than guess."
  };
  function msg(role, text) { return { t: 'msg', role: role, text: text }; }
  function startDemo(state) {
    DEMO = true;
    root.classList.add('ffc-still');
    if (state.indexOf('closed') === 0 && state !== 'closed') { startClosedDemo(state); return; }
    var build = {
      closed: [],
      greeting: [],
      open: [],
      typing: [msg('user', 'What does Feed Flow track?'), { t: 'msg', role: 'assistant', text: '', typing: true }],
      answered: [msg('user', 'What does Feed Flow track?'), msg('assistant', DEMO_TEXT.track), msg('user', 'Is it free?'), msg('assistant', DEMO_TEXT.free)],
      long: [
        msg('user', 'What does Feed Flow track?'), msg('assistant', DEMO_TEXT.track),
        msg('user', 'Is it free?'), msg('assistant', DEMO_TEXT.free),
        msg('user', 'Can two parents log together?'), msg('assistant', DEMO_TEXT.two),
        msg('user', 'Kannst du mir das auf Deutsch erklären?'), msg('assistant', DEMO_TEXT.german),
        msg('assistant', 'One more thing.'),
        msg('user', 'Where is the guide for that? https://tryfeedflow.app/guides/how-to-keep-track-of-feeds-across-two-parents-and-a-grandparent-with-family-sharing-and-icloud-sync-2026'),
        msg('assistant', DEMO_TEXT.url)
      ],
      escalate: [msg('user', 'My subscription shows twice on my card.'), msg('assistant', DEMO_TEXT.unsure), { t: 'card', status: 'form', needsTopic: true, to: 'support', reason: 'billing', summary: 'Subscription charged twice', topic: 'Subscription charged twice' }],
      handsupport: [
        msg('user', 'All my feeds disappeared after I changed phone'),
        msg('assistant', 'Ah, that sounds stressful.'),
        msg('assistant', 'Feeds live in your iCloud, so they should come back once you sign in with the same Apple ID.'),
        msg('assistant', 'If they do not, leave your email in the form below and support will write back.'),
        { t: 'card', status: 'form', needsTopic: true, to: 'support', reason: 'bug', summary: 'Feeds are missing after switching to a new phone. Visitor signed in on the new phone.', topic: 'Feeds are missing after switching to a new phone. Visitor signed in on the new phone.' }
      ],
      handfounder: [
        msg('user', "I'm a journalist writing about baby apps, who can I talk to?"),
        msg('assistant', 'Nice, thanks for asking.'),
        msg('assistant', 'I can pass this on to Robin, who built Feed Flow. Want me to?'),
        msg('user', 'Yes please'),
        msg('assistant', 'Done. Leave your email in the form below and he will reply by email.'),
        { t: 'card', status: 'form', needsTopic: true, to: 'founder', reason: 'important', summary: 'A journalist writing about baby apps wants to talk to someone at Feed Flow.', topic: 'A journalist writing about baby apps wants to talk to someone at Feed Flow.' }
      ],
      bubbles: [
        msg('user', 'What does Feed Flow do?'),
        msg('assistant', 'Good one to start with.'),
        msg('assistant', 'It keeps your baby\u2019s feeds, growth and health records in one place on your iPhone.'),
        msg('assistant', 'Logging takes a few taps, and your data stays in your own iCloud.')
      ],
      escalated: [msg('user', 'My subscription shows twice on my card.'), msg('assistant', DEMO_TEXT.unsure), { t: 'card', status: 'sent', email: 'sam@example.com', needsTopic: false }],
      'escalate-error': [msg('user', 'My subscription shows twice on my card.'), msg('assistant', DEMO_TEXT.unsure), { t: 'card', status: 'error', email: 'sam@example.com', needsTopic: false }],
      error: [msg('user', 'What does Feed Flow track?'), { t: 'error', code: 'upstream' }],
      ratelimited: [msg('user', 'What does Feed Flow track?'), { t: 'error', code: 'rate_limited' }]
    };
    items = build[state] || [];
    renderAll();
    if (state === 'closed') return;
    if (state === 'greeting') { pill.classList.add('ffc-show'); return; }
    setOpen(true, { focus: false });
  }
  function startClosedDemo(state) {
    var who = 'sam@example.com';
    var note = 'My subscription shows twice on my card. Could you look at it?';
    var pinned = {
      closedform: {},
      closedpill: {},
      closedhours: { hours: true, when: '9:00 AM Eastern (15:00 your time)' },
      closedinvalid: { email: 'sam@example', errEmail: COPY.badEmail, errMessage: COPY.needMessage },
      closedsending: { status: 'sending', email: who, message: note },
      closedsent: { status: 'sent', email: who, message: note },
      closedmailto: { status: 'mailto', email: who, message: note },
      closederror: { email: who, message: note, errServer: 'Too many messages from this connection. Try again in a minute.' }
    };
    enterClosed(newLeave(pinned[state] || {}));
    if (state === 'closedpill') { pill.classList.add('ffc-show'); return; }
    setOpen(true, { focus: false });
  }
  function demoRun() {
    setBusy(true);
    var reply = addItem({ t: 'msg', role: 'assistant', text: '', typing: true });
    setTimeout(function () {
      reply.typing = false;
      reply.text = 'This is the design preview. No message leaves this page.';
      fill(reply.bubble, reply.text);
      setBusy(false);
      toBottom();
    }, 900);
  }

  if (document.body) mount();
  else document.addEventListener('DOMContentLoaded', mount);
})();
