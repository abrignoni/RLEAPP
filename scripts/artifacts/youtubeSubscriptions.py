__artifacts_v2__ = {
    "youtubeSubscriptions": {
        "name": "YouTube Subscriptions",
        "description": "User channel subscriptions for YouTube.",
        "author": "@KevinPagano3",
        "creation_date": "2021-09-25",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/YouTube and YouTube Music/subscriptions/subscriptions.csv'),
        "output_types": "standard",
        "artifact_icon": "youtube",
    }
}

import csv
import os

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def youtubeSubscriptions(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('subscriptions.csv'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for item in reader:
                if len(item) == 0:
                    continue
                data_list.append((item[0], item[1], item[2]))

    data_headers = ('Channel ID', 'Channel URL', 'Channel Title')
    return data_headers, data_list, context.get_relative_path(source_path)
