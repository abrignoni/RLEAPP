"""Workbooks with different column orders must keep each value under its own heading."""
import importlib
import inspect
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

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


class PooledWorkbookHeaders(unittest.TestCase):
    def test_every_module_keeps_values_under_their_own_heading(self):
        for module_name, (parser, names) in MODULES.items():
            module = importlib.import_module(f'scripts.artifacts.{module_name}')
            for function in artifact_functions(module, names):
                with self.subTest(module=module_name, artifact=function.__name__):
                    with mock.patch.object(module, parser, lambda path, *_: WORKBOOKS[path]):
                        headers, rows, source = function(FakeContext(['b.xlsx', 'a.xlsx']))
                    self.assertEqual(headers, ('Sender', 'Recipient', 'Body', 'Source File'))
                    self.assertEqual(rows, [['sender-a', 'recipient-a', 'body-a', 'a.xlsx'],
                                            ['sender-b', 'recipient-b', 'body-b', 'b.xlsx']])
                    self.assertEqual(source, 'a.xlsx\nb.xlsx')

    def test_single_workbook_output_is_unchanged(self):
        module = importlib.import_module('scripts.artifacts.icloudMsgsInCloud')
        headers, rows = module._pool_workbooks([('a.xlsx', ['Sender', 'Body'], [['s', 'b']])])
        self.assertEqual(headers, ('Sender', 'Body'))
        self.assertEqual(rows, [['s', 'b']])

    def test_header_only_workbook_does_not_relabel_the_rows(self):
        module = importlib.import_module('scripts.artifacts.icloudMsgsInCloud')
        headers, rows = module._pool_workbooks([('a.xlsx', ['Sender', 'Body'], [['s', 'b']]),
                                                ('b.xlsx', ['Body', 'Sender'], [])])
        self.assertEqual(headers, ('Sender', 'Body'))
        self.assertEqual(rows, [['s', 'b']])

    def test_missing_extra_and_unheaded_values_survive(self):
        module = importlib.import_module('scripts.artifacts.icloudMsgsInCloud')
        headers, rows = module._pool_workbooks([('a.xlsx', ['Sender'], [['s1', 'beyond-header']]),
                                                ('b.xlsx', ['sender', 'Source File'], [['s2', 'stored']])])
        self.assertEqual(headers, ('Sender', 'Column 2', 'Source File', 'Source File (1)'))
        self.assertEqual(rows, [['s1', 'beyond-header', '', 'a.xlsx'],
                                ['s2', '', 'stored', 'b.xlsx']])


if __name__ == '__main__':
    unittest.main()
