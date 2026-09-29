"""Pin how the TikTok PDF return reader handles page breaks and unlabelled pages.

A line split by a page break is printed at the foot of one page and again at the top of
the next, above where that page's text normally starts. The reader drops the repeat.
An earlier rule also dropped any leading lines whose characters appeared, in order, in
the previous page's last line; a short real line of a wrapped comment passes that test,
so real text could be lost with only a count logged. These tests hold the reader to
dropping only an exact copy printed above the normal first-line position.

LocationInfo is read as 'Name: value' lines whose names are not known in advance. A
wrapped value, or one whose text holds a colon, must stay with its field.

Every line here is made up; none comes from a return.
"""
import pathlib
import sys
import unittest

# admin/test/scripts/<this file>, so the repository root is three levels up.
ROOT_DIR = pathlib.Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.artifacts.tikTokReturnPdf import (  # pylint: disable=wrong-import-position
    _Line, _Pdf, _Rect, _drop_page_break_repeats, _labelled_fields)

NORMAL_TOP = 58      # first line of a page with no repeat
REPEAT_TOP = 52      # where the repeat of a split line is printed
LINE_HEIGHT = 14


def page(texts, top=NORMAL_TOP, x0=33):
    return [_Line(text, _Rect(x0, top + i * LINE_HEIGHT, x0 + 200, top + i * LINE_HEIGHT + 8),
                  [], False) for i, text in enumerate(texts)]


def read(pages):
    pdf = _Pdf()
    _drop_page_break_repeats(pages, pdf)
    return [[line.text for line in lines] for lines in pages], pdf


class PageBreakRepeats(unittest.TestCase):

    def test_repeat_above_the_normal_position_is_dropped_and_logged_by_field(self):
        pages = [page(['Date: 1', 'IP: a', 'Date: 2']),
                 page(['Date: 2'], top=REPEAT_TOP) + page(['IP: b'], top=66),
                 page(['Date: 3', 'IP: c'])]
        texts, pdf = read(pages)
        self.assertEqual(texts[1], ['IP: b'])
        self.assertEqual(pdf.dropped, [(2, 'Date')])
        self.assertEqual(pdf.kept_repeats, [])

    def test_short_lines_of_a_wrapped_comment_are_kept(self):
        # The case that the old subsequence rule dropped: each next-page line's
        # characters appear, in order, in the previous page's last line.
        last = 'Comment: honestly I think the whole thing was planned from the start and'
        for continuation in ('then', 'it was', 'lol'):
            with self.subTest(continuation=continuation):
                pages = [page(['Comment ID: 1', last]),
                         page([continuation, 'Comment ID: 2']),
                         page(['Comment ID: 3'])]
                texts, pdf = read(pages)
                self.assertEqual(texts[1], [continuation, 'Comment ID: 2'])
                self.assertEqual(pdf.dropped, [])

    def test_a_copy_at_the_normal_position_is_kept_and_reported(self):
        # Two identical wrapped lines of a comment, split cleanly by the page break.
        pages = [page(['Comment ID: 1', 'Comment: haha']),
                 page(['haha', 'Comment ID: 2']),
                 page(['Comment ID: 3'])]
        pages[0][-1].text = 'haha'
        texts, pdf = read(pages)
        self.assertEqual(texts[1], ['haha', 'Comment ID: 2'])
        self.assertEqual(pdf.dropped, [])
        self.assertEqual(pdf.kept_repeats, [2])

    def test_without_a_page_to_compare_against_nothing_is_dropped(self):
        pages = [page(['Date: 1']), page(['Date: 1'], top=REPEAT_TOP)]
        texts, pdf = read(pages)
        self.assertEqual(texts[1], ['Date: 1'])
        self.assertEqual(pdf.kept_repeats, [2])


class LabelledFields(unittest.TestCase):

    def test_a_value_is_kept_with_its_field_when_it_wraps_or_holds_a_colon(self):
        lines = page(['Country: Somewhere', 'Region: A long region name that'], x0=39)
        lines += page(['wraps onto a second line', '12:30 PM', 'fe80::1'], top=86, x0=110)
        lines += page(['Last IP: 2001:db8::1'], top=128, x0=39)
        self.assertEqual(_labelled_fields(lines), [
            ('Country', 'Somewhere'),
            ('Region', 'A long region name that\nwraps onto a second line\n12:30 PM\nfe80::1'),
            ('Last IP', '2001:db8::1'),
        ])

    def test_a_name_and_colon_off_the_field_margin_continues_the_value(self):
        lines = page(['Note: first'], x0=39) + page(['Also: part of the note'], top=72, x0=110)
        self.assertEqual(_labelled_fields(lines), [('Note', 'first\nAlso: part of the note')])

    def test_the_no_data_notice_is_not_read_as_a_field(self):
        lines = page(['Our records indicate no available data for the date range specified.'])
        self.assertEqual(_labelled_fields(lines), [])


if __name__ == '__main__':
    unittest.main()
