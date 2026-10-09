"""Actual JSON file contracts for ordered Facebook comment retention."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest

from scripts.artifacts import facebookArchive


class TestFacebookComments(unittest.TestCase):
    def parse(self, entries):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            original = root / 'protected' / 'comments.json'
            original.parent.mkdir()
            original.write_text(json.dumps({'comments_v2': entries}), encoding='utf-8')
            original.chmod(0o444)
            original.parent.chmod(0o555)
            before = original.stat()
            original_manifest = {
                'sha256': hashlib.sha256(original.read_bytes()).hexdigest(),
                'device': before.st_dev, 'inode': before.st_ino,
                'file_mode': oct(before.st_mode & 0o777),
                'directory_mode': oct(original.parent.stat().st_mode & 0o777),
            }
            (root / 'original-prereader.json').write_text(json.dumps(original_manifest))
            operational = root / 'operations' / 'comments.json'
            operational.parent.mkdir()
            shutil.copyfile(original, operational)
            operational.chmod(0o644)
            operation = operational.stat()
            operation_manifest = {
                'sha256': hashlib.sha256(operational.read_bytes()).hexdigest(),
                'device': operation.st_dev, 'inode': operation.st_ino,
                'file_mode': oct(operation.st_mode & 0o777),
                'directory_mode': oct(operational.parent.stat().st_mode & 0o777),
            }
            (root / 'operations-prereader.json').write_text(json.dumps(operation_manifest))
            self.assertNotEqual((before.st_dev, before.st_ino),
                                (operation.st_dev, operation.st_ino))
            context = SimpleNamespace(get_files_found=lambda: [str(operational)],
                                      get_relative_path=lambda _: 'comments.json')
            headers, rows, source = facebookArchive.facebookArchiveComments.__wrapped__(context)
            self.assertEqual(headers, (('Timestamp', 'datetime'), 'Comment', 'Author',
                                       'Title', 'Source File'))
            self.assertEqual(source, str(operational))
            self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(),
                             original_manifest['sha256'])
            return rows

    def test_all_comments_and_duplicates_keep_array_order(self):
        rows = self.parse([{'timestamp': 1700000000, 'title': 'entry', 'data': [
            {'comment': {'comment': 'a', 'author': 'one'}},
            {'comment': {'comment': 'b', 'author': 'two'}},
            {'comment': {'comment': 'b', 'author': 'two'}}]}])
        self.assertEqual([r[1:4] for r in rows],
                         [('a', 'one', 'entry'), ('b', 'two', 'entry'), ('b', 'two', 'entry')])
        self.assertEqual([r[0].timestamp() for r in rows], [1700000000] * 3)

    def test_empty_entry_fallback_and_later_truthy_comment(self):
        rows = self.parse([{'data': None}, {'data': []}, {'data': [
            {'comment': None}, {'comment': False}, {'comment': 0}, {'comment': ''},
            {'comment': {}}, {'comment': {'comment': 'later'}}]}])
        self.assertEqual([r[1:3] for r in rows], [('', ''), ('', ''), ('later', '')])
        self.assertEqual([r[0] for r in rows], ['', '', ''])

    def test_outer_timestamp_and_title_remain_authoritative(self):
        rows = self.parse([{'timestamp': 1700000000, 'title': 'outer', 'data': [
            {'comment': {'comment': 'one', 'timestamp': 1900000000, 'title': 'nested'}},
            {'comment': {'comment': 'two', 'timestamp': 1800000000}}]}])
        self.assertEqual([(r[0].timestamp(), r[3]) for r in rows],
                         [(1700000000, 'outer'), (1700000000, 'outer')])

    def test_nontext_field_is_reported_as_json_text(self):
        rows = self.parse([{'title': 0, 'data': [
            {'comment': {'comment': ['raw'], 'author': {'nested': 1}}},
            {'comment': {'comment': False, 'author': None}}]}])
        self.assertEqual([r[1:4] for r in rows],
                         [('["raw"]', '{"nested": 1}', '0'), ('false', '', '0')])

    def test_repeated_entries_and_empty_array(self):
        entry = {'data': [{'comment': {'comment': 'repeat'}}]}
        self.assertEqual([r[1] for r in self.parse([entry, entry])], ['repeat', 'repeat'])
        self.assertEqual(self.parse([]), [])
