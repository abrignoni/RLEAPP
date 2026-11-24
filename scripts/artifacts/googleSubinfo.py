__artifacts_v2__ = {
    "googleSubinfo": {
        "name": "Google Returns - Subscriber Info",
        "description": "Google Account subscriber info page from a Google law enforcement return "
                       "(Google Account/*.SubscriberInfo.html).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-05-16",
        "last_update_date": "2026-11-22",
        "requirements": "none",
        "category": "Google",
        "notes": "The return ships this as a pre-rendered HTML page. The text of the full document is "
                 "stored in the Subscriber Info column, decoded as UTF-8. A byte that is not valid "
                 "UTF-8 is written as a backslash escape, and CR LF line ends are stored as LF. The "
                 "HTML report shows it as source text with the markup escaped and does not render it. "
                 "LAVA and the TSV export hold the same text without HTML escaping.",
        "paths": ('*/*GoogleAccount.SubscriberInfo_*/Google Account/*.SubscriberInfo.html',),
        "output_types": "standard",
        "multiline_columns": ["Subscriber Info"],
        "artifact_icon": "user",
    }
}

import os

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def googleSubinfo(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.html') or os.path.basename(file_found).startswith('.'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            data_list.append((f.read(), context.get_relative_path(file_found)))

    data_headers = ('Subscriber Info', 'Source File')
    return data_headers, data_list, context.get_relative_path(source_path)
