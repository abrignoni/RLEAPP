__artifacts_v2__ = {
    "instagramSavedposts": {  # This should match the function name exactly
        "name": "Instagram Archive - Saved Posts",
        "description": "Parses Instagram saved posts",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-30",
        "last_update_date": "2025-07-02",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/saved/saved_posts.json'),
        "output_types": "standard",  # or ["html", "tsv", "timeline", "lava"]
        "artifact_icon": "instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc

@artifact_processor
def instagramSavedposts(context):
    files_found = context.get_files_found()
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('saved_posts.json'):
            
            with open(file_found, "r", encoding="utf-8") as fp:
                deserialized = json.load(fp)
        
            for x in deserialized['saved_saved_media']:
                title = x['title']
                href = x['string_map_data']['Saved on'].get('href', '')
                timestamp = x['string_map_data']['Saved on'].get('timestamp', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                    
                data_list.append((timestamp, title, href, context.get_relative_path(file_found)))
    
    data_headers = (('Timestamp', 'datetime'),'Profile Name', 'URL', 'File Source')
    return data_headers, data_list, 'See source path(s) below'