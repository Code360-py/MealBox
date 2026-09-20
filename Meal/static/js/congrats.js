/* =============================================================
   Congratulations overlay
   Triggers from URL params: ?welcome=1, ?first_save=1, ?birthday=1
   ============================================================= */
(function () {
  'use strict';

  const overlay = document.getElementById('mbCongrats');
  if (!overlay) return;

  const emojiEl  = document.getElementById('mbCongratsEmoji');
  const titleEl  = document.getElementById('mbCongratsTitle');
  const textEl   = document.getElementById('mbCongratsText');
  const dismiss  = document.getElementById('mbCongratsDismiss');
  const confetti = overlay.querySelector('.mb-congrats-confetti');

  const params = new URLSearchParams(location.search);
  let trigger = null;

  if (params.has('welcome'))       trigger = 'welcome';
  else if (params.has('first_save')) trigger = 'first_save';
  else if (params.has('birthday'))   trigger = 'birthday';

  if (!trigger) return;

  const username = params.get('u') || '';

  const COPY = {
    welcome: {
      emoji: '🎉',
      title: username ? `Welcome, ${username}!` : 'Welcome to MealBox!',
      text:  'Your account is ready. Start exploring recipes.',
      confetti: true,
    },
    first_save: {
      emoji: '🎂',
      title: 'First bookmark saved!',
      text:  'Your saved recipes live in the Saved tab.',
      confetti: true,
    },
    birthday: {
      emoji: '🥳',
      title: username ? `Happy Birthday, ${username}!` : 'Happy Birthday!',
      text:  'Hope your day is full of good food.',
      confetti: true,
    },
  };

  const cfg = COPY[trigger];
  if (!cfg) return;

  emojiEl.textContent = cfg.emoji;
  titleEl.textContent = cfg.title;
  textEl.textContent  = cfg.text;

  /* ---------- Confetti ---------- */
  function burst() {
    if (!cfg.confetti) return;
    const colors = ['#00e5ff', '#a855f7', '#ff2d92', '#22ff88', '#ffb43c'];
    const N = 24;

    for (let i = 0; i < N; i++) {
      const p = document.createElement('span');
      p.className = 'mb-confetti-piece';
      p.style.left = Math.random() * 100 + '%';
      p.style.background = colors[Math.floor(Math.random() * colors.length)];
      p.style.animationDuration = (2.2 + Math.random() * 1.8) + 's';
      p.style.animationDelay = (Math.random() * 0.4) + 's';
      p.style.width = (6 + Math.random() * 6) + 'px';
      p.style.height = (10 + Math.random() * 8) + 'px';
      confetti.appendChild(p);

      setTimeout(function () { p.remove(); }, 5000);
    }
  }

  /* ---------- Show / hide ---------- */
  let hideTimer = null;

  function show() {
    overlay.classList.add('is-open');
    overlay.setAttribute('aria-hidden', 'false');
    burst();
    hideTimer = setTimeout(hide, 6000);
  }

  function hide() {
    clearTimeout(hideTimer);
    overlay.classList.remove('is-open');
    overlay.setAttribute('aria-hidden', 'true');
    stripQuery();
  }

  function stripQuery() {
    const url = new URL(location.href);
    ['welcome', 'first_save', 'birthday', 'u'].forEach(function (k) {
      url.searchParams.delete(k);
    });
    history.replaceState({}, '', url.pathname + (url.search ? url.search : '') + url.hash);
  }

  if (dismiss) dismiss.addEventListener('click', hide);
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) hide();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && overlay.classList.contains('is-open')) hide();
  });

  // Show after a tick so the fade-in is visible
  requestAnimationFrame(function () {
    setTimeout(show, 150);
  });

})();
