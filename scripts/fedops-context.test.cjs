const {test} = require('node:test');
const assert = require('node:assert/strict');
const {readOrigin, contextualHref, apply} = require('../assets/js/fedops-context.js');
const docs = 'https://gachon-cclab.github.io/fedops-docs-1.3/';
const main = 'https://ccl.gachon.ac.kr';
const cloud = 'http://210.109.52.27:30080';

test('two installations remain isolated across interleaved page navigation', () => {
  for (const origin of [main, cloud, main, cloud]) {
    const start = docs + '?fedops_origin=' + encodeURIComponent(origin);
    const target = contextualHref('blog/?q=test#article', start, readOrigin(new URL(start).search));
    assert.equal(readOrigin(new URL(target).search), origin);
    assert.equal(new URL(target).hash, '#article');
    const link = {getAttribute: () => '/fedops/console/task'};
    apply({querySelectorAll: selector => selector === '[data-fedops-path]' ? [link] : []}, new URL(target));
    assert.equal(link.href, origin + '/fedops/console/task');
  }
  assert.equal(readOrigin(''), undefined); // Never inherits another tab's origin.
});
test('invalid, credential-bearing, and duplicate origins fail closed', () => {
  for (const value of ['javascript:alert(1)', '//evil.example', 'https://user:pass@example.org', 'https://example.org/path', 'https://example.org?x=1', 'null']) {
    assert.equal(readOrigin('?fedops_origin=' + encodeURIComponent(value)), null);
  }
  assert.equal(readOrigin('?fedops_origin=' + main + '&fedops_origin=' + cloud), null);
});
test('context does not leak to unrelated destinations', () => {
  assert.equal(contextualHref('https://example.org/', docs, cloud), 'https://example.org/');
});
