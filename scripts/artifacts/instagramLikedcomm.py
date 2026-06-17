__artifacts_v2__ = {
    "instagramLikedcomm": {  # This should match the function name exactly
        "name": "Instagram Archive - Liked Comments",
        "description": "Parses Instagram liked comments",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-30",
        "last_update_date": "2025-07-03",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/likes/liked_comments.json'),
        "output_types": "standard",  # or ["html", "tsv", "timeline", "lava"]
        "artifact_icon": "instagram",
    }
}

import os
import datetime
import json
from pathlib import Path	

from scripts.ilapfuncs import artifact_processor, utf8_in_extended_ascii

@artifact_processor

def instagramLikedcomm(files_found, report_folder, seeker, wrap_text):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('liked_comments.json'):
            
            with open(file_found, "r") as fp:
                deserialized = json.load(fp)
        
            for x in deserialized['likes_comment_likes']:
                title = x.get('title', '')
                href = x['string_list_data'][0].get('href', '')
                value = x['string_list_data'][0].get('value', '')
                value = utf8_in_extended_ascii(value)[1]
                timestamp = x['string_list_data'][0].get('timestamp', '')
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                    
                data_list.append((timestamp, title, href, value))
                
    data_headers = (('Timestamp', 'datetime'),'Account Name', 'Post URL', 'Value')
    return data_headers, data_list, file_found