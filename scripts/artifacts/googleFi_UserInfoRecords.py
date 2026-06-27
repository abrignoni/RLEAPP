__artifacts_v2__ = {
    "googleFi_UserInfoRecords": {
        "name": "Google Fi - User Info Records",
        "description": "Parses Google Fi user info records from Takeout",
        "author": "@KevinPagano3",
        "creation_date": "2022-02-28",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Google Fi/User Info*/GoogleFi.UserInfo.Records.txt'),
        "output_types": "standard",
        "artifact_icon": "phone",
    }
}

import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor


def _utc_label_to_dt(value):
    # Source values are labelled " UTC"; strip the label and parse to an aware UTC datetime.
    value = value.replace(' UTC', '').strip()
    if not value:
        return value
    try:
        return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
    except ValueError:
        return value


@artifact_processor
def googleFi_UserInfoRecords(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'GoogleFi.UserInfo.Records.txt':
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            lines = f.readlines()[1:]

        for line in lines:
            entry = line.split('\t')
            if len(entry) < 17:
                continue
            data_list.append((
                _utc_label_to_dt(entry[2]), _utc_label_to_dt(entry[3]),
                entry[0], entry[1].replace('USAGE_TYPE_', '').title(),
                entry[4].replace('DIRECTION_', '').title(), entry[5].replace('Duration:', ''),
                entry[8], entry[9], entry[10], entry[11], _utc_label_to_dt(entry[12]),
                entry[13].title(), entry[14].title(), entry[15].title(), entry[16].strip().title()))

    data_headers = (('Start Timestamp', 'datetime'), ('End Timestamp', 'datetime'),
                    ('User Phone Number', 'phonenumber'), 'Usage Type', 'Direction',
                    'Duration (Minutes)', ('Remote Phone Number', 'phonenumber'),
                    'Equipment ID', 'Carrier', 'Network Carrier',
                    ('Network Carrier Start Timestamp', 'datetime'), 'Is Wifi?', 'Is Hosted Voice?',
                    'Is Hangouts?', 'Is Voicemail?')
    return data_headers, data_list, context.get_relative_path(source_path)
