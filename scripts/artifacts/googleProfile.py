__artifacts_v2__ = {
    "googleProfile": {
        "name": "Google Profile",
        "description": "Parses Google profile information from Takeout",
        "author": "@KevinPagano3",
        "creation_date": "2021-08-23",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Profile/Profile.json', '*/Profile/ProfilePhoto.jpg'),
        "output_types": "standard",
        "artifact_icon": "user",
    }
}

import json
import os

from scripts.ilapfuncs import artifact_processor, check_in_media


@artifact_processor
def googleProfile(context):
    data_list = []
    source_path = ''
    files_found = context.get_files_found()

    photo_ref = None
    for file_found in files_found:
        if os.path.basename(str(file_found)) == 'ProfilePhoto.jpg':
            photo_ref = check_in_media(str(file_found), 'ProfilePhoto.jpg')

    for file_found in files_found:
        file_found = str(file_found)
        if os.path.basename(file_found) != 'Profile.json':
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        name = data.get('name', {}).get('formattedName', '')
        display_name = data.get('displayName', '')
        birthday = data.get('birthday', '')
        gender = data.get('gender', {}).get('type', '') if data.get('gender') else ''
        emails = '; '.join(e.get('value', '') for e in data.get('emails', []))
        data_list.append((name, display_name, emails, birthday, gender, photo_ref))

    data_headers = ('Name', 'Display Name', 'Email Address(s)', 'Birthday', 'Gender',
                    ('Profile Pic', 'media'))
    return data_headers, data_list, context.get_relative_path(source_path)
