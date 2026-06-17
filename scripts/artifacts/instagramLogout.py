__artifacts_v2__ = {
    "instagramLogout": {  # This should match the function name exactly
        "name": "Instagram Archive - Logout Activity",
        "description": "Parses Instagram logout activity",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-30",
        "last_update_date": "2025-07-04",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/login_and_*_creation/logout_activity.json'),
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
def instagramLogout(files_found, report_folder, seeker, wrap_text):
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
    
        if filename.startswith("logout_activity.json"):
            data_list =[]
            with open(file_found, "rb") as fp:
                deserialized = json.load(fp)
                
            login = (deserialized['account_history_logout_history'])
            for x in login:
                
                title = (x.get('title', '')).replace('T',' ')
                cookiename = (x['string_map_data']['Cookie Name'].get('value', ''))
                ipaddress = (x['string_map_data']['IP Address'].get('value', ''))
                langagecode = (x['string_map_data']['Language Code'].get('value', ''))
                timestamp = (x['string_map_data']['Time'].get('timestamp', ''))
                useragent = (x['string_map_data']['User Agent'].get('value', ''))
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                    
                data_list.append((timestamp, title, ipaddress, useragent, langagecode, cookiename))
    
    data_headers = (('Timestamp (Local)','datetime'), 'Timestamp (UTC)', 'IP Address', 'User Agent', 'Language Code', 'Cookie Name')
    return data_headers, data_list, file_found