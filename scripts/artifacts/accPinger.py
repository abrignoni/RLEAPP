__artifacts_v2__ = {
    "accPinger": {
        "name": "Pinger - Account",
        "description": "User account data from a Pinger law enforcement return (docx).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-07-17",
        "last_update_date": "2026-11-22",
        "requirements": "mammoth",
        "category": "Pinger",
        "notes": "User Data is the document converted to HTML by the mammoth library. The tags and "
                 "entities in the stored value are the converter's. The HTML report shows that markup "
                 "as escaped text and does not render it.",
        "paths": ('*/*.docx',),
        "output_types": "standard",
        "multiline_columns": ["User Data"],
        "artifact_icon": "user",
    }
}

import os

import mammoth

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def accPinger(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        basename = os.path.basename(file_found)
        if basename.startswith('~') or basename.startswith('.'):
            continue
        source_path = file_found
        with open(file_found, 'rb') as docx_file:
            result = mammoth.convert_to_html(docx_file)
        data_list.append((result.value,))

    data_headers = ('User Data',)
    return data_headers, data_list, context.get_relative_path(source_path)
