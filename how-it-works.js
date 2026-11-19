/* Home page "How logging works": steps 01 and 02 are two real recordings (<video>, played while in view, the
   poster alone with prefers-reduced-motion); every other phone plays once when it scrolls into view,
   steps chained (a phone starts as the one before it lands). The HTML is the final state,
   so with JS off or prefers-reduced-motion nothing moves and everything is shown.
   The cards below the steps each play on their own when they scroll into view.
   ?hiwdemo=0..100 pins every sequence at that percent of its timeline (for screenshots);
   add &hiwcards=0..100 to pin the cards at a different percent from the steps.
   Steps 03 and 04 are real frames of the same feed, so the amount on the bottle screen is the amount that
   lands on the timeline and on the day meter. */
(function () {
  var section = document.getElementById('how-it-works');
  if (!section) return;
  var params = new URLSearchParams(window.location.search);
  function percent(name) {
    var value = params.get(name);
    return value === null || value === '' || isNaN(Number(value)) ? null : Math.max(0, Math.min(100, Number(value))) / 100;
  }
  var demo = percent('hiwdemo');
  var demoCards = percent('hiwcards');
  if (demo === null) demo = demoCards;
  if (demoCards === null) demoCards = demo;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Steps 01 and 02 are the real recordings. Each plays (muted, looped) while at least 40% of it is in view and
     stops when it leaves; with reduced motion, no IntersectionObserver or ?hiwdemo it stays on its poster. The
     recording of step 02 does not draw a halo, so data-glow="from,to" (seconds into the video) breathes the
     round button's halo until the press, and lets it settle once the app shows the press. */
  Array.prototype.forEach.call(section.querySelectorAll('[data-hiw-video]'), function (figure) {
    var video = figure.querySelector('video');
    if (!video) return;
    video.muted = true;
    if (reduce || demo !== null || !('IntersectionObserver' in window)) return;
    var glow = figure.querySelector('.hiw-press-glow');
    var glowAt = (figure.getAttribute('data-glow') || '').split(',').map(Number);
    var frame = 0;
    function paint() {
      var t = video.currentTime, g0 = glowAt[0], g1 = glowAt[1], level = 0, scale = 1;
      if (t >= g0 && t < g1) {
        var breath = 0.5 - 0.5 * Math.cos(2 * Math.PI * 1.5 * (t - g0) / (g1 - g0));
        level = Math.min(0.999, 0.25 + 0.75 * breath); scale = 1 + 0.07 * breath;
      } else if (t >= g1 && t < g1 + 0.4) {
        level = 0.5 * (1 - (t - g1) / 0.4);
      }
      glow.style.opacity = level ? String(level) : '';
      glow.style.transform = scale === 1 ? '' : 'translate(-50%, -50%) scale(' + scale.toFixed(4) + ')';
      frame = video.paused ? 0 : window.requestAnimationFrame(paint);
    }
    new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var started = video.play();
          if (started && started.catch) started.catch(function () {});
          if (glow && glowAt.length === 2 && !frame) frame = window.requestAnimationFrame(paint);
        } else {
          video.pause();
        }
      });
    }, { threshold: 0.4 }).observe(figure);
  });
  if (demo === null && (reduce || !('IntersectionObserver' in window) || !window.requestAnimationFrame)) return;

  var EASE = {
    out: function (k) { return 1 - Math.pow(1 - k, 3); },
    quart: function (k) { return 1 - Math.pow(1 - k, 4); },
    inout: function (k) { return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; },
    back: function (k) { var c = 1.5; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); },
    lin: function (k) { return k; }
  };

  /* Piece rectangles are [left, top, right, bottom] in % of the screenshot.
     Each piece is a copy of the real screenshot clipped to that rectangle. */
  var SCRIPTS = {
    /* Step 03: the bottle screen arrives piece by piece (the bottle rises like milk filling it), then the
       "Log · finish" button is pressed and sparks fly. */
    log: {
      duration: 4900, rate: 1.35,
      pieces: [
        { r: [8, 1.2, 95, 5.6], a: 'fade', t: [300, 600] },
        { r: [2, 9.8, 98, 21.2], a: 'fade', t: [350, 650] },
        { r: [36, 21.5, 64, 34.5], a: 'sweep', t: [700, 1650], c: [50, 28] },
        { r: [8, 24, 36, 31.5], a: 'up', t: [800, 1100] },
        { r: [64.5, 24, 91, 31.5], a: 'up', t: [900, 1200] },
        { r: [18, 36.5, 82, 80.5], a: 'rise', t: [1100, 2100], f: [3, 1.2, 3] },
        { r: [30, 81, 70, 85.7], a: 'up', t: [1850, 2200] },
        { r: [4.5, 86.2, 49.5, 93], a: 'up', t: [2000, 2350] },
        { r: [50.5, 86.2, 96, 93], a: 'up', t: [2000, 2350], press: [3450, 3750], origin: [72.5, 89.5] }
      ],
      callout: [2300, 2900],
      sparks: { t: [3660, 4890], c: [72.5, 89.5] }
    },
    /* Step 04: the screen's frame arrives first (status bar, header card, "Today", the action panel),
       with no feeds on the timeline. Then the feeds arrive one by one, oldest first, each with the gap
       pill beneath it as one piece (the pill belongs to the newer feed). The newest, the one just
       logged, comes last, together with the "+ amount" chip. */
    finish: {
      duration: 3580, rate: 1.35,
      pieces: [
        { r: [8, 1.2, 95, 5.6], a: 'fade', t: [300, 600] },
        { r: [3, 6.6, 97, 26.5], a: 'fade', t: [400, 750] },
        { r: [3, 27.5, 28, 31.5], a: 'fade', t: [600, 900], f: [4, 0.3] },
        { r: [0, 62.1, 100, 100], a: 'up', t: [700, 1100], f: [4, 0.2] },
        { r: [3, 50, 97, 62.1], a: 'up', t: [1150, 1600], f: [4, 0.3] },
        { r: [3, 42.4, 97, 50], a: 'up', t: [1515, 1965], f: [4, 0.3] },
        { r: [3, 32, 97, 42.4], a: 'drop', t: [1880, 2380], lift: 9, f: [4, 0.3] }
      ],
      /* The day meter: the same bar from the frame before the feed (the "before" image) sits on
         top of this frame's bar (after the feed). Its number cross-fades and its right part is wiped away
         left to right, so the real fill and the real usual-zone marks settle where the app drew them. */
      meter: { from: 'before', r: [4.5, 20.3, 72.5, 25.7], split: 46.5, to: 62, show: [400, 750] },
      count: { t: [2480, 3480], show: [2130, 2430], add: [1880, 2180] }
    },
    flowcast: {
      duration: 3000,
      focus: { t: [350, 1500], keep: [0, 0, 100, 46.5] },
      pieces: [
        { r: [3, 46.5, 97, 55.5], a: 'up', t: [1450, 1900] },
        { r: [3, 55.5, 97, 65.3], a: 'up', t: [1700, 2150] },
        { r: [3, 65.3, 97, 75], a: 'up', t: [1950, 2400] },
        { r: [3, 75, 97, 84], a: 'up', t: [2200, 2650] },
        { r: [0, 84, 100, 100], a: 'up', t: [2450, 2850] }
      ]
    },
    report: {
      duration: 11000,
      scroll: { header: 480 / 4062, travel: (4062 - 2622) / 4062, down: [900, 8400], back: [9100, 10700] }
    },
    /* The four cards below keep the whole screenshot in view and hold back only the rectangles in
       `hold` (shown as the card's own plain colour) until their pieces arrive. */
    growth: {
      duration: 5200,
      hold: [[11, 58.5, 85, 76]],
      pieces: [
        { r: [11, 58.5, 70, 76], a: 'wipe', t: [600, 3300], ease: 'inout', f: [0, 0, 0] },
        { r: [70, 58.5, 85, 76], ellipse: [2.6, 1.2, 72, 63.2], a: 'drop', t: [3300, 3800], lift: 5 },
        { r: [70, 58.5, 85, 76], a: 'fade', t: [3750, 4050], f: [0, 0, 0] }
      ],
      glow: { r: [7, 46.8, 80, 52.8], t: [3950, 5150] }
    },
    health: {
      duration: 4700,
      hold: [[6.2, 54.5, 23, 62.5], [6.9, 62.5, 93.1, 89]],
      pieces: [62.5, 68.4, 74.3, 80.2, 86].map(function (top, i) {
        return { r: [6.9, top, 93.1, Math.min(89, top + 5.9)], a: 'drop', t: [500 + i * 300, 900 + i * 300], lift: 3, f: [0, 0.2, 0] };
      }).concat([{ r: [6.2, 54.5, 23, 62.5], a: 'sweep', t: [2150, 3350], c: [15, 58.5], f: [0, 0, 0] }])
    },
    family: {
      duration: 3700,
      hold: [[2.9, 19.2, 97.1, 36.5], [2.9, 38.8, 97.1, 99]],
      pieces: [168, 239, 341, 413, 485, 556, 628, 700, 771].map(function (y, i) {
        return { r: [2.9, (y - 2) / 8.7, 97.1, (y + 64) / 8.7], a: 'slide', dx: i % 2 ? 45 : -45, t: [450 + i * 240, 1000 + i * 240], f: [0, 0, 0] };
      })
    },
    themes: {
      duration: 2600,
      fan: { t: [500, 1500], stagger: 180 }
    }
  };

  function clamp(k) { return k < 0 ? 0 : k > 1 ? 1 : k; }
  function inset(r) { return 'inset(' + r[1] + '% ' + (100 - r[2]) + '% ' + (100 - r[3]) + '% ' + r[0] + '%)'; }
  function holed(r, h) {
    var p = function (x, y) { return x + '% ' + y + '%'; };
    return 'polygon(evenodd, ' + [p(r[0], r[1]), p(r[2], r[1]), p(r[2], r[3]), p(r[0], r[3]), p(r[0], r[1]),
      p(h[0], h[1]), p(h[0], h[3]), p(h[2], h[3]), p(h[2], h[1]), p(h[0], h[1])].join(', ') + ')';
  }
  /* Soft edges: each piece fades in over a few % outside its rectangle, so it melts into the
     blurred wash instead of showing a hard box. */
  function feather(r, f) {
    var fx = f ? f[0] : 4, fy = f ? f[1] : 1.8, fxr = f && f.length > 2 ? f[2] : fx;
    return 'linear-gradient(to right, transparent ' + (r[0] - fx) + '%, #000 ' + r[0] + '%, #000 ' + r[2] + '%, transparent ' + (r[2] + fxr) + '%), ' +
      'linear-gradient(to bottom, transparent ' + (r[1] - fy) + '%, #000 ' + r[1] + '%, #000 ' + r[3] + '%, transparent ' + (r[3] + fy) + '%)';
  }
  function holes(list) {
    var p = function (x, y) { return x + '% ' + y + '%'; };
    var path = [p(0, 0), p(100, 0), p(100, 100), p(0, 100), p(0, 0)];
    list.forEach(function (h) { path.push(p(h[0], h[1]), p(h[0], h[3]), p(h[2], h[3]), p(h[2], h[1]), p(h[0], h[1]), p(0, 0)); });
    return 'polygon(evenodd, ' + path.join(', ') + ')';
  }
  function setMask(el, mask) {
    el.style.webkitMaskImage = mask;
    el.style.maskImage = mask;
    el.style.webkitMaskComposite = 'source-in';
    el.style.maskComposite = 'intersect';
  }
  function layer(img, cls) {
    var copy = new Image();
    copy.className = 'hiw-layer ' + (cls || '');
    copy.alt = '';
    copy.setAttribute('aria-hidden', 'true');
    copy.decoding = 'sync';
    copy.src = img.currentSrc || img.src;
    return copy;
  }
  function loaded(img) {
    if (img.complete && img.naturalWidth) return Promise.resolve();
    return new Promise(function (resolve) {
      img.addEventListener('load', resolve, { once: true });
      img.addEventListener('error', resolve, { once: true });
    });
  }

  /* Build one phone: returns { duration, tracks, finish } */
  function build(figure) {
    var spec = SCRIPTS[figure.getAttribute('data-hiw')];
    var device = figure.parentNode;
    var shot = figure.querySelector('.hiw-shot');
    var tracks = [];
    var elements = [];
    var rate = spec.rate || 1;
    function track(from, to, ease, apply) { tracks.push({ from: from / rate, to: to / rate, ease: EASE[ease] || EASE.out, apply: apply }); }
    function state(el, base) { var s = { el: el, op: 1, tx: 0, ty: 0, sc: 1, rot: 0, base: base || '' }; elements.push(s); return s; }

    var dev = state(device);
    track(0, 550, 'out', function (k) { dev.op = clamp(k * 1.6); dev.ty = 5 * (1 - k); });

    if (spec.scroll) {
      var header = layer(shot);
      header.style.clipPath = 'inset(0 0 ' + (100 - spec.scroll.header * 100) + '% 0)';
      header.style.zIndex = 2;
      figure.appendChild(header);
      var body = state(shot);
      var travel = spec.scroll.travel * 100;
      track(spec.scroll.down[0], spec.scroll.down[1], 'inout', function (k) { body.ty = -travel * k; });
      track(spec.scroll.back[0], spec.scroll.back[1], 'inout', function (k) { if (k > 0) body.ty = -travel * (1 - k); });
      return { duration: spec.duration / rate, tracks: tracks, elements: elements, cleanup: function () { header.remove(); } };
    }

    if (spec.fan) {
      /* Four phones, one per theme: they start as one stack and fan out to where the CSS puts them. */
      Array.prototype.forEach.call(figure.querySelectorAll('.hiw-phone'), function (phone, i, all) {
        var f = i - (all.length - 1) / 2;
        var ps = state(phone);
        var from = spec.fan.t[0] + i * spec.fan.stagger;
        track(from, from + (spec.fan.t[1] - spec.fan.t[0]), 'back', function (k) {
          ps.base = 'translateX(' + (f * 24 * k).toFixed(3) + '%) rotate(' + (f * 4.5 * k).toFixed(3) + 'deg)';
          ps.sc = 0.94 + 0.06 * k;
        });
      });
      return { duration: spec.duration / rate, tracks: tracks, elements: elements, cleanup: function () { elements.forEach(function (s) { s.base = ''; }); } };
    }

    /* Before a piece lands its area is the phone's plain background (the capture's own left edge,
       made by scripts/prepare-how-it-works.py), never a blurred copy of the hidden content. */
    figure.style.background = 'url(/screens/how/' + figure.getAttribute('data-hiw') + '-bg.png) 0 0 / 100% 100% no-repeat, var(--bg-soft)';
    shot.style.position = 'relative';
    shot.style.zIndex = 1;
    var main = state(shot);
    var added = [];

    if (spec.hold) {
      shot.style.clipPath = holes(spec.hold);
      var whole = layer(shot);
      whole.style.zIndex = 7;
      figure.appendChild(whole);
      added.push(whole);
      var ws = state(whole);
      track(spec.duration - 320, spec.duration, 'lin', function (k) { ws.op = k; });
    } else if (spec.focus) {
      var keep = spec.focus.keep;
      track(spec.focus.t[0], spec.focus.t[1], 'out', function (k) {
        main.op = k;
        shot.style.filter = k < 1 ? 'blur(' + (14 * (1 - k)).toFixed(2) + 'px)' : '';
      });
      track(spec.duration - 250, spec.duration, 'lin', function (k) {
        shot.style.clipPath = k < 1 ? inset(keep) : '';
      });
    } else {
      track(spec.duration - 320, spec.duration, 'lin', function (k) { main.op = k; });
    }

    if (spec.meter) {
      var mt = spec.meter, mr = mt.r, ct = spec.count.t;
      var beforeSrc = (shot.currentSrc || shot.src).replace('/' + figure.getAttribute('data-hiw') + '-', '/' + mt.from + '-');
      var oldNumber = layer(shot), oldBar = layer(shot);
      [oldNumber, oldBar].forEach(function (el) { el.src = beforeSrc; el.style.zIndex = 3; figure.appendChild(el); added.push(el); });
      oldNumber.style.clipPath = inset([mr[0], mr[1], mt.split, mr[3]]);
      var ons = state(oldNumber), obs = state(oldBar);
      track(mt.show[0], mt.show[1], 'out', function (k) { ons.op = k; obs.op = k; });
      track(ct[0] + 150, ct[0] + 550, 'lin', function (k) { ons.op *= 1 - k; });
      track(ct[0], ct[1], 'quart', function (k) {
        oldBar.style.clipPath = inset([mt.split + (mt.to - mt.split) * k, mr[1], mr[2], mr[3]]);
        if (k >= 1) obs.op = 0;
      });
    }

    spec.pieces.forEach(function (p) {
      var el = layer(shot);
      el.style.zIndex = 2;
      if (p.hole) el.style.clipPath = holed(p.r, p.hole);
      if (p.ellipse) el.style.clipPath = 'ellipse(' + p.ellipse[0] + '% ' + p.ellipse[1] + '% at ' + p.ellipse[2] + '% ' + p.ellipse[3] + '%)';
      else setMask(el, feather(p.r, p.f));
      figure.appendChild(el);
      added.push(el);
      var s = state(el);
      var a = p.t[0], b = p.t[1];
      if (p.a === 'drop') {
        var lift = p.lift || 6;
        track(a, b, 'back', function (k) { s.ty = -lift * (1 - k); });
        track(a, a + (b - a) * 0.45, 'lin', function (k) { s.op = k; });
      } else if (p.a === 'up') {
        track(a, b, 'out', function (k) { s.ty = 2.5 * (1 - k); s.op = k; });
      } else if (p.a === 'slide') {
        track(a, b, 'out', function (k) { s.tx = (p.dx || -8) * (1 - k); s.op = clamp(k * 1.5); });
      } else if (p.a === 'fade') {
        track(a, b, 'out', function (k) { s.op = k; });
      } else if (p.a === 'rise') {
        track(a, b, 'out', function (k) {
          var top = p.r[3] - (p.r[3] - p.r[1]) * k;
          el.style.clipPath = k >= 1 ? '' : 'inset(' + top + '% 0 0 0)';
        });
      } else if (p.a === 'wipe') {
        track(a, b, p.ease || 'out', function (k) {
          el.style.clipPath = k >= 1 ? '' : 'inset(0 ' + (100 - p.r[0] - (p.r[2] - p.r[0]) * k) + '% 0 0)';
        });
      } else if (p.a === 'sweep') {
        track(a, b, 'inout', function (k) {
          var angle = (k * 360).toFixed(1);
          setMask(el, feather(p.r, p.f) + (k >= 1 ? '' : ', conic-gradient(from 0deg at ' + p.c[0] + '% ' + p.c[1] + '%, #000 ' + angle + 'deg, transparent ' + angle + 'deg)'));
        });
      }
      if (p.press) {
        el.style.transformOrigin = p.origin[0] + '% ' + p.origin[1] + '%';
        track(p.press[0], p.press[1], 'lin', function (k) {
          s.sc = k < 0.35 ? 1 - 0.1 * EASE.out(k / 0.35) : 0.9 + 0.1 * EASE.back((k - 0.35) / 0.65);
          if (k === 0 || k === 1) s.sc = 1;
          el.style.filter = s.sc < 1 ? 'brightness(' + (1 - (1 - s.sc) * 2.2).toFixed(3) + ')' : '';
        });
      }
    });

    if (spec.glow) {
      var glow = document.createElement('span');
      glow.className = 'hiw-glow';
      glow.setAttribute('aria-hidden', 'true');
      glow.style.left = spec.glow.r[0] + '%'; glow.style.top = spec.glow.r[1] + '%';
      glow.style.width = (spec.glow.r[2] - spec.glow.r[0]) + '%'; glow.style.height = (spec.glow.r[3] - spec.glow.r[1]) + '%';
      figure.appendChild(glow);
      added.push(glow);
      var gs = state(glow);
      track(spec.glow.t[0], spec.glow.t[1], 'lin', function (k) { gs.op = k < 0.25 ? EASE.out(k / 0.25) : k > 0.6 ? 1 - EASE.inout((k - 0.6) / 0.4) : 1; if (k <= 0 || k >= 1) gs.op = 0; });
    }

    function drawn(cls, parent, z) {
      var node = document.createElement('span');
      node.className = cls;
      node.setAttribute('aria-hidden', 'true');
      node.style.zIndex = z;
      parent.appendChild(node);
      added.push(node);
      return node;
    }
    var callout = device.querySelector('.hiw-callout');
    if (spec.callout && callout) {
      var cs = state(callout, 'translateX(-50%)');
      track(spec.callout[0], spec.callout[1], 'out', function (k) { cs.op = k; cs.ty = 40 * (1 - k); });
    }

    if (spec.sparks) {
      var sp = spec.sparks, hues = ['var(--coral)', 'var(--teal)'];
      for (var i = 0; i < 14; i++) {
        (function (i) {
          var spark = drawn('hiw-spark', device, 6);
          var size = 8 + (i * 3) % 5;
          spark.style.left = sp.c[0] + '%'; spark.style.top = sp.c[1] + '%';
          spark.style.width = size + 'px'; spark.style.height = size + 'px';
          spark.style.background = hues[i % 2];
          var angle = (i / 14) * Math.PI * 2 + (i % 2 ? 0.12 : -0.1), dist = 42 + (i * 11) % 28;
          var ss = state(spark, 'translate(-50%, -50%)');
          ss.px = true;
          var from = sp.t[0] + i * 10;
          track(from, from + 1100, 'lin', function (k) {
            var out = EASE.quart(k);
            ss.tx = Math.cos(angle) * dist * out; ss.ty = Math.sin(angle) * dist * out + 14 * k * k;
            ss.rot = (i % 2 ? 1 : -1) * 70 * k;
            ss.sc = k < 0.15 ? 0.4 + k / 0.15 * 0.6 : 1;
            ss.op = k <= 0 || k >= 1 ? 0 : k < 0.6 ? 0.999 : 1 - (k - 0.6) / 0.4;
          });
        })(i);
      }
    }

    var meter = device.querySelector('.hiw-meter');
    var count = device.querySelector('.hiw-count');
    if (spec.count && meter && count) {
      var target = Number(count.getAttribute('data-to')) || 0;
      var origin = Number(count.getAttribute('data-from')) || 0;
      var pill = meter.querySelector('.hiw-pill');
      var add = meter.querySelector('.hiw-add');
      if (add) {
        var as = state(add);
        track(spec.count.add[0], spec.count.add[1], 'out', function (k) { as.op = k; as.ty = 40 * (1 - k); });
      }
      var ms = state(pill || meter);
      track(spec.count.show[0], spec.count.show[1], 'out', function (k) { ms.op = k; ms.ty = 30 * (1 - k); });
      /* in the app's own steps: half an ounce, or data-step (5 ml) */
      var step = Number(count.getAttribute('data-step')) || 0.5;
      track(spec.count.t[0], spec.count.t[1], 'quart', function (k) { count.textContent = String(Math.round((origin + (target - origin) * k) / step) * step); });
    }

    return {
      duration: spec.duration / rate, tracks: tracks, elements: elements,
      cleanup: function () { added.forEach(function (el) { el.remove(); }); figure.style.background = ''; shot.style.position = ''; shot.style.zIndex = ''; shot.style.filter = ''; shot.style.clipPath = ''; }
    };
  }

  function render(seq, t) {
    seq.elements.forEach(function (s) { s.op = 1; s.tx = 0; s.ty = 0; s.sc = 1; s.rot = 0; });
    seq.tracks.forEach(function (tr) {
      var k = clamp((t - tr.from) / (tr.to - tr.from));
      tr.apply(k <= 0 ? 0 : k >= 1 ? 1 : tr.ease(k));
    });
    seq.elements.forEach(function (s) {
      s.el.style.opacity = s.op >= 1 ? '' : String(s.op);
      var transform = s.base;
      var unit = s.px ? 'px' : '%';
      if (s.tx || s.ty) transform += ' translate(' + s.tx.toFixed(3) + unit + ', ' + s.ty.toFixed(3) + unit + ')';
      if (s.rot) transform += ' rotate(' + s.rot.toFixed(2) + 'deg)';
      if (s.sc !== 1) transform += ' scale(' + s.sc.toFixed(4) + ')';
      s.el.style.transform = transform;
    });
  }
  function finish(seq) {
    render(seq, seq.duration + 1);
    seq.cleanup();
    seq.elements.forEach(function (s) { s.el.style.opacity = ''; s.el.style.transform = s.base; });
    seq.done = true;
  }

  var figures = Array.prototype.slice.call(section.querySelectorAll('[data-hiw]'));
  if (demo !== null) figures.forEach(function (f) { Array.prototype.forEach.call(f.querySelectorAll('img'), function (img) { img.loading = 'eager'; img.decoding = 'sync'; }); });

  var sequences = figures.map(function (figure) {
    return { figure: figure, chained: !!figure.closest('.hiw-step'), prev: null, start: null, visible: false, ready: false, done: false };
  });
  var steps = sequences.filter(function (s) { return s.chained; });
  steps.forEach(function (s, i) { s.prev = i ? steps[i - 1] : null; });
  var OVERLAP = 500;

  sequences.forEach(function (seq) {
    var img = seq.figure.querySelector('.hiw-shot');
    Promise.all(Array.prototype.map.call(seq.figure.querySelectorAll('img'), loaded)).then(function () {
      /* the day meter also needs the frame from before the feed */
      var spec = SCRIPTS[seq.figure.getAttribute('data-hiw')];
      if (!spec.meter) return;
      var before = new Image();
      before.src = (img.currentSrc || img.src).replace('/' + seq.figure.getAttribute('data-hiw') + '-', '/' + spec.meter.from + '-');
      return loaded(before);
    }).then(function () {
      if (!img.naturalWidth) return;
      var built = build(seq.figure);
      seq.duration = built.duration; seq.tracks = built.tracks; seq.elements = built.elements; seq.cleanup = built.cleanup;
      seq.ready = true;
      if (demo !== null) return demoRender();
      render(seq, 0);
      kick();
    });
  });

  function demoRender() {
    if (!sequences.every(function (s) { return s.ready; })) return;
    var offset = 0;
    var starts = steps.map(function (s) { var at = offset; offset += s.duration - OVERLAP; return at; });
    var total = offset + OVERLAP;
    sequences.forEach(function (seq) {
      var at = seq.chained ? demo : demoCards;
      var t = seq.chained ? demo * total - starts[steps.indexOf(seq)] : demoCards * seq.duration;
      if (at >= 1) finish(seq); else render(seq, t);
    });
    document.documentElement.setAttribute('data-hiwdemo', 'ready');
  }

  var running = false;
  function canStart(seq, now) {
    if (!seq.ready || !seq.visible) return false;
    var p = seq.prev;
    if (!p || p.done || !p.ready) return true;
    if (p.start === null) return !p.visible;
    return now >= p.start + p.duration - OVERLAP;
  }
  function tick(now) {
    var keep = false;
    sequences.forEach(function (seq) {
      if (seq.done || !seq.ready) return;
      if (seq.start === null) {
        if (canStart(seq, now)) seq.start = now;
        else { if (seq.visible) keep = true; return; }
      }
      var t = now - seq.start;
      if (t >= seq.duration) finish(seq);
      else { render(seq, t); keep = true; }
    });
    running = keep;
    if (keep) window.requestAnimationFrame(tick);
  }
  function kick() { if (!running) { running = true; window.requestAnimationFrame(tick); } }

  if (demo === null) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var seq = sequences.filter(function (s) { return s.figure === entry.target; })[0];
        if (seq && entry.isIntersecting) { seq.visible = true; observer.unobserve(entry.target); kick(); }
      });
    }, { threshold: 0.4 });
    sequences.forEach(function (seq) { observer.observe(seq.figure); });
  }
})();
