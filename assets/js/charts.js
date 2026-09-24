// Interactive charts for the project pages. Plain SVG, no library.
// Each chart reads its data from a <script type="application/json"> next to it,
// so the numbers on the page are exactly the ones the analysis produced.

(function () {
    "use strict";

    var NS = 'http://www.w3.org/2000/svg';

    function el(name, attrs, parent) {
        var node = document.createElementNS(NS, name);
        for (var k in attrs) node.setAttribute(k, attrs[k]);
        if (parent) parent.appendChild(node);
        return node;
    }

    function readData(root) {
        var src = root.querySelector('script[type="application/json"]');
        return src ? JSON.parse(src.textContent) : null;
    }

    function niceMax(v) {
        var p = Math.pow(10, Math.floor(Math.log10(v)));
        var n = v / p;
        var step = n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10;
        return step * p;
    }

    function tooltip(root) {
        var tip = document.createElement('div');
        tip.className = 'chart-tip';
        tip.setAttribute('role', 'status');
        tip.hidden = true;
        root.querySelector('.chart-canvas').appendChild(tip);
        return {
            show: function (html, x, y) {
                tip.innerHTML = html;
                tip.hidden = false;
                var box = root.querySelector('.chart-canvas').getBoundingClientRect();
                var w = tip.offsetWidth;
                var left = Math.min(Math.max(x - w / 2, 4), box.width - w - 4);
                tip.style.left = left + 'px';
                tip.style.top = Math.max(y - tip.offsetHeight - 12, 4) + 'px';
            },
            hide: function () { tip.hidden = true; }
        };
    }

    function segmented(root, onChange) {
        var buttons = root.querySelectorAll('[data-metric]');
        buttons.forEach(function (b) {
            b.addEventListener('click', function () {
                buttons.forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
                onChange(b.getAttribute('data-metric'));
            });
        });
    }

    // ------------------------------------------------------------------ bar chart

    function barChart(root) {
        var data = readData(root);
        var metrics = JSON.parse(root.getAttribute('data-metrics'));
        var canvas = root.querySelector('.chart-canvas');
        var tip = tooltip(root);
        var metric = metrics[0].key;
        var rowH = 30, labelW = 170, padR = 70, top = 8;

        var svg = el('svg', { class: 'chart-svg', role: 'img' }, canvas);
        var gridG = el('g', { class: 'grid' }, svg);
        var barsG = el('g', {}, svg);

        var rows = data.map(function (d, i) {
            var g = el('g', { class: 'bar-row', tabindex: '0' }, barsG);
            var label = el('text', { class: 'bar-label', x: labelW - 12, 'text-anchor': 'end', 'dominant-baseline': 'middle' }, g);
            label.textContent = d.label;
            var rect = el('rect', { class: 'bar', x: labelW, height: rowH - 10, rx: 3 }, g);
            var val = el('text', { class: 'bar-value', 'dominant-baseline': 'middle' }, g);
            return { d: d, g: g, rect: rect, val: val, label: label };
        });

        function fmt(m, v) {
            var def = metrics.filter(function (x) { return x.key === m; })[0];
            var s = def.decimals ? v.toLocaleString('en-NZ', { minimumFractionDigits: def.decimals, maximumFractionDigits: def.decimals })
                : Math.round(v).toLocaleString('en-NZ');
            return (def.prefix || '') + s + (def.suffix || '');
        }

        function draw() {
            var width = canvas.clientWidth;
            var narrow = width < 520;
            labelW = narrow ? 118 : 170;
            var plotW = Math.max(width - labelW - padR, 60);
            var height = top + rows.length * rowH + 22;
            svg.setAttribute('viewBox', '0 0 ' + width + ' ' + height);
            svg.setAttribute('height', height);

            var sorted = rows.slice().sort(function (a, b) { return b.d[metric] - a.d[metric]; });
            var max = niceMax(sorted[0].d[metric]);
            var def = metrics.filter(function (x) { return x.key === metric; })[0];
            svg.setAttribute('aria-label', def.label + ' by region, 2025. Highest: ' + sorted[0].d.label + ', ' + fmt(metric, sorted[0].d[metric]) + '.');

            while (gridG.firstChild) gridG.removeChild(gridG.firstChild);
            for (var t = 0; t <= 4; t++) {
                var gx = labelW + plotW * t / 4;
                el('line', { x1: gx, x2: gx, y1: top - 4, y2: height - 20 }, gridG);
                var tl = el('text', { x: gx, y: height - 4, 'text-anchor': 'middle', class: 'axis' }, gridG);
                tl.textContent = fmt(metric, max * t / 4).replace(/\.0+(?=\D*$)/, '');
            }

            // Optional target line (e.g. a 2% return-rate target): bars past it are highlighted.
            var oldLine = svg.querySelector('.target-line');
            if (oldLine) oldLine.parentNode.removeChild(oldLine);
            var oldLabel = svg.querySelector('.target-label');
            if (oldLabel) oldLabel.parentNode.removeChild(oldLabel);
            if (def.threshold != null) {
                var tx = labelW + plotW * def.threshold / max;
                el('line', { x1: tx, x2: tx, y1: top - 4, y2: height - 20, class: 'target-line' }, svg);
                var tlab = el('text', { x: tx + 5, y: top + 6, class: 'target-label' }, svg);
                tlab.textContent = fmt(metric, def.threshold) + ' target';
            }

            sorted.forEach(function (r, i) {
                var y = top + i * rowH;
                var w = Math.max(plotW * r.d[metric] / max, 1.5);
                r.g.classList.toggle('over', def.threshold != null && r.d[metric] > def.threshold);
                r.g.style.transform = 'translateY(' + y + 'px)';
                r.rect.setAttribute('y', 5);
                r.rect.setAttribute('width', w);
                r.rect.style.width = w + 'px';
                r.label.setAttribute('y', rowH / 2);
                r.label.setAttribute('x', labelW - 10);
                r.label.textContent = narrow ? r.d.short || r.d.label : r.d.label;
                r.val.setAttribute('x', labelW + w + 8);
                r.val.setAttribute('y', rowH / 2);
                r.val.textContent = fmt(metric, r.d[metric]);
                r.g.classList.toggle('lead', i === 0 && def.threshold == null);
                r.g.setAttribute('aria-label', r.d.label + ': ' + fmt(metric, r.d[metric]) + ', rank ' + (i + 1));
            });
        }

        rows.forEach(function (r) {
            function show() {
                var box = r.rect.getBoundingClientRect();
                var cbox = canvas.getBoundingClientRect();
                var html = '<strong>' + r.d.label + '</strong>' + metrics.map(function (m) {
                    return '<span' + (m.key === metric ? ' class="on"' : '') + '>' + m.label + '<b>' + fmt(m.key, r.d[m.key]) + '</b></span>';
                }).join('');
                tip.show(html, box.left - cbox.left + box.width / 2, box.top - cbox.top);
            }
            r.g.addEventListener('mouseenter', show);
            r.g.addEventListener('focus', show);
            r.g.addEventListener('mouseleave', tip.hide);
            r.g.addEventListener('blur', tip.hide);
        });

        segmented(root, function (m) { metric = m; tip.hide(); draw(); });
        draw();
        if (window.ResizeObserver) new ResizeObserver(draw).observe(canvas);
        else window.addEventListener('resize', draw);
    }

    // ------------------------------------------------------------------ line chart

    function lineChart(root) {
        var data = readData(root);
        var canvas = root.querySelector('.chart-canvas');
        var tip = tooltip(root);
        var metric = 'rent';
        var names = Object.keys(data.series);
        var selected = JSON.parse(root.getAttribute('data-default'));
        var palette = ['var(--c1)', 'var(--c2)', 'var(--c3)', 'var(--c4)', 'var(--c5)'];
        var chips = root.querySelector('.chips');
        var legend = {};

        names.forEach(function (n) {
            var b = document.createElement('button');
            b.type = 'button';
            b.className = 'chip-btn';
            b.textContent = n;
            b.setAttribute('aria-pressed', selected.indexOf(n) > -1 ? 'true' : 'false');
            b.addEventListener('click', function () {
                var i = selected.indexOf(n);
                if (i > -1) {
                    if (selected.length === 1) return;
                    selected.splice(i, 1);
                } else {
                    if (selected.length >= 5) selected.shift();
                    selected.push(n);
                }
                names.forEach(function (m) { legend[m].setAttribute('aria-pressed', selected.indexOf(m) > -1 ? 'true' : 'false'); });
                draw();
            });
            legend[n] = b;
            chips.appendChild(b);
        });

        var svg = el('svg', { class: 'chart-svg', role: 'img' }, canvas);
        var pad = { l: 52, r: 16, t: 14, b: 30 };
        var height = 340;
        var hoverLine, dotsG;

        function yLabel(v) {
            return metric === 'rent' ? '$' + v : v + '%';
        }

        function draw() {
            var width = canvas.clientWidth;
            height = width < 520 ? 260 : 340;
            svg.setAttribute('viewBox', '0 0 ' + width + ' ' + height);
            svg.setAttribute('height', height);
            while (svg.firstChild) svg.removeChild(svg.firstChild);

            var qs = data.quarters;
            var all = [];
            selected.forEach(function (n) { data.series[n][metric].forEach(function (v) { if (v != null) all.push(v); }); });
            var lo = Math.min.apply(null, all), hi = Math.max.apply(null, all);
            if (metric === 'ratio') { lo = Math.min(lo, 30); hi = Math.max(hi, 30); }
            // Round axis: pick a tidy step (1, 2, 2.5, 5 × 10ⁿ) giving about four intervals.
            var raw = (hi - lo || 1) / 4;
            var mag = Math.pow(10, Math.floor(Math.log10(raw)));
            var step = [1, 2, 2.5, 5, 10].map(function (m) { return m * mag; }).filter(function (s) { return s >= raw; })[0];
            lo = Math.floor(lo / step) * step;
            hi = Math.ceil(hi / step) * step;

            var pw = width - pad.l - pad.r, ph = height - pad.t - pad.b;
            function x(i) { return pad.l + pw * i / (qs.length - 1); }
            function y(v) { return pad.t + ph * (1 - (v - lo) / (hi - lo)); }

            var grid = el('g', { class: 'grid' }, svg);
            for (var v = lo; v <= hi + step / 2; v += step) {
                var gy = y(v);
                el('line', { x1: pad.l, x2: width - pad.r, y1: gy, y2: gy }, grid);
                var tl = el('text', { x: pad.l - 8, y: gy, 'text-anchor': 'end', 'dominant-baseline': 'middle', class: 'axis' }, grid);
                tl.textContent = yLabel(Math.round(v * 10) / 10);
            }
            qs.forEach(function (q, i) {
                if (q.slice(5) === 'Q1') {
                    var yl = el('text', { x: x(i), y: height - 8, 'text-anchor': 'middle', class: 'axis' }, grid);
                    yl.textContent = q.slice(0, 4);
                }
            });

            if (metric === 'ratio') {
                var ty = y(30);
                el('line', { x1: pad.l, x2: width - pad.r, y1: ty, y2: ty, class: 'threshold' }, svg);
                var tt = el('text', { x: width - pad.r, y: ty - 6, 'text-anchor': 'end', class: 'threshold-label' }, svg);
                tt.textContent = '30% affordability threshold';
            }

            selected.forEach(function (n, si) {
                var pts = data.series[n][metric];
                var d = '';
                pts.forEach(function (v, i) { if (v != null) d += (d ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1); });
                var path = el('path', { d: d, class: 'line', style: 'stroke:' + palette[si] }, svg);
                var len = path.getTotalLength ? path.getTotalLength() : 0;
                if (len && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                    path.style.strokeDasharray = len;
                    path.style.strokeDashoffset = len;
                    path.getBoundingClientRect();
                    path.style.transition = 'stroke-dashoffset 0.9s cubic-bezier(0.2, 0.7, 0.2, 1)';
                    path.style.strokeDashoffset = 0;
                }
                var last = pts.length - 1;
                el('circle', { cx: x(last), cy: y(pts[last]), r: 3.5, class: 'end-dot', style: 'fill:' + palette[si] }, svg);
                legend[n].style.setProperty('--dot', palette[si]);
            });
            names.forEach(function (n) { if (selected.indexOf(n) < 0) legend[n].style.removeProperty('--dot'); });

            hoverLine = el('line', { y1: pad.t, y2: height - pad.b, class: 'hover-line', visibility: 'hidden' }, svg);
            dotsG = el('g', {}, svg);

            svg.setAttribute('aria-label', (metric === 'rent' ? 'Median weekly rent' : 'Rent as a share of median household income') +
                ', ' + qs[0] + ' to ' + qs[qs.length - 1] + ', for ' + selected.join(', ') + '.');

            var overlay = el('rect', { x: pad.l, y: pad.t, width: pw, height: ph, fill: 'transparent', class: 'overlay' }, svg);
            function move(clientX) {
                var box = svg.getBoundingClientRect();
                var px = (clientX - box.left) * (width / box.width);
                var i = Math.round((px - pad.l) / pw * (qs.length - 1));
                i = Math.max(0, Math.min(qs.length - 1, i));
                hoverLine.setAttribute('x1', x(i));
                hoverLine.setAttribute('x2', x(i));
                hoverLine.setAttribute('visibility', 'visible');
                while (dotsG.firstChild) dotsG.removeChild(dotsG.firstChild);
                var rowsHtml = selected.map(function (n, si) {
                    var v = data.series[n][metric][i];
                    el('circle', { cx: x(i), cy: y(v), r: 4.5, class: 'hover-dot', style: 'stroke:' + palette[si] }, dotsG);
                    return { n: n, v: v, c: palette[si] };
                }).sort(function (a, b) { return b.v - a.v; }).map(function (r) {
                    return '<span><i style="background:' + r.c + '"></i>' + r.n + '<b>' + yLabel(r.v) + (metric === 'rent' ? '/wk' : '') + '</b></span>';
                }).join('');
                var sx = x(i) * (box.width / width);
                tip.show('<strong>' + qs[i] + '</strong>' + rowsHtml, sx, pad.t);
            }
            overlay.addEventListener('mousemove', function (e) { move(e.clientX); });
            overlay.addEventListener('touchstart', function (e) { move(e.touches[0].clientX); }, { passive: true });
            overlay.addEventListener('touchmove', function (e) { move(e.touches[0].clientX); }, { passive: true });
            overlay.addEventListener('mouseleave', function () {
                tip.hide();
                hoverLine.setAttribute('visibility', 'hidden');
                while (dotsG.firstChild) dotsG.removeChild(dotsG.firstChild);
            });
        }

        segmented(root, function (m) { metric = m; tip.hide(); draw(); });
        draw();
        var lastW = canvas.clientWidth;
        if (window.ResizeObserver) new ResizeObserver(function () {
            if (canvas.clientWidth !== lastW) { lastW = canvas.clientWidth; draw(); }
        }).observe(canvas);
    }

    document.querySelectorAll('.chart[data-chart="bar"]').forEach(barChart);
    document.querySelectorAll('.chart[data-chart="line"]').forEach(lineChart);
})();
