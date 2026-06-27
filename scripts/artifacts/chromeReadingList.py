__artifacts_v2__ = {
    "chromeReadingList": {
        "name": "Chrome Reading List",
        "description": "Parses Google Chrome reading list from Takeout",
        "author": "@KevinPagano3",
        "creation_date": "2023-08-24",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Chrome/ReadingList.html'),
        "output_types": "standard",
        "artifact_icon": "list",
    }
}

import bs4

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


@artifact_processor
def chromeReadingList(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        source_path = file_found
        with open(file_found, encoding='utf-8') as fp:
            soup = bs4.BeautifulSoup(fp.read(), 'html.parser')

        for i in soup.find_all('dt'):
            n = i.find_next()
            add_date = n.get('add_date', '')
            add_date = convert_unix_ts_to_utc(add_date) if add_date else ''
            data_list.append((add_date, n.text, n.get('href', '')))

    data_headers = (('Added Timestamp', 'datetime'), 'Title', 'URL')
    return data_headers, data_list, context.get_relative_path(source_path)
