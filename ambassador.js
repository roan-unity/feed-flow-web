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
    showStatus('success', 'Your email app should open with the application ready to send to support@tryfeedflow.app. Press Send there to complete it.');
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
    // Hosted on Cloudflare Pages (2026-11-16): no form backend, so the application opens ready in the visitor's email app.
    emailFallback(new FormData(form));
  });
})();
