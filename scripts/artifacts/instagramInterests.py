__artifacts_v2__ = {
    "instagramInterests": {
        "name": "Instagram Archive - Interests",
        "description": "Parses inferred advertising interests from an Instagram data archive (ads_interests.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-30",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/information_about_you/ads_interests.json'),
        "output_types": "standard",
        "artifact_icon": "instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def instagramInterests(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith('ads_interests.json'):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['inferred_data_ig_interest']:
                interest = x['string_map_data']['Interest'].get('value', '')
                data_list.append((interest,))

    data_headers = ('Interests',)
    return data_headers, data_list, context.get_relative_path(source_path)
