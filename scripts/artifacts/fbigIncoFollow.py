__artifacts_v2__ = {
    "fbigIncoFollow": {
        "name": "Facebook Instagram Returns - Incoming Follow Requests",
        "description": "Incoming follow requests parsed from a Facebook/Instagram law enforcement return (index.html / preservation).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "",
        "paths": ('*/index.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "user-plus",
    }
}

import os

from bs4 import BeautifulSoup

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def fbigIncoFollow(context):
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

        for section in soup.find_all('div', {'id': 'property-incoming_follow_requests'}):
            for table in section.find_all('table'):
                th = table.find('th')
                td = th.find_next_sibling('td') if th else None
                if not td:
                    continue
                for br in td.find_all('br'):
                    br.replace_with('\n')
                for user in td.get_text().split('\n'):
                    user = user.strip()
                    if user:
                        data_list.append((user,))

    data_headers = ('User',)
    return data_headers, data_list, context.get_relative_path(source_path)
