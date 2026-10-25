(function () {
  'use strict';
  var L = JSON.parse(document.getElementById('i18n').textContent);
  var $ = function (id) { return document.getElementById(id); };
  var PI = Math.PI, CX = 220, CY = 220, R = 150, EPS = 1e-9;
  var inp = $('ang'), svg = $('svg');
  var nf = new Intl.NumberFormat(L.locale, { maximumFractionDigits: 4 });
  /* aperto dal computer (file://): il browser non apre da solo index.html dentro le cartelle */
  if (location.protocol === 'file:') {
    var fixHref = function (h) { return /^(\.\.?\/)*[a-z]{0,2}\/?$/.test(h) && /\/$/.test(h) ? h + 'index.html' : h; };
    Array.prototype.forEach.call(document.querySelectorAll('a[href]'), function (el) {
      el.setAttribute('href', fixHref(el.getAttribute('href')));
    });
    Object.keys(L.langs).forEach(function (k) { L.langs[k] = fixHref(L.langs[k]); });
  }
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function fmt(n) { if (Math.abs(n) < 5e-5) n = 0; return nf.format(n).replace('-', '\u2212'); }
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a || 1; }

  function parse(raw) {
    var s = String(raw).trim().replace(/,/g, '.').replace(/[\u2212\u2013]/g, '-').replace(/\u00d7/g, '*').replace(/[\u00f7:]/g, '/');
    var deg = false;
    if (/(\u00b0|\u00ba|deg|gradi|grad|grados|graus|degr\u00e9s)$/i.test(s)) { deg = true; s = s.replace(/(\u00b0|\u00ba|deg|gradi|grad|grados|graus|degr\u00e9s)$/i, ''); }
    var t = s.replace(/pi|\u03c0/gi, 'P');
    if (!t.trim() || !/^[0-9P+\-*/(). ]+$/.test(t)) return null;
    if (deg && /P/.test(t)) return null;
    t = t.replace(/(\d|\)|P)\s*(?=P|\()/g, '$1*').replace(/P\s*(?=\d)/g, 'P*').replace(/\)\s*(?=\d)/g, ')*').replace(/P/g, '(' + PI + ')');
    var v;
    try { v = Function('"use strict";return (' + t + ')')(); } catch (e) { return null; }
    if (typeof v !== 'number' || !isFinite(v) || Math.abs(v) > 1e6) return null;
    return { a: deg ? v * PI / 180 : v, deg: deg };
  }

  function asPiFraction(a) {
    var r = a / PI;
    for (var d = 1; d <= 180; d++) {
      var k = Math.round(r * d);
      if (Math.abs(r * d - k) < 1e-8) { var g = gcd(k, d); return { k: k / g, d: d / g }; }
    }
    return null;
  }

  function frac(n, d) { return '<span class="frac"><span>' + n + '</span><span>' + d + '</span></span>'; }
  function root(n) { return '\u221a<span class="rad">' + n + '</span>'; }
  function piHTML(k, d) {
    if (k === 0) return '0';
    var sign = k < 0 ? '<span class="sign">\u2212</span>' : '';
    var num = (Math.abs(k) === 1 ? '' : Math.abs(k)) + '\u03c0';
    return '<span class="ex">' + sign + (d === 1 ? num : frac(num, d)) + '</span>';
  }
  function piText(k, d) {
    if (k === 0) return '0';
    var num = (Math.abs(k) === 1 ? '' : Math.abs(k)) + '\u03c0';
    return (k < 0 ? '\u2212' : '') + (d === 1 ? num : num + '/' + d);
  }

  var S2 = Math.SQRT2, S3 = Math.sqrt(3), S6 = Math.sqrt(6);
  var EXACT = [[0, '0'], [1, '1'], [0.5, frac('1', '2')], [S2 / 2, frac(root(2), '2')], [S3 / 2, frac(root(3), '2')],
    [(S6 - S2) / 4, frac(root(6) + ' \u2212 ' + root(2), '4')], [(S6 + S2) / 4, frac(root(6) + ' + ' + root(2), '4')]];
  var EXACT_TAN = [[0, '0'], [1, '1'], [S3, root(3)], [S3 / 3, frac(root(3), '3')], [2 - S3, '2 \u2212 ' + root(3)], [2 + S3, '2 + ' + root(3)]];

  function exact(v, table) {
    var m = Math.abs(v);
    for (var i = 0; i < table.length; i++) {
      if (Math.abs(m - table[i][0]) < 1e-9) {
        if (table[i][0] === 0) return '0';
        return '<span class="ex">' + (v < 0 ? '<span class="sign">\u2212</span>' : '') + table[i][1] + '</span>';
      }
    }
    return null;
  }
  function valueHTML(v, table, known) {
    var e = known ? exact(v, table) : null;
    if (e !== null) {
      var isInt = Math.abs(Math.abs(v) - Math.round(Math.abs(v))) < EPS;
      return e + (isInt ? '' : '<span class="d">\u2248 ' + fmt(v) + '</span>');
    }
    return '<span>' + (Math.abs(v) < 5e-5 ? '0' : '\u2248 ' + fmt(v)) + '</span>';
  }

  /* ticks for the special angles */
  var ticks = [];
  (function () {
    var list = [];
    for (var i = 0; i < 12; i++) { var g = gcd(i, 6); list.push([i / g, 6 / g]); }
    [1, 3, 5, 7].forEach(function (k) { list.push([k, 4]); });
    var NS = 'http://www.w3.org/2000/svg', box = $('ticks');
    list.forEach(function (n) {
      var a = n[0] * PI / n[1];
      var g = document.createElementNS(NS, 'g'); g.setAttribute('class', 'tick');
      var c = document.createElementNS(NS, 'circle');
      c.setAttribute('cx', CX + R * Math.cos(a)); c.setAttribute('cy', CY - R * Math.sin(a)); c.setAttribute('r', 4);
      var t = document.createElementNS(NS, 'text');
      t.setAttribute('x', CX + (R + 27) * Math.cos(a)); t.setAttribute('y', CY - (R + 27) * Math.sin(a) + 4.5);
      t.setAttribute('text-anchor', 'middle'); t.textContent = piText(n[0], n[1]);
      g.appendChild(c); g.appendChild(t); box.appendChild(g);
      ticks.push({ el: g, a: a });
    });
  })();

  function set(id, o) { var el = $(id); for (var k in o) el.setAttribute(k, o[k]); }
  function drawAt(a) {
    var c = Math.cos(a), s = Math.sin(a), px = CX + R * c, py = CY - R * s;
    set('radL', { x1: CX, y1: CY, x2: px, y2: py });
    set('cosL', { x1: CX, y1: CY, x2: px, y2: CY });
    set('sinL', { x1: px, y1: CY, x2: px, y2: py });
    set('dash', { x1: CX, y1: py, x2: px, y2: py });
    set('pt', { cx: px, cy: py });
    var ar = 34, neg = a < 0, full = Math.abs(a), sweep = full % (2 * PI);
    if (full > EPS && sweep < 1e-6) sweep = 2 * PI - 1e-4;
    if (sweep < 1e-6) { $('arc').setAttribute('d', ''); return; }
    var end = neg ? -sweep : sweep;
    $('arc').setAttribute('d', 'M ' + (CX + ar) + ' ' + CY + ' A ' + ar + ' ' + ar + ' 0 ' + (sweep > PI ? 1 : 0) + ' ' + (neg ? 1 : 0) + ' ' +
      (CX + ar * Math.cos(end)) + ' ' + (CY - ar * Math.sin(end)));
  }

  var current = 0, target = 0, raf = null;
  function moveTo(a, instant) {
    if (raf) cancelAnimationFrame(raf);
    target = a;
    if (instant || reduce) { current = a; drawAt(a); return; }
    var from = current;
    if (Math.abs(a - from) > 4 * PI) from = a - Math.sign(a - from) * 4 * PI;
    var t0 = performance.now(), dur = 500;
    (function step(now) {
      var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      current = from + (a - from) * e; drawAt(current);
      if (p < 1) raf = requestAnimationFrame(step);
    })(t0);
  }

  function updateUrl() {
    try {
      var u = new URL(location.href);
      u.searchParams.set('a', inp.value.trim());
      history.replaceState(null, '', u.toString());
    } catch (e) { }
  }

  function chip(html) { return '<li>' + html + '</li>'; }

  function go(opts) {
    opts = opts || {};
    var p = parse(inp.value);
    if (!p) { $('err').textContent = L.err; return; }
    $('err').textContent = '';
    var a = p.a, pf = asPiFraction(a), known = !!pf && 12 % pf.d === 0;
    var c = Math.cos(a), s = Math.sin(a), degs = a * 180 / PI;

    $('angOut').innerHTML = '<span>\u03b8 =</span> ' + (pf ? piHTML(pf.k, pf.d) : (p.deg ? fmt(degs) + '\u00b0' : fmt(a) + ' rad'));

    var chips = [];
    if (pf || !p.deg) chips.push(chip('<span class="m">' + fmt(degs) + '\u00b0</span>'));
    if (!pf) chips.push(chip('<span class="m">\u2248 ' + (p.deg ? fmt(a) + ' rad' : fmt(a / PI) + '\u03c0') + '</span>'));
    if (pf) {
      var d2 = 2 * pf.d, kr = ((pf.k % d2) + d2) % d2;
      if (kr !== pf.k) { var g = gcd(kr, pf.d); chips.push(chip(L.equiv + ' <span class="m">' + piText(kr / g, pf.d / g) + '</span>')); }
    } else {
      var nr = ((a % (2 * PI)) + 2 * PI) % (2 * PI);
      if (Math.abs(nr - a) > 1e-6) chips.push(chip(L.equiv + ' <span class="m">' + (p.deg ? fmt(nr * 180 / PI) + '\u00b0' : fmt(nr) + ' rad') + '</span>'));
    }
    var nd = ((degs % 360) + 360) % 360;
    var onAxis = [0, 90, 180, 270, 360].some(function (x) { return Math.abs(nd - x) < 1e-7; });
    chips.push(chip(onAxis ? L.axes : L.quadrants[Math.floor(nd / 90) % 4]));
    $('chips').innerHTML = chips.join('');

    $('cosOut').innerHTML = valueHTML(c, EXACT, known);
    $('sinOut').innerHTML = valueHTML(s, EXACT, known);
    $('tanOut').innerHTML = Math.abs(c) < 1e-12 ? '<span class="d">' + L.undef + '</span>' : valueHTML(s / c, EXACT_TAN, known);

    ticks.forEach(function (t) {
      t.el.classList.toggle('on', Math.abs(Math.cos(t.a) - c) < 1e-9 && Math.abs(Math.sin(t.a) - s) < 1e-9);
    });
    moveTo(a, opts.instant);
    if (!opts.noUrl) updateUrl();
  }

  /* dragging the point */
  var dragging = false;
  function svgPoint(e) {
    var pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
    return pt.matrixTransform(svg.getScreenCTM().inverse());
  }
  function setFromPointer(e) {
    var p = svgPoint(e), a = Math.atan2(CY - p.y, p.x - CX);
    if (a < 0) a += 2 * PI;
    var step = PI / 12, k = Math.round(a / step), txt;
    if (Math.abs(a - k * step) < 4 * PI / 180) { k = k % 24; var g = gcd(k, 12); txt = piText(k / g, 12 / g); }
    else txt = Math.round(a * 180 / PI) + '\u00b0';
    if (txt !== inp.value) { inp.value = txt; go({ instant: true, noUrl: true }); }
  }
  svg.addEventListener('pointerdown', function (e) {
    var p = svgPoint(e);
    if (Math.hypot(p.x - CX, p.y - CY) < 18) return;
    dragging = true;
    try { svg.setPointerCapture(e.pointerId); } catch (x) { }
    if (document.activeElement === inp) inp.blur();
    setFromPointer(e); e.preventDefault();
  });
  svg.addEventListener('pointermove', function (e) { if (dragging) setFromPointer(e); });
  function endDrag() { if (dragging) { dragging = false; updateUrl(); } }
  svg.addEventListener('pointerup', endDrag);
  svg.addEventListener('pointercancel', endDrag);
  svg.addEventListener('keydown', function (e) {
    var dir = (e.key === 'ArrowRight' || e.key === 'ArrowUp') ? 1 : (e.key === 'ArrowLeft' || e.key === 'ArrowDown') ? -1 : 0;
    if (!dir) return;
    e.preventDefault();
    var k = Math.round(target / (PI / 12)) + dir, g = gcd(k, 12);
    inp.value = piText(k / g, 12 / g); go();
  });

  /* input, keypad, copy */
  $('show').addEventListener('click', function () { go(); });
  inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); go(); } });
  inp.addEventListener('input', function () { $('err').textContent = ''; });
  Array.prototype.forEach.call(document.querySelectorAll('[data-ins]'), function (b) {
    b.addEventListener('click', function () {
      var ins = b.getAttribute('data-ins');
      var st = inp.selectionStart == null ? inp.value.length : inp.selectionStart;
      var en = inp.selectionEnd == null ? st : inp.selectionEnd;
      inp.value = inp.value.slice(0, st) + ins + inp.value.slice(en);
      inp.focus(); inp.setSelectionRange(st + ins.length, st + ins.length);
      $('err').textContent = '';
    });
  });
  var copyBtn = $('copy'), copyLabel = copyBtn.textContent;
  copyBtn.addEventListener('click', function () {
    updateUrl();
    var url = location.href;
    var done = function () { copyBtn.textContent = L.copied; setTimeout(function () { copyBtn.textContent = copyLabel; }, 1800); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(done, function () { if (navigator.share) navigator.share({ url: url }).catch(function () { }); });
    } else if (navigator.share) { navigator.share({ url: url }).catch(function () { }); }
    else { window.prompt('', url); }
  });

  /* rows of the table jump to the tool */
  Array.prototype.forEach.call(document.querySelectorAll('a[data-a]'), function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      inp.value = link.getAttribute('data-a'); go();
      $('tool').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    });
  });

  /* language selector and suggestion */
  var sel = $('langSel');
  sel.addEventListener('change', function () {
    try { localStorage.setItem('ucLang', sel.value); } catch (e) { }
    var href = L.langs[sel.value];
    var q = inp.value.trim();
    location.href = href + (q ? '?a=' + encodeURIComponent(q) : '');
  });
  Array.prototype.forEach.call(document.querySelectorAll('footer a[hreflang]'), function (link) {
    link.addEventListener('click', function () { try { localStorage.setItem('ucLang', link.getAttribute('hreflang')); } catch (e) { } });
  });
  try {
    var chosen = localStorage.getItem('ucLang');
    var prefs = (navigator.languages || [navigator.language || '']).map(function (l) { return String(l).slice(0, 2).toLowerCase(); });
    var best = null;
    for (var i = 0; i < prefs.length; i++) { if (L.langs[prefs[i]]) { best = prefs[i]; break; } }
    if (!chosen && best && best !== L.lang) {
      var box = $('suggest');
      box.innerHTML = '<span>' + L.suggest[best].text + '</span> <a href="' + L.langs[best] + '" lang="' + best + '">' + L.suggest[best].link + '</a>' +
        '<button type="button" aria-label="' + L.close + '">\u00d7</button>';
      box.hidden = false;
      box.querySelector('a').addEventListener('click', function () { try { localStorage.setItem('ucLang', best); } catch (e) { } });
      box.querySelector('button').addEventListener('click', function () {
        box.hidden = true; try { localStorage.setItem('ucLang', L.lang); } catch (e) { }
      });
    }
  } catch (e) { }

  /* start */
  var q = null;
  try { q = new URLSearchParams(location.search).get('a'); } catch (e) { }
  if (q) inp.value = q;
  go({ noUrl: !q });
})();
