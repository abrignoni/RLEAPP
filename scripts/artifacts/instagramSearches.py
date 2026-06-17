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
import datetime
import json
from pathlib import Path	

from scripts.ilapfuncs import artifact_processor

@artifact_processor
def instagramSearches(files_found, report_folder, seeker, wrap_text):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('account_searches.json'):
            
            with open(file_found, "r") as fp:
                deserialized = json.load(fp)
        
            for x in deserialized['searches_user']:
                search = x['string_map_data']['Search'].get('value', '')
                timestamp = x['string_map_data']['Time'].get('timestamp', '')
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                
                data_list.append((timestamp, search))
    
    data_headers = (('Timestamp','datetime'), 'Search')
    return data_headers, data_list, file_found