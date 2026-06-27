__artifacts_v2__ = {
    "fbigPofilePic": {
        "name": "Facebook Instagram Returns - Profile Picture",
        "description": "Profile picture (linked media) parsed from a Facebook/Instagram law enforcement return (index.html / preservation).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "",
        "paths": ('*/index.html', '*/preservation*.html', '*/linked_media/profile_picture_*'),
        "output_types": "standard",
        "artifact_icon": "user",
    }
}

import os

from bs4 import BeautifulSoup

from scripts.ilapfuncs import artifact_processor, check_in_media


@artifact_processor
def fbigPofilePic(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        basename = os.path.basename(file_found)
        if not (basename.startswith('index.html') or basename.startswith('preservation')):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        for section in soup.find_all('div', {'id': 'property-profile_picture'}):
            for table in section.find_all('table'):
                th = table.find('th')
                if not th or th.get_text() != 'Profile Picture':
                    continue
                td = th.find_next_sibling('td')
                value = td.get_text() if td else ''
                picture_name = value.split('/')[1] if '/' in value else value
                data_list.append((check_in_media(picture_name, picture_name), picture_name))

    data_headers = (('Linked Media File', 'media'), 'Filename')
    return data_headers, data_list, context.get_relative_path(source_path)
