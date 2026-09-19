/* =============================================================
   MealBox — recent search history (localStorage)
   ============================================================= */
(function () {
  'use strict';

  const KEY = 'mb_recent_searches';
  const MAX = 8;

  const input   = document.getElementById('searchInput');
  const form    = document.getElementById('searchForm');
  const wrap    = document.getElementById('recentSearchesWrap');
  const chips   = document.getElementById('recentSearches');
  const clearBt = document.getElementById('clearHistory');

  if (!input || !form) return;

  function read() {
    try {
      const raw = localStorage.getItem(KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) { return []; }
  }

  function write(list) {
    try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {}
  }

  function push(term) {
    term = (term || '').trim();
    if (!term) return;
    let list = read();
    list = list.filter(t => t.toLowerCase() !== term.toLowerCase());
    list.unshift(term);
    if (list.length > MAX) list = list.slice(0, MAX);
    write(list);
    render();
  }

  function remove(term) {
    const list = read().filter(t => t !== term);
    write(list);
    render();
  }

  function clearAll() {
    write([]);
    render();
  }

  function render() {
    const list = read();

    if (!list.length) {
      wrap.style.display = 'none';
      chips.innerHTML = '';
      return;
    }

    wrap.style.display = 'block';
    chips.innerHTML = '';

    list.forEach(function (term) {
      const a = document.createElement('a');
      a.href = '?q=' + encodeURIComponent(term);
      a.className = 'mb-chip';
      a.innerHTML =
        '<i class="fa-solid fa-clock-rotate-left"></i>' +
        '<span>' + escapeHtml(term) + '</span>' +
        '<button type="button" class="mb-chip-x" aria-label="Remove">×</button>';

      // Remove button inside chip
      a.querySelector('.mb-chip-x').addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        remove(term);
      });

      chips.appendChild(a);
    });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' })[c];
    });
  }

  // Save on submit
  form.addEventListener('submit', function () {
    push(input.value);
  });

  // Clear all
  if (clearBt) {
    clearBt.addEventListener('click', clearAll);
  }

  // Initial render + save query if loaded from URL
  render();

  const params = new URLSearchParams(location.search);
  const q = params.get('q');
  if (q) push(q);

})();
