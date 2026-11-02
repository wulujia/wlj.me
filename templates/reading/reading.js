// The complete document remains visible without JavaScript.
(function () {
  const root = document.documentElement;
  const theme = document.getElementById('reading-theme');
  if (theme) {
    theme.value = root.getAttribute('data-theme') || 'system';
    theme.addEventListener('change', function () {
      if (theme.value === 'system') root.removeAttribute('data-theme');
      else root.setAttribute('data-theme', theme.value);
    });
  }
  const outline = document.querySelector('.outline details');
  const mobile = window.matchMedia('(max-width: 900px)');
  function resize() {
    if (outline) outline.open = !mobile.matches;
  }
  resize();
  mobile.addEventListener('change', resize);
  const links = Array.from(document.querySelectorAll('.outline a[href^="#"]'));
  const targets = links.map(function (link) {
    return document.getElementById(decodeURIComponent(link.hash.slice(1)));
  }).filter(Boolean);
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (link) {
          const active = decodeURIComponent(link.hash.slice(1)) === entry.target.id;
          link.classList.toggle('active', active);
          if (active) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '0px 0px -75% 0px', threshold: 0 });
    targets.forEach(function (target) { observer.observe(target); });
  }
})();
