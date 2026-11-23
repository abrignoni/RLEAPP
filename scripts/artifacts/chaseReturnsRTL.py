__artifacts_v2__ = {
    "chaseReturnsRTL": {
        "name": "Chase - Refresh Token Login",
        "description": "Text blocks in a PDF that start with 'Refresh Token Login' at the start of a "
                       "line or after a comma and print a date before the next comma. Written for "
                       "Chase Bank returns. The module does not check that a PDF is one.",
        "author": "@AlexisBrignoni, Shawn Ramsey, Codex",
        "creation_date": "2022-12-29",
        "last_update_date": "2026-11-23",
        "requirements": "pypdf",
        "category": "Chase Returns",
        "notes": "Timestamp starts two characters before the first slash in the block and ends at "
                 "the next comma. If the text before the date holds a slash, Timestamp and Username "
                 "are wrong. It is read from the PDF text with line breaks removed. It is not "
                 "converted, and the timeline key is this same text, which does not sort by time. "
                 "The time zone of the printed value is not established here. Username is the "
                 "module's name for the text between 'Refresh Token Login' and the Timestamp "
                 "start. Its meaning is not established. GEOLAT and GEOLON are shown as Latitude "
                 "and Longitude. A row with any text in both is written to KML as printed, "
                 "including text that is not a number. The KML point does not carry the timestamp. "
                 "The format of the printed coordinates is not established. A login block runs to "
                 "the next login header. It ends earlier only at an item that follows a comma, has "
                 "no ' - ' separator, and prints a date and a time. Other text in between, "
                 "including a different event type, is read as part of that login. A field value "
                 "is cut at its first ' - ' or ', '. A repeated field keeps its first value. With "
                 "several PDFs, the rows are combined. The located-at line on this artifact's "
                 "report page and the LAVA source path list the PDFs that produced rows. The "
                 "processed files log lists every PDF matched. A row does not name its own PDF.",
        "paths": ('*.pdf',),
        "output_types": ['html', 'tsv', 'timeline', 'lava', 'kml'],
        "artifact_icon": "login-2",
    },
    "chaseAccountInfo": {
        "name": "Chase - Account Information",
        "description": "Fields of each text span that starts at 'User Data' in a PDF. Written for "
                       "Chase Bank returns. The module does not check that a PDF is one, so any "
                       "PDF holding the phrase gives a row, which can be empty.",
        "author": "@AlexisBrignoni, Shawn Ramsey",
        "creation_date": "2022-12-29",
        "last_update_date": "2026-11-23",
        "requirements": "pypdf",
        "category": "Chase Returns",
        "notes": "Reports the text after each label (User ID, E-mail Address, Name, Address 1, "
                 "Address 2, City, State, Zip, Country Code, W. Phone, H. Phone) up to the next "
                 "expected label. H. Phone runs to the end of the block. A block runs from 'User "
                 "Data' to the next 'Combined Events', or to the end of the text if there is none. "
                 "A label that ends its line gives an empty field. E-mail Address ends at the word "
                 "'Customer'. If a label is missing, its own field is empty and the field before "
                 "it can hold more text "
                 "than its own value. Values come from the PDF text with line breaks removed and "
                 "outer spaces trimmed. With several PDFs, the rows are combined. The located-at "
                 "line on this artifact's report page and the LAVA source path list the PDFs that "
                 "produced rows. The processed files log lists every PDF matched. A row does not "
                 "name its own PDF. These rows carry no event time, so they are not written to "
                 "the timeline.",
        "paths": ('*.pdf',),
        "output_types": ['html', 'tsv', 'lava'],
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
# Its header and date can sit on different lines.
_RTL_OTHER_EVENT = re.compile(
    rf'{_RTL_ITEM_START}(?![^,]* - )[^,]+?{_RTL_DATE}\s+\d{{1,2}}:\d{{2}}', re.M)
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
    """End a login at the next login header or other event, read from text with its line breaks.

    Another event must follow a comma. Text after an unfinished field continues that field.
    """
    next_header = _RTL_EVENT_START.search(text, header_end)
    limit = next_header.start() if next_header else len(text)
    for event in _RTL_OTHER_EVENT.finditer(text, header_end, limit):
        if text[header_end:event.start()].rstrip().endswith(','):
            return event.start()
    return limit


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


def _pdf_files(context):
    """The matched PDFs in a fixed order, so rows do not depend on the walk order."""
    return sorted(path for path in map(str, context.get_files_found())
                  if path.lower().endswith('.pdf'))


@artifact_processor
def chaseReturnsRTL(context):
    data_list, row_sources = [], []
    pdf_files = _pdf_files(context)
    for file_found in pdf_files:
        rows_before = len(data_list)
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

        if len(data_list) > rows_before:
            row_sources.append(file_found)

    return _RTL_HEADERS, data_list, '\n'.join(row_sources or pdf_files)


@artifact_processor
def chaseAccountInfo(context):
    data_list, row_sources = [], []
    pdf_files = _pdf_files(context)
    for file_found in pdf_files:
        rows_before = len(data_list)
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

        if len(data_list) > rows_before:
            row_sources.append(file_found)

    data_headers = ('User ID', 'Email', 'Name', 'Address 1', 'Address 2', 'City', 'State', 'Zip',
                    'Country Code', ('W. Phone', 'phonenumber'), ('H. Phone', 'phonenumber'))
    return data_headers, data_list, '\n'.join(row_sources or pdf_files)
