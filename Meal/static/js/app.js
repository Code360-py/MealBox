/* =============================================================
   MealBox — navigation loading UX + YouTube-style skeletons
   ============================================================= */
(function () {
  'use strict';

  const doc = document;
  const body = doc.body;

  /* Minimum shimmer time before an image is revealed */
  const SKEL_MIN_MS = 3000;   /* change to 4000 / 5000 if desired */

  /* ============================================================
     Progress bar
     ============================================================ */
  const progress = doc.createElement('div');
  progress.className = 'mb-progress';
  progress.innerHTML = '<div class="bar"></div>';
  body.appendChild(progress);

  const bar = progress.querySelector('.bar');
  let progTimer = null;

  function startProgress() {
    progress.classList.add('is-active');
    bar.style.width = '0%';
    requestAnimationFrame(() => { bar.style.width = '90%'; });
    clearTimeout(progTimer);
  }
  function finishProgress() {
    clearTimeout(progTimer);
    bar.style.width = '100%';
    progTimer = setTimeout(() => {
      progress.classList.remove('is-active');
      setTimeout(() => { bar.style.width = '0%'; }, 250);
    }, 200);
  }

  /* ============================================================
     Full-screen overlay
     ============================================================ */
  const overlay = doc.createElement('div');
  overlay.className = 'mb-overlay';
  overlay.innerHTML =
    '<div class="mb-spinner"></div>' +
    '<div class="mb-overlay-text">Loading…</div>';
  body.appendChild(overlay);

  const showOverlay = () => overlay.classList.add('is-active');
  const hideOverlay = () => overlay.classList.remove('is-active');

  /* ============================================================
     Navigation interception (progress bar)
     ============================================================ */
  function isInternal(a) {
    if (!a || !a.href) return false;
    if (a.target && a.target !== '_self') return false;
    if (a.hasAttribute('download')) return false;
    if (a.dataset.noProgress !== undefined) return false;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin) return false;
    // same path + same query -> not a real navigation
    if (url.pathname === location.pathname && url.search === location.search) return false;
    return true;
  }

  doc.addEventListener('click', function (e) {
    if (e.defaultPrevented) return;
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const a = e.target.closest('a');
    if (!a || !isInternal(a)) return;
    startProgress();
  }, true);

  /* ============================================================
     Form submit interception
     ============================================================ */
  doc.addEventListener('submit', function (e) {
    const form = e.target;
    if (form.dataset.noOverlay !== undefined) return;

    const btn = form.querySelector(
      'button[type="submit"], button:not([type]), input[type="submit"]'
    );
    if (btn) { btn.classList.add('is-loading'); btn.disabled = true; }

    showOverlay();
    startProgress();
  }, true);

  /* ============================================================
     Restore on pageshow (back button, bfcache)
     ============================================================ */
  window.addEventListener('pageshow', function () {
    hideOverlay();
    finishProgress();
    doc.querySelectorAll('.btn.is-loading').forEach(function (b) {
      b.classList.remove('is-loading');
      b.disabled = false;
    });
  });

  /* ============================================================
     Skeleton preloading with minimum shimmer time
     ============================================================ */

  function revealImage(wrap, img) {
    const started = Number(wrap.dataset.skelStart || Date.now());
    const elapsed = Date.now() - started;
    const wait = Math.max(0, SKEL_MIN_MS - elapsed);

    setTimeout(function () {
      img.classList.add('loaded');
      wrap.classList.add('is-loaded', 'is-ready');
    }, wait);
  }

  function bindSkeletons() {
    /* 1. Images inside .mb-skel wrappers */
    doc.querySelectorAll('.mb-skel').forEach(function (wrap) {
      const img = wrap.querySelector('img');
      if (!img || img.dataset.mbBound) return;
      img.dataset.mbBound = '1';
      wrap.dataset.skelStart = String(Date.now());

      const fire = () => revealImage(wrap, img);

      if (img.complete && img.naturalWidth > 0) {
        fire();
      } else {
        img.addEventListener('load',  fire, { once: true });
        img.addEventListener('error', fire, { once: true });
      }
    });

    /* 2. Standalone images with class="mb-img" (no min time) */
    doc.querySelectorAll('img.mb-img').forEach(function (img) {
      if (img.closest('.mb-skel')) return;
      if (img.dataset.mbBound) return;
      img.dataset.mbBound = '1';

      if (img.complete && img.naturalWidth > 0) {
        img.classList.add('loaded');
      } else {
        img.addEventListener('load',  () => img.classList.add('loaded'), { once: true });
        img.addEventListener('error', () => img.classList.add('loaded'), { once: true });
      }
    });

    /* 3. Deferred card content (reveal immediately) */
    doc.querySelectorAll('.mb-deferred').forEach(function (el) {
      el.classList.add('is-ready');
    });
  }

  if (doc.readyState === 'loading') {
    doc.addEventListener('DOMContentLoaded', bindSkeletons);
  } else {
    bindSkeletons();
  }

  /* ============================================================
     Safety nets
     ============================================================ */
  window.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { hideOverlay(); finishProgress(); }
  });

  setInterval(function () {
    if (overlay.classList.contains('is-active')) {
      const t = overlay.dataset.shownAt || (overlay.dataset.shownAt = Date.now());
      if (Date.now() - t > 8000) { hideOverlay(); finishProgress(); }
    } else {
      delete overlay.dataset.shownAt;
    }
  }, 2000);

})();
