"""Reader for the Meta business-records archive format.

A Meta law enforcement return unpacks to ``records.html``, zero or more
``preservation_N.html`` snapshots and a ``linked_media`` folder. Each HTML file is a
sequence of ``div.content-pane`` sections (one per record category, ``id`` of the form
``property-<name>``) built from four block classes:

    div.t.o            a field: its div.t.i holds the label as a bare text node,
    div.t.i            followed by div.m > div holding either the value text, or a
    div.m              nested list of records made of further div.t.o fields
    div.p              an empty spacer that separates records inside a nested list

The document is paginated for printing. A ``div.pageBreak`` can fall anywhere, and the
generator closes every open block at the break and reopens it on the next page as a
``div.t.o`` with an empty label. So a section's list, a record inside it, and even one
field's value can be split across two or more unlabelled continuation blocks. The reader
merges those back: an unlabelled block continues the labelled block before it, a record
that had no spacer after it continues into the next page, and an unlabelled leaf value
is appended to the leaf before it. Every count the reader produces was checked against
the literal label counts in the source text of a real return (see the artifact notes).

The older archive spelling used ``div.div_table.outer`` / ``div.div_table.inner`` /
``div.most_inner`` for the same three roles. Those class names are accepted as aliases,
but no return in that spelling was available while this reader was written, so that
path is code-present and unexercised.

Data model handed to the artifacts: a *field* is ``Field(label, value, media, text)``
where ``value`` is a ``str`` or a list of *records*, a record is a list of fields in
document order, ``media`` is the list of ``linked_media/...`` references found inside the
field (``img``/``source``/``video``/``audio`` ``src`` and ``a`` ``href``) and ``text`` is
the loose text a nested block carries ahead of its records.
"""

import os
import re
from collections import namedtuple
from datetime import datetime, timezone

from bs4 import BeautifulSoup, NavigableString

from scripts.ilapfuncs import check_in_media

OUTER = {'o', 'outer'}
INNER = {'i', 'inner'}
VALUE = {'m', 'most_inner'}
SPACER = {'p'}
PAGE_BREAK = {'pageBreak'}

NO_RECORDS = 'No responsive records'

# A field of a record. `value` is a str for a leaf or a list of records for a nested
# block; `media` lists the linked_media references inside it; `text` is the loose text a
# nested block carries before its records (the thread id of a Thread block), '' otherwise.
Field = namedtuple('Field', 'label value media text')

_ACCOUNT_RE = re.compile(r'^(?P<user>.*?)\s*\((?:Instagram:\s*)?(?P<id>\d+)\)\s*(?:\[(?P<display>.*)\])?\s*$', re.S)


def _classes(el):
    return set(el.get('class', [])) if getattr(el, 'attrs', None) is not None else set()


def _has(el, names):
    return bool(_classes(el) & names)


def _label(inner):
    for child in inner.children:
        if isinstance(child, NavigableString) and child.strip():
            return ' '.join(child.split())
    return ''


def _media_refs(container):
    refs = []
    for tag in container.find_all(['img', 'source', 'video', 'audio', 'a']):
        target = tag.get('src') or tag.get('href') or ''
        if 'linked_media' in target:
            refs.append(target)
    return refs


def _coalesce(record):
    """Merge every unlabelled field into the field before it (a page break)."""
    out = []
    for entry in record:
        label, value, media, loose, open_ = entry
        if label == '' and out:
            plabel, pvalue, pmedia, ploose, popen = out[-1]
            if isinstance(pvalue, list) and isinstance(value, list):
                _merge_lists(pvalue, value, popen)
                out[-1] = (plabel, pvalue, pmedia + media, ploose or loose, open_)
                continue
            if isinstance(pvalue, str) and isinstance(value, str):
                joined = pvalue + ('\n' if pvalue and value else '') + value
                out[-1] = (plabel, joined, pmedia + media, ploose, False)
                continue
            if isinstance(pvalue, str) and not pvalue.strip() and isinstance(value, list):
                out[-1] = (plabel, value, pmedia + media, loose, open_)
                continue
        out.append(entry)
    return out


def _merge_lists(first, second, first_open):
    """Append record list `second` to `first`; when `first`'s last record had no
    spacer after it (the page broke inside it), `second`'s first record continues it."""
    if first and second and first_open:
        first[-1] = _coalesce(first[-1] + second[0])
        second = second[1:]
    first.extend(second)


def _field(outer):
    inner = next((c for c in outer.children if getattr(c, 'name', None) == 'div' and _has(c, INNER)), None)
    if inner is None:
        return ('', outer.get_text('\n', strip=True), _media_refs(outer), '', False)
    label = _label(inner)
    holder = next((c for c in inner.children if getattr(c, 'name', None) == 'div' and _has(c, VALUE)), None)
    if holder is None:
        return (label, '', [], '', False)
    container = holder
    if 'm' in _classes(holder):
        wrapped = next((c for c in holder.children if getattr(c, 'name', None) == 'div'), None)
        if wrapped is not None:
            container = wrapped
    nested = any(getattr(c, 'name', None) == 'div' and _has(c, OUTER) for c in container.children)
    if nested:
        records, open_ = _parse_list(container)
        loose = '\n'.join(' '.join(c.split()) for c in container.children
                          if isinstance(c, NavigableString) and c.strip())
        return (label, records, _media_refs(container), loose, open_)
    return (label, container.get_text('\n', strip=True), _media_refs(container), '', False)


def _parse_list(container):
    """Records inside a nested container. Returns (records, open); `open` means the
    last record had no trailing spacer, so it may continue on the next page."""
    records, current, open_ = [], [], False
    for child in container.children:
        if getattr(child, 'name', None) != 'div':
            continue
        if _has(child, PAGE_BREAK):
            continue
        if _has(child, OUTER):
            current.append(_field(child))
            open_ = True
        elif _has(child, SPACER):
            if current:
                records.append(_coalesce(current))
                current = []
            open_ = False
    if current:
        records.append(_coalesce(current))
    return records, open_


def _strip(value):
    if isinstance(value, list):
        return [[Field(label, _strip(v), media, loose) for label, v, media, loose, _ in record]
                for record in value]
    return value


def _parse_section(pane):
    fields = [_field(c) for c in pane.children
              if getattr(c, 'name', None) == 'div' and _has(c, OUTER)]
    return [Field(label, _strip(value), media, loose) for label, value, media, loose, _ in _coalesce(fields)]


class Records:
    """One parsed HTML file of a return."""

    def __init__(self, path):
        self.path = str(path)
        self.name = os.path.basename(self.path)
        with open(self.path, 'rb') as handle:
            soup = BeautifulSoup(handle.read(), 'html.parser')
        self.sections = {}
        self.definitions = {}
        self.order = []
        for pane in soup.find_all('div', class_='content-pane'):
            pane_id = pane.get('id', '')
            if not pane_id.startswith('property-'):
                continue
            name = pane_id[len('property-'):]
            fields = _parse_section(pane)
            self.order.append(name)
            self.definitions[name] = '\n'.join(f.value for f in fields
                                                if f.label.endswith('Definition') and isinstance(f.value, str))
            self.sections[name] = [f for f in fields if not f.label.endswith('Definition')]
        self.params = {f.label: f.value for f in self.sections.get('request_parameters', [])
                       if isinstance(f.value, str)}
        target = self.params.get('Target', '').strip()
        self.target_id = target if target.isdigit() else ''

    def has(self, name):
        return name in self.sections

    def fields(self, name):
        return self.sections.get(name, [])

    def text(self, name, label=None):
        """The text value of a section's first leaf field (or the one named)."""
        for entry in self.fields(name):
            if isinstance(entry.value, str) and (label is None or entry.label == label):
                return entry.value
        return ''

    def is_empty(self, name):
        """True when the section holds no records: absent, or every value is the
        provider's 'No responsive records' placeholder or blank."""
        fields = self.fields(name)
        if not fields:
            return True
        for entry in fields:
            if isinstance(entry.value, list) and entry.value:
                return False
            if isinstance(entry.value, str) and entry.value.strip() and entry.value.strip() != NO_RECORDS:
                return False
            if entry.media:
                return False
        return True

    def records(self, name, label=None):
        """The records of a section's nested data field ([] when it holds none)."""
        for entry in self.fields(name):
            if isinstance(entry.value, list) and (label is None or entry.label == label):
                return entry.value
        return []

    def media(self, name):
        refs = []
        for entry in self.fields(name):
            refs.extend(entry.media)
        return refs


_CACHE = {}


def load(path):
    """Parse a return HTML file, once per run (every artifact reads the same files)."""
    path = str(path)
    try:
        stamp = (os.path.getsize(path), os.path.getmtime(path))
    except OSError:
        stamp = None
    cached = _CACHE.get(path)
    if cached is None or cached[0] != stamp:
        cached = (stamp, Records(path))
        _CACHE[path] = cached
    return cached[1]


def is_records_file(path):
    base = os.path.basename(str(path)).lower()
    return base == 'records.html' or (base.startswith('preservation') and base.endswith('.html'))


def records_files(files_found):
    """The return's HTML files among files_found, records.html first, in a stable order."""
    hits = [str(f) for f in files_found if is_records_file(f) and os.path.isfile(str(f))]
    return sorted(set(hits), key=lambda p: (os.path.basename(p).lower() != 'records.html', p))


def field(record, label):
    """The first field of a record carrying this label, or None."""
    for item in record:
        if item.label == label:
            return item
    return None


def text(record, label, default=''):
    """The value of the first leaf field of a record carrying this label."""
    for item in record:
        if item.label == label and isinstance(item.value, str):
            return item.value
    return default


def texts(record, label):
    return [item.value for item in record if item.label == label and isinstance(item.value, str)]


def sub(record, label):
    """The records of the first nested field of a record carrying this label."""
    for item in record:
        if item.label == label and isinstance(item.value, list):
            return item.value
    return []


def subs(record, label):
    return [item for item in record if item.label == label and isinstance(item.value, list)]


def media_refs(record):
    refs = []
    for item in record:
        refs.extend(item.media)
        if isinstance(item.value, list):
            for nested in item.value:
                refs.extend(media_refs(nested))
    return refs


def linked_media_files(record):
    """Every 'Linked Media File:' value inside a record, at any depth."""
    names = []
    for item in record:
        if item.label == 'Linked Media File:' and isinstance(item.value, str) and item.value.strip():
            names.append(item.value.strip())
        if isinstance(item.value, list):
            for nested in item.value:
                names.extend(linked_media_files(nested))
    return names


def lines(value):
    return [line.strip() for line in (value or '').split('\n') if line.strip()]


def parse_ts(value):
    """'YYYY-MM-DD HH:MM:SS UTC', ISO 8601 or epoch seconds -> aware UTC datetime.
    Anything else returns '' (the caller keeps the raw text elsewhere if it matters)."""
    value = (value or '').strip()
    if not value:
        return ''
    cleaned = value[:-4] if value.endswith(' UTC') else value
    if cleaned.isdigit():
        return datetime.fromtimestamp(int(cleaned), tz=timezone.utc)
    try:
        parsed = datetime.fromisoformat(cleaned.replace('Z', '+00:00'))
    except ValueError:
        return ''
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_account(value):
    """'username (Instagram: 123) [display name]' -> (username, id, display name).
    A value that does not carry the pattern comes back as (value, '', '')."""
    value = ' '.join((value or '').split())
    match = _ACCOUNT_RE.match(value)
    if not match:
        return (value, '', '')
    return (match.group('user').strip(), match.group('id'), (match.group('display') or '').strip())


def account_id(value):
    return parse_account(value)[1]


_TYPE_HINTS = {}


def media_type_hint(path):
    """'audio/mp4' for an ISO-BMFF file whose tracks are sound only, else None.

    The return names audio attachments '.mp3' and labels them audio/mpeg, but the bytes
    are ISO-BMFF ('isom' brand) holding one sound track, which a signature sniff types as
    video/mp4 and the report then renders as a video player. The handler boxes settle
    it: a file with a 'soun' handler and no 'vide' handler is audio."""
    path = str(path)
    if path in _TYPE_HINTS:
        return _TYPE_HINTS[path]
    hint = None
    try:
        with open(path, 'rb') as handle:
            head = handle.read(12)
            if head[4:8] == b'ftyp':
                data = head + handle.read()
                handlers = set(re.findall(rb'hdlr.{8}(vide|soun)', data, re.S))
                if handlers == {b'soun'}:
                    hint = 'audio/mp4'
    except OSError:
        hint = None
    _TYPE_HINTS[path] = hint
    return hint


def register_media(context, names):
    """check_in_media for each linked_media name; audio-only ISO-BMFF is typed as audio."""
    refs = []
    for name in names:
        staged = context.get_source_file_path(name)
        hint = media_type_hint(staged) if staged else None
        ref = check_in_media(name, name.rsplit('/', 1)[-1], force_type=hint)
        if ref:
            refs.append(ref)
    return refs


def flatten(record, prefix=''):
    """'label: value' lines for a record, nested records indented by their label."""
    out = []
    for item in record:
        name = f'{prefix}{item.label}' if item.label else prefix.rstrip(' / ')
        if isinstance(item.value, list):
            if item.text:
                out.append(f'{name}: {item.text}' if name else item.text)
            for index, nested in enumerate(item.value, 1):
                out.extend(flatten(nested, f'{name} {index} / ' if len(item.value) > 1 else f'{name} / '))
        else:
            out.append(f'{name}: {item.value}' if name else item.value)
    return out
