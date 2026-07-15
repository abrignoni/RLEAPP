__artifacts_v2__ = {
    "instagramPostcom": {
        "name": "Instagram Archive - Post Comments",
        "description": "Parses post comments from an Instagram data archive (post_comments.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-21",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/comments/post_comments.json'),
        "output_types": "standard",
        "artifact_icon": "brand-instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def instagramPostcom(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('post_comments.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['comments_media_comments']:
                title = x.get('title', '')
                comment = x['string_list_data'][0].get('value', '')
                timestamp = x['string_list_data'][0].get('timestamp', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                data_list.append((timestamp, title, comment))

    data_headers = (('Timestamp', 'datetime'), 'Title', 'Comment')
    return data_headers, data_list, context.get_relative_path(source_path)
