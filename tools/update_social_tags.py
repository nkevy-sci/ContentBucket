#!/usr/bin/env python3
"""Generate Open Graph metadata for one numbered post without rewriting its HTML.

Example:
    python3 tools/update_social_tags.py 0001 \
        --image-alt "A description of the preview image"

Install dependencies with: python3 -m pip install -r tools/requirements.txt
"""

import argparse
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import urljoin, urlsplit

START = "<!-- BEGIN GENERATED OPEN GRAPH -->"
END = "<!-- END GENERATED OPEN GRAPH -->"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SITE_URL = "https://nkevy-sci.github.io/ContentBucket/"


class HeadMetadata(HTMLParser):
    """Read source metadata and detect Open Graph tags in the head."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.in_title = False
        self.titles = []
        self.descriptions = []
        self.has_open_graph = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "head":
            self.in_head = True
        if not self.in_head:
            return
        if tag == "title":
            self.titles.append("")
            self.in_title = True
        if tag == "meta":
            if (attributes.get("name") or "").lower() == "description":
                self.descriptions.append(attributes.get("content") or "")
            for key in ("property", "name"):
                if (attributes.get(key) or "").lower().startswith("og:"):
                    self.has_open_graph = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "head":
            self.in_head = False

    def handle_data(self, data):
        if self.in_title and self.in_head:
            self.titles[-1] += data


def update_html(page_html, page_url, image_url, image_alt):
    """Return updated HTML, raising ValueError before any file is changed."""

    head_open = re.search(r"<head(?:\s[^>]*)?>", page_html, re.IGNORECASE)
    head_close = re.search(r"</head\s*>", page_html, re.IGNORECASE)
    if not head_open or not head_close or head_close.start() < head_open.end():
        raise ValueError("Missing or invalid head element.")

    start = end = head_close.start()
    source_html = page_html

    metadata = HeadMetadata()
    metadata.feed(source_html)
    metadata.close()
    if metadata.has_open_graph:
        raise ValueError("Open Graph tags exist outside the generated block; resolve them first.")
    if len(metadata.titles) != 1 or not metadata.titles[0].strip():
        raise ValueError("The head must contain exactly one nonempty title.")
    if len(metadata.descriptions) != 1 or not metadata.descriptions[0].strip():
        raise ValueError("The head must contain exactly one nonempty description meta tag.")

    properties = [
        ("og:title", metadata.titles[0].strip()),
        ("og:description", metadata.descriptions[0].strip()),
        ("og:type", "article"),
        ("og:url", page_url),
        ("og:image", image_url),
        ("og:image:width", "1200"),
        ("og:image:height", "630"),
        ("og:image:alt", image_alt),
    ]
    newline = "\r\n" if "\r\n" in page_html else "\n"
    block = newline.join([
        START,
        *(f'<meta property="{key}" content="{escape(value, quote=True)}">'
          for key, value in properties),
        END,
    ])
    if start and page_html[start - 1] not in "\r\n":
        block = newline + block
    block += newline
    return page_html[:start] + block + page_html[end:]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("post_id", help="Four-digit post ID, such as 0001")
    parser.add_argument("--site-url", default=DEFAULT_SITE_URL,
                        help=f"Published site root (default: {DEFAULT_SITE_URL})")
    parser.add_argument("--image-alt", required=True, help="Description of the preview image")
    parser.add_argument("--check", action="store_true", help="Check without writing; exit 1 if tags need updating")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[0-9]{4}", args.post_id):
        parser.error("post_id must contain exactly four digits")
    url = urlsplit(args.site_url)
    if (url.scheme not in ("https", "http") or not url.hostname
            or url.query or url.fragment or url.username or url.password):
        parser.error("--site-url must be an absolute HTTP(S) URL without credentials, query, or fragment")
    if not args.image_alt.strip():
        parser.error("--image-alt must not be empty")

    try:
        from PIL import Image
    except ImportError:
        print("Error: install Pillow with: python3 -m pip install -r tools/requirements.txt", file=sys.stderr)
        return 1

    post = PROJECT_ROOT / "posts" / args.post_id
    page = post / "index.html"
    preview = post / "assets" / f"{args.post_id}-preview.jpg"
    try:
        with Image.open(preview) as image:
            if image.size != (1200, 630):
                raise ValueError(f"Preview must be 1200×630; found {image.width}×{image.height}.")
            if image.format != "JPEG":
                raise ValueError("The .jpg preview must contain a JPEG image.")
            image.verify()
        with page.open(encoding="utf-8", newline="") as source:
            page_html = source.read()
        base_url = args.site_url.rstrip("/") + "/"
        page_url = urljoin(base_url, f"posts/{args.post_id}/")
        image_url = urljoin(page_url, f"assets/{preview.name}")
        updated_html = update_html(page_html, page_url, image_url, args.image_alt.strip())
        if updated_html == page_html:
            print(f"Post {args.post_id}: Open Graph tags are up to date.")
            return 0
        if args.check:
            print(f"Post {args.post_id}: Open Graph tags need updating.")
            return 1
        # Write beside the destination, then replace it atomically.
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                                             dir=post, delete=False) as output:
                temporary = Path(output.name)
                output.write(updated_html)
            temporary.chmod(page.stat().st_mode & 0o777)
            temporary.replace(page)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
        print(f"Post {args.post_id}: updated Open Graph tags.")
        return 0
    except (OSError, ValueError, UnicodeError) as error:
        print(f"Error for post {args.post_id}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
