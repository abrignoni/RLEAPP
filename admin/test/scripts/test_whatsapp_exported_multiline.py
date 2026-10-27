"""Bracketed prose is a continuation, not an invented WhatsApp timestamp."""
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.artifacts.whatsappExportedchats import whatsappExportedchats  # pylint: disable=wrong-import-position


class Context:
    def __init__(self, path):
        self.path = str(path)

    def get_files_found(self):
        return [self.path]

    def get_relative_path(self, path):
        return pathlib.Path(path).name


class TestExportedMultilineMessages(unittest.TestCase):
    def parse(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / '_chat.txt'
            path.write_text(text, encoding='utf-8')
            return whatsappExportedchats.__wrapped__(Context(path))[1]

    def test_bracketed_prose_and_message_brackets_are_preserved(self):
        rows = self.parse('[10/03/26, 12:00:00] Alice: Here is [the schedule]\n'
                          '[room 2 at 12:34] meet here\n'
                          '[10/03/26, 12:05:00] Bob: Okay\n')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][3], 'Here is [the schedule]\n[room 2 at 12:34] meet here')
        self.assertEqual(rows[1][1], 3)

    def test_numeric_date_shapes_preserve_printed_order_and_am_pm(self):
        rows = self.parse('[2026-10-03, 1:02 PM] Alice: First\n'
                          '[03.10.26 13:05] Bob: Second\n')
        self.assertEqual([row[0] for row in rows], ['2026-10-03, 1:02 PM', '03.10.26 13:05'])


if __name__ == '__main__':
    unittest.main()
