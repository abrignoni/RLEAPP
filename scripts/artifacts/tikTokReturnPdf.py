__artifacts_v2__ = {
    "tikTokReturnPdfSections": {
        "name": "TikTok PDF Return - Sections",
        "description": "PDF sections found in a TikTok law enforcement return of the PDF layout "
                       "(<folder>/App, /Content, /Profile), each with its title, page count, any "
                       "no-data notice printed in it, and which artifact parses it.",
        "author": "@OneSixForensics, Claude",
        "creation_date": "2026-09-28",
        "last_update_date": "2026-09-28",
        "requirements": "PyMuPDF",
        "category": "TikTok Returns",
        "notes": "Lists sections this module does not parse as well as the ones it does, so a "
                 "section with content and no artifact is visible. 'Provider Notice' carries "
                 "the return's own sentence when a section says it holds no data for the "
                 "requested range; a blank notice does not mean the section had records. "
                 "PDF Created is the creationDate in each PDF's document metadata, as written "
                 "by the software that rendered it; in the tested return all 20 fell within the "
                 "same minute.",
        "paths": ('*/App/*.pdf', '*/Content/*.pdf', '*/Profile/*.pdf'),
        "output_types": "standard",
        "artifact_icon": "list",
        "sample_data": {
            "tiktok-pdf-return-2026-09": "TikTok USDS JV PDF return | 20 rows",
        }
    },
    "tikTokReturnPdfSubscriber": {
        "name": "TikTok PDF Return - Subscriber Info",
        "description": "Basic subscriber information (Profile/BSI.pdf) and location information "
                       "(App/LocationInfo.pdf) from a TikTok law enforcement return, one row "
                       "per field as printed.",
        "author": "@OneSixForensics, Claude",
        "creation_date": "2026-09-28",
        "last_update_date": "2026-09-28",
        "requirements": "PyMuPDF",
        "category": "TikTok Returns",
        "notes": "BSI is a two-column table; fields are paired by row position, so a field "
                 "name not seen before is still reported under its printed name. Values are "
                 "as printed, including the signup date text, which is not converted.",
        "paths": ('*/Profile/BSI.pdf', '*/App/LocationInfo.pdf'),
        "output_types": "standard",
        "artifact_icon": "user",
        "sample_data": {
            "tiktok-pdf-return-2026-09": "TikTok USDS JV PDF return | 10 rows",
        }
    },
    "tikTokReturnPdfLoginLogout": {
        "name": "TikTok PDF Return - Login Logout History",
        "description": "Login and logout records (App/LoginLogoutHistory.pdf) from a TikTok law "
                       "enforcement return.",
        "author": "@OneSixForensics, Claude",
        "creation_date": "2026-09-28",
        "last_update_date": "2026-09-28",
        "requirements": "PyMuPDF",
        "category": "TikTok Returns",
        "notes": "Action is taken from the printed field name ('User login time' or 'User logout "
                 "time'). Country is the country the return prints beside each IP. Country was "
                 "uniform across the tested return, and IP was uniform on its 10 rows.",
        "paths": ('*/App/LoginLogoutHistory.pdf',),
        "output_types": "standard",
        "artifact_icon": "log-in",
        "sample_data": {
            "tiktok-pdf-return-2026-09": "TikTok USDS JV PDF return | 10 rows",
        }
    },
    "tikTokReturnPdfIpSessions": {
        "name": "TikTok PDF Return - IP Session History",
        "description": "IP session records with source port (App/IPSessionHistory_*.pdf) from a "
                       "TikTok law enforcement return.",
        "author": "@OneSixForensics, Claude",
        "creation_date": "2026-09-28",
        "last_update_date": "2026-09-28",
        "requirements": "PyMuPDF",
        "category": "TikTok Returns",
        "notes": "Multi-part sections are read in part order and combined. Country is the "
                 "country the return prints beside each IP. Country was uniform across the "
                 "tested return.",
        "paths": ('*/App/IPSessionHistory_*.pdf',),
        "output_types": "standard",
        "artifact_icon": "globe",
        "sample_data": {
            "tiktok-pdf-return-2026-09": "TikTok USDS JV PDF return | 722 rows",
        }
    },
    "tikTokReturnPdfEventsIp": {
        "name": "TikTok PDF Return - Events IP Data",
        "description": "Event records with IP address (App/EventsIPData_*.pdf) from a TikTok law "
                       "enforcement return.",
        "author": "@OneSixForensics, Claude",
        "creation_date": "2026-09-28",
        "last_update_date": "2026-09-28",
        "requirements": "PyMuPDF",
        "category": "TikTok Returns",
        "notes": "Event is the provider's event name as printed (observed: video_play, publish, "
                 "post_comment, share_video). Their meaning is not documented in the return and "
                 "is not interpreted here. Multi-part sections are combined; large returns may "
                 "exceed the HTML row limit, in which case the TSV and LAVA outputs hold the "
                 "full table. Country is the country the return prints beside each IP. Country "
                 "was uniform across the tested return.",
        "paths": ('*/App/EventsIPData_*.pdf',),
        "output_types": "standard",
        "artifact_icon": "activity",
        "sample_data": {
            "tiktok-pdf-return-2026-09": "TikTok USDS JV PDF return | 23912 rows",
        }
    },
    "tikTokReturnPdfVideoIp": {
        "name": "TikTok PDF Return - Video IP",
        "description": "Post date and IP address per video ID (Content/VideoIP.pdf) from a TikTok "
                       "law enforcement return.",
        "author": "@OneSixForensics, Claude",
        "creation_date": "2026-09-28",
        "last_update_date": "2026-09-28",
        "requirements": "PyMuPDF",
        "category": "TikTok Returns",
        "notes": "Country is the country the return prints beside each IP. Country was uniform "
                 "across the tested return. Video ID is not limited to Videos: of 331 IDs "
                 "in the tested return, 318 were Stories post IDs, 38 Photo post IDs and 4 "
                 "Videos IDs (these overlap), and 5 appeared in no other section.",
        "paths": ('*/Content/VideoIP.pdf',),
        "output_types": "standard",
        "artifact_icon": "globe",
        "sample_data": {
            "tiktok-pdf-return-2026-09": "TikTok USDS JV PDF return | 331 rows",
        }
    },
    "tikTokReturnPdfVideos": {
        "name": "TikTok PDF Return - Videos",
        "description": "Video metadata (Content/VideoMetadata.pdf) from a TikTok law enforcement "
                       "return, with the video file from Content/Videos where one was provided.",
        "author": "@OneSixForensics, Claude",
        "creation_date": "2026-09-28",
        "last_update_date": "2026-09-28",
        "requirements": "PyMuPDF",
        "category": "TikTok Returns",
        "notes": "Media is linked by the video ID, which is the file name of each file in "
                 "Content/Videos. Video Link is the hyperlink behind the printed word 'URL'; "
                 "blank where the PDF carries the word with no hyperlink. Video Type was "
                 "'deleted' on all 4 rows of the tested return.",
        "paths": ('*/Content/VideoMetadata.pdf', '*/Content/Videos/*'),
        "output_types": "standard",
        "artifact_icon": "video",
        "sample_data": {
            "tiktok-pdf-return-2026-09": "TikTok USDS JV PDF return | 4 rows",
        }
    },
    "tikTokReturnPdfStories": {
        "name": "TikTok PDF Return - Stories",
        "description": "Stories metadata (Content/StoriesMetadata.pdf) from a TikTok law "
                       "enforcement return, with the files from Content/Stories/<Post ID>.",
        "author": "@OneSixForensics, Claude",
        "creation_date": "2026-09-28",
        "last_update_date": "2026-09-28",
        "requirements": "PyMuPDF",
        "category": "TikTok Returns",
        "notes": "Media is linked by the post ID, which is the folder name in Content/Stories; "
                 "in the tested return 300 of 318 rows had a folder. Caption was blank on every "
                 "row of the tested return and is kept because the section prints the field. "
                 "Media folders with no metadata row are listed in 'TikTok PDF Return - Media "
                 "Files'.",
        "paths": ('*/Content/StoriesMetadata.pdf', '*/Content/Stories/*'),
        "output_types": "standard",
        "artifact_icon": "image",
        "sample_data": {
            "tiktok-pdf-return-2026-09": "TikTok USDS JV PDF return | 318 rows",
        }
    },
    "tikTokReturnPdfPhotoPosts": {
        "name": "TikTok PDF Return - Photo Posts",
        "description": "Photo post metadata (Content/PhotoMetadata.pdf) from a TikTok law "
                       "enforcement return, with the images and audio from "
                       "Content/Photo Post/<Photo Post ID>.",
        "author": "@OneSixForensics, Claude",
        "creation_date": "2026-09-28",
        "last_update_date": "2026-09-28",
        "requirements": "PyMuPDF",
        "category": "TikTok Returns",
        "notes": "Media is linked by the photo post ID, which is the folder name in "
                 "Content/Photo Post. Audio files are those with an audio MIME type by content. "
                 "Photo URL and Audio URL are the hyperlinks behind the printed word 'URL'.",
        "paths": ('*/Content/PhotoMetadata.pdf', '*/Content/Photo Post/*'),
        "output_types": "standard",
        "artifact_icon": "image",
        "sample_data": {
            "tiktok-pdf-return-2026-09": "TikTok USDS JV PDF return | 38 rows",
        }
    },
    "tikTokReturnPdfComments": {
        "name": "TikTok PDF Return - Comments",
        "description": "Video and photo comments (Content/Video Comments, Content/Photo Comments) "
                       "from a TikTok law enforcement return, with any comment image the return "
                       "names.",
        "author": "@OneSixForensics, Claude",
        "creation_date": "2026-09-28",
        "last_update_date": "2026-09-28",
        "requirements": "PyMuPDF",
        "category": "TikTok Returns",
        "notes": "Comment image media is linked by the file name the return prints for it "
                 "('saved as Images/...'). 'ReplyToComment (as stored)' is kept verbatim: in the "
                 "tested return it equalled the Comment text on all 86 of 229 rows that "
                 "carried it, so it is not labelled as the parent comment. Post URL is the hyperlink behind the "
                 "printed word 'URL'.",
        "paths": ('*/Content/Video Comments/Video Comments.pdf',
                  '*/Content/Photo Comments/*'),
        "output_types": "standard",
        "artifact_icon": "message-square",
        "sample_data": {
            "tiktok-pdf-return-2026-09": "TikTok USDS JV PDF return | 229 rows",
        }
    },
    "tikTokReturnPdfLiveComments": {
        "name": "TikTok PDF Return - Live Comments",
        "description": "Live comment history (Content/LiveComment_*.pdf) from a TikTok law "
                       "enforcement return.",
        "author": "@OneSixForensics, Claude",
        "creation_date": "2026-09-28",
        "last_update_date": "2026-09-28",
        "requirements": "PyMuPDF",
        "category": "TikTok Returns",
        "notes": "Room ID, Host User ID and Device IP are split out of the printed lines. If a "
                 "line does not match the expected layout its text is kept whole in Room ID or "
                 "Comment Time rather than dropped.",
        "paths": ('*/Content/LiveComment_*.pdf',),
        "output_types": "standard",
        "artifact_icon": "message-circle",
        "sample_data": {
            "tiktok-pdf-return-2026-09": "TikTok USDS JV PDF return | 1 row",
        }
    },
    "tikTokReturnPdfMedia": {
        "name": "TikTok PDF Return - Media Files",
        "description": "Media files found under Content/ in a TikTok law enforcement return, with "
                       "the ID taken from each path and whether a metadata section lists that ID.",
        "author": "@OneSixForensics, Claude",
        "creation_date": "2026-09-28",
        "last_update_date": "2026-09-28",
        "requirements": "PyMuPDF",
        "category": "TikTok Returns",
        "notes": "Covers files the metadata sections do not reference, which the per-section "
                 "artifacts cannot show. 'ID In Metadata PDF' was 'Yes' on every row of the "
                 "tested return (no unreferenced files); a 'No' marks a file no parsed section "
                 "lists. Returns delivered as several zip parts split the media across them "
                 "(the tested return: metadata and some media in part 1, the rest in parts 2 "
                 "and 3); extract every part into one folder and parse that, or media in the "
                 "other parts is neither linked nor listed.",
        "paths": ('*/Content/VideoMetadata.pdf', '*/Content/Videos/*',
                  '*/Content/StoriesMetadata.pdf', '*/Content/Stories/*',
                  '*/Content/PhotoMetadata.pdf', '*/Content/Photo Post/*',
                  '*/Content/Photo Comments/*'),
        "output_types": "standard",
        "artifact_icon": "film",
        "sample_data": {
            "tiktok-pdf-return-2026-09": "TikTok USDS JV PDF return | 410 rows",
        }
    },
}

import os
import re
from datetime import datetime, timedelta, timezone

import fitz

from scripts.ilapfuncs import artifact_processor, check_in_media, logfunc

# ---------------------------------------------------------------------------
# PDF reading
#
# The PDF layout prints each record as 'Label: value' lines in one font, so labels
# cannot be told from values by typography and records are split on a known label
# list per section. Three rendering quirks are handled here:
#   * every page ends with a footer (page number, provider name, 'Confidential &
#     Proprietary') that can fall in the middle of a record;
#   * a line that straddles a page break is printed whole at the foot of one page and
#     again, clipped into fragments, at the head of the next. The fragments are dropped
#     when their characters are a subsequence of the previous page's last line;
#   * a record occasionally starts on the same line as the end of the previous one
#     ('...text Comment ID: 123'), so the record-start label is also split mid-line
#     when a digit follows it.
# ---------------------------------------------------------------------------

_SECTIONS = ('App', 'Content', 'Profile')
# Fields whose text is written by users; never inspected for field names or logged.
_FREE_TEXT = {'Comment', 'ReplyToComment', 'Content', 'Video caption', 'Post caption',
              'PhotoPostCaption', 'AudioTitle'}
_PDF_DATE = re.compile(r"^D:(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})"
                       r"(?:Z|([+-])(\d{2})'?(\d{2})'?)?")
_NO_DATA = re.compile(r'^Our records indicate no available data', re.I)
_TS = re.compile(r'^(\d{1,2})/(\d{1,2})/(\d{4}) (\d{1,2}):(\d{2}):(\d{2}) ?([AP]M) ?'
                 r'\(UTC ?([+-])(\d{1,2})(?::?(\d{2}))?\)$', re.I)


class _Line:
    __slots__ = ('text', 'rect', 'uris', 'bold')

    def __init__(self, text, rect, uris, bold):
        self.text = text
        self.rect = rect
        self.uris = uris
        self.bold = bold


class _Pdf:
    __slots__ = ('title', 'lines', 'pages', 'notice', 'is_tiktok', 'dropped', 'created')

    def __init__(self):
        self.title = ''
        self.lines = []
        self.pages = 0
        self.notice = ''
        self.is_tiktok = False
        self.dropped = 0
        self.created = ''


def _nospace(text):
    return re.sub(r'\s+', '', text)


def _is_subsequence(needle, haystack):
    it = iter(haystack)
    return all(ch in it for ch in needle)


def _page_lines(page):
    lines = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            spans = [s for s in line['spans'] if s['text'].strip()]
            if not spans:
                continue
            text = ''.join(s['text'] for s in line['spans']).strip()
            bold = all(s['flags'] & 16 for s in spans)
            lines.append(_Line(text, fitz.Rect(line['bbox']), [], bold))
    # A link box can touch two wrapped lines; give each link only to the line it
    # overlaps most, so it is reported once.
    for link in sorted(page.get_links(), key=lambda l: (l['from'].y0, l['from'].x0)):
        if not link.get('uri'):
            continue
        rect = fitz.Rect(link['from'])
        best = max(lines, key=lambda l, r=rect: (l.rect & r).get_area(), default=None)
        if best is not None and (best.rect & rect).get_area() > 0:
            best.uris.append(link['uri'])
    return lines


def _strip_footer(lines):
    '''Removes the page footer. Returns True if it named TikTok.'''
    if not lines or lines[-1].text != 'Confidential & Proprietary':
        return False
    lines.pop()
    is_tiktok = False
    if lines and lines[-1].text.startswith('TikTok'):
        is_tiktok = True
        lines.pop()
    if lines and lines[-1].text.isdigit():
        lines.pop()
    return is_tiktok


def _read_pdf(path, is_label_start=None, max_pages=None):
    '''Reads a TikTok return PDF into one list of content lines across all pages.

    is_label_start(text) says whether a line begins a field; it is used to find the
    clipped duplicate of a line split over a page break. Pass None for sections whose
    lines are not labelled (the BSI table).'''
    pdf = _Pdf()
    prev_last = None
    with fitz.open(path) as doc:
        pdf.pages = doc.page_count
        pdf.created = _pdf_date((getattr(doc, 'metadata', None) or {}).get('creationDate', ''))
        for page_no, page in enumerate(doc):
            if max_pages is not None and page_no >= max_pages:
                break
            lines = _page_lines(page)
            if _strip_footer(lines):
                pdf.is_tiktok = True
            if page_no == 0:
                while lines and lines[0].bold:
                    if not pdf.title:
                        pdf.title = lines[0].text
                    lines.pop(0)
            elif prev_last is not None and is_label_start is not None:
                k = 0
                while k < len(lines) and not is_label_start(lines[k].text):
                    k += 1
                if 0 < k < len(lines):
                    fragment = ''.join(_nospace(line.text) for line in lines[:k])
                    if _is_subsequence(fragment, _nospace(prev_last)):
                        pdf.dropped += k
                        del lines[:k]
            for line in lines:
                if _NO_DATA.match(line.text):
                    pdf.notice = line.text
            pdf.lines.extend(lines)
            if lines:
                prev_last = lines[-1].text
    return pdf


class _Parser:
    '''Splits labelled lines into records.

    labels: the field names printed for this section. Any label may carry a numeric
    suffix ('Comment photo Link 1:'), stored under the bare label.
    starts: the label(s) that begin a new record.
    Continuation lines of a field outside _FREE_TEXT that look like 'Name: value' are
    reported by name, as a sign the provider added a field; user-written fields are
    never echoed to the log.'''

    def __init__(self, labels, starts):
        alt = '|'.join(re.escape(label) for label in sorted(labels, key=len, reverse=True))
        self.head = re.compile(rf'^({alt})(?: \d+)?:[ \t]?')
        start_alt = '|'.join(re.escape(label) for label in starts)
        self.mid = re.compile(rf'\s(?=(?:{start_alt}):\s?\d)')
        self.starts = set(starts)
        self.unknown = re.compile(r'^([A-Z][A-Za-z ]{0,40}):\s')

    def is_label_start(self, text):
        return bool(self.head.match(text))

    def parse(self, lines):
        '''Returns (records, unknown_labels). Each record maps label -> list of
        {'text', 'uris'} values, in the order printed.'''
        records = []
        unknown = set()
        record = None
        current = None
        current_label = None
        for line in lines:
            pieces = self.mid.split(line.text) if self.mid.search(line.text) else [line.text]
            for idx, piece in enumerate(pieces):
                piece = piece.strip()
                if not piece:
                    continue
                # A link can only be attributed when the line was not split.
                uris = line.uris if len(pieces) == 1 else []
                match = self.head.match(piece)
                if match:
                    label = match.group(1)
                    if label in self.starts or record is None:
                        record = {}
                        records.append(record)
                    current_label = label
                    current = {'text': piece[match.end():].strip(), 'uris': list(uris)}
                    record.setdefault(label, []).append(current)
                    continue
                unk = self.unknown.match(piece)
                if unk and idx == 0 and current_label not in _FREE_TEXT:
                    unknown.add(unk.group(1))
                if current is None:
                    continue
                current['text'] = f"{current['text']}\n{piece}" if current['text'] else piece
                current['uris'].extend(uris)
        return records, unknown


def _val(record, label):
    return '\n'.join(v['text'] for v in record.get(label, []) if v['text'])


def _uris(record, label):
    return '\n'.join(uri for v in record.get(label, []) for uri in v['uris'])


def _ts(value):
    '''"MM/DD/YYYY hh:mm:ssAM (UTC +00)" to an aware UTC datetime; other text kept as is.'''
    match = _TS.match(value.strip()) if value else None
    if not match:
        return value
    mon, day, year, hour, minute, sec, ampm, sign, off_h, off_m = match.groups()
    hour = int(hour) % 12 + (12 if ampm.upper() == 'PM' else 0)
    offset = timedelta(hours=int(off_h), minutes=int(off_m or 0))
    if sign == '-':
        offset = -offset
    try:
        local = datetime(int(year), int(mon), int(day), hour, int(minute), int(sec),
                         tzinfo=timezone(offset))
    except ValueError:
        return value
    return local.astimezone(timezone.utc)


def _pdf_date(value):
    '''PDF date string "D:YYYYMMDDHHmmSS" with "Z" or "+hh'mm'" to aware UTC; other text as is.'''
    match = _PDF_DATE.match(value or '')
    if not match:
        return value or ''
    year, mon, day, hour, minute, sec, sign, off_h, off_m = match.groups()
    offset = timedelta(hours=int(off_h or 0), minutes=int(off_m or 0))
    if sign == '-':
        offset = -offset
    try:
        return datetime(int(year), int(mon), int(day), int(hour), int(minute), int(sec),
                        tzinfo=timezone(offset)).astimezone(timezone.utc)
    except ValueError:
        return value


def _split(path):
    '''Returns (return root, section, parts below the section) for a return file, or
    None. The root is the full path above App/Content/Profile, so two returns in one
    input stay apart.'''
    parts = re.split(r'[\\/]', str(path))
    for idx in range(len(parts) - 1, 0, -1):
        if parts[idx] in _SECTIONS:
            return '/'.join(parts[:idx]), parts[idx], parts[idx + 1:]
    return None


def _part_order(path):
    match = re.search(r'_(\d+)\.pdf$', str(path), re.I)
    return (re.sub(r'_\d+\.pdf$', '', str(path), flags=re.I), int(match.group(1)) if match else 0)


def _pdfs(context, name_re):
    found = [str(f) for f in context.get_files_found()
             if re.search(name_re, os.path.basename(str(f)), re.I)]
    return sorted(set(found), key=_part_order)


def _parse_section(context, name_re, labels, starts):
    '''Yields (file, records) for each matching PDF, logging anything unusual.'''
    parser = _Parser(labels, starts)
    for file_found in _pdfs(context, name_re):
        pdf = _read_pdf(file_found, parser.is_label_start)
        records, unknown = parser.parse(pdf.lines)
        rel = context.get_relative_path(file_found)
        if unknown:
            logfunc(f'{rel}: field names not recognised, kept as text of the previous field: '
                    f'{", ".join(sorted(unknown))}')
        if pdf.dropped:
            logfunc(f'{rel}: {pdf.dropped} page-break duplicate line fragments dropped')
        yield file_found, records


def _media_index(context, section):
    '''Maps (return root, first folder or file stem under Content/<section>) to the
    list of media file paths there.'''
    index = {}
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if file_found.lower().endswith('.pdf') or not os.path.isfile(file_found):
            continue
        split = _split(file_found)
        if not split or split[1] != 'Content' or len(split[2]) < 2:
            continue
        root, _, below = split
        if below[0] != section:
            continue
        key = below[1] if len(below) > 2 else os.path.splitext(below[1])[0]
        index.setdefault((root, key), []).append(file_found)
    for paths in index.values():
        paths.sort()
    return index


def _check_in(paths):
    '''Checks in each file; returns the reference list, or '' when there are none so an
    absent file is a blank cell rather than an empty list.'''
    refs = []
    for path in paths:
        ref = check_in_media(path, os.path.basename(path))
        if ref:
            refs.append(ref)
    return refs or ''


def _is_audio(path):
    '''Sniffs MP3 (ID3 tag or MPEG frame sync) and M4A by content, not extension.'''
    with open(path, 'rb') as fh:
        head = fh.read(12)
    if head[:3] == b'ID3':
        return True
    if len(head) > 1 and head[0] == 0xFF and (head[1] & 0xE0) == 0xE0:
        return True
    return head[4:8] == b'ftyp' and head[8:11] == b'M4A'


# ---------------------------------------------------------------------------
# Artifacts
# ---------------------------------------------------------------------------

_PARSED_BY = (
    (r'^BSI\.pdf$', 'TikTok PDF Return - Subscriber Info'),
    (r'^LocationInfo\.pdf$', 'TikTok PDF Return - Subscriber Info'),
    (r'^LoginLogoutHistory\.pdf$', 'TikTok PDF Return - Login Logout History'),
    (r'^IPSessionHistory_\d+\.pdf$', 'TikTok PDF Return - IP Session History'),
    (r'^EventsIPData_\d+\.pdf$', 'TikTok PDF Return - Events IP Data'),
    (r'^VideoIP\.pdf$', 'TikTok PDF Return - Video IP'),
    (r'^VideoMetadata\.pdf$', 'TikTok PDF Return - Videos'),
    (r'^StoriesMetadata\.pdf$', 'TikTok PDF Return - Stories'),
    (r'^PhotoMetadata\.pdf$', 'TikTok PDF Return - Photo Posts'),
    (r'^(Video|Photo) Comments\.pdf$', 'TikTok PDF Return - Comments'),
    (r'^LiveComment_\d+\.pdf$', 'TikTok PDF Return - Live Comments'),
)


@artifact_processor
def tikTokReturnPdfSections(context):
    data_list = []
    sources = []
    for file_found in _pdfs(context, r'\.pdf$'):
        if not _split(file_found):
            continue
        pdf = _read_pdf(file_found, max_pages=1)
        if not pdf.is_tiktok:
            continue
        name = os.path.basename(file_found)
        parsed_by = next((artifact for pattern, artifact in _PARSED_BY
                          if re.match(pattern, name, re.I)), 'not parsed')
        rel = context.get_relative_path(file_found)
        sources.append(file_found)
        data_list.append((pdf.created, pdf.title, pdf.pages, pdf.notice, parsed_by, rel))

    data_headers = (('PDF Created', 'datetime'), 'Section Title', 'Pages', 'Provider Notice',
                    'Parsed By', 'Source File')
    return data_headers, data_list, '\n'.join(sources)


def _table_fields(lines):
    '''Pairs a two-column table by row: the left column is the field name.'''
    if not lines:
        return []
    left = min(line.rect.x0 for line in lines)
    fields = []
    for line in sorted(lines, key=lambda l: (l.rect.y0, l.rect.x0)):
        if abs(line.rect.x0 - left) < 3:
            fields.append([line.text, '', line.rect])
        elif fields and line.rect.y0 < fields[-1][2].y1 + 12:
            name, value, rect = fields[-1]
            fields[-1] = [name, f'{value}\n{line.text}' if value else line.text, rect | line.rect]
    return [(name, value) for name, value, _ in fields]


@artifact_processor
def tikTokReturnPdfSubscriber(context):
    data_list = []
    sources = []
    for file_found in _pdfs(context, r'^(BSI|LocationInfo)\.pdf$'):
        pdf = _read_pdf(file_found)
        if not pdf.is_tiktok:
            continue
        rel = context.get_relative_path(file_found)
        sources.append(file_found)
        if os.path.basename(file_found).lower() == 'bsi.pdf':
            fields = _table_fields(pdf.lines)
        else:
            fields = [tuple(p.strip() for p in line.text.split(':', 1))
                      for line in pdf.lines if ':' in line.text]
        for name, value in fields:
            data_list.append((pdf.title, name, value, rel))
        if pdf.notice:
            data_list.append((pdf.title, 'Provider Notice', pdf.notice, rel))

    data_headers = ('Section', 'Field', 'Value', 'Source File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def tikTokReturnPdfLoginLogout(context):
    data_list = []
    sources = []
    starts = ('User login time', 'User logout time')
    labels = starts + ('User login IP', 'User login country', 'User logout IP',
                       'User logout country')
    for file_found, records in _parse_section(context, r'^LoginLogoutHistory\.pdf$',
                                              labels, starts):
        sources.append(file_found)
        rel = context.get_relative_path(file_found)
        for rec in records:
            action = 'logout' if 'User logout time' in rec else 'login'
            data_list.append((_ts(_val(rec, f'User {action} time')), action,
                              _val(rec, f'User {action} IP'), _val(rec, f'User {action} country'),
                              rel))

    data_headers = (('Timestamp', 'datetime'), 'Action', 'IP', 'Country', 'Source File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def tikTokReturnPdfIpSessions(context):
    data_list = []
    sources = []
    for file_found, records in _parse_section(context, r'^IPSessionHistory_\d+\.pdf$',
                                              ('Date', 'IP', 'IP Port', 'Country'), ('Date',)):
        sources.append(file_found)
        rel = context.get_relative_path(file_found)
        for rec in records:
            data_list.append((_ts(_val(rec, 'Date')), _val(rec, 'IP'), _val(rec, 'IP Port'),
                              _val(rec, 'Country'), rel))

    data_headers = (('Timestamp', 'datetime'), 'IP', 'Port', 'Country', 'Source File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def tikTokReturnPdfEventsIp(context):
    data_list = []
    sources = []
    for file_found, records in _parse_section(context, r'^EventsIPData_\d+\.pdf$',
                                              ('Date', 'IP', 'Event', 'Country'), ('Date',)):
        sources.append(file_found)
        rel = context.get_relative_path(file_found)
        for rec in records:
            data_list.append((_ts(_val(rec, 'Date')), _val(rec, 'Event'), _val(rec, 'IP'),
                              _val(rec, 'Country'), rel))

    data_headers = (('Timestamp', 'datetime'), 'Event', 'IP', 'Country', 'Source File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def tikTokReturnPdfVideoIp(context):
    data_list = []
    sources = []
    for file_found, records in _parse_section(context, r'^VideoIP\.pdf$',
                                              ('VID', 'Post date', 'IP', 'Country'), ('VID',)):
        sources.append(file_found)
        rel = context.get_relative_path(file_found)
        for rec in records:
            data_list.append((_ts(_val(rec, 'Post date')), _val(rec, 'VID'), _val(rec, 'IP'),
                              _val(rec, 'Country'), rel))

    data_headers = (('Post Date', 'datetime'), 'Video ID', 'IP', 'Country', 'Source File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def tikTokReturnPdfVideos(context):
    data_list = []
    sources = []
    media = _media_index(context, 'Videos')
    labels = ('VID', 'Video type', 'Post date', 'Video caption', 'Video link', 'Deletion time')
    for file_found, records in _parse_section(context, r'^VideoMetadata\.pdf$', labels, ('VID',)):
        sources.append(file_found)
        rel = context.get_relative_path(file_found)
        root = _split(file_found)[0]
        for rec in records:
            vid = _val(rec, 'VID')
            refs = _check_in(media.get((root, vid), []))
            data_list.append((_ts(_val(rec, 'Post date')), _ts(_val(rec, 'Deletion time')),
                              refs, vid, _val(rec, 'Video type'), _val(rec, 'Video caption'),
                              _uris(rec, 'Video link'), rel))

    data_headers = (('Post Date', 'datetime'), ('Deletion Time', 'datetime'), ('Media', 'media'),
                    'Video ID', 'Video Type', 'Caption', 'Video Link', 'Source File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def tikTokReturnPdfStories(context):
    data_list = []
    sources = []
    media = _media_index(context, 'Stories')
    for file_found, records in _parse_section(context, r'^StoriesMetadata\.pdf$',
                                              ('Post ID', 'Post caption', 'Post date'),
                                              ('Post ID',)):
        sources.append(file_found)
        rel = context.get_relative_path(file_found)
        root = _split(file_found)[0]
        for rec in records:
            post_id = _val(rec, 'Post ID')
            refs = _check_in(media.get((root, post_id), []))
            data_list.append((_ts(_val(rec, 'Post date')), refs, post_id,
                              _val(rec, 'Post caption'), rel))

    data_headers = (('Post Date', 'datetime'), ('Media', 'media'), 'Post ID', 'Caption',
                    'Source File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def tikTokReturnPdfPhotoPosts(context):
    data_list = []
    sources = []
    media = _media_index(context, 'Photo Post')
    labels = ('PhotopostID', 'PhotoPostCaption', 'Post date', 'Delete date', 'PhotoURL',
              'AudioID', 'AudioAuthor', 'AudioTitle', 'AudioURL', 'HasLivePhoto',
              'LivePhotoVideoID')
    for file_found, records in _parse_section(context, r'^PhotoMetadata\.pdf$', labels,
                                              ('PhotopostID',)):
        sources.append(file_found)
        rel = context.get_relative_path(file_found)
        root = _split(file_found)[0]
        for rec in records:
            post_id = _val(rec, 'PhotopostID')
            files = media.get((root, post_id), [])
            audio = [f for f in files if _is_audio(f)]
            images = [f for f in files if f not in audio]
            data_list.append((_ts(_val(rec, 'Post date')), _ts(_val(rec, 'Delete date')),
                              _check_in(images), _check_in(audio), post_id,
                              _val(rec, 'PhotoPostCaption'), _val(rec, 'AudioID'),
                              _val(rec, 'AudioAuthor'), _val(rec, 'AudioTitle'),
                              _val(rec, 'HasLivePhoto'), _val(rec, 'LivePhotoVideoID'),
                              _uris(rec, 'PhotoURL'), _uris(rec, 'AudioURL'), rel))

    data_headers = (('Post Date', 'datetime'), ('Delete Date', 'datetime'), ('Images', 'media'),
                    ('Audio', 'media'), 'Photo Post ID', 'Caption', 'Audio ID', 'Audio Author',
                    'Audio Title', 'HasLivePhoto (as stored)', 'Live Photo Video ID',
                    'Photo URL', 'Audio URL', 'Source File')
    return data_headers, data_list, '\n'.join(sources)


_SAVED_AS = re.compile(r'saved as ([^\]]+)\]')
_COMMENT_LABELS = ('Comment ID', 'Date', 'VideoPostID', 'VideoPostURL', 'PhotoPostID',
                   'PhotoPostURL', 'ReplyToComment', 'Comment', 'Comment photo Link')


@artifact_processor
def tikTokReturnPdfComments(context):
    data_list = []
    sources = []
    # Files under Content/Photo Comments, keyed by (return root, path below that folder).
    images = {}
    for file_found in context.get_files_found():
        file_found = str(file_found)
        split = _split(file_found)
        if (split and split[1] == 'Content' and len(split[2]) > 1
                and split[2][0] == 'Photo Comments' and not file_found.lower().endswith('.pdf')):
            images[(split[0], '/'.join(split[2][1:]))] = file_found

    for file_found, records in _parse_section(context, r'^(Video|Photo) Comments\.pdf$',
                                              _COMMENT_LABELS, ('Comment ID',)):
        sources.append(file_found)
        rel = context.get_relative_path(file_found)
        root = _split(file_found)[0]
        post_type = 'Photo' if os.path.basename(file_found).lower().startswith('photo') else 'Video'
        for rec in records:
            linked = []
            for value in rec.get('Comment photo Link', []):
                for name in _SAVED_AS.findall(value['text']):
                    path = images.get((root, name.strip().replace('\\', '/')))
                    if path:
                        linked.append(path)
                    else:
                        logfunc(f'{rel}: comment image named in the PDF not found in the return')
            data_list.append((_ts(_val(rec, 'Date')), post_type, _val(rec, 'Comment ID'),
                              _val(rec, f'{post_type}PostID'), _val(rec, 'Comment'),
                              _check_in(linked), _val(rec, 'ReplyToComment'),
                              _uris(rec, f'{post_type}PostURL'),
                              _uris(rec, 'Comment photo Link'), rel))

    data_headers = (('Timestamp', 'datetime'), 'Post Type', 'Comment ID', 'Post ID', 'Comment',
                    ('Comment Image', 'media'), 'ReplyToComment (as stored)', 'Post URL',
                    'Comment Image URL', 'Source File')
    return data_headers, data_list, '\n'.join(sources)


_LIVE_ROOM = re.compile(r'^(\S+)\s+Host User ID:\s*(\S+?):?$')
_LIVE_TIME = re.compile(r'^(.*?),\s*Device IP:\s*(\S+)$')


@artifact_processor
def tikTokReturnPdfLiveComments(context):
    data_list = []
    sources = []
    labels = ('Live comment in room ID', 'Comment Time', 'Content')
    for file_found, records in _parse_section(context, r'^LiveComment_\d+\.pdf$', labels,
                                              ('Live comment in room ID',)):
        sources.append(file_found)
        rel = context.get_relative_path(file_found)
        for rec in records:
            room, host = _val(rec, 'Live comment in room ID'), ''
            match = _LIVE_ROOM.match(room)
            if match:
                room, host = match.groups()
            when, ip = _val(rec, 'Comment Time'), ''
            match = _LIVE_TIME.match(when)
            if match:
                when, ip = match.groups()
            data_list.append((_ts(when), room, host, _val(rec, 'Content'), ip, rel))

    data_headers = (('Comment Time', 'datetime'), 'Room ID', 'Host User ID', 'Content',
                    'Device IP', 'Source File')
    return data_headers, data_list, '\n'.join(sources)


_MEDIA_SECTIONS = (
    ('Videos', r'^VideoMetadata\.pdf$', ('VID',), ('VID', 'Video type', 'Post date',
                                                   'Video caption', 'Video link',
                                                   'Deletion time')),
    ('Stories', r'^StoriesMetadata\.pdf$', ('Post ID',), ('Post ID', 'Post caption', 'Post date')),
    ('Photo Post', r'^PhotoMetadata\.pdf$', ('PhotopostID',),
     ('PhotopostID', 'PhotoPostCaption', 'Post date', 'Delete date', 'PhotoURL', 'AudioID',
      'AudioAuthor', 'AudioTitle', 'AudioURL', 'HasLivePhoto', 'LivePhotoVideoID')),
)


@artifact_processor
def tikTokReturnPdfMedia(context):
    data_list = []
    listed = set()
    for _, name_re, starts, labels in _MEDIA_SECTIONS:
        for file_found, records in _parse_section(context, name_re, labels, starts):
            root = _split(file_found)[0]
            listed.update((root, _val(rec, starts[0])) for rec in records)
    comment_images = set()
    for file_found, records in _parse_section(context, r'^Photo Comments\.pdf$',
                                              _COMMENT_LABELS, ('Comment ID',)):
        root = _split(file_found)[0]
        for rec in records:
            for value in rec.get('Comment photo Link', []):
                comment_images.update((root, name.strip().replace('\\', '/'))
                                      for name in _SAVED_AS.findall(value['text']))

    sources = []
    for file_found in sorted({str(f) for f in context.get_files_found()}):
        split = _split(file_found)
        if (not split or split[1] != 'Content' or len(split[2]) < 2
                or file_found.lower().endswith('.pdf') or not os.path.isfile(file_found)):
            continue
        root, _, below = split
        folder = below[0]
        if folder == 'Photo Comments':
            item_id = re.sub(r'_\d+$', '', os.path.splitext(below[-1])[0])
            in_metadata = 'Yes' if (root, '/'.join(below[1:])) in comment_images else 'No'
        elif folder in ('Videos', 'Stories', 'Photo Post'):
            item_id = below[1] if len(below) > 2 else os.path.splitext(below[1])[0]
            in_metadata = 'Yes' if (root, item_id) in listed else 'No'
        else:
            continue
        sources.append(file_found)
        data_list.append((_check_in([file_found]), folder, item_id, in_metadata,
                          '/'.join(below[1:]), context.get_relative_path(file_found)))

    data_headers = (('Media', 'media'), 'Content Folder', 'ID From Path', 'ID In Metadata PDF',
                    'Path In Folder', 'Source File')
    return data_headers, data_list, '\n'.join(sources)
