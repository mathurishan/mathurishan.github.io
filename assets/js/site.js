// Ishan Mathur — portfolio. Small, dependency-free enhancements.

(function () {
    "use strict";

    // Hairline under the header once the page scrolls.
    var header = document.querySelector('.site-header');
    if (header) {
        var onScroll = function () {
            header.classList.toggle('scrolled', window.scrollY > 8);
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var root = document.documentElement;

    // Theme switch. Follows the device until the visitor chooses, then remembers.
    var toggle = document.querySelector('.theme-toggle');
    var darkQuery = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

    function currentTheme() {
        var set = root.getAttribute('data-theme');
        if (set === 'light' || set === 'dark') return set;
        return darkQuery && darkQuery.matches ? 'dark' : 'light';
    }

    function syncToggle() {
        var theme = currentTheme();
        if (toggle) {
            toggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
            toggle.setAttribute('title', theme === 'dark' ? 'Light theme' : 'Dark theme');
        }
        // Both the light and dark theme-color tags follow the chosen theme.
        document.querySelectorAll('meta[name="theme-color"]').forEach(function (meta) {
            meta.setAttribute('content', theme === 'dark' ? '#1a1917' : '#faf9f5');
        });
    }

    function applyTheme(theme) {
        root.setAttribute('data-theme', theme);
        try { localStorage.setItem('theme', theme); } catch (e) { /* private mode: still switches */ }
        syncToggle();
    }

    if (toggle) {
        syncToggle();
        if (darkQuery && darkQuery.addEventListener) darkQuery.addEventListener('change', syncToggle);

        toggle.addEventListener('click', function () {
            var next = currentTheme() === 'dark' ? 'light' : 'dark';

            if (calm) { applyTheme(next); return; }

            // Preferred: the new theme spreads out in a circle from the button.
            if (document.startViewTransition) {
                var box = toggle.getBoundingClientRect();
                var x = box.left + box.width / 2;
                var y = box.top + box.height / 2;
                var reach = Math.hypot(Math.max(x, window.innerWidth - x), Math.max(y, window.innerHeight - y));
                root.classList.add('theme-switching');
                var transition = document.startViewTransition(function () { applyTheme(next); });
                transition.finished.finally(function () { root.classList.remove('theme-switching'); });
                transition.ready.then(function () {
                    root.animate(
                        { clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + reach + 'px at ' + x + 'px ' + y + 'px)'] },
                        { duration: 700, easing: 'cubic-bezier(0.2, 0.7, 0.2, 1)', pseudoElement: '::view-transition-new(root)' }
                    );
                }).catch(function () { });
                return;
            }

            // Fallback: a short colour fade.
            root.classList.add('theme-fading');
            applyTheme(next);
            window.setTimeout(function () { root.classList.remove('theme-fading'); }, 500);
        });
    }

    // Sections rise into view as they reach the screen.
    var risers = document.querySelectorAll('.rise');
    if (!('IntersectionObserver' in window) || calm) {
        risers.forEach(function (el) { el.classList.add('in'); });
    } else {
        var seen = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in');
                    seen.unobserve(entry.target);
                }
            });
        }, { rootMargin: '0px 0px -8% 0px', threshold: 0 });
        risers.forEach(function (el) { seen.observe(el); });
    }

    // Key figures count up once, e.g. <b data-count="40" data-suffix="%">40%</b>.
    // Small whole numbers ("6 pages") just flicker, so only larger figures animate.
    var counters = Array.prototype.filter.call(document.querySelectorAll('[data-count]'), function (el) {
        return parseFloat(el.getAttribute('data-count')) >= 20;
    });
    function countUp(el) {
        var end = parseFloat(el.getAttribute('data-count'));
        var suffix = el.getAttribute('data-suffix') || '';
        var start = null;
        function frame(t) {
            if (start === null) start = t;
            var p = Math.min((t - start) / 1100, 1);
            var eased = 1 - Math.pow(1 - p, 3);
            el.textContent = Math.round(end * eased) + suffix;
            if (p < 1) requestAnimationFrame(frame);
        }
        requestAnimationFrame(frame);
    }
    if (counters.length && !calm && 'IntersectionObserver' in window) {
        var counted = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    countUp(entry.target);
                    counted.unobserve(entry.target);
                }
            });
        }, { threshold: 0.6 });
        counters.forEach(function (el) { counted.observe(el); });
    }

    // Copy email to the clipboard, with a small confirmation.
    var toast = null;
    function say(message) {
        if (!toast) {
            toast = document.createElement('div');
            toast.className = 'toast';
            toast.setAttribute('role', 'status');
            toast.setAttribute('aria-live', 'polite');
            document.body.appendChild(toast);
        }
        toast.innerHTML = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" ' +
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3.5 8.5 3 3 6-7"/></svg>' + message;
        toast.classList.add('show');
        clearTimeout(say.timer);
        say.timer = setTimeout(function () { toast.classList.remove('show'); }, 2200);
    }

    function legacyCopy(text) {
        var area = document.createElement('textarea');
        area.value = text;
        area.setAttribute('readonly', '');
        area.style.position = 'fixed';
        area.style.opacity = '0';
        document.body.appendChild(area);
        area.select();
        var ok = false;
        try { ok = document.execCommand('copy'); } catch (e) { /* ignore */ }
        document.body.removeChild(area);
        return ok;
    }

    // Resolves true when the text reached the clipboard, false when every method was refused.
    function copyText(text) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return legacyCopy(text); });
        }
        return Promise.resolve(legacyCopy(text));
    }

    document.querySelectorAll('[data-copy]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var text = btn.getAttribute('data-copy');
            copyText(text).then(function (ok) { say(ok ? 'Email copied' : text); });
        });
    });

    var finePointer = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    // Depth: a gentle tilt and a soft light that follows the cursor (mouse only, motion allowed).
    if (finePointer && !calm) {
        document.querySelectorAll('.feature .stage, .card .frame, .note-card').forEach(function (el) {
            el.classList.add('tilt', 'glow');
            var max = el.classList.contains('stage') ? 3 : 4;
            el.addEventListener('pointermove', function (e) {
                var r = el.getBoundingClientRect();
                var px = (e.clientX - r.left) / r.width;
                var py = (e.clientY - r.top) / r.height;
                el.classList.add('tilting');
                el.style.setProperty('--ry', ((px - 0.5) * max * 2).toFixed(2) + 'deg');
                el.style.setProperty('--rx', ((0.5 - py) * max * 2).toFixed(2) + 'deg');
                el.style.setProperty('--mx', (px * 100).toFixed(1) + '%');
                el.style.setProperty('--my', (py * 100).toFixed(1) + '%');
            });
            el.addEventListener('pointerleave', function () {
                el.classList.remove('tilting');
                el.style.setProperty('--rx', '0deg');
                el.style.setProperty('--ry', '0deg');
            });
        });

        // The two hero dashboards drift apart slightly as the page scrolls.
        var back = document.querySelector('.hero-visual .pane.back');
        var front = document.querySelector('.hero-visual .pane.front');
        if (back && front) {
            var drift = function () {
                var y = Math.min(window.scrollY, 700);
                back.style.translate = '0 ' + (-y * 0.05).toFixed(1) + 'px';
                front.style.translate = '0 ' + (y * 0.035).toFixed(1) + 'px';
            };
            window.addEventListener('scroll', function () { requestAnimationFrame(drift); }, { passive: true });
            drift();
        }
    }

    // Tools grid: highlight the column under the pointer (rows highlight in CSS).
    document.querySelectorAll('.matrix').forEach(function (table) {
        var clear = function () {
            table.querySelectorAll('.col-hover').forEach(function (c) { c.classList.remove('col-hover'); });
        };
        table.addEventListener('mouseover', function (e) {
            var cell = e.target.closest('[data-col]');
            clear();
            if (!cell) return;
            table.querySelectorAll('[data-col="' + cell.getAttribute('data-col') + '"]').forEach(function (c) {
                c.classList.add('col-hover');
            });
        });
        table.addEventListener('mouseleave', clear);
    });

    // Before-and-after slider.
    document.querySelectorAll('.ba').forEach(function (ba) {
        var range = ba.querySelector('input[type="range"]');
        var set = function () { ba.style.setProperty('--pos', range.value + '%'); };
        range.addEventListener('input', set);
        set();
    });

    // Quick search: Ctrl+K (or ⌘K) opens a palette of pages, sections and links.
    var ITEMS = [
        ['Home', './', 'Page'],
        ['Selected work', './#work', 'Home'],
        ['How I work', './#approach', 'Home'],
        ['About Ishan', 'about.html', 'Page'],
        ['Experience timeline', 'about.html#experience', 'About'],
        ['Where each tool shows up', 'about.html#tools', 'About'],
        ['Notes on reporting', 'notes.html', 'Page'],
        ['How I work', 'how-i-work.html', 'Page'],
        ['Contact', './#contact', 'Home'],
        ['Retail Sales & Returns Analysis', 'powerbi-retail.html', 'Power BI'],
        ['Retail DAX measures', 'powerbi-retail.html#dax', 'Power BI'],
        ['Air New Zealand Analysis', 'powerbi-air-nz.html', 'Power BI'],
        ['Air NZ route cancellations', 'powerbi-air-nz.html#explore', 'Power BI'],
        ['Air NZ DAX measures', 'powerbi-air-nz.html#dax', 'Power BI'],
        ['NZ Building Consents', 'sql-nz-building-consents.html', 'SQL'],
        ['Building consents SQL queries', 'sql-nz-building-consents.html#sql', 'SQL'],
        ['Star schema data model', 'sql-nz-building-consents.html#diagram', 'SQL'],
        ['NZ Housing Affordability', 'python_nz_housing_affordability.html', 'Python'],
        ['Rents by region chart', 'python_nz_housing_affordability.html#explore', 'Python'],
        ['NZ Business Financials', 'python_business_financials.html', 'Python'],
        ['One name for every system', 'note-one-name-for-every-system.html', 'Note'],
        ['A number needs a sentence', 'note-a-number-needs-a-sentence.html', 'Note'],
        ['Half a day to under an hour', 'note-half-a-day-to-under-an-hour.html', 'Note'],
        ['Validate before you visualise', 'note-validate-before-you-visualise.html', 'Note'],
        ['Why my reports start with a star schema', 'note-start-with-a-star-schema.html', 'Note'],
        ['Reading rent data honestly', 'note-reading-rent-data-honestly.html', 'Note'],
        ['Résumé', 'resume.html', 'Page'],
        ['Download résumé (PDF)', 'files/Ishan-Mathur-Resume.pdf', 'File'],
        ['Email Ishan', 'mailto:mathur.ishan11@gmail.com', 'Contact'],
        ['LinkedIn', 'https://www.linkedin.com/in/mathurishan', 'Contact'],
        ['GitHub', 'https://github.com/mathurishan', 'Contact']
    ];
    var palette = null, input, list, results = [], active = 0, returnFocus = null;

    function buildPalette() {
        palette = document.createElement('div');
        palette.className = 'palette';
        palette.setAttribute('role', 'dialog');
        palette.setAttribute('aria-modal', 'true');
        palette.setAttribute('aria-label', 'Search the site');
        palette.innerHTML = '<div class="palette-box"><input type="text" placeholder="Search projects, notes and sections" ' +
            'aria-label="Search" role="combobox" aria-expanded="true" aria-controls="palette-list" autocomplete="off" />' +
            '<ul id="palette-list" role="listbox"></ul>' +
            '<div class="palette-foot"><span>↑↓ to move</span><span>Enter to open</span><span>Esc to close</span></div></div>';
        document.body.appendChild(palette);
        input = palette.querySelector('input');
        list = palette.querySelector('ul');
        input.addEventListener('input', render);
        input.addEventListener('keydown', function (e) {
            if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
            else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
            else if (e.key === 'Enter' && results[active]) { e.preventDefault(); go(results[active][1]); }
            else if (e.key === 'Escape') { closePalette(); }
            else if (e.key === 'Tab') { e.preventDefault(); }
        });
        palette.addEventListener('click', function (e) { if (e.target === palette) closePalette(); });
    }

    function render() {
        var q = input.value.trim().toLowerCase();
        results = ITEMS.filter(function (it) {
            if (!q) return true;
            var hay = (it[0] + ' ' + it[2]).toLowerCase();
            return q.split(/\s+/).every(function (w) { return hay.indexOf(w) > -1; });
        });
        active = 0;
        list.innerHTML = results.length ? results.map(function (it, i) {
            return '<li role="presentation"><a role="option" id="pal-' + i + '" href="' + it[1] + '" aria-selected="' +
                (i === 0) + '">' + it[0] + '<span>' + it[2] + '</span></a></li>';
        }).join('') : '<li class="empty">No matches</li>';
        input.setAttribute('aria-activedescendant', results.length ? 'pal-0' : '');
        list.querySelectorAll('a').forEach(function (a, i) {
            a.addEventListener('mousemove', function () { select(i); });
            a.addEventListener('click', function (e) { e.preventDefault(); go(results[i][1]); });
        });
    }

    function select(i) {
        var links = list.querySelectorAll('a');
        if (!links.length) return;
        active = (i + links.length) % links.length;
        links.forEach(function (a, j) { a.setAttribute('aria-selected', j === active ? 'true' : 'false'); });
        links[active].scrollIntoView({ block: 'nearest' });
        input.setAttribute('aria-activedescendant', 'pal-' + active);
    }

    function move(n) { select(active + n); }

    function go(href) {
        closePalette();
        if (/^https?:/.test(href)) { window.open(href, '_blank', 'noopener'); return; }
        window.location.href = href;
    }

    function openPalette() {
        if (!palette) buildPalette();
        returnFocus = document.activeElement;
        input.value = '';
        render();
        palette.classList.add('open');
        document.body.classList.add('lightbox-open');
        input.focus();
    }

    function closePalette() {
        if (!palette) return;
        palette.classList.remove('open');
        document.body.classList.remove('lightbox-open');
        if (returnFocus && returnFocus.focus) returnFocus.focus();
    }

    var isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);
    document.querySelectorAll('[data-palette]').forEach(function (b) {
        var k = b.querySelector('kbd');
        if (k && isMac) k.textContent = '⌘K';
        b.addEventListener('click', openPalette);
    });
    document.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) {
            e.preventDefault();
            if (palette && palette.classList.contains('open')) closePalette(); else openPalette();
        }
    });

    // Phone menu: a full-screen sheet opened from the Menu button.
    var menuBtn = document.querySelector('.menu-btn');
    var sheet = document.getElementById('menu-sheet');
    if (menuBtn && sheet) {
        var setMenu = function (open) {
            menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
            menuBtn.querySelector('.menu-label').textContent = open ? 'Close' : 'Menu';
            document.body.classList.toggle('menu-open', open);
            if (open) {
                sheet.hidden = false;
                requestAnimationFrame(function () { sheet.classList.add('open'); });
                var first = sheet.querySelector('a');
                if (first) first.focus();
            } else {
                sheet.classList.remove('open');
                sheet.hidden = true;
            }
        };
        menuBtn.addEventListener('click', function () {
            setMenu(menuBtn.getAttribute('aria-expanded') !== 'true');
        });
        sheet.addEventListener('click', function (e) {
            if (e.target.closest('a, [data-palette]')) setMenu(false);
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && menuBtn.getAttribute('aria-expanded') === 'true') {
                setMenu(false);
                menuBtn.focus();
            }
        });
        window.addEventListener('resize', function () {
            if (window.innerWidth > 760 && menuBtn.getAttribute('aria-expanded') === 'true') setMenu(false);
        });
    }

    // Reading progress bar along the top of project and article pages.
    var bar = document.querySelector('.progress');
    if (bar) {
        var ticking = false;
        var paint = function () {
            var max = document.documentElement.scrollHeight - window.innerHeight;
            bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(window.scrollY / max, 1) : 0) + ')';
            ticking = false;
        };
        window.addEventListener('scroll', function () {
            if (!ticking) { ticking = true; requestAnimationFrame(paint); }
        }, { passive: true });
        window.addEventListener('resize', paint);
        paint();
    }

    // Section menu: underline the section currently in view.
    var subnav = document.querySelector('.subnav');
    if (subnav && 'IntersectionObserver' in window) {
        var links = Array.prototype.slice.call(subnav.querySelectorAll('a[href^="#"]'));
        var byId = {};
        links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
        var mark = function (id) {
            links.forEach(function (a) { a.removeAttribute('aria-current'); });
            var a = byId[id];
            if (a) {
                a.setAttribute('aria-current', 'true');
                var wrap = subnav.querySelector('.wrap');
                var left = a.offsetLeft - wrap.clientWidth / 2 + a.clientWidth / 2;
                wrap.scrollTo({ left: left, behavior: calm ? 'auto' : 'smooth' });
            }
        };
        var spy = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) { if (e.isIntersecting) mark(e.target.id); });
        }, { rootMargin: '-35% 0px -60% 0px', threshold: 0 });
        Object.keys(byId).forEach(function (id) {
            var target = document.getElementById(id);
            if (target) spy.observe(target);
        });
    }

    // Tabbed code samples (arrow keys move between tabs), with a copy button.
    document.querySelectorAll('[data-tabs]').forEach(function (card) {
        var tabs = Array.prototype.slice.call(card.querySelectorAll('[role="tab"]'));
        function select(tab) {
            tabs.forEach(function (t) {
                var on = t === tab;
                t.setAttribute('aria-selected', on ? 'true' : 'false');
                t.tabIndex = on ? 0 : -1;
                document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
            });
        }
        tabs.forEach(function (t, i) {
            t.addEventListener('click', function () { select(t); });
            t.addEventListener('keydown', function (e) {
                var n = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
                if (!n) return;
                e.preventDefault();
                var target = tabs[(i + n + tabs.length) % tabs.length];
                select(target);
                target.focus();
            });
        });
        var copy = card.querySelector('[data-copy-code]');
        if (copy) copy.addEventListener('click', function () {
            var panel = card.querySelector('[role="tabpanel"]:not([hidden]) code');
            copyText(panel.textContent).then(function (ok) { say(ok ? 'SQL copied' : 'Select the code to copy it'); });
        });
    });

    // Screenshot viewer: click (or Enter) on a project image to see it full size.
    var images = Array.prototype.slice.call(document.querySelectorAll('.shot img'));
    if (!images.length) return;

    var box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Screenshot viewer');
    box.innerHTML =
        '<span class="lb-count" aria-live="polite"></span>' +
        '<button type="button" class="lb-close" aria-label="Close">&#x2715;</button>' +
        '<button type="button" class="lb-prev" aria-label="Previous image">&#x2039;</button>' +
        '<button type="button" class="lb-next" aria-label="Next image">&#x203A;</button>' +
        '<figure><img alt="" /><figcaption></figcaption></figure>';
    document.body.appendChild(box);

    var big = box.querySelector('img');
    var caption = box.querySelector('figcaption');
    var count = box.querySelector('.lb-count');
    var prev = box.querySelector('.lb-prev');
    var next = box.querySelector('.lb-next');
    var close = box.querySelector('.lb-close');
    var current = 0;
    var opener = null;

    function captionFor(img) {
        var fig = img.closest('figure');
        var cap = fig && fig.querySelector('figcaption');
        return cap ? cap.textContent.trim() : img.alt;
    }

    function show(i) {
        current = (i + images.length) % images.length;
        var img = images[current];
        big.src = img.currentSrc || img.src;
        big.alt = img.alt;
        caption.textContent = captionFor(img);
        count.textContent = images.length > 1 ? (current + 1) + ' / ' + images.length : '';
    }

    function open(i) {
        opener = images[i];
        show(i);
        box.classList.add('is-open');
        document.body.classList.add('lightbox-open');
        close.focus();
    }

    function hide() {
        box.classList.remove('is-open');
        document.body.classList.remove('lightbox-open');
        if (opener) opener.focus();
    }

    prev.hidden = next.hidden = images.length < 2;

    images.forEach(function (img, i) {
        img.classList.add('zoomable');
        img.tabIndex = 0;
        img.setAttribute('role', 'button');
        img.setAttribute('aria-label', 'View larger: ' + (img.alt || 'screenshot'));
        img.addEventListener('click', function () { open(i); });
        img.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); }
        });
    });

    close.addEventListener('click', hide);
    prev.addEventListener('click', function () { show(current - 1); });
    next.addEventListener('click', function () { show(current + 1); });
    big.addEventListener('click', hide);
    box.addEventListener('click', function (e) { if (e.target === box) hide(); });

    document.addEventListener('keydown', function (e) {
        if (!box.classList.contains('is-open')) return;
        if (e.key === 'Escape') hide();
        else if (e.key === 'ArrowLeft') show(current - 1);
        else if (e.key === 'ArrowRight') show(current + 1);
        else if (e.key === 'Tab') {
            var focusable = [close, prev, next].filter(function (b) { return !b.hidden; });
            var idx = focusable.indexOf(document.activeElement);
            e.preventDefault();
            focusable[(idx + (e.shiftKey ? -1 : 1) + focusable.length) % focusable.length].focus();
        }
    });
})();
