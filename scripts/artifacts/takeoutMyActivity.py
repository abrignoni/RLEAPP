__artifacts_v2__ = {
    "takeoutMyActivity": {
        "name": "Google Takeout - My Activity",
        "description": "Parses and displays MyActivity.html files from Google Takeout for various "
                       "services (e.g., Ads, Chrome, YouTube).",
        "author": "@Jadoo4QFan",
        "creation_date": "2025-07-23",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Each service's MyActivity.html file is checked in as a media item so the "
                 "original HTML can be opened and reviewed manually from the report; the file "
                 "contents are not parsed into rows. The Service column is taken from the "
                 "folder name under 'My Activity' in the Takeout path.",
        "paths": ('*/My Activity/*/MyActivity.html',),
        "output_types": "standard",
        "artifact_icon": "activity",
    }
}

import os

from scripts.ilapfuncs import artifact_processor, check_in_media


def _service_name(file_found):
    # Extract service name from path: .../My Activity/Service Name/MyActivity.html
    path_parts = os.path.normpath(file_found).split(os.sep)
    try:
        my_activity_index = path_parts.index('My Activity')
        return path_parts[my_activity_index + 1]
    except (ValueError, IndexError):
        return 'Unknown'


@artifact_processor
def takeoutMyActivity(context):
    data_list = []
    source_path = ''
    seen = set()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'MyActivity.html':
            continue
        real_path = os.path.realpath(file_found)
        if real_path in seen:
            continue
        seen.add(real_path)
        source_path = file_found
        service_name = _service_name(file_found)
        media_ref = check_in_media(file_found, f'My Activity - {service_name}')
        data_list.append((service_name, media_ref, context.get_relative_path(file_found)))

    data_headers = ('Service', ('HTML File', 'media'), 'Source File')
    return data_headers, data_list, context.get_relative_path(source_path)
