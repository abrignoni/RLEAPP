__artifacts_v2__ = {
    "chromeBookmarks": {
        "name": "Chrome Bookmarks",
        "description": "Parses Google Chrome bookmarks from Takeout",
        "author": "@KevinPagano3",
        "creation_date": "2023-08-21",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Chrome/Bookmarks.html'),
        "output_types": "standard",
        "artifact_icon": "bookmark",
    }
}

import bs4

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


def _bookmark_add_date(value):
    # add_date: 13-digit value = ms epoch; otherwise Chrome/WebKit microseconds since 1601
    if not value or value == '0':
        return ''
    if len(value) == 13:
        return convert_unix_ts_to_utc(int(value))
    return convert_unix_ts_to_utc((int(value) / 1000000) - 11644473600)


def _bookmark_ms(value):
    if not value or value == '0':
        return ''
    return convert_unix_ts_to_utc(int(value))


@artifact_processor
def chromeBookmarks(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        source_path = file_found
        with open(file_found, encoding='utf-8') as fp:
            soup = bs4.BeautifulSoup(fp.read(), 'html.parser')

        folder_name = ''
        for i in soup.find_all('dt'):
            n = i.find_next()
            add_date = _bookmark_add_date(n.get('add_date', ''))
            last_modified = _bookmark_ms(n.get('last_modified', ''))
            if n.name == 'h3':
                folder_name = n.text
                data_list.append((add_date, last_modified, n.text, '', ''))
            else:
                data_list.append((add_date, last_modified, n.text, n.get('href', ''), folder_name))

    data_headers = (('Added Timestamp', 'datetime'), ('Last Modified', 'datetime'),
                    'Title', 'URL', 'Parent Folder Name')
    return data_headers, data_list, context.get_relative_path(source_path)
