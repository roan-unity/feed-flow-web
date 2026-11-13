/* Shareable ambassador application and Netlify form with an email fallback. */
(function () {
  var shareUrl = 'https://tryfeedflow.app/ambassador';
  var feedback = document.getElementById('shareFeedback');

  function copied(message) {
    if (feedback) feedback.textContent = message;
  }
  function copyLink() {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(shareUrl);
    }
    return new Promise(function (resolve, reject) {
      var field = document.createElement('textarea');
      field.value = shareUrl;
      field.setAttribute('readonly', '');
      field.style.position = 'fixed';
      field.style.opacity = '0';
      document.body.appendChild(field);
      field.select();
      try {
        if (document.execCommand('copy')) resolve(); else reject(new Error('copy unavailable'));
      } catch (e) { reject(e); }
      field.remove();
    });
  }
  document.querySelectorAll('[data-share-page]').forEach(function (button) {
    button.addEventListener('click', function () {
      if (navigator.share) {
        navigator.share({ title: 'Work as a Feed Flow ambassador', text: 'Help families with feeding, growth and health tracking. See the Feed Flow ambassador program.', url: shareUrl })
          .then(function () { copied('Share sheet opened.'); })
          .catch(function (error) { if (error.name !== 'AbortError') copyLink().then(function () { copied('Application link copied.'); }); });
      } else {
        copyLink().then(function () { copied('Application link copied.'); }).catch(function () { copied('Share link: ' + shareUrl); });
      }
    });
  });

  var form = document.getElementById('ambassadorForm');
  if (!form) return;
  var status = document.getElementById('formStatus');
  var submit = document.getElementById('amb-submit');

  function showStatus(kind, message) {
    status.hidden = false;
    status.className = 'form-status ' + kind;
    status.textContent = message;
  }
  function emailFallback(data) {
    var platforms = data.getAll('platform').join(', ') || 'Not specified';
    var body = [
      'Name: ' + data.get('name'), 'Email: ' + data.get('email'), 'Country: ' + data.get('country'),
      'Role: ' + data.get('role'), 'Platforms: ' + platforms,
      'Audience size: ' + (data.get('audience-size') || 'Not specified'),
      'Profile / practice: ' + (data.get('handle') || 'Not provided'), '',
      'Why Feed Flow fits:', data.get('note'), '',
      'Disclosure and honest-opinion agreement: ' + data.get('disclosure-agreement')
    ].join('\n');
    var href = 'mailto:support@tryfeedflow.app?subject=' + encodeURIComponent('Ambassador application — ' + data.get('name')) + '&body=' + encodeURIComponent(body);
    showStatus('error', 'Automatic submission was unavailable. Your email app should open with the application ready; press Send there to complete it.');
    window.location.href = href;
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    status.hidden = true;
    if (!form.checkValidity()) {
      form.reportValidity();
      var invalid = form.querySelector(':invalid');
      if (invalid) invalid.focus();
      showStatus('error', 'Please complete the required fields and accept the honest-disclosure statement.');
      return;
    }
    var data = new FormData(form);
    submit.disabled = true;
    submit.textContent = 'Sending…';
    var encoded = new URLSearchParams();
    data.forEach(function (value, key) { if (typeof value === 'string') encoded.append(key, value); });

    fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: encoded.toString() })
      .then(function (response) {
        if (!response.ok) throw new Error('Submission unavailable');
        showStatus('success', 'Thank you. Your application has been received. We will review the fit and contact you using the email you provided.');
        form.reset();
        submit.textContent = 'Send another application';
        submit.disabled = false;
        status.focus();
      })
      .catch(function () {
        submit.disabled = false;
        submit.textContent = 'Send my application';
        emailFallback(data);
      });
  });
})();
