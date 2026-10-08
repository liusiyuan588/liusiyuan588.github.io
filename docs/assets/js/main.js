(() => {
  const menuBtn = document.querySelector('[data-menu-toggle]');
  const menu = document.querySelector('[data-mobile-nav]');
  if (menuBtn && menu) {
    const closeMenu = () => {
      menu.classList.remove('is-open');
      menuBtn.setAttribute('aria-expanded', 'false');
      menuBtn.setAttribute('aria-label', 'Open navigation menu');
      document.body.classList.remove('nav-open');
    };
    menuBtn.addEventListener('click', () => {
      const next = !menu.classList.contains('is-open');
      menu.classList.toggle('is-open', next);
      menuBtn.setAttribute('aria-expanded', String(next));
      menuBtn.setAttribute('aria-label', next ? 'Close navigation menu' : 'Open navigation menu');
      document.body.classList.toggle('nav-open', next);
    });
    menu.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
  }

  const header = document.querySelector('.site-header');
  const progress = document.querySelector('.scroll-progress');
  const updateScroll = () => {
    if (header) header.classList.toggle('has-scrolled', window.scrollY > 12);
    if (progress) {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = `scaleX(${max > 0 ? window.scrollY / max : 0})`;
    }
  };
  window.addEventListener('scroll', updateScroll, { passive: true });
  updateScroll();

  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        observer.unobserve(entry.target);
      }
    }), { threshold: .10, rootMargin: '0px 0px -36px 0px' });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  } else {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('in-view'));
  }
})();
