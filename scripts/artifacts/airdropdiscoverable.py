__artifacts_v2__ = {
    "airdropdiscoverable": {
        "name": "AirDrop - Discoverable",
        "description": "AirDrop 'Updated people' discoverability events from the unified log "
                       "(airdrop.ndjson): nearby people and their advertised identity fields.",
        "author": "@AlexisBrignoni",
        "creation_date": "2022-09-08",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Airdrop Discoverable",
        "notes": "Timestamp is the unified-log time parsed with its UTC offset and normalized to "
                 "UTC. The 'Updated People' column was named 'Update' in the original (a SQL "
                 "reserved word); the 'UWB Capable' header fixes the original 'UWC capable' typo "
                 "(Ultra Wideband).",
        "paths": ('*/airdrop.ndjson',),
        "output_types": "standard",
        "artifact_icon": "radio",
    }
}

import json
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor


def _log_ts(value):
    value = (value or '').strip()
    if not value:
        return value
    for fmt in ('%Y-%m-%d %H:%M:%S.%f%z', '%Y-%m-%d %H:%M:%S%z'):
        try:
            return datetime.strptime(value, fmt).astimezone(timezone.utc)
        except ValueError:
            continue
    return value


@artifact_processor
def airdropdiscoverable(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('airdrop.ndjson') or os.path.basename(file_found).startswith('.'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as data:
            for line in data:
                if not line.strip():
                    continue
                deserialized = json.loads(line)
                if deserialized.get('finished', '') == 1:
                    break
                eventmessage = deserialized.get('eventMessage', '')
                if 'Updated people:' not in eventmessage:
                    continue

                eventtimestamp = _log_ts(deserialized.get('timestamp', ''))
                traceid = deserialized.get('traceID', '')

                realname = displayname = secondaryname = ''
                isme = isknown = israpport = uwbcapable = updatedp = ''
                for part in eventmessage.split(','):
                    if '<NSOrderedCollectionDifference' in part:
                        updatedp = part.split('(')[1].replace('<', '')
                    elif 'Updated people' in part:
                        updatedp = part.split(': ')[1]
                    elif 'realName' in part:
                        realname = part.split(': ')[1]
                    elif 'displayName' in part:
                        displayname = part.split(': ')[1]
                    elif 'secondaryName' in part:
                        secondaryname = part.split(': ')[1]
                    elif 'isMe' in part:
                        isme = part.split(': ')[1]
                    elif 'isKnown' in part:
                        isknown = part.split(': ')[1]
                    elif 'isRapport' in part:
                        israpport = part.split(': ')[1]
                    elif 'uwbCapable' in part:
                        uwbcapable = part.split(': ')[1].replace('>', '')

                data_list.append((eventtimestamp, traceid, updatedp, realname, displayname,
                                  secondaryname, isme, isknown, israpport, uwbcapable))

    data_headers = (('Timestamp', 'datetime'), 'Trace ID', 'Updated People', 'Real Name',
                    'Display Name', 'Secondary Name', 'Is me?', 'Is Known?', 'Is Rapport?',
                    'UWB Capable')
    return data_headers, data_list, context.get_relative_path(source_path)
