__artifacts_v2__ = {
    "chromeSearchEngines": {
        "name": "Chrome Search Engines",
        "description": "Parses Google Chrome Search Engines from Takeout",
        "author": "@upintheairsheep & @KevinPagano3",
        "creation_date": "2023-08-17",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Chrome/SearchEngines.json'),
        "output_types": "standard",
        "artifact_icon": "search",
    }
}

import json

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def chromeSearchEngines(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        for site in data.get('Search Engines', []):
            date_created = site.get('date_created', '')
            date_created = convert_unix_ts_to_utc(date_created) if date_created else ''
            last_modified = site.get('last_modified', '')
            last_modified = convert_unix_ts_to_utc(last_modified) if last_modified else ''
            data_list.append((
                date_created, last_modified, site.get('short_name', ''), site.get('keyword', ''),
                site.get('url', ''), site.get('originating_url', ''), site.get('sync_guid', ''),
                site.get('favicon_url', ''), site.get('suggestions_url', ''), site.get('new_tab_url', ''),
                site.get('input_encodings', ''), site.get('safe_for_autoreplace', ''),
                site.get('prepopulate_id', ''), site.get('image_url_post_params', ''),
                site.get('is_active', ''), site.get('image_url', ''), site.get('starter_pack_id', '')))

    data_headers = (('Date Created', 'datetime'), ('Date Last Modified', 'datetime'),
                    '(Short) Name', 'Keyword', 'URL Syntax', 'API URL', 'Sync GUID', 'Favicon URL',
                    'Suggestions URL', 'New Tab URL', 'Input Encodings', 'Safe Autoreplace?',
                    'Pre-populate ID', 'Image URL Post Parameters', 'Is Active?', 'Image URL',
                    'Starter Pack ID')
    return data_headers, data_list, context.get_relative_path(source_path)
