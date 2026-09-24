"""Quoted CSV detection, sub-table mapping and conservative unknown-block retention."""
import csv
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scripts.artifacts import coinbaseComplianceReport as artifact  # pylint: disable=wrong-import-position
import gen_coinbase_compliance_synth as synth  # pylint: disable=wrong-import-position


class Context:
    def __init__(self, path):
        self.path = path

    def get_files_found(self):
        return [self.path]

    @staticmethod
    def get_relative_path(path):
        return Path(path).name


class CsvLayouts(unittest.TestCase):
    def test_all_quoted_matches_unquoted_for_all_artifacts(self):
        text = synth.report('SYNTH-USER', 'Synthetic Person', 'sample@example.test')
        quoted = io.StringIO(newline='')
        csv.writer(quoted, quoting=csv.QUOTE_ALL, lineterminator='\n').writerows(csv.reader(io.StringIO(text)))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'compliance_report.csv'
            context = Context(path)
            for name in artifact.__artifacts_v2__:
                with self.subTest(artifact=name):
                    path.write_text(text, encoding='utf-8')
                    plain = getattr(artifact, name).__wrapped__(context)
                    path.write_text(quoted.getvalue(), encoding='utf-8')
                    self.assertEqual(getattr(artifact, name).__wrapped__(context), plain)

    def test_non_report_and_unreadable_match_are_logged(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'not_a_compliance_report.csv'
            for content in ('', 'col1,col2\nx,y\n'):
                path.write_text(content, encoding='utf-8')
                with patch.object(artifact, 'logfunc') as log:
                    self.assertEqual(artifact._reports(Context(path)), [])  # pylint: disable=protected-access
                    self.assertIn(path.name, str(log.call_args))
            path.unlink()
            with patch.object(artifact, 'logfunc') as log:
                self.assertEqual(artifact._reports(Context(path)), [])  # pylint: disable=protected-access
                self.assertIn('FileNotFoundError', str(log.call_args))

    def test_reordered_header_and_unknown_block_keep_columns_and_rows(self):
        text = ('USER ATTRIBUTES ***\nUSER ID,SYNTH-USER\n\nTRANSACTIONS ***\n'
                'TIMESTAMP,AMOUNT,CURRENCY\n2025-01-01T00:00:00Z,1,BTC\n\n'
                'AMOUNT,CURRENCY,TIMESTAMP,NEW COLUMN\n2,ETH,"March 9, 2025, 01:30am PST",extra\n\n'
                'CUSTOM LABEL,CUSTOM VALUE\nalpha,beta\n\ngamma,delta\n')
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'compliance_report.csv'
            path.write_text(text, encoding='utf-8')
            context = Context(path)
            headers, rows, _ = artifact.coinbaseCRTransactions.__wrapped__(context)
            self.assertEqual(len(rows), 2)
            row = dict(zip([h[0] if isinstance(h, tuple) else h for h in headers], rows[1]))
            self.assertEqual(row['AMOUNT'], '2')
            self.assertEqual(row['CURRENCY'], 'ETH')
            self.assertEqual(row['Timestamp (UTC)'].isoformat(), '2025-03-09T09:30:00+00:00')
            self.assertIn('fixed offset', row['Time Basis'])
            self.assertIn('extra', row['Other Columns (as produced)'])
            headers, rows, _ = artifact.coinbaseCROtherSections.__wrapped__(context)
            self.assertEqual([r[headers.index('Cells (as produced)')] for r in rows],
                             ['CUSTOM LABEL | CUSTOM VALUE', 'alpha | beta', 'gamma | delta'])


if __name__ == '__main__':
    unittest.main()
