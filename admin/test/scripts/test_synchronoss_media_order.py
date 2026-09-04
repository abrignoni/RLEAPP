"""Pin MMS media resolution as independent of the order the seeker returns files.

Attachment names are not unique across date folders in a Synchronoss return:
image000000.jpg and the extensionless "0" recur daily. The superseded index kept
one path per name, so only whichever copy the seeker returned last held a
date-folder entry, and a message resolved against its own folder's copy or did
not depending on file order. That order varies by platform -- the same return
linked a message on Windows and reported it unlinked on Linux -- and the
unlinked wording named a date folder that did in fact hold a copy, so the report
stated something false rather than merely omitting it.

The committed test case cannot guard this on its own, because the ordering is
the thing that varies: on macOS the pre-fix code passes that case, since the
seeker order happens to be favourable there. These tests drive the index
directly with both orderings, which is the axis the defect lives on.

test_superseded_index_is_order_dependent is a control. It reimplements the old
one-path-per-name construction and asserts it DOES differ under reversal. If the
fixture paths below ever stop provoking the ordering difference, that test fails
and says so, rather than the real tests passing vacuously.
"""
import pathlib
import sys
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from scripts.artifacts.synchronoss import (  # pylint: disable=wrong-import-position
    _date_from_media_path, _index_mms_media)

BASE = '/case/return/9995551234/messages/attachments/mms/in'

# dup.jpg is the probe: the same name in two date folders. The others are the
# shapes a real return carries alongside it -- a name unique to one folder, and
# the extensionless "0" that also recurs.
MEDIA_PATHS = [
    BASE + '/2025-12-02/dup.jpg',
    BASE + '/2025-12-02/image000000.jpg',
    BASE + '/2025-12-02/0',
    BASE + '/2025-12-03/dup.jpg',
    BASE + '/2025-12-03/unique.png',
    BASE + '/2025-12-03/0',
]


def _superseded_index(media_paths):
    """The construction this change replaced: one path per name."""
    by_name = {}
    for raw in media_paths:
        by_name[pathlib.PurePosixPath(raw).name] = raw
    date_media = {}
    for fname, fpath in by_name.items():
        date_media.setdefault(_date_from_media_path(fpath), {})[fname] = fpath
    return date_media


class DateFromMediaPath(unittest.TestCase):
    """The date folder is the path segment after 'in' or 'out'."""

    def test_posix_and_windows_shapes_agree(self):
        posix = BASE + '/2025-12-02/dup.jpg'
        # built with chr(92) so this file carries no literal backslash escapes
        windows = 'C:' + (BASE + '/2025-12-02/dup.jpg').replace('/', chr(92))
        self.assertEqual(_date_from_media_path(posix), '2025-12-02')
        self.assertEqual(_date_from_media_path(windows), '2025-12-02')

    def test_outbound_direction(self):
        self.assertEqual(
            _date_from_media_path('/x/mms/out/2025-12-05/a.jpg'), '2025-12-05')

    def test_no_direction_segment_yields_empty(self):
        self.assertEqual(_date_from_media_path('/x/y/z/a.jpg'), '')


class IndexIsOrderIndependent(unittest.TestCase):
    """The index must be a pure function of the set of paths, not their order."""

    def test_date_media_identical_under_reversal(self):
        _, forward = _index_mms_media(MEDIA_PATHS)
        _, reverse = _index_mms_media(list(reversed(MEDIA_PATHS)))
        self.assertEqual(forward, reverse)

    def test_name_paths_hold_every_copy_under_reversal(self):
        forward, _ = _index_mms_media(MEDIA_PATHS)
        reverse, _ = _index_mms_media(list(reversed(MEDIA_PATHS)))
        self.assertEqual(sorted(forward), sorted(reverse))
        for name in forward:
            self.assertEqual(sorted(forward[name]), sorted(reverse[name]))

    def test_each_date_folder_keeps_its_own_copy(self):
        """The point of the fix: a message resolves against its own folder."""
        _, date_media = _index_mms_media(MEDIA_PATHS)
        self.assertEqual(date_media['2025-12-02']['dup.jpg'],
                         BASE + '/2025-12-02/dup.jpg')
        self.assertEqual(date_media['2025-12-03']['dup.jpg'],
                         BASE + '/2025-12-03/dup.jpg')

    def test_duplicated_name_recorded_in_both_folders(self):
        name_paths, date_media = _index_mms_media(MEDIA_PATHS)
        self.assertEqual(len(name_paths['dup.jpg']), 2)
        self.assertEqual(len(name_paths['0']), 2)
        self.assertIn('dup.jpg', date_media['2025-12-02'])
        self.assertIn('dup.jpg', date_media['2025-12-03'])

    def test_unique_name_still_resolves(self):
        name_paths, date_media = _index_mms_media(MEDIA_PATHS)
        self.assertEqual(name_paths['unique.png'],
                         [BASE + '/2025-12-03/unique.png'])
        self.assertEqual(date_media['2025-12-03']['unique.png'],
                         BASE + '/2025-12-03/unique.png')


class SupersededIndexControl(unittest.TestCase):
    """Prove these paths actually provoke the ordering difference.

    Without this, the tests above could pass because nothing varies rather than
    because the index is order-independent.
    """

    def test_superseded_index_is_order_dependent(self):
        forward = _superseded_index(MEDIA_PATHS)
        reverse = _superseded_index(list(reversed(MEDIA_PATHS)))
        self.assertNotEqual(
            forward, reverse,
            'the fixture paths no longer provoke an ordering difference, so the '
            'order-independence tests above are not proving anything')

    def test_superseded_index_loses_a_copy(self):
        """It drops one date folder's copy entirely, which is the defect."""
        forward = _superseded_index(MEDIA_PATHS)
        present = [d for d in ('2025-12-02', '2025-12-03')
                   if 'dup.jpg' in forward.get(d, {})]
        self.assertEqual(len(present), 1)


if __name__ == '__main__':
    unittest.main()
