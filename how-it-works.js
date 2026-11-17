/* Home page "How logging works": each phone plays once when it scrolls into view,
   steps chained (a phone starts as the one before it lands). The HTML is the final state,
   so with JS off or prefers-reduced-motion nothing moves and everything is shown.
   The cards below the steps each play on their own when they scroll into view.
   ?hiwdemo=0..100 pins every sequence at that percent of its timeline (for screenshots);
   add &hiwcards=0..100 to pin the cards at a different percent from the four steps.
   Steps 02 to 04 are three frames of one real recording of a 2.5 oz bottle, so the amount on the
   bottle screen is the amount that lands on the timeline and on the day meter. */
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
    start: {
      duration: 2900, rate: 1.45,
      pieces: [
        { r: [8, 2.4, 95, 5.4], a: 'fade', t: [350, 650] },
        { r: [15, 31, 85, 36.2], a: 'up', t: [450, 850] },
        { r: [40.5, 36.4, 59.5, 46], a: 'drop', t: [600, 1000] },
        { r: [6.5, 47.2, 29, 61], a: 'drop', t: [750, 1150] },
        { r: [36.5, 46.4, 63.5, 61], a: 'drop', t: [900, 1300], press: [1900, 2350], origin: [50, 53.5] },
        { r: [70.5, 47.2, 93, 61], a: 'drop', t: [1050, 1450] },
        { r: [0, 61.7, 100, 100], a: 'up', t: [1500, 1950] }
      ],
      ring: { c: [50, 52.5], w: 25, t: [2050, 2700] }
    },
    /* Step 02: the whole Today screen arrives, everything but the log button softly blurs and dims
       (the .hiw-dim overlay, which stays), two rings pulse out of the button, then it is pressed. */
    press: {
      duration: 2100,
      whole: [150, 550],
      dim: [500, 1000],
      pieces: [
        { r: [35.5, 77.8, 64.5, 91], ellipse: [14, 6.44, 50, 84.4], a: 'fade', t: [150, 550], press: [1500, 1850], origin: [50, 84.4] }
      ],
      rings: [{ c: [50, 84.4], w: 26, t: [850, 1400] }, { c: [50, 84.4], w: 26, t: [1150, 1700] }],
      cue: [900, 1200]
    },
    log: {
      duration: 4900, rate: 1.35,
      pieces: [
        { r: [8, 1.2, 95, 5.6], a: 'fade', t: [300, 600] },
        { r: [3, 10, 97, 14.6], a: 'fade', t: [350, 650] },
        { r: [4.5, 15.2, 95.5, 21], a: 'slide', t: [450, 900] },
        { r: [36.5, 21.6, 63.5, 34.4], a: 'sweep', t: [700, 1650], c: [50, 27.9] },
        { r: [9, 24.5, 36, 31.5], a: 'up', t: [800, 1100] },
        { r: [64.5, 24.5, 91, 31.5], a: 'up', t: [900, 1200] },
        { r: [27, 36, 74, 80.6], hole: [30.5, 56.8, 71.3, 79.8], a: 'fade', t: [1050, 1450], f: [12, 5] },
        { r: [30.5, 56.8, 66.6, 79.8], a: 'rise', t: [1300, 2050], f: [4, 1.8, 0.01] },
        { r: [66.6, 69.3, 71.3, 72.1], a: 'fade', t: [1700, 2050], f: [0.2, 0.7, 0.7], ride: true },
        { r: [19, 67.3, 29, 73.3], a: 'fade', t: [1900, 2200] },
        { r: [72, 67.3, 82, 73.3], a: 'fade', t: [1900, 2200], f: [0.4, 1.8, 4] },
        { r: [30, 81, 44.8, 85.5], a: 'up', t: [1850, 2200], f: [4, 1.8, 0.01], taken: true },
        { r: [44.8, 81, 70, 85.5], a: 'up', t: [1850, 2200], f: [0.01, 1.8, 4] },
        { r: [4.5, 86.2, 49.5, 93], a: 'up', t: [2000, 2350] },
        { r: [50.5, 86.2, 96, 93], a: 'up', t: [2000, 2350], press: [3450, 3750], origin: [73.3, 89.6] }
      ],
      /* The recording's bottle goes from 3.5 oz left (0.5 taken) to 1.5 oz left (2.5 taken); the frame
         shown is the second. The screenshot cannot move its own level, so a drawn milk band, a drawn
         handle and a fingertip dot play that drag on top of it; at the end they swap for the real ones. */
      drag: { t: [2500, 3350], from: 60.95, to: 70.69, band: [33.5, 66.4, 60.95, 71.7], hx: [40.2, 68.7], show: [1500, 2050], taken: [0.5, 2.5] },
      sparks: { t: [3660, 4890], c: [73.3, 89.6] }
    },
    finish: {
      duration: 3550, rate: 1.35,
      pieces: [
        { r: [8, 1.2, 95, 5.6], a: 'fade', t: [300, 600] },
        { r: [3, 6.6, 97, 26.8], a: 'fade', t: [400, 750] },
        { r: [3, 27.8, 28, 31.6], a: 'fade', t: [600, 900] },
        { r: [3, 53.2, 97, 59.8], a: 'drop', t: [750, 1100] },
        { r: [3, 49.8, 30, 52.8], a: 'fade', t: [950, 1200] },
        { r: [3, 42.7, 97, 49.3], a: 'drop', t: [1050, 1400] },
        { r: [3, 39.3, 30, 42.3], a: 'fade', t: [1250, 1500] },
        { r: [3, 32.2, 97, 38.8], a: 'drop', t: [1700, 2150], lift: 9 },
        { r: [0, 60.2, 100, 100], a: 'up', t: [2300, 2700] }
      ],
      /* The day meter: the same bar from the frame before the feed (17.5 oz, step 02's image) sits on
         top of this frame's bar (20 oz). Its number cross-fades and its right part is wiped away left
         to right, so the real fill and the real usual-zone marks grow to where the app drew them. */
      meter: { from: 'press', r: [4.5, 20.3, 72.5, 25.7], split: 42.3, to: 57, show: [400, 750] },
      count: { t: [2450, 3450], show: [2100, 2400], add: [1850, 2150] }
    },
    flowcast: {
      duration: 3000,
      focus: { t: [350, 1500], keep: [0, 0, 100, 61.5] },
      pieces: [
        { r: [3, 61.8, 97, 65], a: 'fade', t: [1350, 1650] },
        { r: [3, 65.3, 97, 72.2], a: 'up', t: [1500, 1950] },
        { r: [3, 73.3, 97, 81], a: 'up', t: [1750, 2200] },
        { r: [3, 82.3, 97, 90], a: 'up', t: [2000, 2450] },
        { r: [3, 91.3, 97, 99.6], a: 'up', t: [2250, 2700] }
      ]
    },
    report: {
      duration: 11000,
      scroll: { header: 392 / 4794, travel: (4794 - 2622) / 4794, down: [900, 8400], back: [9100, 10700] }
    },
    /* The four cards below keep the whole screenshot in view and hold back only the rectangles in
       `hold` (shown as the card's own plain colour) until their pieces arrive. */
    growth: {
      duration: 5200,
      hold: [[14.6, 37.2, 78.2, 54]],
      pieces: [
        { r: [14.6, 37.2, 73.4, 54], a: 'wipe', t: [600, 3300], ease: 'inout', f: [0, 0, 0] },
        { r: [73.4, 37.2, 78.2, 54], ellipse: [2.3, 1.05, 75.33, 42.5], a: 'drop', t: [3300, 3800], lift: 5 },
        { r: [73.4, 37.2, 78.2, 54], a: 'fade', t: [3750, 4050], f: [0, 0, 0] }
      ],
      glow: { r: [5.4, 25.9, 78.4, 31.3], t: [3950, 5150] }
    },
    health: {
      duration: 4700,
      hold: [[6.2, 29, 22.4, 36.6], [6.9, 37.1, 93.1, 88.5]],
      pieces: [0, 1, 2, 3, 4, 5, 6, 7, 8].map(function (i) {
        var top = (581 + 90.5 * i) / 15.65, bottom = Math.min(88.5, (664 + 90.5 * i) / 15.65);
        return { r: [6.9, top, 93.1, bottom], a: 'drop', t: [500 + i * 250, 900 + i * 250], lift: 3, f: [0, 0.2, 0] };
      }).concat([{ r: [6.2, 29, 22.4, 36.6], a: 'sweep', t: [3150, 4350], c: [14.17, 32.84], f: [0, 0, 0] }])
    },
    family: {
      duration: 3700,
      hold: [[2.9, 17.5, 97.1, 47.3], [2.9, 51, 97.1, 95.9]],
      pieces: [278, 397, 516, 635, 805, 924, 1043, 1162, 1281, 1400].map(function (y, i) {
        return { r: [2.9, (y - 3) / 15.72, 97.1, (y + 107) / 15.72], a: 'slide', dx: i % 2 ? 45 : -45, t: [450 + i * 240, 1000 + i * 240], f: [0, 0, 0] };
      })
    },
    themes: {
      duration: 2600,
      fan: { t: [500, 1500], stagger: 180 }
    }
  };

  /* The live "oz taken" number is set in the system font, which only matches the screenshot's own
     digits on Apple devices; elsewhere the screenshot's number is left as it is. */
  var appleFont = /Mac|iPhone|iPad|iPod/.test(navigator.platform || navigator.userAgent || '');
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
    } else if (spec.whole) {
      track(spec.whole[0], spec.whole[1], 'out', function (k) { main.op = k; });
    } else {
      track(spec.duration - 320, spec.duration, 'lin', function (k) { main.op = k; });
    }

    if (spec.dim) {
      /* .hiw-dim and .hiw-cue-ring are in the HTML (the resting state); here they only arrive. */
      var dim = figure.querySelector('.hiw-dim');
      if (dim) { var ds = state(dim); track(spec.dim[0], spec.dim[1], 'inout', function (k) { ds.op = k; }); }
      var cue = figure.querySelector('.hiw-cue-ring');
      if (cue) { var qs = state(cue, 'translate(-50%, -50%)'); track(spec.cue[0], spec.cue[1], 'out', function (k) { qs.op = k; qs.sc = 1.12 - 0.12 * k; }); }
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
      if (p.taken && spec.drag && spec.drag.taken && appleFont) {
        /* The screenshot's own "3.5" waits until the drag ends; a live number counts up to it in the
           app's half-ounce steps while the level drops, then hands over to the real pixels. */
        var live = document.createElement('span');
        live.className = 'hiw-taken';
        live.setAttribute('aria-hidden', 'true');
        figure.appendChild(live);
        added.push(live);
        var ls = state(live);
        var amounts = spec.drag.taken, dt = spec.drag.t;
        track(a, b, 'out', function (k) { ls.ty = 2.5 * (1 - k); ls.op = k; s.op = 0; });
        track(dt[0], dt[1], 'inout', function (k) { live.textContent = String(Math.round((amounts[0] + (amounts[1] - amounts[0]) * k) * 2) / 2); });
        track(dt[1] + 60, dt[1] + 300, 'lin', function (k) { ls.op *= 1 - k; s.op = k; });
      }
      if (p.ride && spec.drag) {
        /* the real right-hand handle, moved with the drag: pixel-true */
        track(spec.drag.t[0], spec.drag.t[1], 'inout', function (k) { s.ty = (spec.drag.from + (spec.drag.to - spec.drag.from) * k) - spec.drag.to; });
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

    (spec.rings || (spec.ring ? [spec.ring] : [])).forEach(function (spot) {
      var ring = document.createElement('span');
      ring.className = 'hiw-ring';
      ring.setAttribute('aria-hidden', 'true');
      ring.style.left = spot.c[0] + '%';
      ring.style.top = spot.c[1] + '%';
      ring.style.width = spot.w + '%';
      figure.appendChild(ring);
      added.push(ring);
      var rs = state(ring, 'translate(-50%, -50%)');
      track(spot.t[0], spot.t[1], 'out', function (k) {
        rs.sc = 1 + 0.45 * k;
        rs.op = k <= 0 || k >= 1 ? 0 : 0.95 * (1 - k);
      });
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
    if (spec.drag) {
      var d = spec.drag, t0 = d.t[0], t1 = d.t[1];
      var level = function (k) { return d.from + (d.to - d.from) * k; };
      var fadeOut = function (s) { track(t1, t1 + 220, 'lin', function (k) { s.op *= 1 - k; }); };
      /* The "2 oz left" marker travels with the handle in the app; here it is held back behind a patch of
         the bottle's own interior until the drag ends, then it appears. */
      var tip = drawn('hiw-tipcover', figure, 3);
      var ts = state(tip);
      track(d.show[0], d.show[1], 'out', function (k) { ts.op = k; });
      fadeOut(ts);
      var band = drawn('hiw-band', figure, 3);
      band.style.left = d.band[0] + '%'; band.style.width = (d.band[1] - d.band[0]) + '%';
      band.style.top = d.band[2] + '%'; band.style.height = (d.band[3] - d.band[2]) + '%';
      var bs = state(band);
      track(d.show[0], d.show[1], 'out', function (k) { bs.op = k; });
      track(t0, t1, 'inout', function (k) {
        band.style.clipPath = 'inset(' + ((level(k) - d.band[2]) / (d.band[3] - d.band[2]) * 100).toFixed(3) + '% 0 0 0)';
      });
      fadeOut(bs);
      d.hx.slice(0, 1).forEach(function (x) {
        var handle = drawn('hiw-handle', figure, 4);
        handle.style.left = x + '%';
        var hs = state(handle, 'translate(-50%, -50%)');
        track(d.show[0] + 200, d.show[1], 'out', function (k) { hs.op = k; });
        track(t0, t1, 'inout', function (k) { handle.style.top = level(k) + '%'; });
        fadeOut(hs);
      });
      var finger = drawn('hiw-finger', figure, 5);
      finger.style.left = d.hx[1] + '%';
      var fs = state(finger, 'translate(-50%, -50%)');
      track(t0 - 300, t0, 'out', function (k) { fs.op = k * 0.9; fs.sc = 1.5 - 0.5 * k; });
      track(t0, t1, 'inout', function (k) { finger.style.top = level(k) + '%'; });
      track(t1, t1 + 260, 'lin', function (k) { fs.op *= 1 - k; });
      var callout = device.querySelector('.hiw-callout');
      if (callout) {
        var cs = state(callout);
        var line = callout.querySelector('.hiw-callout-line');
        track(t1 - 250, t1 + 350, 'out', function (k) { cs.op = k; if (line) line.style.transform = 'scaleX(' + k.toFixed(3) + ')'; });
      }
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
      /* half-ounce steps, the app's own */
      track(spec.count.t[0], spec.count.t[1], 'quart', function (k) { count.textContent = String(Math.round((origin + (target - origin) * k) * 2) / 2); });
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
