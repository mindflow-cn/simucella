(() => {
  const menu = document.querySelector('.paper-menu');
  const links = document.querySelector('.paper-nav-links');
  if (!menu || !links) return;

  menu.addEventListener('click', () => {
    const open = links.classList.toggle('is-open');
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });

  links.addEventListener('click', (event) => {
    if (!event.target.closest('a')) return;
    links.classList.remove('is-open');
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', 'Open navigation');
  });
})();
