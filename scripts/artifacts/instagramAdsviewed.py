__artifacts_v2__ = {
    "instagramAdsviewed": {  # must match the function name exactly
        "name": "Instagram Archive - Ads Viewed",
        "description": "Parses ads viewed from an Instagram data archive (ads_viewed.json)",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-27",
        "last_update_date": "2026-06-26",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/ads_and_content/ads_viewed.json'),
        "output_types": "standard",  # or ["html", "tsv", "timeline", "lava"]
        "artifact_icon": "instagram",
    }
}

import os
import datetime
import json

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def instagramAdsviewed(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)

        if os.path.basename(file_found).startswith('ads_viewed.json'):
            source_path = file_found

            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['impressions_history_ads_seen']:
                author = x['string_map_data']['Author'].get('value', '')
                timestamp = x['string_map_data']['Time'].get('timestamp', '')
                # Epoch seconds -> render as UTC (the legacy code used naive
                # fromtimestamp, i.e. the parsing machine's local time).
                if timestamp:
                    timestamp = datetime.datetime.fromtimestamp(
                        int(timestamp), tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

                data_list.append((timestamp, author))

    data_headers = (('Timestamp', 'datetime'), 'Author')
    return data_headers, data_list, context.get_relative_path(source_path)
