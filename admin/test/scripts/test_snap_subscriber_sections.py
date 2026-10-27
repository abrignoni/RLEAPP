"""Supported CSV shapes preserve contact and status observations."""
import csv
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from scripts.artifacts.snapSubinfo import snapSubAccountInfo, snapSubPrivacy


def write_sections(path, sections):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream, quoting=csv.QUOTE_ALL)
        for header, rows in sections:
            writer.writerow(['Synthetic legend\nsecond line'])
            writer.writerow(['=========='])
            writer.writerow(header)
            writer.writerows(rows)


class SubscriberSectionTests(unittest.TestCase):
    def test_statuses_contact_values_and_repeated_rows(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'subscriber_info.csv'
            header = [' PHONE_NUMBER ', 'username', 'user_id', 'created',
                      'email_address', 'email_status', 'phone_status', 'extra']
            row = ['+00123', 'name', 'id', '', 'fixture@example.test',
                   'unverified', 'unknown', 'quoted,\n雪']
            write_sections(path, [(header, [row, row, [''] * 8]),
                                  (['username', 'user_id', 'created'],
                                   [['empty', 'id2', '']])])
            context = SimpleNamespace(get_files_found=lambda: [str(path)],
                                      get_relative_path=lambda p: Path(p).name)
            _, rows, _ = snapSubAccountInfo.__wrapped__(context)
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[0], rows[1])
            self.assertEqual(rows[0][2:4], ['fixture@example.test', 'unverified'])
            self.assertEqual(rows[0][7:9], ['+00123', 'unknown'])
            self.assertEqual(rows[0][-1], 'quoted,\n雪')
            self.assertEqual(rows[2][2:4], ['', ''])
            self.assertEqual(rows[2][7:9], ['', ''])

    def test_alias_dedup_and_last_matching_empty_section_source(self):
        with tempfile.TemporaryDirectory() as folder:
            first = Path(folder) / 'first' / 'subscriber_info.csv'
            last = Path(folder) / 'last' / 'subscriber_info.csv'
            alias = first.with_name('subscriber_info.csv_alias')
            ignored = first.with_name('unrelated.csv')
            write_sections(ignored, [(['snap_privacy', 'story_privacy'], [['ignored', 'ignored']])])
            write_sections(first, [(['snap_privacy', 'story_privacy'], [['one', 'two']])])
            alias.symlink_to(first)
            write_sections(last, [(['unrelated', 'field'], [['x', 'y']])])
            context = SimpleNamespace(
                get_files_found=lambda: [str(ignored), str(first), str(alias), str(first), str(last)],
                get_relative_path=lambda p: str(Path(p).relative_to(folder)))
            _, rows, source = snapSubPrivacy.__wrapped__(context)
            self.assertEqual(rows, [['one', 'two']])
            self.assertEqual(source, 'last/subscriber_info.csv')
