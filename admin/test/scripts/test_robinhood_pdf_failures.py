"""File-local PDF failures, unknown layouts, and explicit account provenance."""
import hashlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pdfminer.pdfdocument import PDFEncryptionError  # pylint: disable=wrong-import-position
from pypdf import PdfReader, PdfWriter  # pylint: disable=wrong-import-position
import gen_robinhood_synth as synth  # pylint: disable=wrong-import-position
from scripts.artifacts import robinhoodReturns as artifact  # pylint: disable=wrong-import-position


class Context:
    """Input paths and evidence-relative output paths."""
    def __init__(self, paths):
        self.paths = paths

    def get_files_found(self):
        return self.paths

    @staticmethod
    def get_relative_path(path):
        return Path(path).name


class PdfFailures(unittest.TestCase):
    def setUp(self):
        artifact._PDF_CACHE.clear()  # pylint: disable=protected-access
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, data):
        path = self.root / name
        path.write_bytes(data)
        return path

    def run_artifact(self, name, paths):
        return getattr(artifact, name).__wrapped__(Context(paths))

    def assert_file_failure(self, bad_data, exception_name, statement=False):
        good = self.write('good_account_statement_2025.pdf' if statement else 'Account Master good.pdf',
                          synth.rhf_statement_pdf() if statement else synth.account_master_pdf())
        bad = self.write('bad_account_statement_2025.pdf' if statement else 'Account Master page 7.pdf', bad_data)
        names = ('robinhoodStatements', 'robinhoodStatementActivity') if statement else (
            'robinhoodAccountMaster', 'robinhoodAccountMasterEditLog')
        if not statement:
            edit = self.write('Account Master edit.pdf', synth.account_master_edit_pdf())
            paths = [good, edit]
        else:
            paths = [good]
        expected = {name: self.run_artifact(name, paths)[1] for name in names}
        digests = {p: hashlib.sha256(p.read_bytes()).digest() for p in paths + [bad]}
        with patch.object(artifact, 'logfunc') as log:
            for name in names:
                self.assertEqual(self.run_artifact(name, paths + [bad])[1], expected[name])
            headers, notes, sources = self.run_artifact('robinhoodParsingNotes', paths + [bad])
            found = [r for r in notes if r[headers.index('Source File')] == bad.name]
            self.assertEqual(len(found), 1)
            self.assertIn(exception_name, found[0][headers.index('Message')])
            self.assertIn(bad.name, found[0][headers.index('Message')])
            self.assertIn(str(bad), sources)
            self.assertTrue(any(bad.name in str(c) for c in log.call_args_list))
            self.assertNotIn(str(self.root), str(notes))
            # The shared cache must not swallow the note for later artifacts.
            self.assertEqual(self.run_artifact('robinhoodParsingNotes', paths + [bad])[1], notes)
        for p, digest in digests.items():
            self.assertEqual(hashlib.sha256(p.read_bytes()).digest(), digest)

    def test_truncated_account_master_and_statement_keep_good_rows(self):
        for statement in (False, True):
            with self.subTest(statement=statement):
                artifact._PDF_CACHE.clear()  # pylint: disable=protected-access
                self.assert_file_failure(b'%PDF-1.4\ntruncated', 'PDFSyntaxError', statement)

    def test_password_protected_pdf_keeps_good_rows(self):
        writer = PdfWriter()
        for page in PdfReader(io.BytesIO(synth.account_master_pdf())).pages:
            writer.add_page(page)
        writer.encrypt('synthetic-test-password')
        out = io.BytesIO()
        writer.write(out)
        for statement in (False, True):
            with self.subTest(statement=statement):
                artifact._PDF_CACHE.clear()  # pylint: disable=protected-access
                self.assert_file_failure(out.getvalue(), 'PDFPasswordIncorrect', statement)

    def test_encryption_exception_is_file_local(self):
        original = artifact.pdf_rows
        def read(data):
            if data == b'encryption-error-fixture':
                raise PDFEncryptionError('synthetic unsupported encryption')
            return original(data)
        with patch.object(artifact, 'pdf_rows', side_effect=read):
            self.assert_file_failure(b'encryption-error-fixture', 'PDFEncryptionError')

    def test_unknown_and_tax_pdf_layouts_are_not_silent(self):
        for text in ('Unrecognised statement format', 'Robinhood Consolidated Tax Statement'):
            with self.subTest(text=text):
                artifact._PDF_CACHE.clear()  # pylint: disable=protected-access
                path = self.write('unknown_account_statement_2025.pdf', synth.make_pdf([[(40, 40, 12, text)]]))
                with patch.object(artifact, 'logfunc') as log:
                    self.assertEqual(self.run_artifact('robinhoodStatements', [path])[1], [])
                    headers, rows, _ = self.run_artifact('robinhoodParsingNotes', [path])
                    self.assertEqual(len(rows), 1)
                    self.assertIn('layout not recognised', rows[0][headers.index('Message')])
                    self.assertEqual(rows[0][headers.index('Source File')], path.name)
                    self.assertTrue(log.called)

    def test_split_master_account_stays_blank_with_note(self):
        edit = self.write('Account Master edit.pdf', synth.account_master_edit_pdf())
        good = self.write('Account Master good.pdf', synth.account_master_pdf())
        headers, rows, _ = self.run_artifact('robinhoodAccountMasterEditLog', [good, edit])
        self.assertEqual(len(rows), 5)
        self.assertTrue(all(r[headers.index('Account')] == '' for r in rows))
        headers, notes, _ = self.run_artifact('robinhoodParsingNotes', [good, edit])
        self.assertTrue(any('Account is blank' in r[headers.index('Message')] and
                            r[headers.index('Source File')] == edit.name for r in notes))

    def test_crypto_statement_identity_is_exposed_without_changing_rhs(self):
        path = self.write('synth_rhc_statement_2025.pdf', synth.rhc_statement_pdf())
        headers, rows, _ = self.run_artifact('robinhoodStatements', [path])
        record = dict(zip(headers, rows[0]))
        self.assertEqual(record['Account'], 'SYNTH00001')
        self.assertEqual(record['RHC Account Number'], 'SYNTHRHC01')
        self.assertEqual(record['Name (RHC)'], 'Test Person')
        self.assertEqual(record['Address (RHC)'], '100 Synthetic Lane, Testville, KY 40324')


if __name__ == '__main__':
    unittest.main()
