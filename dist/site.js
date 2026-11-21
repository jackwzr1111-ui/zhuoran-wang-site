// Marks the page as script-enabled and reveals sections as they scroll into view.
// Content is fully visible without JavaScript; this only adds the entrance motion.
(() => {
  const root = document.documentElement;
  const items = document.querySelectorAll('.reveal');
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (still || !('IntersectionObserver' in window) || !items.length) return;
  root.classList.add('js-reveal');
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  items.forEach((el) => io.observe(el));
})();
