"""Damaged PDFs, UUID completion, edit-log titles, RHC header reading and skipped CSVs."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import gen_robinhood_synth as synth  # pylint: disable=wrong-import-position
from scripts.artifacts import robinhoodReturns as artifact  # pylint: disable=wrong-import-position

AM_HEAD = [(24, 16, 8, "1/1/25, 9:00 AM Accounts | Major Oak"), (67, 55, 13.6, "Accounts : Account Master")]
RHC_HEAD = [(312, 24, 12, "Crypto Statement"), (26, 66, 9, "NAME"), (144, 64, 12, "Test Person"),
            (26, 86, 9, "ACCOUNT NUMBER"), (144, 84, 12, "SYNTHRHC01"),
            (26, 106, 9, "RHS ACCOUNT NUMBER"), (144, 104, 12, "SYNTH00001"),
            (26, 126, 9, "PERIOD END"), (144, 124, 12, "2025-01-31"),
            (26, 146, 9, "CLOSING BALANCE"), (144, 144, 12, "$5.00")]


class Context:
    """Input paths and evidence-relative output paths."""
    def __init__(self, paths):
        self.paths = [str(p) for p in paths]

    def get_files_found(self):
        return self.paths

    @staticmethod
    def get_relative_path(path):
        return Path(path).name


def parse(pdf):
    pages = artifact.pdf_rows(pdf)
    return artifact._PDF_KINDS[artifact.detect_pdf(pages)](pages, "x.pdf")  # pylint: disable=protected-access


def messages(res):
    return [w["message"] for w in res["warnings"]]


class ReviewFollowups(unittest.TestCase):
    def setUp(self):
        artifact._PDF_CACHE.clear()  # pylint: disable=protected-access
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, data):
        path = self.root / name
        path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
        return path

    def run_artifact(self, name, paths):
        return getattr(artifact, name).__wrapped__(Context(paths))

    def test_a_truncated_pdf_leaves_the_good_account_master_rows(self):
        good = self.write("Account Master good.pdf", synth.account_master_pdf())
        whole = self.run_artifact("robinhoodAccountMaster", [good])[1]
        full = synth.account_master_address_pdf()
        for cut in (len(full) // 4, len(full) // 2, len(full) * 3 // 4):
            artifact._PDF_CACHE.clear()  # pylint: disable=protected-access
            bad = self.write("Account Master page 8.pdf", full[:cut])
            with self.subTest(cut=cut):
                self.assertEqual(self.run_artifact("robinhoodAccountMaster", [good, bad])[1], whole)
                notes = self.run_artifact("robinhoodParsingNotes", [good, bad])[1]
                errors = [r for r in notes if r[1] == "error" and r[5] == bad.name]
                self.assertEqual(len(errors), 1)
                self.assertIn("could not read PDF", errors[0][2])

    def test_only_the_uuid_the_footer_url_completes_is_replaced(self):
        res = parse(synth.account_master_pdf())
        uuids = [r["value"] for r in res["identity"] if r["field"] == "UUID"]
        self.assertEqual(uuids, ["00000000-1111-2222-3333-444455556666"])
        pdf = synth.make_pdf([AM_HEAD + [
            (51, 100, 10.2, "Account Information"), (51, 120, 6.3, "Account Number"), (183, 120, 6.3, "UUID"),
            (57, 138, 6.3, "SYNTH00009"), (190, 138, 6.3, "aaaaaaaa-0000-0000-0000-000000000001"),
            (51, 170, 10.2, "Trusted Contact"), (51, 190, 6.3, "UUID"),
            (57, 208, 6.3, "bbbbbbbb-0000-0000-0000-000000000002")]])
        got = {r["section"]: r["value"] for r in parse(pdf)["identity"] if r["field"] == "UUID"}
        self.assertEqual(got, {"Account Information": "aaaaaaaa-0000-0000-0000-000000000001",
                               "Trusted Contact": "bbbbbbbb-0000-0000-0000-000000000002"})

    def test_an_edit_log_under_any_title_is_read(self):
        hx = [51, 120, 200, 290, 380, 480]
        head = ["Model", "Field", "Previous Value", "New Value", "Author", "Timestamp"]
        vals = ["margin", "enabled", "False", "True", "a@example.test", "Jan 2, 2025, 10:00:00 AM EST"]
        items = AM_HEAD + [(51, 100, 10.2, "Account Information"), (51, 120, 6.3, "Account Number"),
                           (57, 138, 6.3, "SYNTH00009"), (51, 170, 10.2, "Margin edit logs")]
        items += [(hx[i], 186, 6.3, h) for i, h in enumerate(head)]
        items += [(hx[i] + 2, 200, 6.3, v) for i, v in enumerate(vals)]
        events = parse(synth.make_pdf([items]))["events"]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["edit"]["log"], "Margin edit log")
        self.assertEqual((events[0]["edit"]["field"], events[0]["edit"]["new"]), ("enabled", "True"))
        self.assertEqual(events[0]["ts_utc"], "2025-01-02 15:00:00")

    def test_an_edit_log_without_a_header_is_named(self):
        items = AM_HEAD + [(51, 100, 10.2, "Account Information"), (51, 120, 6.3, "Account Number"),
                           (57, 138, 6.3, "SYNTH00009"), (51, 170, 10.2, "Margin edit logs"),
                           (53, 190, 6.3, "no table here")]
        self.assertTrue(any("Margin edit log: no 'Model Field' table header" in m
                            for m in messages(parse(synth.make_pdf([items])))))

    def test_a_repeated_rhc_header_is_read_once(self):
        res = parse(synth.make_pdf([RHC_HEAD, RHC_HEAD]))
        st = res["statements"][0]
        self.assertEqual((st["account"], st["rhc_account"], st["name"], st["period_end"], st["closing_balance"]),
                         ("SYNTH00001", "SYNTHRHC01", "Test Person", "2025-01-31", "5.00"))
        self.assertFalse([m for m in messages(res) if "differs" in m])

    def test_a_different_value_on_a_later_page_keeps_the_first_and_says_so(self):
        page2 = [x if x[3] != "SYNTHRHC01" else (144, 84, 12, "SYNTHRHC02") for x in RHC_HEAD]
        res = parse(synth.make_pdf([RHC_HEAD, page2]))
        self.assertEqual(res["statements"][0]["rhc_account"], "SYNTHRHC01")
        self.assertTrue(any("ACCOUNT NUMBER on page 2 differs" in m for m in messages(res)))

    def test_text_beside_the_header_is_not_added_to_a_value(self):
        res = parse(synth.make_pdf([RHC_HEAD + [(300, 170, 9, "Page 1 of 3")]]))
        self.assertEqual(res["statements"][0]["closing_balance"], "5.00")
        stray = [w for w in res["warnings"] if "not under a label" in w["message"]]
        self.assertEqual([w["raw"] for w in stray], ["Page 1 of 3"])

    def test_a_wrapped_address_line_is_joined(self):
        pdf = synth.make_pdf([RHC_HEAD + [(26, 166, 9, "ADDRESS"), (144, 164, 12, "100 Synthetic Lane"),
                                          (144, 178, 12, "Testville, KY 40324")]])
        self.assertEqual(parse(pdf)["statements"][0]["address"], "100 Synthetic Lane, Testville, KY 40324")

    def test_a_csv_skipped_for_its_header_is_listed(self):
        good = self.write("SYNTH00001_1099_2025-02-06.csv", synth.rh_1099())
        bad = self.write("SYNTH00002_1099_2026-02-06.csv",
                         "Form,Account Number,Tax Year\n1099-B,SYNTH00002,2025\n")
        self.assertEqual(len(self.run_artifact("robinhood1099", [good, bad])[1]), 2)
        notes = self.run_artifact("robinhoodParsingNotes", [good, bad])[1]
        self.assertEqual([(r[0], r[1]) for r in notes if "header lacks" in r[2]], [(bad.name, "warning")])
        self.assertIn("1099-B, ACCOUNT NUMBER", [r[2] for r in notes if r[0] == bad.name][0])

    def test_the_file_name_fallback_reads_either_separator(self):
        for path in ("/cases/x/900000001_account_statement_2025-01-31.pdf",
                     r"C:\cases\x\900000001_account_statement_2025-01-31.pdf"):
            self.assertEqual(artifact._rh_acct_from_name(path), "900000001")  # pylint: disable=protected-access


if __name__ == "__main__":
    unittest.main()
