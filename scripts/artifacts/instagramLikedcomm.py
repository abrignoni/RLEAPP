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
        "artifact_icon": "brand-instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, utf8_in_extended_ascii, convert_unix_ts_to_utc

@artifact_processor

def instagramLikedcomm(context):
    files_found = context.get_files_found()
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('liked_comments.json'):
            
            with open(file_found, "r", encoding="utf-8") as fp:
                deserialized = json.load(fp)
        
            for x in deserialized['likes_comment_likes']:
                title = x.get('title', '')
                href = x['string_list_data'][0].get('href', '')
                value = x['string_list_data'][0].get('value', '')
                value = utf8_in_extended_ascii(value)[1]
                timestamp = x['string_list_data'][0].get('timestamp', '')
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                    
                data_list.append((timestamp, title, href, value))
                
    data_headers = (('Timestamp', 'datetime'),'Account Name', 'Post URL', 'Value')
    return data_headers, data_list, context.get_relative_path(file_found)