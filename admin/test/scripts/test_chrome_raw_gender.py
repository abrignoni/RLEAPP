"""Exercise decoded JSON values and the existing first-file contract."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from scripts.artifacts.chrome import chrome_os_settings


VALUES = [None, False, True, 0, 1, 2, 3, -1, 0.0, 1.0, 2.0, 0.5,
          '', '0', 'Female', 'snow雪', [], [0, None], {}, {'gender': False}]


def write_settings(path, values):
    """Write actual Takeout-shaped JSON, preserving nested JSON types."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, value in enumerate(values):
        rows.append({'preference': {
            'name': f'preference{index}',
            'value': json.dumps({'gender': value, 'birth_year': 1980 + index})}})
    path.write_text(json.dumps({'OS Priority Preference': rows}), encoding='utf-8')


class ChromeRawGenderTests(unittest.TestCase):
    def test_native_json_kinds_and_repeated_preferences(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'Takeout' / 'Chrome' / 'OS Settings.json'
            values = VALUES + [False, {'gender': False}]
            write_settings(path, values)
            document = json.loads(path.read_text(encoding='utf-8'))
            document['OS Priority Preference'].append(document['OS Priority Preference'][1])
            path.write_text(json.dumps(document), encoding='utf-8')
            context = SimpleNamespace(get_files_found=lambda: [str(path)])
            _, rows, source = chrome_os_settings.__wrapped__(context)
            expected = [(f'preference{i}', value, 1980 + i)
                        for i, value in enumerate(values)]
            expected.append(expected[1])
            self.assertEqual(rows, expected)
            self.assertEqual([[type(v) for v in row] for row in rows],
                             [[type(v) for v in row] for row in expected])
            self.assertEqual(source, str(path))

    def test_only_first_matching_file_contributes(self):
        with tempfile.TemporaryDirectory() as folder:
            first = Path(folder) / 'one' / 'OS Settings.json'
            second = Path(folder) / 'two' / 'OS Settings.json'
            write_settings(first, [False, 0.5])
            write_settings(second, ['independent'])
            context = SimpleNamespace(get_files_found=lambda: [str(first), str(second)])
            _, rows, source = chrome_os_settings.__wrapped__(context)
            self.assertEqual(rows, [('preference0', False, 1980),
                                    ('preference1', 0.5, 1981)])
            self.assertEqual(source, str(first))
            reverse = SimpleNamespace(get_files_found=lambda: [str(second), str(first)])
            _, rows, source = chrome_os_settings.__wrapped__(reverse)
            self.assertEqual(rows, [('preference0', 'independent', 1980)])
            self.assertEqual(source, str(second))
