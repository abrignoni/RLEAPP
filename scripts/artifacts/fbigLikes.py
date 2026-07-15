__artifacts_v2__ = {
    "fbigLikes": {
        "name": "Facebook Instagram Returns - Likes",
        "description": "Likes parsed from a Facebook/Instagram law enforcement return (records.html / preservation).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-07-01",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "thumb-up",
    }
}

import os
from datetime import datetime, timezone

from bs4 import BeautifulSoup

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


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


_FIELDS = {
    'Taken': 'taken', 'Status': 'status', 'Liked Post Author Vanity': 'vanity',
    'Like Timestamp': 'ltime', 'Url': 'url', 'Source': 'source', 'Filter': 'filter',
    'Is Published': 'ispub', 'Carousel Id': 'cid', 'Shared By Author': 'sba', 'Upload Ip': 'uip',
}


def _likes_row(r):
    return (_fbig_ts(r.get('taken', '')), r.get('id', ''), r.get('status', ''), r.get('vanity', ''),
            _fbig_ts(r.get('ltime', '')), r.get('url', ''), r.get('source', ''), r.get('filter', ''),
            r.get('ispub', ''), r.get('cid', ''), r.get('sba', ''), r.get('uip', ''))


@artifact_processor
def fbigLikes(context):
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

        for section in soup.find_all('div', {'id': 'property-likes'}):
            record = {}
            started = False
            for index, div in enumerate(section.find_all('div', class_='div_table inner')):
                if index <= 1:
                    continue
                parts = div.get_text(separator='|', strip=True).split('|')
                if len(parts) < 2:
                    continue
                label = parts[0]
                value = '|'.join(parts[1:])
                if label == 'Id':
                    if started:
                        data_list.append(_likes_row(record))
                    record = {'id': value}
                    started = True
                elif label in _FIELDS:
                    record[_FIELDS[label]] = value
            if started:
                data_list.append(_likes_row(record))

    data_headers = (('Timestamp', 'datetime'), 'ID', 'Status', 'Vanity',
                    ('Like Timestamp', 'datetime'), 'URL', 'Source', 'Filter', 'Is Published',
                    'Carousel Id', 'Shared By Author', 'Upload IP')
    return data_headers, data_list, context.get_relative_path(source_path)
