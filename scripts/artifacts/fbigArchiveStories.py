__artifacts_v2__ = {
    "fbigArchiveStories": {
        "name": "Facebook Instagram Returns - Archived Stories",
        "description": "Archived stories with linked media parsed from a Facebook/Instagram law enforcement return (index.html / preservation).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "",
        "paths": ('*/index.html', '*/preservation*.html', '*/linked_media/archived_stories_*'),
        "output_types": "standard",
        "artifact_icon": "book-open",
    }
}

import os
from datetime import datetime, timezone

from bs4 import BeautifulSoup

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc, check_in_media


def _fbig_ts(value):
    # Return timestamps vary by export; convert epoch / ISO (incl. ' UTC') to aware UTC, else keep raw.
    value = (value or '').strip()
    if not value:
        return value
    cleaned = value.replace(' UTC', '').strip()
    if cleaned.isdigit():
        return convert_unix_ts_to_utc(int(cleaned))
    try:
        dt = datetime.fromisoformat(cleaned.replace('Z', '+00:00'))
    except ValueError:
        return value
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


@artifact_processor
def fbigArchiveStories(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        basename = os.path.basename(file_found)
        if not (basename.startswith('index.html') or basename.startswith('preservation')):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        story_id = ''
        timestamp = ''
        for section in soup.find_all('div', {'id': 'property-archived_stories'}):
            for table in section.find_all('table'):
                th = table.find('th')
                if not th:
                    continue
                label = th.get_text()
                td = th.find_next_sibling('td')
                value = td.get_text() if td else ''
                if label == 'Story Id':
                    story_id = value
                elif label == 'Timestamp':
                    timestamp = value
                elif label == 'Linked Media File:':
                    media_name = value.split('/')[1] if '/' in value else value
                    data_list.append((_fbig_ts(timestamp), story_id, value,
                                      check_in_media(media_name, media_name)))

    data_headers = (('Timestamp', 'datetime'), 'Story ID', 'Filename', ('Thumb', 'media'))
    return data_headers, data_list, context.get_relative_path(source_path)
