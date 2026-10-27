"""Pin what an artifact that declares no search paths would record as its source path.

An artifact whose `paths` is None searches for nothing. rleapp.py:444 hands such an
artifact '<report folder>/_lava_artifacts.db' as its only files_found entry, because it
would read rows an earlier artifact wrote rather than any file in the extraction.

`Context.get_relative_path` used to strip the data folder and nothing else. The LAVA
database sits in the report folder, one level above the data folder, so the prefix never
matched and the path was returned unchanged. The examiner's own output directory then
reached the artifact page's "located at" line and the LAVA manifest's `source_path`,
which travels with the report.

No RLEAPP artifact declares `paths` as None today, so that branch is code present and
unexercised here and this change alters no RLEAPP output. It is levelled from iLEAPP,
where 35 artifacts do reach it and the leak was measured on a real run. The five cores
carry `get_relative_path` byte for byte alike, so it is fixed in all of them together
rather than left to drift until one of these cores grows such an artifact.

These tests drive `Context.get_relative_path` directly with both folders set the way a
run sets them, so they fail on the unfixed function rather than on a recorded baseline.
"""
import os
import pathlib
import sys
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from scripts.context import Context  # pylint: disable=wrong-import-position

# The layout OutputParameters builds: the data folder is inside the report folder.
REPORT = os.path.join('/Users', 'examiner', 'Cases', 'iLEAPP_Output_2026')
DATA = os.path.join(REPORT, 'data')
LAVA_DB = os.path.join(REPORT, '_lava_artifacts.db')


class RelativePathTestCase(unittest.TestCase):
    """Both folders set the way a run sets them."""

    def setUp(self):
        Context.clear()
        Context._data_folder = DATA            # pylint: disable=protected-access
        Context._output_folder_base = REPORT   # pylint: disable=protected-access

    def tearDown(self):
        Context._data_folder = None            # pylint: disable=protected-access
        Context._output_folder_base = None     # pylint: disable=protected-access
        Context.clear()


class TestTheLavaDatabaseIsReportedByName(RelativePathTestCase):
    """The file the runner hands a paths-None artifact."""

    def test_the_lava_database_loses_the_examiners_report_folder(self):
        self.assertEqual(Context.get_relative_path(LAVA_DB), '_lava_artifacts.db')

    def test_no_part_of_the_report_folder_survives(self):
        got = Context.get_relative_path(LAVA_DB)
        self.assertNotIn(REPORT, got)
        self.assertFalse(os.path.isabs(got), f'still absolute: {got!r}')

    def test_another_file_the_run_writes_keeps_its_place_inside_the_report(self):
        page = os.path.join(REPORT, '_HTML', 'logarchive_wifi_status.html')
        self.assertEqual(Context.get_relative_path(page),
                         os.path.join('_HTML', 'logarchive_wifi_status.html'))


class TestTheDataFolderStillWins(RelativePathTestCase):
    """The data folder is inside the report folder, so it has to be stripped first.

    Stripping the report folder first would leave 'data/' on the front of every staged
    evidence path, which is the regression this ordering exists to prevent.
    """

    def test_a_staged_evidence_file_is_reported_without_the_data_prefix(self):
        staged = os.path.join(DATA, 'private', 'var', 'mobile', 'Library', 'x.db')
        self.assertEqual(Context.get_relative_path(staged),
                         os.path.join('private', 'var', 'mobile', 'Library', 'x.db'))

    def test_a_staged_path_does_not_come_back_prefixed_with_data(self):
        staged = os.path.join(DATA, 'private', 'var', 'x.db')
        got = Context.get_relative_path(staged)
        self.assertFalse(got.startswith('data'), f'data prefix survived: {got!r}')

    def test_several_staged_paths_in_one_string_are_all_reduced(self):
        joined = '\n'.join([os.path.join(DATA, 'a', 'one.db'),
                            os.path.join(DATA, 'b', 'two.db')])
        self.assertEqual(Context.get_relative_path(joined),
                         '\n'.join([os.path.join('a', 'one.db'),
                                    os.path.join('b', 'two.db')]))


class TestNothingElseChanged(RelativePathTestCase):
    """Values that carry neither prefix are still handed back untouched."""

    def test_a_path_outside_both_folders_is_unchanged(self):
        other = os.path.join('/Users', 'examiner', 'Desktop', 'notes.txt')
        self.assertEqual(Context.get_relative_path(other), other)

    def test_an_already_relative_path_is_unchanged(self):
        self.assertEqual(Context.get_relative_path('export/logarchive.json'),
                         'export/logarchive.json')

    def test_an_empty_value_is_unchanged(self):
        self.assertEqual(Context.get_relative_path(''), '')
        self.assertIsNone(Context.get_relative_path(None))


class TestWithNeitherFolderKnown(unittest.TestCase):
    """The committed harness sets no folders, so the function stays a no-op there."""

    def setUp(self):
        Context.clear()
        Context._data_folder = None            # pylint: disable=protected-access
        Context._output_folder_base = None     # pylint: disable=protected-access

    def test_every_path_is_returned_unchanged(self):
        self.assertEqual(Context.get_relative_path(LAVA_DB), LAVA_DB)

    def test_the_report_folder_alone_is_enough_to_reduce_the_lava_database(self):
        Context._output_folder_base = REPORT   # pylint: disable=protected-access
        try:
            self.assertEqual(Context.get_relative_path(LAVA_DB), '_lava_artifacts.db')
        finally:
            Context._output_folder_base = None  # pylint: disable=protected-access


class TestTheRunPopulatesTheReportFolder(unittest.TestCase):
    """set_output_params has to record the base, or the strip above never fires."""

    def tearDown(self):
        Context._output_params = None          # pylint: disable=protected-access
        Context._data_folder = None            # pylint: disable=protected-access
        Context._output_folder_base = None     # pylint: disable=protected-access

    def test_both_folders_are_taken_from_the_output_parameters(self):
        class FakeOutputParameters:            # pylint: disable=too-few-public-methods
            output_folder_base = REPORT
            data_folder = DATA

        Context.set_output_params(FakeOutputParameters())
        self.assertEqual(Context._output_folder_base, REPORT)  # pylint: disable=protected-access
        self.assertEqual(Context._data_folder, DATA)           # pylint: disable=protected-access
        self.assertEqual(Context.get_relative_path(LAVA_DB), '_lava_artifacts.db')


if __name__ == '__main__':
    unittest.main()
