__artifacts_v2__ = {
    "instagramVideoswatched": {
        "name": "Instagram Archive - Videos Watched",
        "description": "Parses videos watched from an Instagram data archive (videos_watched.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-27",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/ads_and_content/videos_watched.json'),
        "output_types": "standard",
        "artifact_icon": "instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def instagramVideoswatched(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('videos_watched.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['impressions_history_videos_watched']:
                author = x['string_map_data']['Author'].get('value', '')
                timestamp = x['string_map_data']['Time'].get('timestamp', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                data_list.append((timestamp, author))

    data_headers = (('Timestamp', 'datetime'), 'Author')
    return data_headers, data_list, context.get_relative_path(source_path)
