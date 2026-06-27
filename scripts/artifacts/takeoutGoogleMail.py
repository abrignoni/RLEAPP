__artifacts_v2__ = {
    "takeoutGoogleMail": {
        "name": "Google Takeout - Mail (MBOX)",
        "description": "Parses MBOX mailboxes (All Mail, Deleted) from a Google Takeout export, including attachments.",
        "author": "@AlexisBrignoni",
        "creation_date": "2022-01-19",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Mail/All mail Including Spam and Trash.mbox', '*/Deleted.mbox'),
        "output_types": "standard",
        "artifact_icon": "mail",
    }
}

import mailbox
from datetime import timezone
from email.utils import parsedate_to_datetime

from scripts.ilapfuncs import artifact_processor, check_in_embedded_media


def _get_body(message):
    """Return the first text/plain body of an email message, or '' if none."""
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == 'text/plain' and not part.is_multipart():
                payload = part.get_payload(decode=True)
                if payload is not None:
                    return payload.decode('Latin_1')
    elif message.get_content_type() == 'text/plain':
        payload = message.get_payload(decode=True)
        if payload is not None:
            return payload.decode('Latin_1')
    return ''


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
            data_list.append((_parse_date(message.get('date', '')), message.get('from', ''),
                              message.get('to', ''), str(message.get('Subject', '')),
                              _get_body(message), attachments, rel))

    data_headers = (('Date', 'datetime'), 'From Address', 'To Address', 'Subject', 'Body',
                    ('Attachments', 'media'), 'Source File')
    return data_headers, data_list, context.get_relative_path(source_path)
