/* =============================================================
   Smart Assistant — floating button + bottom sheet
   ============================================================= */
(function () {
  'use strict';

  const fab      = document.getElementById('mbAssistantFab');
  const sheet    = document.getElementById('mbAssistantSheet');
  const backdrop = document.getElementById('mbAssistantBackdrop');

  if (!fab || !sheet || !backdrop) return;

  const closeBtn = sheet.querySelector('.mb-sheet-close');

  function open() {
    sheet.classList.add('is-open');
    backdrop.classList.add('is-open');
    fab.classList.add('is-hidden');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    sheet.classList.remove('is-open');
    backdrop.classList.remove('is-open');
    fab.classList.remove('is-hidden');
    document.body.style.overflow = '';
  }

  fab.addEventListener('click', open);
  backdrop.addEventListener('click', close);
  if (closeBtn) closeBtn.addEventListener('click', close);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && sheet.classList.contains('is-open')) close();
  });

  // Swipe-down to close on the sheet handle area
  let startY = null;
  sheet.addEventListener('touchstart', function (e) {
    if (e.target.closest('.mb-sheet-handle')) startY = e.touches[0].clientY;
  }, { passive: true });
  sheet.addEventListener('touchmove', function (e) {
    if (startY === null) return;
    const dy = e.touches[0].clientY - startY;
    if (dy > 60) {
      startY = null;
      close();
    }
  }, { passive: true });
  sheet.addEventListener('touchend', function () { startY = null; });

  // Close sheet on same-page anchor clicks (so navigation feels instant)
  sheet.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', close);
  });

})();
