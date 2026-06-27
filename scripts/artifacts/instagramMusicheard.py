__artifacts_v2__ = {
    "instagramMusicheard": {
        "name": "Instagram Archive - Music Heard In Stories",
        "description": "Parses music heard in stories from an Instagram data archive (music_heard_in_stories.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-27",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/ads_and_content/music_heard_in_stories.json'),
        "output_types": "standard",
        "artifact_icon": "instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def instagramMusicheard(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('music_heard_in_stories.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['impressions_history_music_heard_in_stories']:
                song = x['string_map_data']['Song'].get('value', '')
                artist = x['string_map_data']['Artist'].get('value', '')
                timestamp = x['string_map_data']['Time'].get('timestamp', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                data_list.append((timestamp, song, artist))

    data_headers = (('Timestamp', 'datetime'), 'Song', 'Artist')
    return data_headers, data_list, context.get_relative_path(source_path)
