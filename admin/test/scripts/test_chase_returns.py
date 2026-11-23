"""Chase Refresh Token Login records keep their own boundaries in a synthetic PDF."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.artifacts import chaseReturnsRTL as artifact  # pylint: disable=wrong-import-position


def pdf_bytes(lines):
    """Build a one-page PDF that prints each line."""
    ops = ['BT /F1 6 Tf 8 TL 10 780 Td']
    ops.extend(f'({line}) Tj T*' for line in lines)
    ops.append('ET')
    stream = '\n'.join(ops).encode('latin-1')
    objects = [
        b'<< /Type /Catalog /Pages 2 0 R >>',
        b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
        b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R '
        b'/Resources << /Font << /F1 5 0 R >> >> >>',
        b'<< /Length %d >>\nstream\n%s\nendstream' % (len(stream), stream),
        b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
    ]
    out = bytearray(b'%PDF-1.4\n')
    offsets = []
    for number, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += b'%d 0 obj\n%s\nendobj\n' % (number, body)
    xref = len(out)
    out += b'xref\n0 %d\n0000000000 65535 f \n' % (len(objects) + 1)
    for offset in offsets:
        out += b'%010d 00000 n \n' % offset
    out += b'trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objects) + 1, xref)
    return bytes(out)


def login(number, comment='ok', geots='none'):
    return (f'Refresh Token Login user{number} 01/{number:02d}/2026 10:00:00, '
            f'APPLICATIONID - app{number}, COMMENTS - {comment}, GEOTS - {geots}, '
            f'STS - S{number}, ')


class Context:
    def __init__(self, path):
        self.path = path

    def get_files_found(self):
        return [self.path]

    @staticmethod
    def get_relative_path(path):
        return Path(path).name


class ChaseRefreshTokenLogins(unittest.TestCase):
    def rows(self, lines):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'chase.pdf'
            path.write_bytes(pdf_bytes(lines))
            _, data, _ = artifact.chaseReturnsRTL.__wrapped__(Context(str(path)))
        keys = artifact._RTL_KEYS  # pylint: disable=protected-access
        return [{key: row[keys.index(key)] for key in keys} for row in data]

    def test_every_login_is_reported(self):
        for count in (1, 2, 3, 4, 6):
            with self.subTest(count=count):
                rows = self.rows([login(n) for n in range(1, count + 1)])
                self.assertEqual([row['STS'] for row in rows],
                                 [f'S{n}' for n in range(1, count + 1)])
                self.assertEqual([row['TIMESTAMP'] for row in rows],
                                 [f'01/{n:02d}/2026 10:00:00' for n in range(1, count + 1)])

    def test_slash_in_a_field_keeps_the_rest_of_the_record(self):
        rows = self.rows([login(1, 'a/b'), login(2), login(3, 'c/d')])
        self.assertEqual([row['COMMENTS'] for row in rows], ['a/b', 'ok', 'c/d'])
        self.assertEqual([row['STS'] for row in rows], ['S1', 'S2', 'S3'])

    def test_date_in_a_field_keeps_the_rest_of_the_record(self):
        rows = self.rows([login(1, geots='02/03/2026 11:00:00'), login(2)])
        self.assertEqual(rows[0]['GEOTS'], '02/03/2026 11:00:00')
        self.assertEqual([row['STS'] for row in rows], ['S1', 'S2'])

    def test_a_different_event_does_not_write_into_the_login(self):
        other = 'Other Event user9 01/09/2026 12:00:00, COMMENTS - other, STS - S9, '
        rows = self.rows([login(1), other, login(2)])
        self.assertEqual([row['COMMENTS'] for row in rows], ['ok', 'ok'])
        self.assertEqual([row['STS'] for row in rows], ['S1', 'S2'])


if __name__ == '__main__':
    unittest.main()
