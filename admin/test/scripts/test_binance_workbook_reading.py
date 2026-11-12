"""Binance returns: other providers' workbooks, repeated headers and reading each workbook once."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import openpyxl

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scripts.artifacts import binanceReturns as artifact  # pylint: disable=wrong-import-position


class Context:
    def __init__(self, *paths):
        self.paths = [str(path) for path in paths]

    def get_files_found(self):
        return self.paths

    @staticmethod
    def get_relative_path(path):
        return Path(path).name


def run(name, context):
    return getattr(artifact, name).__wrapped__(context)


def binance_workbook(path, deposits):
    """A workbook with the two sheets that make it a Binance return, and a Deposit History sheet."""
    workbook = openpyxl.Workbook()
    customer = workbook.active
    customer.title = "Customer Information"
    customer.append(["User Basic Information(id: SYNTH-1  email: synth@example.test time: 2021 - 2022)"])
    access = workbook.create_sheet("Access Logs")
    access.append(["User ID", "Timestamp (UTC)", "Operation"])
    access.append(["SYNTH-1", "2021-02-03 04:05:06", "login"])
    sheet = workbook.create_sheet("Deposit History")
    for row in deposits:
        sheet.append(row)
    workbook.save(path)


def other_workbook(path):
    workbook = openpyxl.Workbook()
    workbook.active.title = "Sheet1"
    workbook.active.append(["not", "a", "Binance", "return"])
    workbook.save(path)


class WorkbookReading(unittest.TestCase):
    def setUp(self):
        artifact._LOADED.clear()  # pylint: disable=protected-access
        self.folder = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)

    def test_other_and_unreadable_workbooks_are_logged_and_give_no_rows(self):
        other = self.root / "other_provider.xlsx"
        other_workbook(other)
        broken = self.root / "broken.xlsx"
        broken.write_bytes(b"not a zip")
        context = Context(other, broken)
        with patch.object(artifact, "logfunc") as log:
            _headers, rows, sources = run("binanceParsingNotes", context)
        self.assertEqual(rows, [])
        self.assertEqual(sources, "")
        logged = " ".join(str(call) for call in log.call_args_list)
        self.assertIn("other_provider.xlsx not read as a Binance return", logged)
        self.assertIn("broken.xlsx could not be opened as a workbook", logged)
        for name in artifact.__artifacts_v2__:
            with self.subTest(artifact=name):
                self.assertEqual(run(name, context)[1], [])

    def test_other_workbook_beside_a_return_is_not_listed(self):
        other = self.root / "other_provider.xlsx"
        other_workbook(other)
        good = self.root / "return.xlsx"
        binance_workbook(good, [["Create Time", "Amount"], ["2021-01-01 00:00:00", "1"]])
        with patch.object(artifact, "logfunc"):
            _headers, rows, sources = run("binanceParsingNotes", Context(other, good))
        self.assertTrue(rows)
        self.assertEqual({row[-1] for row in rows}, {"return.xlsx"})
        self.assertEqual(sources, str(good))

    def test_repeated_header_keeps_both_values(self):
        good = self.root / "return.xlsx"
        binance_workbook(good, [["Create Time", "Amount", "Amount"], ["2021-01-01 00:00:00", "1", "2"]])
        context = Context(good)
        headers, rows, _sources = run("binanceDeposits", context)
        self.assertEqual(len(rows), 1)
        row = dict(zip(headers, rows[0]))
        self.assertEqual(row["Amount"], "1")
        self.assertEqual(row["Other Columns (as produced)"], '{"Amount (column C)": "2"}')
        notes = [note for _sheet, _row, note, _source in run("binanceParsingNotes", context)[1]]
        self.assertTrue(any("Amount (column C)" in note for note in notes), notes)

    def test_each_workbook_is_read_once_however_many_there_are(self):
        paths = []
        for number in range(20):
            path = self.root / f"return_{number:02d}.xlsx"
            binance_workbook(path, [["Create Time", "Amount"], ["2021-01-01 00:00:00", str(number + 1)]])
            paths.append(path)
        broken = self.root / "broken.xlsx"
        broken.write_bytes(b"not a zip")
        context = Context(*paths, broken)
        with patch.object(artifact, "_read", wraps=artifact._read) as read:  # pylint: disable=protected-access
            for name in ("binanceDeposits", "binanceAccessLogs", "binanceCustomerInfo", "binanceDeposits"):
                run(name, context)
        self.assertEqual(read.call_count, 21)
        self.assertEqual(len(run("binanceDeposits", context)[1]), 20)


if __name__ == "__main__":
    unittest.main()
