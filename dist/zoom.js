// Progressive enhancement for report figures: opens the full-size chart in a dialog
// with fit / original / 2x zoom. Without JavaScript the figure link opens the image file.
(() => {
  const viewer = document.querySelector('dialog.viewer');
  if (!viewer || typeof viewer.showModal !== 'function') return;
  const d = viewer.dataset;
  viewer.innerHTML =
    '<div class="viewer-bar">' +
    '<div class="viewer-zoom" role="group">' +
    `<button type="button" data-level="fit" aria-pressed="true">${d.fit}</button>` +
    `<button type="button" data-level="native" aria-pressed="false">${d.native}</button>` +
    `<button type="button" data-level="double" aria-pressed="false">${d.double}</button>` +
    '</div>' +
    `<button type="button" class="viewer-close" data-close aria-label="${d.close}"><span class="viewer-close-text">${d.close} </span>✕</button>` +
    '</div>' +
    '<div class="viewer-stage" data-level="fit" tabindex="0"><img alt=""></div>' +
    '<p class="viewer-caption"></p>';
  const stage = viewer.querySelector('.viewer-stage');
  const img = stage.querySelector('img');
  const caption = viewer.querySelector('.viewer-caption');
  let opener = null;

  const setLevel = (level) => {
    stage.dataset.level = level;
    viewer.querySelectorAll('[data-level]').forEach((b) => {
      if (b.tagName === 'BUTTON') b.setAttribute('aria-pressed', String(b.dataset.level === level));
    });
  };

  document.querySelectorAll('a[data-zoom]').forEach((link) => {
    link.addEventListener('click', (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
      event.preventDefault();
      opener = link;
      const source = link.querySelector('img');
      img.src = link.href;
      img.alt = source ? source.alt : '';
      const fig = link.closest('figure');
      const cap = fig && fig.querySelector('figcaption');
      caption.textContent = cap ? cap.textContent : img.alt;
      setLevel('fit');
      viewer.showModal();
      viewer.querySelector('[data-close]').focus();
    });
  });

  viewer.addEventListener('click', (event) => {
    const button = event.target.closest('button');
    if (button && button.dataset.level) setLevel(button.dataset.level);
    else if (button && button.hasAttribute('data-close')) viewer.close();
    else if (event.target === viewer) viewer.close();
  });
  viewer.addEventListener('close', () => {
    img.removeAttribute('src');
    if (opener) opener.focus();
  });
})();
