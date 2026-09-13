"""Check generated 1.3 HTML links, images, and versioned search metadata."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / '_site'

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.images = []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag == 'img':
            self.images.append(attrs.get('src', ''))

paths = [ROOT / 'index.html', *sorted((ROOT / 'v1.3').rglob('*.html'))]
assert len(paths) == 10, f'Expected 10 pages, got {len(paths)}'
cache = {}
errors = []
image_count = 0
for path in paths:
    page = cache.setdefault(path, Page(path))
    image_count += len(page.images)
    assert 'FEDOPSCODEBLOCK' not in path.read_text(encoding='utf-8')
    for href in page.links + page.images:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        target = (ROOT / unquote(url.path).lstrip('/')) if url.path.startswith('/') else path.parent / unquote(url.path)
        if not url.path:
            target = path
        if target.is_dir():
            target /= 'index.html'
        if not target.exists():
            errors.append(f'{path.relative_to(ROOT)}: missing {href}')
        elif url.fragment and target.suffix == '.html':
            dest = cache.setdefault(target, Page(target))
            if unquote(url.fragment) not in dest.ids:
                errors.append(f'{path.relative_to(ROOT)}: missing anchor {href}')
data = json.loads((ROOT / 'assets/js/search-data.json').read_text(encoding='utf-8'))
assert {item['docsVersion'] for item in data.values()} == {'1.2', '1.3'}
assert (ROOT / 'v1.2/index.html').exists()
assert image_count == 73, f'Expected 73 guide images, got {image_count}'
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(paths)} pages, {image_count} images, local links/anchors, and both search versions.')
