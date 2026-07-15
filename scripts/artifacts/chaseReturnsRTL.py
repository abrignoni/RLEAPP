__artifacts_v2__ = {
    "chaseReturnsRTL": {
        "name": "Chase - Refresh Token Login",
        "description": "Refresh Token Login events from a Chase Bank PDF return.",
        "author": "@AlexisBrignoni, Shawn Ramsey",
        "creation_date": "2022-12-29",
        "last_update_date": "2026-06-28",
        "requirements": "pypdf",
        "category": "Chase Returns",
        "notes": "Timestamp normalized to UTC. GEOLAT/GEOLON are exposed as Latitude/Longitude so "
                 "the rows map (KML).",
        "paths": ('*.pdf',),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
        "artifact_icon": "login-2",
    },
    "chaseAccountInfo": {
        "name": "Chase - Account Information",
        "description": "Account holder identity (User Data block) from a Chase Bank PDF return.",
        "author": "@AlexisBrignoni, Shawn Ramsey",
        "creation_date": "2022-12-29",
        "last_update_date": "2026-06-28",
        "requirements": "pypdf",
        "category": "Chase Returns",
        "notes": "Surfaces the User Data demographics (name/email/address/phones) the original "
                 "module parsed into an AccountInfo object but never reported.",
        "paths": ('*.pdf',),
        "output_types": "standard",
        "artifact_icon": "user",
    },
}

from datetime import datetime, timezone

from pypdf import PdfReader

from scripts.ilapfuncs import artifact_processor

_RTL_KEYS = ['TIMESTAMP', 'USERNAME', 'APPLICATIONID', 'COMMENTS', 'DEVAPPINSTALL', 'DEVAPPVER',
             'DEVID', 'DEVLOCALE', 'DEVOSVER', 'DEV_MDL_VER', 'DVC_ID', 'DVC_MAK', 'DVC_MDL',
             'DVC_NAME', 'DVC_OS', 'ENC_DVC_ID', 'ERR_CD', 'ERR_DESC', 'GEOLAT', 'GEOLON', 'GEOTS',
             'INPT_DID', 'LANGUAGE', 'MLWR_SC', 'RT_SC', 'STS', 'TKN_TP', 'USR_AGNT_DVC_NM',
             'SERVERID', 'CHANNELID', 'SLOTCODE', 'DEVICE_TRUST_LEVEL', 'FAILED_DVC_TRUST_RULE']
_RTL_FIELD_KEYS = set(_RTL_KEYS[2:])
_RTL_HEADERS = ((('Timestamp', 'datetime'), 'Username', 'APPLICATIONID', 'COMMENTS', 'DEVAPPINSTALL',
                 'DEVAPPVER', 'DEVID', 'DEVLOCALE', 'DEVOSVER', 'DEV_MDL_VER', 'DVC_ID', 'DVC_MAK',
                 'DVC_MDL', 'DVC_NAME', 'DVC_OS', 'ENC_DVC_ID', 'ERR_CD', 'ERR_DESC', 'Latitude',
                 'Longitude', 'GEOTS', 'INPT_DID', 'LANGUAGE', 'MLWR_SC', 'RT_SC', 'STS', 'TKN_TP',
                 'USR_AGNT_DVC_NM', 'SERVERID', 'CHANNELID', 'SLOTCODE', 'DEVICE_TRUST_LEVEL',
                 'FAILED_DVC_TRUST_RULE'))


def find_nth(haystack, needle, n, start=0):
    start = haystack.find(needle, start)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start


def _between(text, start, end):
    start_idx = text.find(start)
    if start_idx == -1:
        return ''
    start_idx += len(start)
    end_idx = text.find(end, start_idx)
    return (text[start_idx:end_idx] if end_idx != -1 else text[start_idx:]).strip()


def _ts(value):
    text = (value or '').strip()
    if not text:
        return ''
    for fmt in ('%m/%d/%Y %H:%M:%S', '%m/%d/%Y %I:%M:%S %p', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    try:
        dt = datetime.fromisoformat(text.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        return value


def _pdf_text(file_found):
    with open(file_found, 'rb') as fp:
        reader = PdfReader(fp)
        return ''.join(page.extract_text() for page in reader.pages).replace('\n', '')


@artifact_processor
def chaseReturnsRTL(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.pdf'):
            continue
        source_path = file_found
        text = _pdf_text(file_found)

        index = 0
        while True:
            index = text.find('Refresh Token Login', index)
            if index == -1:
                break
            start_point = index
            end_point = find_nth(text, '/', 3, index) - 2
            if end_point <= start_point:
                end_point = len(text)
            index = end_point
            subtext = text[start_point:end_point]

            first_slash = find_nth(subtext, '/', 1)
            if first_slash < 2:
                continue
            ts_start = first_slash - 2
            ts_end = find_nth(subtext, ',', 1, ts_start)
            timestamp = subtext[ts_start:ts_end] if ts_end != -1 else subtext[ts_start:]
            username = subtext[subtext.find('Refresh Token Login ') + 20:first_slash - 2]

            row = {key: '' for key in _RTL_KEYS}
            row['TIMESTAMP'] = timestamp
            row['USERNAME'] = username
            for item in subtext.split(', '):
                line_item = item.split(' - ')
                if len(line_item) > 1 and line_item[0] in _RTL_FIELD_KEYS:
                    row[line_item[0]] = line_item[1]

            block = [row[key] for key in _RTL_KEYS]
            block[0] = _ts(block[0])
            data_list.append(block)

    return _RTL_HEADERS, data_list, context.get_relative_path(source_path)


@artifact_processor
def chaseAccountInfo(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.pdf'):
            continue
        source_path = file_found
        text = _pdf_text(file_found)

        index = 0
        while True:
            user_index = text.find('User Data', index)
            if user_index == -1:
                break
            end_point = text.find('Combined Events', user_index)
            if end_point == -1:
                end_point = len(text)
            subtext = text[user_index:end_point]
            index = end_point

            data_list.append((
                _between(subtext, 'User ID: ', 'E-mail'),
                _between(subtext, 'E-mail Address: ', 'Customer'),
                _between(subtext, 'Name: ', 'Address 1'),
                _between(subtext, 'Address 1: ', 'Address 2'),
                _between(subtext, 'Address 2: ', 'City:'),
                _between(subtext, 'City: ', 'State:'),
                _between(subtext, 'State: ', 'Zip:'),
                _between(subtext, 'Zip: ', 'Country Code:'),
                _between(subtext, 'Country Code: ', 'W. Phone:'),
                _between(subtext, 'W. Phone: ', 'H. Phone:'),
                _between(subtext, 'H. Phone: ', 'Combined Events'),
            ))

    data_headers = ('User ID', 'Email', 'Name', 'Address 1', 'Address 2', 'City', 'State', 'Zip',
                    'Country Code', ('Work Phone', 'phonenumber'), ('Home Phone', 'phonenumber'))
    return data_headers, data_list, context.get_relative_path(source_path)
