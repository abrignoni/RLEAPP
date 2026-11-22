"""A multiline column is escaped on the report page, with its line breaks shown."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from scripts import artifact_report  # pylint: disable=wrong-import-position


class MultilineCellTest(unittest.TestCase):
    def test_the_page_shows_breaks_and_escapes_markup(self):
        self.assertEqual(artifact_report.cell_html('<b>one</b> &amp;\ntwo', 'Body', [], ['Body']),
                         '&lt;b&gt;one&lt;/b&gt; &amp;amp;<br>two')

    def test_other_columns_keep_the_default_escape(self):
        self.assertEqual(artifact_report.cell_html('a\nb', 'Other', [], ['Body']), 'a\nb')


if __name__ == '__main__':
    unittest.main()
