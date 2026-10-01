/* Installation context belongs to this URL only. Never use shared storage. */
(function () {
  function readOrigin(search) {
    const values = new URLSearchParams(search).getAll('fedops_origin');
    if (!values.length) return undefined;
    if (values.length !== 1) return null;
    try {
      const url = new URL(values[0]);
      if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password ||
          url.origin !== values[0]) return null;
      return url.origin;
    } catch (_) { return null; }
  }

  function contextualHref(href, pageHref, origin) {
    const url = new URL(href, pageHref);
    // Propagate only within the public Docs/Blog/News site, never to third parties.
    if (url.origin === 'https://gachon-cclab.github.io' &&
        /^\/(fedops-docs-1\.3|fedops-publications)(\/|$)/.test(url.pathname)) {
      url.searchParams.set('fedops_origin', origin);
    }
    return url.href;
  }

  function apply(doc, location) {
    const origin = readOrigin(location.search);
    for (const link of doc.querySelectorAll('[data-fedops-path]')) {
      if (origin === undefined) {
        link.href = link.getAttribute('data-fedops-default');
        link.title = 'Default FedOps site: ' + new URL(link.href).origin;
      } else if (!origin) {
        link.removeAttribute('href');
        link.setAttribute('aria-disabled', 'true');
        link.title = 'Invalid FedOps installation address; reopen Docs from your FedOps Home.';
      } else {
        link.href = origin + link.getAttribute('data-fedops-path');
        link.title = 'Return to ' + origin;
      }
    }
    for (const label of doc.querySelectorAll('[data-fedops-context]')) {
      label.textContent = origin === undefined ? 'Default FedOps site (opened directly)' : origin ? 'FedOps site: ' + origin : 'Invalid FedOps site address';
    }
    if (!origin) return;
    for (const link of doc.querySelectorAll('a[href]')) {
      link.href = contextualHref(link.getAttribute('href'), location.href, origin);
    }
    // Search results can be inserted after load. Preserve context for mouse,
    // keyboard and open-in-new-tab navigation without cross-tab storage.
    if (doc.addEventListener) {
      const update = event => {
        const link = event.target.closest && event.target.closest('a[href]');
        if (link) link.href = contextualHref(link.getAttribute('href'), location.href, origin);
      };
      for (const event of ['click', 'pointerdown', 'focusin', 'contextmenu']) doc.addEventListener(event, update, true);
    }
  }

  if (typeof module !== 'undefined') module.exports = { readOrigin, contextualHref, apply };
  if (typeof document !== 'undefined') apply(document, window.location);
})();
