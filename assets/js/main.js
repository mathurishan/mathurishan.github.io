/*
    Forty by HTML5 UP
    html5up.net | @ajlkn
    Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function () {

    "use strict";

    var $body = document.querySelector('body');

    // Methods/Polyfills

    // classList | (c) @remy | github.com/remy/polyfills | rem.mit-license.org
    !function () { function t(t) { this.el = t; for (var n = t.className.replace(/^\s+|\s+$/g, "").split(/\s+/), i = 0; i < n.length; i++)e.call(this, n[i]) } function n(t, n, i) { Object.defineProperty ? Object.defineProperty(t, n, { get: i }) : t.__defineGetter__(n, i) } if (!("undefined" == typeof window.Element || "classList" in document.documentElement)) { var i = Array.prototype, e = i.push, s = i.splice, o = i.join; t.prototype = { add: function (t) { this.contains(t) || (e.call(this, t), this.el.className = this.toString()) }, contains: function (t) { return -1 != this.el.className.indexOf(t) }, item: function (t) { return this.el.className.split(/\s+/)[t] || null }, remove: function (t) { if (this.contains(t)) { for (var n = this.el.className.split(/\s+/), i = 0; i < n.length; i++)n[i] == t && s.call(this, i, 1); this.el.className = n.join(" ") } }, toString: function () { return o.call(this, " ") }, toggle: function (t) { return this.contains(t) ? this.remove(t) : this.add(t), this.contains(t) } }, window.DOMTokenList = t, n(Element.prototype, "classList", function () { return new t(this) }) } }();

    // canUse
    window.canUse = function (p) { if (!window._canUse) window._canUse = document.createElement("div"); var e = window._canUse.style, up = p.charAt(0).toUpperCase() + p.slice(1); return p in e || "Moz" + up in e || "Webkit" + up in e || "O" + up in e || "ms" + up in e };

    // window.addEventListener
    (function () { if ("addEventListener" in window) return; window.addEventListener = function (type, f) { window.attachEvent("on" + type, f) } })();

    // Play initial animations as soon as the page is parsed. Waiting for the
    // window 'load' event kept the hero hidden until every image had downloaded.
    window.setTimeout(function () {
        $body.classList.remove('is-preload');
    }, 50);

    // Scrolly.
    document.querySelectorAll('.scrolly').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);
            if (target) {
                const headerHeight = document.getElementById('header') ? document.getElementById('header').offsetHeight : 0;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerHeight;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });

    // Tiles.
    var tiles = document.querySelectorAll('.tiles > article');
    tiles.forEach(tile => {
        var img = tile.querySelector('.image img');
        var link = tile.querySelector('.link');

        if (img) {
            tile.style.backgroundImage = `url(${img.src})`;
            img.style.display = 'none';
            if (img.dataset.position) {
                tile.style.backgroundPosition = img.dataset.position;
            }
        }

        if (link) {
            var linkClone = link.cloneNode(true);
            linkClone.classList.add('primary');
            linkClone.innerText = ''; // Clear text
            tile.appendChild(linkClone);
        }
    });

    // Header.
    var header = document.getElementById('header');
    var banner = document.getElementById('banner');

    if (banner && header && header.classList.contains('alt')) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) {
                    header.classList.remove('alt');
                    header.classList.add('reveal');
                } else {
                    header.classList.add('alt');
                    header.classList.remove('reveal');
                }
            });
        }, { threshold: 0, rootMargin: `-${header.offsetHeight}px 0px 0px 0px` });

        observer.observe(banner);
    }

    // Menu.
    var menu = document.getElementById('menu');
    var menuInner = menu ? menu.querySelector('.inner') : null;

    if (menu) {
        document.body.appendChild(menu);

        if (!menuInner) {
            var innerDiv = document.createElement('div');
            innerDiv.className = 'inner';
            while (menu.firstChild) {
                innerDiv.appendChild(menu.firstChild);
            }
            menu.appendChild(innerDiv);
            menuInner = innerDiv;
        }

        var closeBtn = document.createElement('a');
        closeBtn.href = '#menu';
        closeBtn.className = 'close';
        closeBtn.innerText = 'Close';
        menu.appendChild(closeBtn);

        function toggleMenu(e) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }
            $body.classList.toggle('is-menu-visible');
        }

        function hideMenu(e) {
            if (e) e.stopPropagation();
            $body.classList.remove('is-menu-visible');
        }

        document.querySelectorAll('a[href="#menu"]').forEach(btn => {
            btn.addEventListener('click', toggleMenu);
        });

        closeBtn.addEventListener('click', hideMenu);

        menu.addEventListener('click', function (e) {
            e.stopPropagation();
        });

        $body.addEventListener('click', function (e) {
            if ($body.classList.contains('is-menu-visible')) {
                hideMenu();
            }
        });

        window.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') hideMenu();
        });
    }

})();

// Scroll Animations using IntersectionObserver
document.addEventListener('DOMContentLoaded', function () {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // No observer support, or the visitor prefers less motion: show everything.
    if (!('IntersectionObserver' in window) || reduceMotion) {
        animatedElements.forEach(el => el.classList.add('is-visible'));
        document.documentElement.classList.remove('no-js');
        document.documentElement.classList.add('js');
        return;
    }

    // threshold 0 so tall sections (taller than the screen) still reveal.
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -40px 0px',
        threshold: 0
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    animatedElements.forEach(el => observer.observe(el));

    // Enable JS mode only after observer is ready
    document.documentElement.classList.remove('no-js');
    document.documentElement.classList.add('js');
});
// Screenshot viewer: click (or Enter) on a case-study image to see it full size.
document.addEventListener('DOMContentLoaded', function () {
    const images = Array.from(document.querySelectorAll('#main .image.main img, #main .image.fit img'));
    if (!images.length) return;

    const box = document.createElement('div');
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

    const big = box.querySelector('img');
    const caption = box.querySelector('figcaption');
    const count = box.querySelector('.lb-count');
    const prev = box.querySelector('.lb-prev');
    const next = box.querySelector('.lb-next');
    const close = box.querySelector('.lb-close');
    let current = 0;
    let opener = null;

    // Caption: the paragraph under the image if there is one, otherwise its alt text.
    function captionFor(img) {
        const wrap = img.closest('.image');
        const p = wrap && wrap.nextElementSibling;
        return p && p.tagName === 'P' ? p.textContent.trim() : img.alt;
    }

    function show(i) {
        current = (i + images.length) % images.length;
        const img = images[current];
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
        if (opener && opener.focus) opener.focus();
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
            // Keep focus inside the viewer.
            const focusable = [close, prev, next].filter(function (b) { return !b.hidden; });
            const idx = focusable.indexOf(document.activeElement);
            e.preventDefault();
            focusable[(idx + (e.shiftKey ? -1 : 1) + focusable.length) % focusable.length].focus();
        }
    });
});
