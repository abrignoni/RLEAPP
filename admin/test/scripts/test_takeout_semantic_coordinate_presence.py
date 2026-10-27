"""Exercise supported coordinate presence through actual JSON files."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from scripts.artifacts import takeoutSemanticLocationHistory as semantic


class CoordinatePresenceTests(unittest.TestCase):
    def parse(self, key, elements, repeats=1):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'records.json'
            path.write_text(json.dumps({'timelineObjects': elements}), encoding='utf-8-sig')
            context = SimpleNamespace(
                get_files_found=lambda: [path] * repeats,
                get_relative_path=lambda value: Path(value).name)
            return getattr(semantic, key).__wrapped__(context)

    def test_places_keep_missing_distinct_from_numeric_zero(self):
        locations = [{}, {'latitudeE7': 0}, {'longitudeE7': 0},
                     {'latitudeE7': 0, 'longitudeE7': 0},
                     {'latitudeE7': -123456789, 'longitudeE7': 234567890}]
        elements = [{'placeVisit': {'location': location}} for location in locations]
        _, rows, source = self.parse('takeoutSemanticPlaceVisits', elements)
        self.assertEqual([row[4:6] for row in rows],
                         [(None, None), (0.0, None), (None, 0.0),
                          (0.0, 0.0), (-12.3456789, 23.456789)])
        self.assertIsNone(rows[0][4])
        self.assertIs(type(rows[3][4]), float)
        self.assertEqual(source, 'records.json')
        self.assertTrue(all(len(row) == 8 for row in rows))

    def test_segments_keep_absent_whole_location_sentinel(self):
        elements = [{'activitySegment': {}},
                    {'activitySegment': {'startLocation': {}, 'endLocation': {}}},
                    {'activitySegment': {'startLocation': {'latitudeE7': 0},
                                         'endLocation': {'longitudeE7': 0}}}]
        _, rows, _ = self.parse('takeoutSemanticActivitySegments', elements)
        self.assertEqual([row[2:6] for row in rows],
                         [('NOT_SPECIFIED',) * 4, (None,) * 4,
                          (0.0, None, None, 0.0)])
        self.assertTrue(all(len(row) == 11 for row in rows))

    def test_repeated_events_and_inputs_preserve_order_and_other_fields(self):
        first = {'placeVisit': {'location': {'name': 'one', 'latitudeE7': 10000000}}}
        second = {'placeVisit': {'location': {'name': 'two', 'longitudeE7': 20000000}}}
        _, rows, _ = self.parse('takeoutSemanticPlaceVisits', [first, second, first], 2)
        self.assertEqual([row[2] for row in rows], ['one', 'two', 'one'] * 2)
        self.assertEqual([row[4:6] for row in rows],
                         [(1.0, None), (None, 2.0), (1.0, None)] * 2)
        self.assertTrue(all(row[0:2] == ('', '') and row[7] == 'records.json'
                            for row in rows))

    def test_safe_arithmetic_and_both_datetime_columns_stay_adjacent(self):
        element = {'activitySegment': {
            'startLocation': {'latitudeE7': True, 'longitudeE7': -0.0},
            'endLocation': {'latitudeE7': 1.5, 'longitudeE7': 20000000},
            'duration': {'startTimestamp': '2026-04-11T04:02:00+02:00',
                         'endTimestamp': '2026-04-11T05:03:00+02:00'},
            'activities': [{'activityType': 'RAW', 'probability': 0}]}}
        headers, rows, _ = self.parse('takeoutSemanticActivitySegments', [element])
        self.assertEqual(rows[0][2:6], (1e-7, -0.0, 1.5e-7, 2.0))
        self.assertEqual([h[1] for h in headers[:2]], ['datetime', 'datetime'])
        self.assertEqual(rows[0][0].isoformat(), '2026-04-11T02:02:00+00:00')
        self.assertEqual(rows[0][9], 'RAW [0]')


if __name__ == '__main__':
    unittest.main()
