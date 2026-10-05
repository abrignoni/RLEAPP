__artifacts_v2__ = {
    "documentsFolder": {
        "name": "iCloud Documents Folders",
        "description": "Files in iCloud backup Documents folders, with detected type and a media "
                       "preview.",
        "author": "@AlexisBrignoni, Codex",
        "creation_date": "2023-02-15",
        "last_update_date": "2026-10-04",
        "requirements": "none",
        "category": "iCloud Documents Folders",
        "notes": "Staged File mtime is the modification-time value of the extracted copy, in "
                 "Unix seconds. It does not establish a source event time. For ZIP inputs the "
                 "staging process interprets the zone-less member time in the examiner's local "
                 "zone, so this value can depend on the machine running the tool.",
        "paths": ('*/backup/*/Documents/**',),
        "output_types": "standard",
        "artifact_icon": "folder",
    }
}

import os

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
        modified = str(os.path.getmtime(file_found))
        media = check_in_media(file_found, filename)
        data_list.append((modified, filename, media, guess_extension(file_found),
                          guess_mime(file_found), context.get_relative_path(file_found)))

    data_headers = ('Staged File mtime (Unix seconds)', 'Filename', ('Media', 'media'), 'EXT', 'MIME',
                    'Path')
    return data_headers, data_list, context.get_relative_path(source_path)
