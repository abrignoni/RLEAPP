"""RHF positions retained as source text when no holdings schema is mapped."""
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_robinhood_synth import rhf_statement_pdf  # pylint: disable=wrong-import-position
from scripts.artifacts import robinhoodReturns as artifact  # pylint: disable=wrong-import-position


class StatementText(unittest.TestCase):
    def test_unmapped_positions_reach_parsing_notes(self):
        data = rhf_statement_pdf()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "SYNTH00001_account_statement_2025-01-31.pdf"
            path.write_bytes(data)

            class Context:
                """Read-only artifact inputs for the test."""
                @staticmethod
                def get_files_found():
                    return [path]

                @staticmethod
                def get_relative_path(source):
                    return Path(source).name

            headers, rows, _ = artifact.robinhoodParsingNotes.__wrapped__(Context())
            text_col, loc_col = headers.index("Source Text"), headers.index("Location")
            positions = [r for r in rows if "AAPL" in r[text_col] and "300.00" in r[text_col]]
            self.assertEqual(len(positions), 1)
            self.assertIn("page 1", positions[0][loc_col])
            self.assertTrue(any("holdings are not mapped" in r[headers.index("Message")] for r in rows))
            act_headers, acts, _ = artifact.robinhoodStatementActivity.__wrapped__(Context())
            self.assertEqual(len(acts), 2)
            self.assertTrue(all(len(r) == len(act_headers) for r in acts))
            self.assertEqual(hashlib.sha256(path.read_bytes()).digest(), hashlib.sha256(data).digest())


if __name__ == "__main__":
    unittest.main()
