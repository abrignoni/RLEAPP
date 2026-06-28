__artifacts_v2__ = {
    "msftheadReturn": {
        "name": "Microsoft Returns - Headers",
        "description": "Email header metadata from Microsoft law enforcement returns "
                       "(*.eml_hdr.eml).",
        "author": "@AlexisBrignoni",
        "creation_date": "2022-02-09",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Microsoft Returns",
        "notes": "Timestamp is the email Date header (RFC 2822) normalized to UTC. The original "
                 "additionally wrote an EMLHeader.db SQLite database and two CSVs into the report "
                 "folder; that redundant on-disk export is removed (LAVA produces the table/TSV).",
        "paths": ('*.eml_hdr.eml',),
        "output_types": "standard",
        "artifact_icon": "mail",
    }
}

import email
import os
from datetime import timezone
from email.utils import parsedate_to_datetime

from scripts.ilapfuncs import artifact_processor


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
def msftheadReturn(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('.'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            msg = email.message_from_file(f)
        data_list.append((_mail_ts(msg['Date']), msg['x-originating-ip'] or '', msg['From'] or '',
                          msg['To'] or '', context.get_relative_path(file_found)))

    data_headers = (('Timestamp', 'datetime'), 'X Originating IP', 'From Address', 'To Address',
                    'Filename')
    return data_headers, data_list, context.get_relative_path(source_path)
