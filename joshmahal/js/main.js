(function () {
  // ---------- lightbox ----------
  var dlg = document.getElementById('lightbox');
  var img = dlg.querySelector('img');
  var titleEl = dlg.querySelector('.lb-title');
  var capEl = dlg.querySelector('.lb-cap');
  var countEl = dlg.querySelector('.lb-count');
  var group = [], idx = 0;

  function show(i) {
    idx = (i + group.length) % group.length;
    var a = group[idx];
    img.src = a.getAttribute('href');
    img.alt = a.dataset.title || '';
    titleEl.textContent = a.dataset.title || '';
    capEl.textContent = a.dataset.caption || '';
    countEl.textContent = (idx + 1) + ' of ' + group.length;
    dlg.classList.remove('zoomed');
    dlg.classList.toggle('zoomable', a.dataset.group === 'dwg');
  }

  document.querySelectorAll('a.lb').forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (!dlg.showModal) return;   // very old browsers: follow the link
      e.preventDefault();
      group = Array.prototype.slice.call(document.querySelectorAll('a.lb[data-group="' + a.dataset.group + '"]'));
      show(group.indexOf(a));
      dlg.showModal();
    });
  });
  dlg.querySelector('.lb-close').addEventListener('click', function () { dlg.close(); });
  dlg.querySelector('.lb-prev').addEventListener('click', function () { show(idx - 1); });
  dlg.querySelector('.lb-next').addEventListener('click', function () { show(idx + 1); });
  dlg.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') show(idx - 1);
    if (e.key === 'ArrowRight') show(idx + 1);
  });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  img.addEventListener('click', function () {
    if (dlg.classList.contains('zoomable')) dlg.classList.toggle('zoomed');
  });
  dlg.addEventListener('close', function () { img.removeAttribute('src'); });

  // ---------- 360 viewer (loads when the section comes into view) ----------
  var box = document.getElementById('pano');
  var viewer = null;
  function load(src) {
    if (typeof pannellum === 'undefined') {
      box.innerHTML = '<p style="padding:24px">The 360° viewer could not load. <a href="' + src + '">Open the panorama image</a>.</p>';
      return;
    }
    if (viewer) viewer.destroy();
    viewer = pannellum.viewer('pano', {
      type: 'equirectangular', panorama: src, autoLoad: true, showZoomCtrl: true,
      hfov: 100, autoRotate: -1.5, autoRotateInactivityDelay: 4000, compass: false
    });
  }
  var started = false;
  function start() { if (!started) { started = true; load(box.dataset.first); } }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (ents, obs) {
      if (ents[0].isIntersecting) { start(); obs.disconnect(); }
    }, { rootMargin: '200px' }).observe(box);
  } else { start(); }
  document.querySelectorAll('.pano-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.pano-btn').forEach(function (o) { o.classList.remove('on'); o.setAttribute('aria-pressed', 'false'); });
      b.classList.add('on'); b.setAttribute('aria-pressed', 'true');
      started = true;
      load(b.dataset.src);
    });
  });
})();
