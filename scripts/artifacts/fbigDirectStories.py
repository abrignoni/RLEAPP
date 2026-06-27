__artifacts_v2__ = {
    "fbigDirectStories": {
        "name": "Facebook Instagram Returns - Direct Stories",
        "description": "Direct stories (with linked media) parsed from a Facebook/Instagram law enforcement return (index.html / preservation).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-07-01",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "",
        "paths": ('*/index.html', '*/preservation*.html', '*/linked_media/direct_stories_*'),
        "output_types": "standard",
        "html_columns": ["Data"],
        "artifact_icon": "share-2",
    }
}

import os
from datetime import datetime, timezone

from bs4 import BeautifulSoup

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc, check_in_media


def _fbig_ts(value):
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
def fbigDirectStories(context):
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

        for section in soup.find_all('div', {'id': 'property-direct_stories'}):
            timestamp = thumb = media_name = ''
            agg_parts = []
            started = False
            for table in section.find_all('table'):
                th = table.find('th')
                if not th:
                    continue
                label = th.get_text()
                td = th.find_next_sibling('td')
                value = td.get_text() if td else ''
                if label in ('Direct Stories', 'Videos Definition'):
                    continue
                if label == 'Time':
                    timestamp = value
                elif label == 'Linked Media File:':
                    media_name = value.split('/')[1] if '/' in value else value
                    thumb = check_in_media(media_name, media_name)
                elif label == 'Media Id':
                    if started:
                        data_list.append((_fbig_ts(timestamp), thumb, '<br>'.join(agg_parts), media_name))
                        timestamp = thumb = media_name = ''
                        agg_parts = []
                    started = True
                    agg_parts.append(f'{label}: {value}')
                else:
                    agg_parts.append(f'{label}: {value}')
            if started:
                data_list.append((_fbig_ts(timestamp), thumb, '<br>'.join(agg_parts), media_name))

    data_headers = (('Timestamp', 'datetime'), ('Thumb', 'media'), 'Data', 'Filename')
    return data_headers, data_list, context.get_relative_path(source_path)
