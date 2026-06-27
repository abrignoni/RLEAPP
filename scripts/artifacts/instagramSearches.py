__artifacts_v2__ = {
    "instagramSearches": {  # This should match the function name exactly
        "name": "Instagram Archive - Searches",
        "description": "Parses Instagram searches",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-30",
        "last_update_date": "2025-07-02",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/recent_searches/account_searches.json'),
        "output_types": "standard",  # or ["html", "tsv", "timeline", "lava"]
        "artifact_icon": "instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc

@artifact_processor
def instagramSearches(context):
    files_found = context.get_files_found()
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('account_searches.json'):
            
            with open(file_found, "r", encoding="utf-8") as fp:
                deserialized = json.load(fp)
        
            for x in deserialized['searches_user']:
                search = x['string_map_data']['Search'].get('value', '')
                timestamp = x['string_map_data']['Time'].get('timestamp', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                
                data_list.append((timestamp, search))
    
    data_headers = (('Timestamp','datetime'), 'Search')
    return data_headers, data_list, context.get_relative_path(file_found)