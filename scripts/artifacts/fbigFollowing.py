__artifacts_v2__ = {
    "fbigFollowing": {
        "name": "Facebook Instagram Returns - Following",
        "description": "Accounts followed, parsed from a Facebook/Instagram law enforcement return (records.html / preservation).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "user-check",
    }
}

import os

from bs4 import BeautifulSoup

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def fbigFollowing(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        basename = os.path.basename(file_found)
        if not (basename.startswith('records.html') or basename.startswith('preservation')):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as fp:
            soup = BeautifulSoup(fp, 'lxml')

        for section in soup.find_all('div', {'id': 'property-following'}):
            for index, div in enumerate(section.find_all('div', class_='div_table inner')):
                if index == 0:
                    continue
                inner = div.find('div', class_='most_inner')
                if not inner:
                    continue
                for br in inner.find_all('br'):
                    br.replace_with('\n')
                for user in inner.get_text().split('\n'):
                    user = user.strip()
                    if user:
                        data_list.append((user,))

    data_headers = ('User',)
    return data_headers, data_list, context.get_relative_path(source_path)
