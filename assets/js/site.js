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
        var meta = document.querySelector('meta[name="theme-color"]');
        if (meta) meta.setAttribute('content', theme === 'dark' ? '#1a1917' : '#faf9f5');
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
    var counters = document.querySelectorAll('[data-count]');
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
