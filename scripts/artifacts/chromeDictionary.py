__artifacts_v2__ = {
    "chromeDictionary": {
        "name": "Google Chrome User Dictionary",
        "description": "Words added by the user to the Google Chrome custom spelling "
                       "dictionary, parsed from a Google Takeout archive "
                       "(Chrome/Dictionary.csv). The Entry Order column preserves the "
                       "order in which the words appear in the file.",
        "author": "@upintheairsheep2",
        "creation_date": "2023-08-02",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Chrome/Dictionary.csv',),
        "output_types": "standard",
        "artifact_icon": "book",
    }
}

import os

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def chromeDictionary(context):
    data_list = []
    source_path = ''
    parsed = set()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'Dictionary.csv':
            continue
        real_path = os.path.realpath(file_found)
        if real_path in parsed:
            continue
        parsed.add(real_path)
        source_path = file_found
        counter = 1
        with open(file_found, 'r', encoding='utf-8-sig') as csvfile:
            for row in csvfile:
                data_list.append((counter, row.rstrip('\r\n')))
                counter += 1

    data_headers = ('Entry Order', 'Word')
    return data_headers, data_list, context.get_relative_path(source_path)
