"""Regression checks for content preservation and safe file handling."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest

from format_post import format_css, format_html, format_js, main


class FormatterTests(unittest.TestCase):
    def test_html_preserves_inline_and_sensitive_content(self):
        sensitive = '<p>Hello <strong>world</strong>!</p><pre>  a\n b</pre><textarea> x\n y</textarea><script>const x = ` a\n b`;</script>'
        source = '<!doctype html><html><head><title>A &amp; B</title></head><body>' + sensitive + '</body></html>'
        result = format_html(source, '\t')
        for fragment in ['<p>Hello <strong>world</strong>!</p>', '<pre>  a\n b</pre>', '<textarea> x\n y</textarea>', '<script>const x = ` a\n b`;</script>']:
            self.assertIn(fragment, result)
        self.assertIn('\n\t<body>\n', result)
        self.assertEqual(format_html(result, '\t'), result)

    def test_comments_and_mixed_content_are_untouched(self):
        source = '<div><!-- keep me -->hello<span>there</span></div>\n'
        self.assertEqual(format_html(source, '\t'), source)

    def test_malformed_html_is_rejected(self):
        with self.assertRaises(ValueError):
            format_html('<div><p>broken</div>', '\t')

    def test_css_strings_comments_urls_and_nested_rules(self):
        source = '/* {;} */\n@media (width > 10px) { a { content: "a; \\" }"; background: url(data:image/svg+xml;a;b); color: red; } }'
        result = format_css(source, '\t')
        self.assertIn('"a; \\" }"', result)
        self.assertIn('url(data:image/svg+xml;a;b)', result)
        self.assertEqual(format_css(result, '\t'), result)

    def test_custom_property_value_is_preserved(self):
        result = format_css(':root { --label: "a b"  ; color: red; }', '\t')
        self.assertIn('--label: "a b"  ;', result)

    def test_js_indentation_and_sensitive_constructs(self):
        self.assertEqual(format_js('if (x) {\n  run();\n}\n', '\t', 2), 'if (x) {\n\trun();\n}\n')
        for source in ['const x = `a\n  b`;', '/* a\n  b */', "const x = 'a\\\n  b';"]:
            self.assertEqual(format_js(source, '\t', 2), source)

    def test_preview_backup_check_and_vendor_exclusion(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            root = Path(directory)
            path = root / 'index.html'
            original = '<html><body><p>Hello</p></body></html>'
            path.write_text(original)
            vendor = root / 'assets'
            vendor.mkdir()
            (vendor / 'library.js').write_text('  untouched();')
            self.assertEqual(main([str(root)]), 0)
            self.assertEqual(path.read_text(), original)
            self.assertEqual(main([str(root), '--check']), 1)
            self.assertEqual(main([str(root), '--write']), 0)
            self.assertEqual(path.with_name('index.html.bak').read_text(), original)
            self.assertEqual((vendor / 'library.js').read_text(), '  untouched();')
            self.assertEqual(main([str(root), '--check']), 0)
            path.write_text(original)
            self.assertEqual(main([str(root), '--write']), 2)
            self.assertEqual(path.read_text(), original)


if __name__ == '__main__':
    unittest.main()
