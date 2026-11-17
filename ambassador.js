/* Ambassador application: POST /api/ambassador, with the visitor's own email app as the fallback
   so an application is never lost. */
(function () {
  var form = document.getElementById('ambassadorForm');
  if (!form) return;
  var card = document.getElementById('formCard');
  var status = document.getElementById('formStatus');
  var submit = document.getElementById('amb-submit');
  var opened = Date.now();

  function mailtoHref(data) {
    var body = [
      'Name: ' + data.name, 'Email: ' + data.email, 'Where to see my work: ' + data.work, '',
      'Anything else:', data.note || '(nothing)', '',
      'I will tell my audience I am a Feed Flow ambassador and only share honest opinions: yes'
    ].join('\n');
    return 'mailto:support@tryfeedflow.app?subject=' + encodeURIComponent('Ambassador application: ' + data.name) + '&body=' + encodeURIComponent(body);
  }
  function showStatus(kind, message, data) {
    status.hidden = false;
    status.className = 'form-status ' + kind;
    status.textContent = message;
    if (data) {
      var link = document.createElement('a');
      link.href = mailtoHref(data);
      link.textContent = 'Send it by email instead';
      status.appendChild(document.createTextNode(' '));
      status.appendChild(link);
    }
  }
  function emailFallback(data) {
    submit.disabled = false;
    showStatus('error', "That didn't go through on our side. Your email app should open with your application ready. Press Send there and we have it.", data);
    window.location.href = mailtoHref(data);
  }
  function done(data) {
    if (window.plausible) window.plausible('Ambassador application');
    card.innerHTML = '<div class="done-card" role="status" tabindex="-1"><svg class="icon" aria-hidden="true"><use href="/assets/icons.svg#check"/></svg><h3>Thank you, <span data-first></span>. We have your application.</h3><p>We read every application ourselves and answer by email, at <strong></strong>.</p><p>Until then, the best thing you can do is use the app with your own baby. <a href="/">See what Feed Flow does</a></p></div>';
    card.querySelector('[data-first]').textContent = data.name.split(' ')[0];
    card.querySelector('strong').textContent = data.email;
    card.querySelector('.done-card').focus();
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    status.hidden = true;
    form.querySelectorAll('[aria-invalid]').forEach(function (field) { field.removeAttribute('aria-invalid'); });
    if (!form.checkValidity()) {
      form.querySelectorAll(':invalid').forEach(function (field) { field.setAttribute('aria-invalid', 'true'); });
      var first = form.querySelector(':invalid');
      if (first) first.focus();
      showStatus('error', 'Fill in your name, your email and one link to your work, and tick the box.');
      return;
    }
    var fields = new FormData(form);
    var data = {
      name: String(fields.get('name') || '').trim(), email: String(fields.get('email') || '').trim(),
      work: String(fields.get('work') || '').trim(), note: String(fields.get('note') || '').trim()
    };
    submit.disabled = true;
    fetch('/api/ambassador', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: data.name, email: data.email, work: data.work, note: data.note, agree: !!fields.get('agree'),
        company: fields.get('company') || '', elapsedMs: Date.now() - opened
      })
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (body) { return { status: r.status, ok: r.ok, body: body }; });
    }).then(function (res) {
      if (res.ok && res.body && res.body.ok) { done(data); return; }
      // A field the server did not accept can be fixed here. Anything else goes out by email.
      if (res.status === 400 && res.body && res.body.message && res.body.code !== 'bad_request') {
        submit.disabled = false;
        showStatus('error', res.body.message, data);
        return;
      }
      emailFallback(data);
    }).catch(function () {
      emailFallback(data);
    });
  });
})();
