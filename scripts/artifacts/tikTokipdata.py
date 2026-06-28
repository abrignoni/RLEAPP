__artifacts_v2__ = {
    "tikTokipdata": {
        "name": "TikTok - IP Data",
        "description": "IP login/activity data from a TikTok law enforcement return (*- IP Data.xlsx).",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-09-29",
        "last_update_date": "2026-06-28",
        "requirements": "openpyxl",
        "category": "TikTok Returns",
        "notes": "Source File column added so per-subscriber provenance (originally encoded in the "
                 "report title) survives when multiple returns are merged into one table.",
        "paths": ('*/*/*- IP Data.xlsx',),
        "output_types": "standard",
        "artifact_icon": "globe",
    }
}

import os
from datetime import datetime, timezone

import openpyxl

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


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


def _cell(value):
    return '' if value is None else value


@artifact_processor
def tikTokipdata(context):
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
                cells = list(row) + ['', '', '', '']
                data_list.append((_to_utc(cells[0]), _to_utc(cells[1]), _cell(cells[2]),
                                  _cell(cells[3]), rel))
        finally:
            wb.close()

    data_headers = (('Timestamp', 'datetime'), ('Active Start Time', 'datetime'), 'IP',
                    'IP Country', 'Source File')
    return data_headers, data_list, context.get_relative_path(source_path)
