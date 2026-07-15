__artifacts_v2__ = {
    "fbigDevices": {
        "name": "Facebook Instagram Returns - Devices",
        "description": "Devices parsed from a Facebook/Instagram law enforcement return (index.html / preservation).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "",
        "paths": ('*/index.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "device-mobile",
    }
}

import os

from bs4 import BeautifulSoup

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def fbigDevices(context):
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

        for section in soup.find_all('div', {'id': 'property-devices'}):
            for table in section.find_all('table'):
                th = table.find('th')
                if not th or th.get_text() != 'Devices':
                    continue
                type_ = device_id = ''
                for subtable in table.find_all('table'):
                    sth = subtable.find('th')
                    if not sth:
                        continue
                    label = sth.get_text()
                    std = sth.find_next_sibling('td')
                    value = std.get_text() if std else ''
                    if label == 'Type':
                        type_ = value
                    elif label == 'Id':
                        device_id = value
                    elif label == 'Active':
                        data_list.append((type_, device_id, value, ''))
                        type_ = device_id = ''
                    elif label == 'User':
                        data_list.append(('', '', '', value))

    data_headers = ('Type', 'ID', 'Active', 'User')
    return data_headers, data_list, context.get_relative_path(source_path)
