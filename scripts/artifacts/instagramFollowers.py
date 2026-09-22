__artifacts_v2__ = {
    "instagramFollowers": {  # This should match the function name exactly
        "name": "Instagram Archive - Followers",
        "description": "Parses Instagram followers",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-30",
        "last_update_date": "2025-07-02",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/followers_and_following/followers.json',
                  '*/followers_and_following/followers_*.json'),
        "output_types": "standard",  # or ["html", "tsv", "timeline", "lava"]
        "artifact_icon": "brand-instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc

@artifact_processor
def instagramFollowers(context):
    files_found = context.get_files_found()
    data_list = []
    source_paths = set()
    for file_found in files_found:
        file_found = str(file_found)

        filename = os.path.basename(file_found)

        if filename.startswith('followers') and 'following' not in filename:
            source_paths.add(file_found)

            with open(file_found, "r", encoding="utf-8") as fp:
                deserialized = json.load(fp)
        
            records = deserialized.get('relationships_followers', deserialized) \
                if isinstance(deserialized, dict) else deserialized
            for x in records:
                href = x['string_list_data'][0].get('href', '')
                value = x['string_list_data'][0].get('value', '')
                timestamp = x['string_list_data'][0].get('timestamp', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                
                data_list.append((timestamp, value, href, context.get_relative_path(file_found)))
    
    data_headers = (('Timestamp', 'datetime'),'Follower', 'Profile URL', 'File Source')
    return data_headers, data_list, '\n'.join(sorted(source_paths))