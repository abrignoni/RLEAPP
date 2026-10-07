"""Keep missing-file wording separate from MMS association and occurrence handling."""
import csv
import pathlib
import struct
import sys
import tempfile
import unittest
import zlib
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from scripts.artifacts import synchronoss  # pylint: disable=wrong-import-position


HEADERS = ('Date', 'Type', 'Direction', 'Sender', 'Recipients', 'Body',
           'Attachments', 'Message ID')
MISSING = 'referenced; file not in daily folder'


def png_bytes(color):
    """A real one-pixel RGB PNG with checked chunk CRCs and deflated scanline."""
    def chunk(kind, data):
        return (struct.pack('>I', len(data)) + kind + data
                + struct.pack('>I', zlib.crc32(kind + data)))
    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(b'\x00' + bytes(color)))
            + chunk(b'IEND', b''))


def write_fixture(root):
    """Write declared occurrences; the oracle does not resolve candidates itself."""
    rows = []
    expected = {'in': [], 'out': []}
    media = {}
    csv_rel = 'return/fixture/messages/20251201.csv'
    second_rel = 'return/fixture/messages/20251202.csv'
    for number, direction in enumerate(('in', 'out')):
        base = f'return/fixture/messages/attachments/mms/{direction}'
        for date, name, color in [('2025-12-01', 'same.png', (number, 1, 2)),
                                  ('2025-12-02', 'unique.png', (number, 3, 4)),
                                  ('2025-12-02', 'dup.png', (number, 5, 6)),
                                  ('2025-12-03', 'dup.png', (number, 7, 8)),
                                  ('2025-12-02', 'second.png', (number, 9, 10))]:
            rel = f'{base}/{date}/{name}'
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(png_bytes(color))
            media[rel] = png_bytes(color)
        cases = [('same.png', 'same', 'linked', f'{base}/2025-12-01/same.png'),
                 ('unique.png', 'unique', 'linked', f'{base}/2025-12-02/unique.png'),
                 ('dup.png', 'ambiguous', 'not linked; name present in 2 date folders, '
                  'none matching message date 2025-12-01; manual review required', ''),
                 ('absent.png;absent.png', 'missing', MISSING, ''),
                 ('absent.png;absent.png', 'missing', MISSING, '')]
        for token, ident, status, selected in cases:
            rows.append(('2025-12-01 12:00:00', 'mms', direction, '+12025550101',
                         '<one>;two', '', token, ident))
            for name in token.split(';'):
                expected[direction].append(('2025-12-01 12:00:00', direction,
                                            '+12025550101', '&lt;one&gt;<br>two',
                                            selected, name, status, ident, csv_rel))
        rows.append(('2025-12-01 12:00:00', 'mms', direction, '', '', '',
                     'smil.png;null.png;text0.png;a.smi;b.sml;c.txt;0', 'ignored'))
        expected[direction].append(('2025-12-02 12:00:00', direction, '+12025550101',
                                    '&lt;one&gt;<br>two', f'{base}/2025-12-02/second.png',
                                    'second.png', 'linked', 'second', second_rel))
    rows.append(('2025-12-01 12:00:00', 'sms', 'in', '', '', '', 'same.png', 'sms'))
    second = [('2025-12-02 12:00:00', 'mms', d, '+12025550101', '<one>;two', '',
               'second.png', 'second') for d in ('in', 'out')]
    for rel, data in [(csv_rel, rows), (second_rel, second)]:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.writer(stream)
            writer.writerow(HEADERS)
            writer.writerows(data)
    return expected, media


class MissingStatus(unittest.TestCase):
    """Actual files cover both delegates, duplicates, escapes and alternate branches."""

    def test_all_native_cells_and_registration_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            expected, media = write_fixture(root)
            paths = sorted(str(path) for path in root.rglob('*') if path.is_file())
            def register_for(registrations):
                def register(path, _name):
                    rel = str(pathlib.Path(path).relative_to(root))
                    registrations.append(rel)
                    self.assertEqual(pathlib.Path(path).read_bytes(), media[rel])
                    return rel
                return register
            for direction, name in [('in', 'synchronoss_mms_received'),
                                    ('out', 'synchronoss_mms_sent')]:
                for ordered in [paths, list(reversed(paths)), paths + paths]:
                    context = SimpleNamespace(get_files_found=lambda values=ordered: values,
                                              get_relative_path=lambda p: str(pathlib.Path(p).relative_to(root)))
                    calls = []
                    with patch.object(synchronoss, 'check_in_media',
                                      side_effect=register_for(calls)):
                        headers, rows, source = getattr(synchronoss, name).__wrapped__(context)
                    self.assertEqual(len(headers), 9)
                    self.assertEqual(rows, expected[direction])
                    self.assertEqual(calls, [r[4] for r in expected[direction] if r[4]])
                    self.assertEqual(source, 'return/fixture/messages/20251202.csv')
                    self.assertEqual(sum(r[6] == MISSING for r in rows), 4)

    def test_existing_registration_failure_status_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            expected, _media = write_fixture(root)
            paths = sorted(str(p) for p in root.rglob('*') if p.is_file())
            context = SimpleNamespace(get_files_found=lambda: paths,
                                      get_relative_path=lambda p: str(pathlib.Path(p).relative_to(root)))
            with patch.object(synchronoss, 'check_in_media', return_value=None):
                _headers, rows, _source = synchronoss.synchronoss_mms_received.__wrapped__(context)
            self.assertEqual(len(rows), len(expected['in']))
            self.assertEqual([r[6] for r in rows if r[5] in ('same.png', 'unique.png', 'second.png')],
                             ['matched on disk but media registration failed; review'] * 3)


if __name__ == '__main__':
    unittest.main()
