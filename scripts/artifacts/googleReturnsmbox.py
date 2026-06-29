__artifacts_v2__ = {
    "googleReturnsmbox": {
        "name": "Google Returns - Mail (MBOX)",
        "description": "Email messages from a Google law enforcement return mbox.",
        "author": "@AlexisBrignoni",
        "creation_date": "2022-01-19",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Google Returns",
        "notes": "Parses the same mbox as the Takeout 'Google Takeout - Mail (MBOX)' artifact, plus "
                 "the warrant-return *.Mail.MessageContent_* folder. Attachments are embedded "
                 "in-memory via check_in_embedded_media (the original wrote each attachment to disk "
                 "in the report folder).",
        "paths": ('*/*.Mail.MessageContent_*/Mail/All mail Including Spam and Trash.mbox',
                  '*/Mail/All mail Including Spam and Trash.mbox'),
        "output_types": "standard",
        "artifact_icon": "mail",
    }
}

import mailbox
from datetime import timezone
from email.utils import parsedate_to_datetime

from scripts.ilapfuncs import artifact_processor, check_in_embedded_media


def getbody(message):
    body = None
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload(decode=True).decode('Latin_1')
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode('Latin_1')
    elif message.get_content_type() == 'text/plain':
        body = message.get_payload(decode=True).decode('Latin_1')
    return body


def _mail_ts(value):
    value = (value or '').strip()
    if not value:
        return value
    try:
        dt = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return value
    if dt is None:
        return value
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


@artifact_processor
def googleReturnsmbox(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.mbox'):
            continue
        source_path = file_found
        for message in mailbox.mbox(file_found):
            thebody = getbody(message)
            if thebody is None:
                thebody = 'Check source data.'

            refs = []
            attachment_number = 0
            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    filename = part.get_filename()
                    if filename is None:
                        attachment_number += 1
                        filename = str(attachment_number)
                    data = part.get_payload(decode=True)
                    if data:
                        ref = check_in_embedded_media(file_found, data, filename)
                        if ref:
                            refs.append(ref)

            data_list.append((_mail_ts(message['date']), message['from'] or '',
                              message['to'] or '', str(message['Subject']), thebody, refs))

    data_headers = (('Date', 'datetime'), 'From Address', 'To Address', 'Subject', 'Body',
                    ('Attachments', 'media'))
    return data_headers, data_list, context.get_relative_path(source_path)
