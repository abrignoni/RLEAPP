"""Chrome sync settings from a Google Takeout, for RLEAPP.

Author: @AlexisBrignoni, Claude.
"""

__artifacts_v2__ = {
    "chromeSyncSettings": {
        "name": "Chrome Sync Settings",
        "description": "Name and value entries from the Chrome/SyncSettings.json file of a Google Takeout, "
                       "each with the section it sits in (Apps, App Settings, Preferences and Themes in the "
                       "tested export).",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-11-14",
        "last_update_date": "2026-11-14",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Reads each Chrome/SyncSettings.json a Takeout holds. The file is a JSON object whose "
                 "top-level keys are sections; in the tested export they are Apps, App Settings, Preferences "
                 "and Themes, each a list. Preferences held name and value entries; the other three lists "
                 "were empty, so the shape of their entries was not seen. One row is written per entry: "
                 "Section is the top-level key it came from, Name is the entry's name field and Value is its "
                 "value field as stored. In the tested export every value was a JSON string, so a value that "
                 "is itself a JSON object or array is kept as the string the export holds, and a string "
                 "setting keeps its quotes; nothing in the value is parsed or interpreted. A value that is "
                 "not a JSON string is written as its JSON text, re-serialised by the parser. An entry that "
                 "is not an object with name and value fields is written with an empty Name and the entry's "
                 "own JSON in Value and counted in the run log; a section whose value is not a list is "
                 "counted and skipped; neither case, and no non-string value, occurred in the tested export. "
                 "Every top-level section is read, including any a later Takeout adds beyond the four above. "
                 "Source File names the SyncSettings.json each row came from. The file name suggests Chrome "
                 "settings synced to the Google account; what Google puts in it is not sourced here. It is a "
                 "Takeout export file, not a reading of a Chrome profile on a device. Chrome/Extensions.json "
                 "is not read here; Chrome Extensions reads its Extensions key. "
                 "On thisisdfir_takeout the Preferences section held 10 entries and the Apps, App Settings "
                 "and Themes sections were each empty, so Section held Preferences on all 10 rows and Source "
                 "File held the one SyncSettings.json path on all 10 rows; the Apps, App Settings and Themes "
                 "sections are read but were not exercised by this sample. One Preferences value was a JSON "
                 "object with 6 members and another a JSON object with 2 members, each kept as the stored "
                 "JSON string. Name and Value are reported as stored; no section or value is given a meaning "
                 "here.",
        "paths": ('*/Chrome/SyncSettings.json',),
        "output_types": "standard",
        "artifact_icon": "settings",
        "sample_data": {
            "thisisdfir_takeout": "Google Takeout | 10 rows (Preferences; Apps, App Settings and Themes empty)",
        },
    }
}

import json
import os
from collections import Counter

from scripts.ilapfuncs import artifact_processor, logfunc


def _read(path):
    with open(path, encoding='utf-8') as handle:
        return json.load(handle)


@artifact_processor
def chromeSyncSettings(context):
    data_headers = ('Section', 'Name', 'Value', 'Source File')
    data_list = []
    read = []
    problems = Counter()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'SyncSettings.json':
            continue
        try:
            data = _read(file_found)
        except (OSError, ValueError):
            problems['SyncSettings.json files that could not be read as JSON'] += 1
            continue
        if not isinstance(data, dict):
            problems['SyncSettings.json files whose top level is not an object'] += 1
            continue
        relative = context.get_relative_path(file_found)
        wrote = False
        for section, entries in data.items():
            if not isinstance(entries, list):
                problems[f'{section} sections whose value is not a list, skipped'] += 1
                continue
            for entry in entries:
                if isinstance(entry, dict) and 'name' in entry and 'value' in entry:
                    name = entry['name']
                    value = entry['value']
                    if not isinstance(value, str):
                        value = json.dumps(value, ensure_ascii=False)
                else:
                    name = ''
                    value = json.dumps(entry, ensure_ascii=False)
                    problems[f'{section} entries not in name/value form'] += 1
                data_list.append((section, name, value, relative))
                wrote = True
        if wrote:
            read.append(file_found)
    if problems:
        logfunc('Chrome Sync Settings: '
                + ', '.join(f'{count} {kind}' for kind, count in sorted(problems.items())))
    return data_headers, data_list, '\n'.join(read)
