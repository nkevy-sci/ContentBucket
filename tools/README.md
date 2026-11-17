# Project tools

## Format a post

`format_post.py` is the reusable version of the original post 0002 formatting script. It uses Python 3.9+ and the standard library; no installation is required.

Run from the project root:

```sh
# Preview which files would change; does not modify files.
python3 tools/format_post.py posts/0003

# Apply formatting, creating a .bak copy of each changed file first.
python3 tools/format_post.py posts/0003 --write

# Check formatting without writing (exit 1 if changes would be needed).
python3 tools/format_post.py posts/0003 --check

# Format one file, optionally using spaces instead of the default tabs.
python3 tools/format_post.py posts/0003/index.html --write --spaces 2
```

Folder mode handles only immediate `.html`, `.css`, and `.js` files. It excludes subfolders, symlinks, and `.min.` files, so assets and bundled libraries stay untouched. All formatting results are prepared before writing. Existing backups are never overwritten: keep or remove them before another write, or explicitly use `--no-backup`.

Formatting is deliberately conservative:

- **HTML:** Indents explicit structural tags. Preserves text-bearing elements, inline spacing, attributes, comments, embedded code, and whitespace-sensitive elements such as `pre` and `textarea`. Mixed-content or unfamiliar structures may remain as written. Requires explicitly matched closing tags; it reports malformed or implicitly closed markup rather than trying to repair it. CSS-defined whitespace behavior is not inferred; review the previewed changes if a structural container uses whitespace-sensitive CSS.
- **CSS:** Expands rules and declarations, with nested-rule indentation. Keeps quoted values, comments, escapes, and delimiters inside URLs/functions intact. Custom-property brace blocks and escaped line continuations are left unchanged.
- **JavaScript:** Converts existing leading indentation, rather than parsing or rewriting code. Assumes two-space indentation by default; use `--source-indent 4` for four-space source. Files containing template literals, block comments, or escaped line continuations are left unchanged to protect their contents.

This is a small post-source helper, not a full parser or replacement for a language-aware formatter. Review changes before committing. Backups can be restored by copying the `.bak` file over its corresponding source file; remove backups before publication.

Run the regression checks:

```sh
python3 -m unittest discover -s tools -p 'test_format_post.py'
```

Other tools in this directory build the post index and update social metadata. Their behavior is unchanged.
