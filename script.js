/* Everyday Ecology Challenge — interactions */
(function () {
  'use strict';

  /* ---------- mobile drawer ---------- */
  var toggle = document.getElementById('navToggle');
  var drawer = document.getElementById('drawer');

  if (toggle && drawer) {
    toggle.addEventListener('click', function () {
      var open = drawer.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        drawer.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------- scroll progress ---------- */
  var progress = document.getElementById('progress');
  function onScroll() {
    if (progress) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- reveal on scroll ---------- */
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var reveals = document.querySelectorAll('.reveal');
  if (reduced || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          obs.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- lightbox ---------- */
  var lb = document.getElementById('lightbox');
  var lbImg = document.getElementById('lbImg');
  var lbCap = document.getElementById('lbCap');
  var shots = Array.prototype.slice.call(document.querySelectorAll('.shot'));
  var index = 0;
  var lastFocus = null;

  function show(i) {
    if (!shots.length) return;
    index = (i + shots.length) % shots.length;
    var btn = shots[index];
    var img = btn.querySelector('img');
    lbImg.src = btn.getAttribute('data-full');
    lbImg.alt = img ? img.alt : '';
    lbCap.textContent = btn.getAttribute('data-cap') || (img ? img.alt : '');
  }

  function open(i) {
    lastFocus = document.activeElement;
    show(i);
    lb.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    document.getElementById('lbClose').focus();
  }

  function close() {
    lb.classList.remove('is-open');
    lbImg.src = '';
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }

  shots.forEach(function (btn, i) {
    btn.setAttribute('type', 'button');
    btn.addEventListener('click', function () { open(i); });
  });

  if (lb) {
    document.getElementById('lbClose').addEventListener('click', close);
    document.getElementById('lbPrev').addEventListener('click', function () { show(index - 1); });
    document.getElementById('lbNext').addEventListener('click', function () { show(index + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(index - 1);
      if (e.key === 'ArrowRight') show(index + 1);
    });
  }
})();
