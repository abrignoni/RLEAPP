__artifacts_v2__ = {
    "googleMyactisearch": {
        "name": "Google Returns - My Activity Image Search",
        "description": "My Activity > Image Search page from a Google law enforcement return "
                       "(My Activity/Image Search/MyActivity.html).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-05-16",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Google Returns My Activity Image Search",
        "notes": "The return ships this as a pre-rendered HTML page; the full document is embedded "
                 "verbatim in the Image Search Activity column (rendered, not escaped).",
        "paths": ('*/*MyActivity.MyActivity_*/My Activity/Image Search/MyActivity.html',),
        "output_types": "standard",
        "html_columns": ["Image Search Activity"],
        "artifact_icon": "photo",
    }
}

import os

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def googleMyactisearch(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.html') or os.path.basename(file_found).startswith('.'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            data_list.append((f.read(), context.get_relative_path(file_found)))

    data_headers = ('Image Search Activity', 'Source File')
    return data_headers, data_list, context.get_relative_path(source_path)
