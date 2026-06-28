__artifacts_v2__ = {
    "fbigNcmec": {
        "name": "Facebook Instagram Returns - NCMEC Reports",
        "description": "NCMEC CyberTip reports parsed from a Facebook/Instagram law enforcement return (index.html / preservation).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-07-01",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "",
        "paths": ('*/index.html', '*/preservation*.html', '*/linked_media/ncmec_reports_*'),
        "output_types": "standard",
        "html_columns": ["Data"],
        "artifact_icon": "alert-triangle",
    }
}

import os
from datetime import datetime, timezone

from bs4 import BeautifulSoup

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc, check_in_media

_SKIP_LABELS = ('Ncmec Reports Definition', 'NCMEC Cybertips', 'Media uploaded in this cybertip')


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
def fbigNcmec(context):
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

        for section in soup.find_all('div', {'id': 'property-ncmec_reports'}):
            cybertip_id = time_val = resid = ''
            agg_parts = []
            media_refs = []
            started = False
            for table in section.find_all('table'):
                th = table.find('th')
                if not th:
                    continue
                label = th.get_text()
                if label in _SKIP_LABELS:
                    continue
                td = th.find_next_sibling('td')
                value = td.get_text() if td else ''
                if label == 'CyberTip ID':
                    if started:
                        data_list.append((_fbig_ts(time_val), cybertip_id, resid,
                                          '<br>'.join(agg_parts), media_refs))
                        cybertip_id = time_val = resid = ''
                        agg_parts = []
                        media_refs = []
                    started = True
                    cybertip_id = value
                elif label == 'Time':
                    time_val = value
                elif label == 'Responsible Id':
                    resid = value
                elif label == 'Linked Media File:':
                    media_name = value.split('/')[1] if '/' in value else value
                    ref = check_in_media(media_name, media_name)
                    if ref:
                        media_refs.append(ref)
                    agg_parts.append(f'Linked Media File: {value}')
                else:
                    agg_parts.append(f'{label} {value}')
            if started:
                data_list.append((_fbig_ts(time_val), cybertip_id, resid,
                                  '<br>'.join(agg_parts), media_refs))

    data_headers = (('Time', 'datetime'), 'CyberTip ID', 'Responsible ID', 'Data',
                    ('Media', 'media'))
    return data_headers, data_list, context.get_relative_path(source_path)
