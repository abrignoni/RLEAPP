__artifacts_v2__ = {
    "instagramPersinfo": {
        "name": "Instagram Archive - Personal Info",
        "description": "Parses Instagram personal information about the local user account",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-30",
        "last_update_date": "2025-07-06",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/*_information/personal_information.json', '*/media/other/*.jpg'),
        "output_types": "standard",  # or ["html", "tsv", "timeline", "lava"]
        "artifact_icon": "instagram",
    }
}

import datetime
import inspect
import json
import os
import shutil
from pathlib import Path

from scripts.ilapfuncs import artifact_processor, check_in_media, logfunc

def timestamp_check(timestamp):
    if timestamp > 0:
        timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
    else:
        timestamp = ''
    return timestamp

@artifact_processor
def instagramPersinfo(files_found, report_folder, seeker, wrap_text):
    artifact_info = inspect.stack()[0]
    data_list = []
    sources = []
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        if filename.startswith('personal_information.json'):
            sources.append(file_found)
            with open(file_found, "rb") as fp:
                deserialized = json.load(fp)
                for x in deserialized['profile_user']:
                    for key, values in x.items():
                        if key == 'media_map_data':
                            for a, b in values.items():
                                if a == 'Profile Photo':
                                    photo = (b.get('uri', '')).replace('media/other/','')
                                    value = (b.get('title', ''))
                                    timestamp = timestamp_check(b.get('creation_timestamp', ''))
                                    
                                    media_item = ''
                                    
                                    for match in files_found:
                                        if photo in match:
                                            if str(match).startswith('\\'):
                                                sources.append(match[4:])
                                            else:
                                                sources.append(match)
                                            # locationfiles = f'{report_folder}/media/other'
                                            # filename = os.path.basename(match)
                                            # Path(f'{locationfiles}').mkdir(parents=True, exist_ok=True)
                                            # shutil.copy2(match, locationfiles)
                                            # thumb = f'<img src="{locationfiles}/{filename}" width="300"></img>'
                                            media_item = check_in_media(match,photo)
                                            break
                                                    
                                    data_list.append((timestamp, a, value, media_item, ''))
                        elif key == 'string_map_data':
                            for a, b in values.items():
                                if a in ['Email','Phone Number','Gender','Date of birth','Website']:
                                    href = (b.get('href', ''))
                                    value = (b.get('value', ''))
                                    timestamp = timestamp_check(b.get('timestamp', ''))
                                    data_list.append((timestamp, a, value, '',href))
                                                   
    data_headers = (('Timestamp', 'datetime'), 'Key', 'Value', ('URI','media'), 'HREF')
    #('HREF/URI','media'))
    source_files = "\n\n".join(sources)
    return data_headers, data_list, source_files