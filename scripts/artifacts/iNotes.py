__artifacts_v2__ = {
    "iNotes": {
        "name": "Apple Notes (iCloud Returns)",
        "description": "Apple Notes from an iCloud return (Notes/Metadata.txt) with note bodies "
                       "and attachments.",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-02-02",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Apple Notes",
        "notes": "Created/Modified are CloudKit millisecond timestamps normalized to UTC (the "
                 "original rendered them in local/Pacific time).",
        "paths": ('*/Notes/Metadata.txt', '*/Notes/*/**'),
        "output_types": "standard",
        "html_columns": ["Note"],
        "artifact_icon": "file-text",
    }
}

import json
import os

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc, check_in_media


@artifact_processor
def iNotes(context):
    data_list = []
    source_path = ''
    files = [str(f) for f in context.get_files_found()]
    for file_found in files:
        if not file_found.endswith('Metadata.txt'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)
        for record in data:
            recordname = record['recordName']
            created = record.get('created')
            created = convert_unix_ts_to_utc(created['timestamp']) if created else ''
            modified = record.get('modified')
            modified = convert_unix_ts_to_utc(modified['timestamp']) if modified else ''
            deleted = record.get('deleted')
            participants = record.get('participants')

            note_text = ''
            refs = []
            notapath = ''
            for match in files:
                if match.endswith('.DS_Store') or not os.path.isfile(match):
                    continue
                if recordname not in match:
                    continue
                ref = check_in_media(match, os.path.basename(match))
                if ref:
                    refs.append(ref)
                notapath = match
                if 'content' not in match:
                    with open(match, encoding='utf-8', errors='backslashreplace') as g:
                        note_text = g.read().replace('\n', '<br>')

            data_list.append((created, modified, note_text, recordname, refs,
                              '' if deleted is None else deleted,
                              '' if participants is None else str(participants),
                              context.get_relative_path(notapath)))

    data_headers = (('Timestamp Created', 'datetime'), ('Timestamp Modified', 'datetime'), 'Note',
                    'Record Name', ('Attachments', 'media'), 'Deleted?', 'Participants', 'Source')
    return data_headers, data_list, context.get_relative_path(source_path)
