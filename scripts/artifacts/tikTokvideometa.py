__artifacts_v2__ = {
    "tikTokvideometa": {
        "name": "TikTok - Video Metadata",
        "description": "Video metadata (with linked media) from a TikTok law enforcement return "
                       "(*- video metadata.xlsx + Video Content/*).",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-09-29",
        "last_update_date": "2026-06-28",
        "requirements": "openpyxl",
        "category": "TikTok Returns",
        "notes": "Reads the active sheet of each '- video metadata.xlsx' file. The first row is "
                 "skipped as the header and the first three columns are reported, by position, as "
                 "Media ID, Timestamp Upload and Media Caption; the spreadsheet's own column titles "
                 "are not checked. Media is linked when a matched file's name equals the Media ID "
                 "value exactly. A date with no time zone is stored as UTC; the zone the provider "
                 "uses was not established here. Source File names the spreadsheet each row came "
                 "from. No tested return is recorded for this artifact.",
        "paths": ('*/*/*- video metadata.xlsx', '*/*/*/Video Content/*'),
        "output_types": "standard",
        "artifact_icon": "video",
    }
}

import os
from datetime import datetime, timezone

import openpyxl

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc, check_in_media


def _to_utc(value):
    if value is None or value == '':
        return ''
    if isinstance(value, datetime):
        return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)
    s = str(value).strip()
    if not s:
        return ''
    if s.isdigit():
        return convert_unix_ts_to_utc(int(s))
    try:
        dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        return value


@artifact_processor
def tikTokvideometa(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        filename = os.path.basename(file_found)
        if filename.startswith('~') or filename.startswith('.') or not filename.endswith('.xlsx'):
            continue
        source_path = file_found
        rel = context.get_relative_path(file_found)
        wb = openpyxl.load_workbook(file_found, read_only=True, data_only=True)
        try:
            sheet = wb.active
            for idx, row in enumerate(sheet.iter_rows(values_only=True)):
                if idx == 0:
                    continue  # header row inside the spreadsheet
                cells = list(row) + ['', '', '']
                videoid = cells[0]
                media = check_in_media(str(videoid), str(videoid)) if videoid not in (None, '') else ''
                data_list.append((media, _to_utc(cells[1]),
                                  '' if videoid is None else videoid,
                                  '' if cells[2] is None else cells[2], rel))
        finally:
            wb.close()

    data_headers = (('Media', 'media'), ('Timestamp Upload', 'datetime'), 'Media ID',
                    'Media Caption', 'Source File')
    return data_headers, data_list, context.get_relative_path(source_path)
