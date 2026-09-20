document.addEventListener('DOMContentLoaded', function () {
  var button = document.querySelector('.docs-nav-toggle');
  var nav = document.getElementById('docs-global-menu');
  if (!button || !nav) return;
  function close() { button.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); }
  button.addEventListener('click', function () {
    var open = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(open)); nav.classList.toggle('open', open);
  });
  document.addEventListener('keydown', function (event) { if (event.key === 'Escape') { close(); } });
  nav.addEventListener('click', function (event) { if (event.target.closest('a')) close(); });
});
