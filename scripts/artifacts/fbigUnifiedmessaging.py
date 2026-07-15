__artifacts_v2__ = {
    "fbigUnifiedMessages": {
        "name": "Facebook Instagram Returns - Unified Messaging",
        "description": "Unified messaging (messages) parsed from a Facebook/Instagram law enforcement return (records.html / preservation).",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-31",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "",
        "paths": ('*/records.html', '*/preservation*.html', '*/linked_media/*.*'),
        "output_types": "standard",
        "artifact_icon": "message",
    },
    "fbigThreadParticipants": {
        "name": "Facebook Instagram Returns - Thread Participants",
        "description": "Messaging thread participants parsed from a Facebook/Instagram law enforcement return (records.html / preservation).",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-31",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "users",
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


def _msg_row(f, media_names, thread_id):
    refs = [r for r in (check_in_media(m, m) for m in sorted(media_names)) if r]
    return (_fbig_ts(f.get('sent', '')), f.get('author', ''), f.get('body', ''), refs,
            f.get('attach', ''), f.get('typef', ''), f.get('sizef', ''), f.get('url', ''),
            f.get('pt', ''), f.get('dcf', ''), f.get('textf', ''), f.get('urlb', ''),
            f.get('subsevent', ''), thread_id)


@artifact_processor
def fbigUnifiedMessages(context):
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

        fields = {}
        media_names = set()
        thread_id = ''
        started = False
        for div in soup.find_all('div', class_='div_table inner'):
            parts = div.get_text(separator='|', strip=True).split('|')
            label = parts[0] if parts else ''
            value = '|'.join(parts[1:]) if len(parts) > 1 else ''
            if label == 'Thread':
                thread_id = value
            elif label == 'Author':
                if started:
                    data_list.append(_msg_row(fields, media_names, thread_id))
                    fields = {}
                    media_names = set()
                started = True
                fields['author'] = value
            elif label == 'Sent':
                fields['sent'] = value
            elif label == 'Body':
                fields['body'] = value
            elif label == 'Attachments':
                fields['attach'] = value
            elif label == 'Type':
                fields['typef'] = value
            elif label == 'Size':
                fields['sizef'] = value
            elif label == 'URL':
                fields['url'] = value
            elif label == 'Product Type':
                fields['pt'] = value
            elif label == 'Date Created':
                fields['dcf'] = value
            elif label == 'Text':
                fields['textf'] = value
            elif label == 'Linked Media File:':
                if value:
                    media_names.add(value)
            elif label == 'Url':
                fields['urlb'] = value
            elif label == 'Subscription Event':
                fields['subsevent'] = value
        if started:
            data_list.append(_msg_row(fields, media_names, thread_id))

    data_headers = (('Timestamp', 'datetime'), 'Author', 'Body', ('Media', 'media'), 'Attachments',
                    'Type', 'Size', 'URL', 'Product Type', 'Date Created Share', 'Text', 'Link URL',
                    'Subscription Event', 'Thread ID')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def fbigThreadParticipants(context):
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

        thread_id = currpar = pastpar = ''
        started = False
        for div in soup.find_all('div', class_='div_table inner'):
            parts = div.get_text(separator='|', strip=True).split('|')
            label = parts[0] if parts else ''
            if label == 'Thread':
                if started:
                    data_list.append((thread_id, currpar, pastpar))
                    currpar = pastpar = ''
                started = True
                thread_id = '|'.join(parts[1:]) if len(parts) > 1 else ''
            elif label == 'Current Participants':
                currpar = ', '.join(parts[1:])
            elif label == 'Past Participants':
                pastpar = ', '.join(parts[1:])
        if started:
            data_list.append((thread_id, currpar, pastpar))

    data_headers = ('Thread ID', 'Current Participants', 'Past Participants')
    return data_headers, data_list, context.get_relative_path(source_path)
