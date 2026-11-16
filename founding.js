/* Founding families: live spot counter and the sign-up form (POST /api/founding). */
(function () {
  var TOTAL = 100;
  var left = document.getElementById('spotsLeft');
  var bar = document.getElementById('spotsBar');
  var note = document.getElementById('spotsNote');
  var form = document.getElementById('foundingForm');
  var card = document.getElementById('formCard');
  var status = document.getElementById('formStatus');
  var submit = document.getElementById('ff-submit');
  var opened = Date.now();

  function showStatus(kind, message) {
    status.hidden = false;
    status.className = 'form-status ' + kind;
    status.textContent = message;
  }
  function closeList() {
    if (note) note.textContent = 'All 100 founding spots are taken. Thank you, every one of you.';
    if (card) card.innerHTML = '<div class="done-card"><h3>All 100 spots are taken</h3><p>The founding list is full. Feed Flow! is still free to download, and logging feeds and sharing with your family are free.</p></div>';
  }
  function paint(claimed) {
    var remaining = Math.max(0, TOTAL - claimed);
    if (left) left.textContent = String(remaining);
    if (bar) bar.style.width = Math.min(100, (claimed / TOTAL) * 100) + '%';
    if (remaining === 0) closeList();
  }
  fetch('/founding.json', { cache: 'no-store' })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (d) { if (d && typeof d.claimed === 'number') paint(d.claimed); })
    .catch(function () {});

  if (!form) return;
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    status.hidden = true;
    if (!form.checkValidity()) {
      form.reportValidity();
      showStatus('error', 'Fill in your first name and email, and tick the box if your App Store account is a US one.');
      return;
    }
    var data = new FormData(form);
    submit.disabled = true;
    fetch('/api/founding', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        first: data.get('first'), email: data.get('email'), us: !!data.get('us'),
        company: data.get('company') || '', elapsedMs: Date.now() - opened
      })
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (body) { return { ok: r.ok, body: body }; });
    }).then(function (res) {
      if (!res.ok) {
        submit.disabled = false;
        showStatus('error', (res.body && res.body.message) || "That didn't go through. Try again in a minute, or write to support@tryfeedflow.app.");
        return;
      }
      if (window.plausible) window.plausible('Founding signup');
      card.innerHTML = '<div class="done-card"><h3>You are on the list</h3><p>Your code is on its way to <strong></strong>. It usually arrives within ten minutes. Look in spam or promotions if you don\'t see it.</p><p>Open the email on your iPhone and tap the link. Any trouble, write to support@tryfeedflow.app.</p></div>';
      card.querySelector('strong').textContent = String(data.get('email'));
    }).catch(function () {
      submit.disabled = false;
      showStatus('error', "That didn't go through. Check your connection and try again, or write to support@tryfeedflow.app.");
    });
  });
})();
