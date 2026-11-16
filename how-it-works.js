/* Home page "How logging works": each phone plays once when it scrolls into view,
   steps chained (a phone starts as the one before it lands). The HTML is the final state,
   so with JS off or prefers-reduced-motion nothing moves and everything is shown.
   The cards below the steps each play on their own when they scroll into view.
   ?hiwdemo=0..100 pins every sequence at that percent of its timeline (for screenshots);
   add &hiwcards=0..100 to pin the cards at a different percent from the three steps. */
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
      duration: 2900,
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
    log: {
      duration: 4900,
      pieces: [
        { r: [3.5, 13.8, 96.5, 19.3], a: 'slide', t: [450, 900] },
        { r: [37.5, 19.6, 62.5, 31.2], a: 'sweep', t: [700, 1650], c: [50, 25.4] },
        { r: [12, 22, 37, 29], a: 'up', t: [800, 1100] },
        { r: [64.5, 22, 86.5, 29], a: 'up', t: [900, 1200] },
        { r: [27, 34, 74, 81.5], hole: [30.5, 57.5, 73.6, 80.5], a: 'fade', t: [1050, 1450], f: [12, 5] },
        { r: [30.5, 57.5, 68.9, 80.5], a: 'rise', t: [1300, 2050], f: [4, 1.8, 0.01] },
        { r: [68.9, 70, 73.6, 73.6], a: 'fade', t: [1700, 2050], f: [0.2, 0.7, 0.7], ride: true },
        { r: [15, 68.5, 26, 75.5], a: 'fade', t: [1900, 2200] },
        { r: [74, 68.5, 85, 75.5], a: 'fade', t: [1900, 2200], f: [0.4, 1.8, 4] },
        { r: [30, 82.5, 45.1, 87.2], a: 'up', t: [1850, 2200], f: [4, 1.8, 0.01], taken: true },
        { r: [45.1, 82.5, 70, 87.2], a: 'up', t: [1850, 2200], f: [0.01, 1.8, 4] },
        { r: [3.5, 87.4, 49.6, 93.9], a: 'up', t: [2000, 2350] },
        { r: [50.2, 87.4, 96.5, 93.9], a: 'up', t: [2000, 2350], press: [3450, 3750], origin: [73.3, 90.6] }
      ],
      /* The bottle starts at 4 oz and the handle is dragged down to the screenshot's own 2 oz.
         The screenshot cannot move its own level, so a drawn milk band, two drawn handles and a
         fingertip dot play the drag on top of it; at the end they swap for the real ones. */
      drag: { t: [2500, 3350], from: 63.8, to: 71.76, band: [31.35, 68.9, 63.8, 73.1], hx: [39.2, 71], show: [1500, 2050], taken: [1.5, 3.5] },
      sparks: { t: [3660, 4890], c: [73.3, 90.6] }
    },
    finish: {
            duration: 3550,
      pieces: [
        { r: [3, 6.3, 97, 17.2], a: 'fade', t: [400, 750] },
        { r: [55, 17.3, 97, 22.8], a: 'fade', t: [550, 850] },
        { r: [2, 24.5, 25, 28.3], a: 'fade', t: [600, 900] },
        { r: [4, 57.5, 97, 63.4], a: 'drop', t: [750, 1100] },
        { r: [4, 54, 60, 57.2], a: 'fade', t: [950, 1200] },
        { r: [4, 48, 97, 53.7], a: 'drop', t: [1050, 1400] },
        { r: [4, 44.3, 60, 47.4], a: 'fade', t: [1250, 1500] },
        { r: [4, 38.2, 97, 44], a: 'drop', t: [1350, 1700] },
        { r: [4, 34.5, 60, 37.7], a: 'fade', t: [1550, 1800] },
        { r: [4, 28.5, 97, 34.3], a: 'drop', t: [1700, 2150], lift: 9 },
        { r: [2.5, 18.8, 56.3, 22.4], a: 'wipe', t: [2450, 3450], ease: 'quart' },
        { r: [0, 65, 100, 100], a: 'up', t: [2300, 2700] }
      ],
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
    function track(from, to, ease, apply) { tracks.push({ from: from, to: to, ease: EASE[ease] || EASE.out, apply: apply }); }
    function state(el, base) { var s = { el: el, op: 1, tx: 0, ty: 0, sc: 1, rot: 0, base: base || '' }; elements.push(s); return s; }

    var dev = state(device);
    track(0, 550, 'out', function (k) { dev.op = clamp(k * 1.6); dev.ty = -7 * (1 - k); });

    if (spec.scroll) {
      var header = layer(shot);
      header.style.clipPath = 'inset(0 0 ' + (100 - spec.scroll.header * 100) + '% 0)';
      header.style.zIndex = 2;
      figure.appendChild(header);
      var body = state(shot);
      var travel = spec.scroll.travel * 100;
      track(spec.scroll.down[0], spec.scroll.down[1], 'inout', function (k) { body.ty = -travel * k; });
      track(spec.scroll.back[0], spec.scroll.back[1], 'inout', function (k) { if (k > 0) body.ty = -travel * (1 - k); });
      return { duration: spec.duration, tracks: tracks, elements: elements, cleanup: function () { header.remove(); } };
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
      return { duration: spec.duration, tracks: tracks, elements: elements, cleanup: function () { elements.forEach(function (s) { s.base = ''; }); } };
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

    if (spec.ring) {
      var ring = document.createElement('span');
      ring.className = 'hiw-ring';
      ring.setAttribute('aria-hidden', 'true');
      ring.style.left = spec.ring.c[0] + '%';
      ring.style.top = spec.ring.c[1] + '%';
      ring.style.width = spec.ring.w + '%';
      figure.appendChild(ring);
      added.push(ring);
      var rs = state(ring, 'translate(-50%, -50%)');
      track(spec.ring.t[0], spec.ring.t[1], 'out', function (k) {
        rs.sc = 1 + 0.45 * k;
        rs.op = k <= 0 || k >= 1 ? 0 : 0.95 * (1 - k);
      });
    }

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
      track(spec.count.t[0], spec.count.t[1], 'quart', function (k) { count.textContent = String(Math.round(origin + (target - origin) * k)); });
    }

    return {
      duration: spec.duration, tracks: tracks, elements: elements,
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
  var OVERLAP = 250;

  sequences.forEach(function (seq) {
    var img = seq.figure.querySelector('.hiw-shot');
    Promise.all(Array.prototype.map.call(seq.figure.querySelectorAll('img'), loaded)).then(function () {
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
