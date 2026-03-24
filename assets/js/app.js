/* FLLC // GOVINT — Main Application */
(function () {
  'use strict';

  /* ── Clock ── */
  function tickClock() {
    var el = document.getElementById('header-clock');
    if (el) el.textContent = new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC';
    setTimeout(tickClock, 1000);
  }
  tickClock();

  /* ── Mark active nav link ── */
  var page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href === page) a.classList.add('active');
  });

  /* ── Status bar last-update ── */
  window.setLastUpdate = function (ts) {
    var el = document.getElementById('status-update');
    if (el && ts) el.textContent = 'Last update: ' + ts;
  };
})();
