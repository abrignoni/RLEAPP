__artifacts_v2__ = {
    "fbigPhotos": {
        "name": "Facebook Instagram Returns - Photos",
        "description": "Photos (with linked media) parsed from a Facebook/Instagram law enforcement return (records.html / preservation).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-07-01",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "",
        "paths": ('*/records.html', '*/preservation*.html', '*/linked_media/*.*'),
        "output_types": "standard",
        "html_columns": ["Caption", "Comments", "Location"],
        "artifact_icon": "image",
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


def _row(fields):
    return (_fbig_ts(fields.get('taken', '')), fields.get('thumb'), fields.get('lmf', ''),
            fields.get('url', ''), fields.get('source', ''), fields.get('filter', ''),
            fields.get('pub', ''), fields.get('sba', ''), fields.get('carid', ''),
            fields.get('caption', ''), fields.get('comments', ''), fields.get('location', ''))


@artifact_processor
def fbigPhotos(context):
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

        for section in soup.find_all('div', {'id': 'property-photos'}):
            fields = {}
            started = False
            for index, div in enumerate(section.find_all('div', class_='div_table outer')):
                if index <= 1:
                    continue
                inner_div = div.find('div', class_='div_table inner')
                label = inner_div.text if inner_div else ''
                if 'Image' in label:
                    if started:
                        data_list.append(_row(fields))
                    fields = {}
                    started = True
                    continue
                if not started:
                    continue
                most_inner = div.find('div', class_='most_inner')
                value = most_inner.get_text() if most_inner else div.get_text(' ', strip=True)
                if 'Linked Media File' in label:
                    fields['lmf'] = value
                    fields['thumb'] = check_in_media(value, value)
                elif 'Url' in label:
                    fields['url'] = value
                elif 'Source' in label:
                    fields['source'] = value
                elif 'Filter' in label:
                    fields['filter'] = value
                elif 'Is Published' in label:
                    fields['pub'] = value
                elif 'Shared By Author' in label:
                    fields['sba'] = value
                elif 'Carousel Id' in label:
                    fields['carid'] = value
                elif 'Caption' in label:
                    fields['caption'] = value
                elif 'Comments' in label:
                    fields['comments'] = value
                elif 'Taken' in label:
                    fields['taken'] = value
                elif 'Location' in label:
                    fields['location'] = value
            if started:
                data_list.append(_row(fields))

    data_headers = (('Timestamp', 'datetime'), ('Thumb', 'media'), 'Linked Media File', 'URL',
                    'Source', 'Filter', 'Is Published', 'Shared by Author', 'Carousel Id',
                    'Caption', 'Comments', 'Location')
    return data_headers, data_list, context.get_relative_path(source_path)
