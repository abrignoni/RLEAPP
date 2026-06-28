__artifacts_v2__ = {
    "documentsFolder": {
        "name": "iCloud Documents Folders",
        "description": "Files in iCloud backup Documents folders, with detected type and a media "
                       "preview.",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-02-15",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "iCloud Documents Folders",
        "notes": "Modified Date is the file's on-disk modification time (UTC).",
        "paths": ('*/backup/*/Documents/**',),
        "output_types": "standard",
        "artifact_icon": "folder",
    }
}

import os
from datetime import datetime, timezone

from scripts.filetype import guess_mime, guess_extension
from scripts.ilapfuncs import artifact_processor, check_in_media


@artifact_processor
def documentsFolder(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.isfile(file_found):
            continue
        filename = os.path.basename(file_found)
        if filename.startswith('.'):
            continue
        source_path = file_found
        modified = datetime.fromtimestamp(os.path.getmtime(file_found), tz=timezone.utc)
        media = check_in_media(file_found, filename)
        data_list.append((modified, filename, media, guess_extension(file_found),
                          guess_mime(file_found), context.get_relative_path(file_found)))

    data_headers = (('Modified Date', 'datetime'), 'Filename', ('Media', 'media'), 'EXT', 'MIME',
                    'Path')
    return data_headers, data_list, context.get_relative_path(source_path)
