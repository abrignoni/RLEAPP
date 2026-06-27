__artifacts_v2__ = {
    "takeoutSavedLinksDefault": {
        "name": "Saved Links - Default List",
        "description": "Collections of saved links (images, places, web pages, etc.) from Google Search and Maps.",
        "author": "@KevinPagano3",
        "creation_date": "2021-09-25",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Saved/Default list.csv',),
        "output_types": "standard",
        "artifact_icon": "link",
    },
    "takeoutSavedLinksFavImages": {
        "name": "Saved Links - Favorite Images",
        "description": "Collections of saved links (images, places, web pages, etc.) from Google Search and Maps.",
        "author": "@KevinPagano3",
        "creation_date": "2021-09-25",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Saved/Favorite images.csv',),
        "output_types": "standard",
        "artifact_icon": "link",
    },
    "takeoutSavedLinksFavPages": {
        "name": "Saved Links - Favorite Pages",
        "description": "Collections of saved links (images, places, web pages, etc.) from Google Search and Maps.",
        "author": "@KevinPagano3",
        "creation_date": "2021-09-25",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Saved/Favorite pages.csv',),
        "output_types": "standard",
        "artifact_icon": "link",
    },
    "takeoutSavedLinksWantToGo": {
        "name": "Saved Links - Want To Go",
        "description": "Collections of saved links (images, places, web pages, etc.) from Google Search and Maps.",
        "author": "@KevinPagano3",
        "creation_date": "2021-09-25",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Saved/Want to go.csv',),
        "output_types": "standard",
        "artifact_icon": "link",
    }
}

import csv
import os

from scripts.ilapfuncs import artifact_processor


def _parse_saved_links(context, basename_match):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith(basename_match):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for item in reader:
                if len(item) < 4:
                    continue
                data_list.append((item[0], item[1], item[2], item[3]))

    data_headers = ('Title', 'Note', 'URL', 'Comment')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def takeoutSavedLinksDefault(context):
    return _parse_saved_links(context, 'Default list.csv')


@artifact_processor
def takeoutSavedLinksFavImages(context):
    return _parse_saved_links(context, 'Favorite images.csv')


@artifact_processor
def takeoutSavedLinksFavPages(context):
    return _parse_saved_links(context, 'Favorite pages.csv')


@artifact_processor
def takeoutSavedLinksWantToGo(context):
    return _parse_saved_links(context, 'Want to go.csv')
