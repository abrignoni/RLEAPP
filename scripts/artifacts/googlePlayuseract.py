__artifacts_v2__ = {
    "googlePlayuseract": {
        "name": "Google Returns - Play Store User Activity",
        "description": "Google Play Store user activity page from a Google law enforcement return "
                       "(Google Play Store/User Activity.html).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-05-16",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Google Returns Play User Act",
        "notes": "The return ships this activity as a pre-rendered HTML page; the full document is "
                 "embedded verbatim in the User Activity column (rendered, not escaped).",
        "paths": ('*/*GooglePlayStore.UserActivity_*/Google Play Store/User Activity.html',),
        "output_types": "standard",
        "html_columns": ["User Activity"],
        "artifact_icon": "activity",
    }
}

import os

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def googlePlayuseract(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.html') or os.path.basename(file_found).startswith('.'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            data_list.append((f.read(), context.get_relative_path(file_found)))

    data_headers = ('User Activity', 'Source File')
    return data_headers, data_list, context.get_relative_path(source_path)
