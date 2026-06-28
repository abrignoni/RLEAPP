__artifacts_v2__ = {
    "googleDeviceconfig": {
        "name": "Google Returns - Android Device Config",
        "description": "Android Device Configuration Service profile page from a Google law "
                       "enforcement return (Android Device Configuration Service/Device-*.html).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-05-16",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Google Returns Android Device Config",
        "notes": "The return ships this as a pre-rendered HTML page; the full document is embedded "
                 "verbatim in the Device Configuration column (rendered, not escaped).",
        "paths": ('*/*AndroidDeviceConfigurationService.DeviceAndUserProfile_*/'
                  'Android Device Configuration Service/Device-*.html',),
        "output_types": "standard",
        "html_columns": ["Device Configuration"],
        "artifact_icon": "settings",
    }
}

import os

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def googleDeviceconfig(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.html') or os.path.basename(file_found).startswith('.'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            data_list.append((f.read(), context.get_relative_path(file_found)))

    data_headers = ('Device Configuration', 'Source File')
    return data_headers, data_list, context.get_relative_path(source_path)
