#!/usr/bin/env python3
"""Rebuild the homepage from numbered posts using only the standard library.

Run: python3 tools/build_index.py
Edit templates/index.html to change the homepage layout.
"""

from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
from string import Template
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class PostMetadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.in_title = False
        self.titles = []
        self.descriptions = []
        self.has_og_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "head":
            self.in_head = True
        if not self.in_head:
            return
        if tag == "title":
            self.titles.append("")
            self.in_title = True
        if tag == "meta":
            if (attrs.get("name") or "").lower() == "description":
                self.descriptions.append(attrs.get("content") or "")
            if ((attrs.get("property") or "").lower() == "og:title"
                    and (attrs.get("content") or "").strip()):
                self.has_og_title = True

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "head":
            self.in_head = False
            self.in_title = False

    def handle_data(self, data):
        if self.in_head and self.in_title:
            self.titles[-1] += data


def build_index(root):
    """Validate every post before atomically replacing the homepage."""
    posts_dir = root / "posts"
    if not posts_dir.is_dir():
        raise ValueError(f"Posts directory not found: {posts_dir}")
    pages = sorted(
        (page for page in posts_dir.glob("*/index.html")
         if re.fullmatch(r"[0-9]{4}", page.parent.name) and page.is_file()),
        key=lambda page: int(page.parent.name), reverse=True,
    )
    entries = []
    errors = []
    for page in pages:
        relative = page.relative_to(root).as_posix()
        metadata = PostMetadata()
        try:
            metadata.feed(page.read_text(encoding="utf-8"))
            metadata.close()
        except (OSError, UnicodeError) as error:
            errors.append(f"{relative}: {error}")
            continue
        if not metadata.has_og_title:
            print(f"Warning: {relative} needs Open Graph tags (og:title is missing or empty).",
                  file=sys.stderr)
        valid = True
        for label, values in (("title", metadata.titles),
                              ("description", metadata.descriptions)):
            if len(values) != 1 or not values[0].strip():
                errors.append(f"{relative}: expected exactly one nonempty {label} in the head.")
                valid = False
        if valid:
            title = escape(metadata.titles[0].strip())
            description = escape(metadata.descriptions[0].strip())
            link = f"posts/{page.parent.name}/"
            entries.append(
                f'        <li>\n          <a href="{link}">{title}</a>\n'
                f'          <p>{description}</p>\n        </li>'
            )
    if errors:
        raise ValueError("\n".join(errors))

    template = Template((root / "templates/index.html").read_text(encoding="utf-8"))
    placeholders = [match.group("named") or match.group("braced")
                    for match in template.pattern.finditer(template.template)]
    if "post_list" not in placeholders:
        raise ValueError("Template is missing the $post_list placeholder.")
    # The template already indents the first placeholder line.
    listing = "\n".join(entries).lstrip() if entries else ""
    homepage = template.substitute(post_list=listing)
    destination = root / "index.html"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=root, delete=False) as output:
            temporary = Path(output.name)
            output.write(homepage)
        mode = destination.stat().st_mode & 0o777 if destination.exists() else 0o644
        temporary.chmod(mode)
        temporary.replace(destination)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return len(entries)


def main():
    try:
        count = build_index(PROJECT_ROOT)
    except (OSError, UnicodeError, ValueError, KeyError) as error:
        print(f"Error: {error}\nHomepage left unchanged.", file=sys.stderr)
        return 1
    print(f"Built index.html with {count} {'post' if count == 1 else 'posts'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
