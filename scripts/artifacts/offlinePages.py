__artifacts_v2__ = {
    "offlinePages": {
        "name": "Offline Pages",
        "description": "Saved offline web pages (MHTML) with their original web source and a media "
                       "preview.",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-01-25",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Offline Pages",
        "notes": "Timestamp Modified is the file's on-disk modification time (UTC). MIME Date is the "
                 "raw Date header from the saved page (kept as text; format varies).",
        "paths": ('*/*.mhtml', '*/*.mht'),
        "output_types": "standard",
        "artifact_icon": "globe",
    }
}

import email
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, check_in_media


@artifact_processor
def offlinePages(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('.'):
            continue
        source_path = file_found
        modified = datetime.fromtimestamp(os.path.getmtime(file_found), tz=timezone.utc)
        with open(file_found, 'r', encoding='utf-8', errors='replace') as fp:
            message = email.message_from_file(fp)
        media = check_in_media(file_found, os.path.basename(file_found))
        data_list.append((modified, media, message['Snapshot-Content-Location'] or '',
                          message['Subject'] or '', message['Date'] or '',
                          context.get_relative_path(file_found)))

    data_headers = (('Timestamp Modified', 'datetime'), ('File', 'media'), 'Web Source', 'Subject',
                    'MIME Date', 'Source in Extraction')
    return data_headers, data_list, context.get_relative_path(source_path)
