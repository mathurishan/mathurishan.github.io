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

    // Play initial animations on page load.
    window.addEventListener('load', function () {
        window.setTimeout(function () {
            $body.classList.remove('is-preload');
        }, 100);
    });

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
            linkClone.className = 'primary';
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
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => observer.observe(el));

    // Enable JS mode only after observer is ready
    document.documentElement.classList.remove('no-js');
    document.documentElement.classList.add('js');
});