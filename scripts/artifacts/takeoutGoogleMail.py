__artifacts_v2__ = {
    "takeoutGoogleMail": {
        "name": "Google Takeout - Mail (MBOX)",
        "description": "Parses MBOX mailboxes (All Mail, Deleted) from a Google Takeout export, including attachments.",
        "author": "@AlexisBrignoni, Codex",
        "creation_date": "2022-01-19",
        "last_update_date": "2026-11-22",
        "requirements": "beautifulsoup4",
        "category": "Google Takeout Archive",
        "notes": "Body is the first eligible text/plain part, using a supported declared charset when strict "
                 "decoding succeeds. Supported character sets are ASCII, UTF-8, UTF-16/32 (including "
                 "little/big endian), ISO-8859-1/2/5/15, Windows-1252/932, KOI8-R, Shift-JIS, Big5, GB18030 "
                 "and EUC-JP/KR; their Python codec aliases are accepted. Missing, malformed, unknown or "
                 "unsupported charset declarations and invalid byte sequences use Latin-1 as a compatibility "
                 "fallback, not an inferred original encoding; text may display wrongly. An empty selected "
                 "plain part is not replaced by a later plain part. The plain selection does not skip "
                 "attachments or attached messages, so Body can be a text attachment's text. When the "
                 "selected plain part is missing or blank, Body is text extracted from the first "
                 "text/html part of the message itself that is not marked as an attachment, decoded by"
                 " the same charset rules, and Body Source names the part used. From HTML, tags, "
                 "comments and the text of closed style and script elements are removed, and line "
                 "breaks are placed at br and block tags. When a style or script element is never "
                 "closed, everything after its opening tag is kept as raw source. That includes the "
                 "style or script text and any tags. Within a line, each run of whitespace (no-break "
                 "spaces included), soft hyphens (U+00AD), U+034F, U+200B to U+200D and U+FEFF shows "
                 "as one space, and is dropped at the ends of the line. Other invisible characters are"
                 " left as they are. Each a element with a non-empty href is marked [n], a repeated "
                 "target keeps its first number, and Links lists the link targets by those numbers as "
                 "Python's HTML parser returns them, with character references decoded. Malformed "
                 "HTML, and a link target holding a bare ampersand before an entity name, can read "
                 "differently between Python versions. On thisisdfir_takeout (174 messages) the plain "
                 "part was used for 136 and the HTML part for 37, and 1 had no text in either part. A "
                 "blank Body does not mean the message had no content. A "
                 "Date header with no zone is treated as UTC. Attachments are the multipart message parts "
                 "that carry a Content-Disposition header and nonempty payload, which can include inline "
                 "parts. Selection, repeated inputs and per-row Source File are preserved; the report-level "
                 "source names the last eligible mailbox, including one that contributes no rows.",
        "paths": ('*/Mail/All mail Including Spam and Trash.mbox', '*/Deleted.mbox'),
        "output_types": "standard",
        "multiline_columns": ["Body", "Links"],
        "artifact_icon": "mail",
    }
}

import codecs
import mailbox
import re
from datetime import timezone
from email.utils import parsedate_to_datetime

from scripts.html_body_text import body_text_and_links
from scripts.ilapfuncs import artifact_processor, check_in_embedded_media


_BODY_CHARACTER_CODECS = frozenset({
    'ascii', 'utf-8', 'iso8859-1', 'cp1252',
    'utf-16', 'utf-16-le', 'utf-16-be',
    'utf-32', 'utf-32-le', 'utf-32-be',
    'iso8859-2', 'iso8859-5', 'iso8859-15', 'koi8-r',
    'shift_jis', 'big5', 'gb18030', 'euc_jp', 'euc_kr', 'cp932',
})


def _decode_body_payload(part, payload):
    """Honor supported declared character sets; retain Latin-1 fallback without guessing."""
    charset = part.get_content_charset()
    if charset and len(charset) <= 128 and re.fullmatch(r'[A-Za-z0-9._-]+', charset):
        try:
            canonical = codecs.lookup(charset).name
            if canonical in _BODY_CHARACTER_CODECS:
                return payload.decode(canonical, errors='strict')
        except (LookupError, UnicodeDecodeError):
            pass
    return payload.decode('Latin_1')


def _get_body(message):
    """Return the first text/plain body of an email message, or '' if none."""
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == 'text/plain' and not part.is_multipart():
                payload = part.get_payload(decode=True)
                if payload is not None:
                    return _decode_body_payload(part, payload)
    elif message.get_content_type() == 'text/plain':
        payload = message.get_payload(decode=True)
        if payload is not None:
            return _decode_body_payload(message, payload)
    return ''


def _get_html_body(message):
    """Return the decoded first text/html part of the message itself, or ''.

    Attachments and the contents of attached messages are not this message's body."""
    pending = [message]
    while pending:
        part = pending.pop()
        if part.is_multipart():
            if part is message or part.get_content_maintype() != 'message':
                pending.extend(reversed(part.get_payload()))
            continue
        if part.get_content_type() != 'text/html' or part.get_content_disposition() == 'attachment':
            continue
        payload = part.get_payload(decode=True)
        if payload is not None:
            return _decode_body_payload(part, payload)
    return ''


def _body_columns(message):
    """(Body, Body Source, Links): the plain part, or the HTML part when plain is missing or blank."""
    body = _get_body(message)
    if body.strip():
        return body, 'text/plain', ''
    html_body = _get_html_body(message)
    text, links = body_text_and_links(html_body)
    if text or links:
        return text, 'text/html', links
    return body, '', ''


def _parse_date(value):
    if not value:
        return ''
    try:
        dt = parsedate_to_datetime(value)
    except (ValueError, TypeError):
        return value
    if dt is None:
        return value
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


@artifact_processor
def takeoutGoogleMail(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.mbox'):
            continue
        source_path = file_found
        rel = context.get_relative_path(file_found)

        for message in mailbox.mbox(file_found):
            attachments = []
            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    payload = part.get_payload(decode=True)
                    if payload:
                        name = part.get_filename() or part.get_content_type()
                        ref = check_in_embedded_media(file_found, payload, name)
                        if ref:
                            attachments.append(ref)
            body, body_source, links = _body_columns(message)
            data_list.append((_parse_date(message.get('date', '')), message.get('from', ''),
                              message.get('to', ''), str(message.get('Subject', '')),
                              body, body_source, links, attachments, rel))

    data_headers = (('Date', 'datetime'), 'From Address', 'To Address', 'Subject', 'Body',
                    'Body Source', 'Links', ('Attachments', 'media'), 'Source File')
    return data_headers, data_list, context.get_relative_path(source_path)
