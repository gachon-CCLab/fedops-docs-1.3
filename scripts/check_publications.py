"""Check that each Markdown publication is present in the built site."""

from pathlib import Path
import re
from html.parser import HTMLParser
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            source = dict(attrs).get("src")
            if source:
                self.sources.append(source)


def check_images(page: Path):
    parser = Images()
    parser.feed(page.read_text(encoding="utf-8"))
    for source in parser.sources:
        url = urlparse(source)
        if url.scheme or url.netloc or not url.path.startswith("/"):
            continue
        path = url.path.removeprefix("/fedops-docs-1.3/").lstrip("/")
        if not (SITE / path).is_file():
            raise SystemExit(f"Missing image in {page}: {source}")


def display_order(source: Path) -> int:
    front_matter = source.read_text(encoding="utf-8-sig").split("---", 2)[1]
    match = re.search(r"(?m)^display_order:\s*(-?\d+)\s*$", front_matter)
    if not match:
        raise ValueError(f"Missing display_order: {source}")
    return int(match.group(1))


for section in ("blog", "news"):
    sources = list((ROOT / f"_{section}").glob("*.md"))
    index_path = SITE / section / "index.html"
    if not sources or not index_path.is_file():
        raise SystemExit(f"Missing {section} posts or index page")

    ordered = sorted(sources, key=display_order)
    orders = [display_order(source) for source in ordered]
    if len(orders) != len(set(orders)):
        raise SystemExit(f"Duplicate {section} display_order")

    index_html = index_path.read_text(encoding="utf-8")
    check_images(index_path)
    positions = []
    for source in ordered:
        article_path = SITE / section / source.stem / "index.html"
        if not article_path.is_file():
            raise SystemExit(f"Missing built article: {article_path}")
        check_images(article_path)
        marker = f"/{section}/{source.stem}/"
        position = index_html.find(marker)
        if position < 0:
            raise SystemExit(f"Missing article from {section} index: {marker}")
        positions.append(position)
    if positions != sorted(positions):
        raise SystemExit(f"Incorrect {section} article order")
    print(f"{section}: {len(sources)} Markdown posts and built pages verified")
