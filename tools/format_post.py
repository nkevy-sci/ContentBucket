#!/usr/bin/env python3
"""Conservatively format a post's source files, using only Python's standard library."""
import argparse
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import sys

VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
CONTAINERS = set('html head body main article section header footer nav aside div table thead tbody tfoot tr ul ol li form fieldset noscript details'.split())
BLOCKS = CONTAINERS | set('h1 h2 h3 h4 h5 h6 p caption th td figure figcaption pre textarea script style title meta link input button label summary hr'.split())


@dataclass
class Element:
    tag: str
    start: int
    opening_end: int
    closing_start: int = 0
    end: int = 0
    children: list = field(default_factory=list)
    preserve: bool = False


class Structure(HTMLParser):
    """Locate explicit elements without rewriting attributes or text."""

    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.offsets = [0]
        for match in re.finditer('\n', source):
            self.offsets.append(match.end())
        self.root = Element('', 0, 0, len(source), len(source))
        self.stack = [self.root]
        self.feed(source)
        self.close()
        if len(self.stack) != 1:
            raise ValueError('HTML has unclosed tags; leave it unchanged and repair the markup first.')

    def position(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        start = self.position()
        end = start + len(self.get_starttag_text())
        node = Element(tag, start, end)
        # Never reindent text or code in whitespace-sensitive elements.
        node.preserve = tag not in CONTAINERS or any(
            key == 'style' and 'white-space' in (value or '').lower()
            for key, value in attrs
        )
        self.stack[-1].children.append(node)
        if tag in VOID:
            node.closing_start = node.end = end
        else:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            node = self.stack.pop()
            node.closing_start = node.end = node.opening_end

    def handle_endtag(self, tag):
        if len(self.stack) == 1 or self.stack[-1].tag != tag:
            raise ValueError(f'HTML closing tag </{tag}> is not explicitly matched; file unchanged.')
        node = self.stack.pop()
        node.closing_start = self.position()
        node.end = self.source.index('>', node.closing_start) + 1


def format_html(source, indent):
    tree = Structure(source)

    def render(node, depth):
        if node.preserve or not node.children:
            return source[node.start:node.end]
        cursor = node.opening_end
        for child in node.children:
            # Mixed text, comments, inline markup, and unfamiliar elements stay exact.
            if source[cursor:child.start].strip() or child.tag not in BLOCKS:
                return source[node.start:node.end]
            cursor = child.end
        if source[cursor:node.closing_start].strip():
            return source[node.start:node.end]
        opening = source[node.start:node.opening_end]
        closing = source[node.closing_start:node.end]
        middle = '\n'.join(indent * (depth + 1) + render(child, depth + 1)
                           for child in node.children)
        return opening + '\n' + middle + '\n' + indent * depth + closing

    # Preserve the doctype, comments, and other material outside the HTML element.
    output = source
    for node in reversed(tree.root.children):
        output = output[:node.start] + render(node, 0) + output[node.end:]
    return output.rstrip('\r\n') + '\n'


def format_css(source, indent):
    # Escaped line continuations and custom-property brace blocks stay exact.
    if re.search(r'--[\w-]+\s*:[^;{}]*\{', source) or '\\\n' in source or '\\\r\n' in source:
        return source
    lines, buffer = [], []
    depth = parens = brackets = 0
    quote = None
    comment = False
    escaped = False
    i = 0

    def flush(suffix=''):
        raw = ''.join(buffer)
        value = raw.lstrip() if re.match(r'\s*--[\w-]+\s*:', raw) else raw.strip()
        if value or suffix:
            lines.append(indent * depth + value + suffix)
        buffer.clear()

    while i < len(source):
        char = source[i]
        nxt = source[i:i + 2]
        if comment:
            buffer.append(char)
            if nxt == '*/':
                buffer.append('/'); i += 1; comment = False
        elif quote:
            buffer.append(char)
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == quote:
                quote = None
        elif nxt == '/*':
            buffer.extend(['/', '*']); i += 1; comment = True
        elif char in ('"', "'"):
            quote = char; buffer.append(char)
        elif char == '\\':
            # Preserve escaped punctuation in selectors and unquoted URLs.
            buffer.append(char)
            i += 1
            if i < len(source):
                buffer.append(source[i])
        elif char in '([':
            parens += char == '('; brackets += char == '['; buffer.append(char)
        elif char in ')]':
            parens -= char == ')'; brackets -= char == ']'; buffer.append(char)
        elif not parens and not brackets and char == '{':
            flush(' {'); depth += 1
        elif not parens and not brackets and char == ';':
            flush(';')
        elif not parens and not brackets and char == '}':
            if ''.join(buffer).strip():
                flush()
            depth -= 1
            if depth < 0:
                raise ValueError('Unbalanced CSS braces; file unchanged.')
            lines.append(indent * depth + '}')
            if depth == 0:
                lines.append('')
        else:
            buffer.append(char)
        i += 1
    if depth or parens or brackets or quote or comment:
        raise ValueError('Unclosed CSS structure; file unchanged.')
    if ''.join(buffer).strip():
        flush()
    return '\n'.join(lines).rstrip() + '\n'


def format_js(source, indent, source_indent):
    # This is an indentation converter, not a JavaScript parser. Multiline strings,
    # templates, comments, or continuations are left untouched to preserve values.
    if '`' in source or '/*' in source or re.search(r'\\\r?\n', source):
        return source
    lines = []
    for line in source.splitlines(keepends=True):
        match = re.match(r'^[ \t]*', line)
        prefix = match.group()
        columns = len(prefix.expandtabs(source_indent))
        levels, remainder = divmod(columns, source_indent)
        lines.append(indent * levels + ' ' * remainder + line[len(prefix):])
    return ''.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path, help='Post folder or an individual .html, .css, or .js file')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true', help='Apply formatting (default: preview only)')
    mode.add_argument('--check', action='store_true', help='Exit 1 if formatting would change a file')
    parser.add_argument('--spaces', type=int, choices=range(1, 9), metavar='N', help='Use N spaces instead of tabs')
    parser.add_argument('--source-indent', type=int, default=2, choices=range(1, 9), metavar='N', help='Existing JavaScript indentation width (default: 2)')
    parser.add_argument('--no-backup', action='store_true', help='Do not create .bak files when writing')
    args = parser.parse_args(argv)
    if not args.path.exists():
        parser.error('The specified path does not exist.')
    files = sorted(args.path.iterdir()) if args.path.is_dir() else [args.path]
    files = [p for p in files if p.is_file() and not p.is_symlink()
             and p.suffix.lower() in {'.html', '.css', '.js'} and '.min.' not in p.name]
    if not files:
        parser.error('No supported source files found (subfolders and minified files are excluded).')
    indent = ' ' * args.spaces if args.spaces else '\t'
    pending = []
    try:
        # Prepare every result before touching any source file.
        for path in files:
            with path.open(encoding='utf-8', newline='') as stream:
                original = stream.read()
            newline = '\r\n' if '\r\n' in original else '\n'
            normalized = original.replace('\r\n', '\n')
            if path.suffix.lower() == '.html':
                result = format_html(normalized, indent)
            elif path.suffix.lower() == '.css':
                result = format_css(normalized, indent)
            else:
                result = format_js(normalized, indent, args.source_indent)
            result = result.replace('\n', newline)
            if result != original:
                pending.append((path, result))
        if args.write and not args.no_backup:
            for path, _ in pending:
                if path.with_name(path.name + '.bak').exists():
                    raise ValueError(f'{path}.bak already exists; preserve or remove that backup before writing again.')
        for path, result in pending:
            if args.write:
                if not args.no_backup:
                    shutil.copy2(path, path.with_name(path.name + '.bak'))
                with path.open('w', encoding='utf-8', newline='') as stream:
                    stream.write(result)
            print(f'{"Formatted" if args.write else "Would format"}: {path}')
    except (OSError, UnicodeError, ValueError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2
    if not pending:
        print('No formatting changes needed (conservative exclusions may apply).')
    elif not args.write:
        print('Preview only. Add --write to apply changes; backups are created by default.')
    return 1 if args.check and pending else 0


if __name__ == '__main__':
    sys.exit(main())
