__artifacts_v2__ = {
    "discordReturnsfriends": {
        "name": "Discord - Friendships",
        "description": "Relationships/friendships from a Discord law enforcement return (relationships_*.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-12-04",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Discord Returns",
        "notes": "",
        "paths": ('*/relationships_*.csv',),
        "output_types": "standard",
        "artifact_icon": "users",
    }
}

import csv

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def discordReturnsfriends(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.csv'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)  # header
            for item in reader:
                if len(item) < 3:
                    continue
                data_list.append((item[0], item[1], item[2]))

    data_headers = ('User ID', 'Username', 'Relationship')
    return data_headers, data_list, context.get_relative_path(source_path)
