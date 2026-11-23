__artifacts_v2__ = {
    "chaseReturnsRTL": {
        "name": "Chase - Refresh Token Login",
        "description": "Text blocks that start with 'Refresh Token Login' in a PDF. Written for Chase "
                       "Bank returns. The module does not check that a PDF is one.",
        "author": "@AlexisBrignoni, Shawn Ramsey, Codex",
        "creation_date": "2022-12-29",
        "last_update_date": "2026-11-23",
        "requirements": "pypdf",
        "category": "Chase Returns",
        "notes": "Timestamp is the text from the first date to the next comma, taken from the PDF "
                 "text with line breaks removed. It is not converted. The time zone of the printed "
                 "value is not established here. Username is the text printed between 'Refresh "
                 "Token Login' and the date. Its meaning is not established. GEOLAT and GEOLON are "
                 "shown as Latitude and Longitude so rows that have both are written to KML. The "
                 "KML point does not carry the timestamp. The format of the printed coordinates is "
                 "not established.",
        "paths": ('*.pdf',),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
        "artifact_icon": "login-2",
    },
    "chaseAccountInfo": {
        "name": "Chase - Account Information",
        "description": "Fields of the User Data block in a PDF. Written for Chase Bank returns.",
        "author": "@AlexisBrignoni, Shawn Ramsey",
        "creation_date": "2022-12-29",
        "last_update_date": "2026-11-23",
        "requirements": "pypdf",
        "category": "Chase Returns",
        "notes": "Reports the text after each label (User ID, E-mail Address, Name, Address 1, "
                 "Address 2, City, State, Zip, Country Code, W. Phone, H. Phone) up to the next "
                 "expected label, from 'User Data' to the next 'Combined Events'. E-mail Address "
                 "ends at the word 'Customer'. If a label is missing, a field can hold more text "
                 "than its own value. Values come from the PDF text with line breaks removed and "
                 "outer spaces trimmed.",
        "paths": ('*.pdf',),
        "output_types": "standard",
        "artifact_icon": "user",
    },
}

import re

from pypdf import PdfReader

from scripts.ilapfuncs import artifact_processor

_RTL_KEYS = ['TIMESTAMP', 'USERNAME', 'APPLICATIONID', 'COMMENTS', 'DEVAPPINSTALL', 'DEVAPPVER',
             'DEVID', 'DEVLOCALE', 'DEVOSVER', 'DEV_MDL_VER', 'DVC_ID', 'DVC_MAK', 'DVC_MDL',
             'DVC_NAME', 'DVC_OS', 'ENC_DVC_ID', 'ERR_CD', 'ERR_DESC', 'GEOLAT', 'GEOLON', 'GEOTS',
             'INPT_DID', 'LANGUAGE', 'MLWR_SC', 'RT_SC', 'STS', 'TKN_TP', 'USR_AGNT_DVC_NM',
             'SERVERID', 'CHANNELID', 'SLOTCODE', 'DEVICE_TRUST_LEVEL', 'FAILED_DVC_TRUST_RULE']
_RTL_FIELD_KEYS = set(_RTL_KEYS[2:])
_RTL_DATE = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
_RTL_ITEM_START = r'(?:^[ \t]*|(?<=, ))'
# A login header starts a line or a comma-separated item and reaches its date before any comma.
_RTL_EVENT_START = re.compile(rf'{_RTL_ITEM_START}(Refresh Token Login [^,]*?{_RTL_DATE})', re.M)
# Any other event starts the same way, is not a KEY - value item, and prints a date and time.
_RTL_OTHER_EVENT = re.compile(
    rf"{_RTL_ITEM_START}(?!(?:{'|'.join(sorted(_RTL_FIELD_KEYS))}) - )"
    rf'[^,\n]+?{_RTL_DATE}[ \t]+\d{{1,2}}:\d{{2}}', re.M)
_RTL_HEADERS = (('Timestamp (as printed)', 'Username', 'APPLICATIONID', 'COMMENTS', 'DEVAPPINSTALL',
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


def _rtl_record_end(text, header_end):
    """End a login at the next login header or other event, read from text with its line breaks."""
    next_header = _RTL_EVENT_START.search(text, header_end)
    limit = next_header.start() if next_header else len(text)
    other_event = _RTL_OTHER_EVENT.search(text, header_end, limit)
    return other_event.start() if other_event else limit


def _between(text, start, end):
    start_idx = text.find(start)
    if start_idx == -1:
        return ''
    start_idx += len(start)
    end_idx = text.find(end, start_idx)
    return (text[start_idx:end_idx] if end_idx != -1 else text[start_idx:]).strip()


def _ts(value):
    """The return's printed time has no established zone; retain its text."""
    return (value or '').strip()


def _pdf_text(file_found, keep_lines=False):
    with open(file_found, 'rb') as fp:
        reader = PdfReader(fp)
        pages = [page.extract_text() for page in reader.pages]
    return '\n'.join(pages) if keep_lines else ''.join(pages).replace('\n', '')


@artifact_processor
def chaseReturnsRTL(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.pdf'):
            continue
        source_path = file_found
        text = _pdf_text(file_found, keep_lines=True)

        index = 0
        while True:
            header = _RTL_EVENT_START.search(text, index)
            if header is None:
                break
            start_point = header.start(1)
            end_point = _rtl_record_end(text, header.end())
            index = end_point
            subtext = text[start_point:end_point].replace('\n', '')

            first_slash = find_nth(subtext, '/', 1)
            if first_slash < 2:
                continue
            ts_start = first_slash - 2
            ts_end = find_nth(subtext, ',', 1, ts_start)
            timestamp = subtext[ts_start:ts_end] if ts_end != -1 else subtext[ts_start:]
            username = subtext[subtext.find('Refresh Token Login ') + 20:first_slash - 2].strip()

            row = {key: '' for key in _RTL_KEYS}
            row['TIMESTAMP'] = timestamp
            row['USERNAME'] = username
            for item in subtext.split(', '):
                line_item = item.split(' - ')
                if len(line_item) > 1 and line_item[0] in _RTL_FIELD_KEYS and not row[line_item[0]]:
                    row[line_item[0]] = line_item[1].strip()

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
                    'Country Code', ('W. Phone', 'phonenumber'), ('H. Phone', 'phonenumber'))
    return data_headers, data_list, context.get_relative_path(source_path)
