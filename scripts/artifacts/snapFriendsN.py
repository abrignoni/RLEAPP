__artifacts_v2__ = {
    "snapFriendsN": {
        "name": "Snapchat - Friends",
        "description": "Friends list parsed from a Snapchat law enforcement return (friends_list.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-06-13",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Snapchat Returns",
        "notes": "",
        "paths": ('*/friends_list.csv',),
        "output_types": "standard",
        "artifact_icon": "users",
    }
}

import os

from scripts.ilapfuncs import artifact_processor


def _clean_and_group(input_data):
    sections, current, exclude = [], [], False
    for line in input_data.split('\n'):
        if line.startswith('---') or line.startswith('==='):
            exclude = not exclude
            if not exclude and current:
                sections.append(current)
                current = []
            continue
        if not exclude and line.strip():
            current.append(line.strip())
    if current:
        sections.append(current)
    return sections


@artifact_processor
def snapFriendsN(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('friends_list.csv'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            for section in _clean_and_group(f.read()):
                for line in section[1:]:
                    data_list.append((line,))

    data_headers = ('Friends',)
    return data_headers, data_list, context.get_relative_path(source_path)
