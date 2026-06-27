__artifacts_v2__ = {
    "instagramProfchanges": {
        "name": "Instagram Archive - Profile Changes",
        "description": "Parses profile changes from an Instagram data archive (profile_changes.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-20",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/account_information/profile_changes.json'),
        "output_types": "standard",
        "html_columns": ["Items"],
        "artifact_icon": "instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def instagramProfchanges(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('profile_changes.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['profile_profile_change']:
                if not x.get('title'):
                    continue
                title = x.get('title', '')
                aggregator = ''
                for section in ('media_map_data', 'string_map_data'):
                    block = x.get(section)
                    if not block:
                        continue
                    for y, z in block.items():
                        for c, d in z.items():
                            if d and 'timestamp' in c:
                                d = convert_unix_ts_to_utc(d)
                            aggregator += f'{y} - {c} - {d} <br>'
                data_list.append((title, aggregator))

    data_headers = ('Title', 'Items')
    return data_headers, data_list, context.get_relative_path(source_path)
