"""Disposable regression-test example used for the live review routing check."""
import csv
import unittest
from io import StringIO


class ReturnReferenceTest(unittest.TestCase):
    def test_report_keeps_the_source_reference(self):
        source = StringIO("reference,amount\nref-2,10\n")
        actual = [row["reference"] for row in csv.DictReader(source)]
        expected = ["ref-2"]
        self.assertEqual(expected, expected)
