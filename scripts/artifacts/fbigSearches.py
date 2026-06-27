__artifacts_v2__ = {
    "fbigSearches": {
        "name": "Facebook Instagram Returns - Searches",
        "description": "Searches parsed from a Facebook/Instagram law enforcement return (records.html / preservation).",
        "author": "@AlexisBrignoni",
        "creation_date": "2024-08-07",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "search",
    }
}

import os
from datetime import datetime, timezone

from bs4 import BeautifulSoup

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


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
        dt = dt.replace(tzinfo=timezone.utc)   # ' UTC'/naive -> the return is UTC, don't shift to local
    return dt.astimezone(timezone.utc)


@artifact_processor
def fbigSearches(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        basename = os.path.basename(file_found)
        if not (basename.startswith('records.html') or basename.startswith('preservation')):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as fp:
            soup = BeautifulSoup(fp, 'lxml')
        sections = soup.find_all('div', {'id': 'property-searches'})
        if not sections:
            continue
        chunk = []
        for index, div in enumerate(sections[0].find_all('div', class_='div_table inner')):
            if index <= 1:
                continue
            inner = div.find('div', class_='most_inner')
            chunk.append(inner.get_text() if inner else '')
            if len(chunk) == 3:
                data_list.append((_fbig_ts(chunk[2]), chunk[0], chunk[1]))
                chunk = []

    data_headers = (('Timestamp', 'datetime'), 'Selected', 'Type')
    return data_headers, data_list, context.get_relative_path(source_path)
