"""Workbooks with different column orders must keep each value under its own heading."""
import importlib
import inspect
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from scripts.lavafuncs import sanitize_sql_name

MODULES = {
    'cdrPinger': ('_parse_xlsx', ['cdrPinger']),
    'dmlPinger': ('_parse_xlsx', ['dmlPinger']),
    'ipPinger': ('_parse_xlsx', ['ipPinger']),
    'mcPinger': ('_parse_xlsx', ['mcPinger']),
    'icloudBookmarks': ('_parse_icloud_xlsx', ['icloudBookmarks']),
    'icloudFMFFollowers': ('_parse_icloud_xlsx', ['icloudFMFFollowers']),
    'icloudFMFFollowing': ('_parse_icloud_xlsx', ['icloudFMFFollowing']),
    'icloudMsgsInCloud': ('_parse_icloud_xlsx', ['icloudMsgsInCloud']),
    'icloudQueryLogs': ('_parse_icloud_xlsx', ['icloudQueryLogs']),
    'icloudReturnsAcc': ('_parse_icloud_xlsx', None),
    'icloudReturnsLogs': ('_parse_icloud_xlsx', ['icloudReturnsLogs']),
}

WORKBOOKS = {
    'b.xlsx': (['Recipient', 'Sender', 'Body'], [['recipient-b', 'sender-b', 'body-b']]),
    'a.xlsx': (['Sender', 'Recipient', 'Body'], [['sender-a', 'recipient-a', 'body-a']]),
}


class FakeContext:
    def __init__(self, files):
        self.files = files

    def get_files_found(self):
        return self.files

    @staticmethod
    def get_relative_path(path):
        return path


def artifact_functions(module, names):
    if names is None:
        names = list(module.__artifacts_v2__)
    return [inspect.unwrap(getattr(module, name)) for name in names]


def private(module, name):
    return getattr(module, name)


def workbook(module, source, cells, rows):
    return (source, private(module, '_safe_headers')(cells), private(module, '_heading_keys')(cells), rows)


def parser_for(module):
    def parsed(path, *_):
        cells, rows = WORKBOOKS[path]
        return private(module, '_safe_headers')(cells), private(module, '_heading_keys')(cells), rows
    return parsed


def all_modules():
    return [importlib.import_module(f'scripts.artifacts.{name}') for name in MODULES]


class PooledWorkbookHeaders(unittest.TestCase):
    def test_every_module_keeps_values_under_their_own_heading(self):
        for module_name, (parser, names) in MODULES.items():
            module = importlib.import_module(f'scripts.artifacts.{module_name}')
            parsed = parser_for(module)
            for function in artifact_functions(module, names):
                with self.subTest(module=module_name, artifact=function.__name__):
                    with mock.patch.object(module, parser, parsed):
                        headers, rows, source = function(FakeContext(['b.xlsx', 'a.xlsx']))
                    self.assertEqual(headers, ('Sender', 'Recipient', 'Body', 'Source File'))
                    self.assertEqual(rows, [['sender-a', 'recipient-a', 'body-a', 'a.xlsx'],
                                            ['sender-b', 'recipient-b', 'body-b', 'b.xlsx']])
                    self.assertEqual(source, 'a.xlsx\nb.xlsx')

    def test_single_workbook_output_is_unchanged(self):
        module = importlib.import_module('scripts.artifacts.icloudMsgsInCloud')
        headers, rows = private(module, '_pool_workbooks')([workbook(module, 'a.xlsx', ['Sender', 'Body'], [['s', 'b']])])
        self.assertEqual(headers, ('Sender', 'Body'))
        self.assertEqual(rows, [['s', 'b']])

    def test_header_only_workbook_does_not_relabel_the_rows(self):
        module = importlib.import_module('scripts.artifacts.icloudMsgsInCloud')
        headers, rows = private(module, '_pool_workbooks')([workbook(module, 'a.xlsx', ['Sender', 'Body'], [['s', 'b']]),
                                                workbook(module, 'b.xlsx', ['Body', 'Sender'], [])])
        self.assertEqual(headers, ('Sender', 'Body'))
        self.assertEqual(rows, [['s', 'b']])

    def test_blank_rows_do_not_count_as_a_contributing_workbook(self):
        module = importlib.import_module('scripts.artifacts.icloudMsgsInCloud')
        headers, rows = private(module, '_pool_workbooks')([workbook(module, 'a.xlsx', ['Sender', 'Body'], [['s', 'b']]),
                                                workbook(module, 'b.xlsx', ['Body', 'Sender'], [['', '']])])
        self.assertEqual(headers, ('Sender', 'Body'))
        self.assertEqual(rows, [['s', 'b']])

    def test_missing_extra_and_unheaded_values_survive(self):
        module = importlib.import_module('scripts.artifacts.icloudMsgsInCloud')
        headers, rows = private(module, '_pool_workbooks')([
            workbook(module, 'a.xlsx', ['Sender'], [['s1', 'beyond-header']]),
            workbook(module, 'b.xlsx', ['sender', 'Source File'], [['s2', 'stored']])])
        self.assertEqual(headers, ('Sender', 'Column 2', 'Source File', 'Source File (1)'))
        self.assertEqual(rows, [['s1', 'beyond-header', '', 'a.xlsx'],
                                ['s2', '', 'stored', 'b.xlsx']])

    def test_repeated_heading_beside_a_numbered_heading_keeps_its_values(self):
        for module in all_modules():
            with self.subTest(module=module.__name__):
                headers, rows = private(module, '_pool_workbooks')([
                    workbook(module, 'a.xlsx', ['Sender', 'Sender', 'Sender 1'], [['first', 'second', 'numbered']]),
                    workbook(module, 'b.xlsx', ['Sender', 'Sender 1', 'Sender'], [['first', 'numbered', 'second']])])
                self.assertEqual(len(headers), 4)
                self.assertEqual(rows, [['first', 'second', 'numbered', 'a.xlsx'],
                                        ['first', 'second', 'numbered', 'b.xlsx']])
                self.assertEqual(len({sanitize_sql_name(name) for name in headers}), 4)

    def test_added_source_column_never_duplicates_a_workbook_column(self):
        for module in all_modules():
            with self.subTest(module=module.__name__):
                headers, _ = private(module, '_pool_workbooks')([
                    workbook(module, 'a.xlsx', ['Source File', 'Source File (1)'], [['x', 'y']]),
                    workbook(module, 'b.xlsx', ['Source File'], [['z']])])
                self.assertEqual(headers, ('Source File', 'Source File (1)', 'Source File (2)'))
                self.assertEqual(len({sanitize_sql_name(name) for name in headers}), 3)


    def test_blank_and_punctuation_headings_do_not_overwrite_each_other(self):
        for module in all_modules():
            for blank in ('', ' ', None):
                with self.subTest(module=module.__name__, blank=blank):
                    _, rows = private(module, '_pool_workbooks')([
                        workbook(module, 'a.xlsx', [blank, '-', '#'], [['b1', 'd1', 'h1']]),
                        workbook(module, 'b.xlsx', [blank, '#', '-'], [['b2', 'h2', 'd2']])])
                    self.assertEqual(rows, [['b1', 'd1', 'h1', 'a.xlsx'],
                                            ['b2', 'd2', 'h2', 'b.xlsx']])


if __name__ == '__main__':
    unittest.main()
