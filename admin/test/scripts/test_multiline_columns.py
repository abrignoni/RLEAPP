"""A multiline column is escaped on the report page, with its line breaks shown."""
import ast
import pathlib
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from scripts import artifact_report  # pylint: disable=wrong-import-position
from scripts.artifacts import googleSubinfo  # pylint: disable=wrong-import-position

MODULES = ('accPinger', 'googleAccChangeHist', 'googleDeviceconfig', 'googleMyactisearch',
           'googleMyactssearch', 'googlePlayuseract', 'googleSubinfo', 'iNotes')


class MultilineCellTest(unittest.TestCase):
    def test_every_line_ending_shows_one_break(self):
        self.assertEqual(artifact_report.cell_html('a\r\nb\rc\nd', 'Body', [], ['Body']), 'a<br>b<br>c<br>d')

    def test_the_page_shows_breaks_and_escapes_markup(self):
        self.assertEqual(artifact_report.cell_html('<b>one</b> &amp;\ntwo', 'Body', [], ['Body']),
                         '&lt;b&gt;one&lt;/b&gt; &amp;amp;<br>two')

    def test_other_columns_keep_the_default_escape(self):
        self.assertEqual(artifact_report.cell_html('a\nb', 'Other', [], ['Body']), 'a\nb')

    def test_a_changed_artifact_returns_the_value_unescaped(self):
        text = '<p>Made up &amp; text</p>\nsecond'
        with tempfile.TemporaryDirectory() as folder:
            path = pathlib.Path(folder) / 'a.SubscriberInfo.html'
            path.write_text(text, encoding='utf-8')
            context = SimpleNamespace(get_files_found=lambda: [str(path)], get_relative_path=str)
            with patch.object(googleSubinfo, 'artifact_processor', create=True):
                _, rows, _ = googleSubinfo.googleSubinfo.__wrapped__(context)
        self.assertEqual(rows[0][0], text)
        self.assertEqual(artifact_report.cell_html(rows[0][0], 'Subscriber Info', [], ['Subscriber Info']),
                         '&lt;p&gt;Made up &amp;amp; text&lt;/p&gt;<br>second')

    def test_no_changed_artifact_escapes_its_stored_value(self):
        root = pathlib.Path(__file__).resolve().parents[3] / 'scripts' / 'artifacts'
        for name in MODULES:
            tree = ast.parse((root / f'{name}.py').read_text(encoding='utf-8'))
            called = {node.func.id for node in ast.walk(tree)
                      if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
            self.assertNotIn('safe_source', called, name)


if __name__ == '__main__':
    unittest.main()
