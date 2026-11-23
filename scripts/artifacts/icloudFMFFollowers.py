__artifacts_v2__ = {
    "icloudFMFFollowers": {
        "name": "iCloud - FMF Followers",
        "description": "Find My Friends followers from an iCloud law enforcement return (xlsx).",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-18",
        "last_update_date": "2026-11-23",
        "requirements": "openpyxl",
        "category": "iCloud Returns",
        "notes": "When more than one workbook contributes rows, each value is placed under the column whose heading matches its own. Headings are matched ignoring case and punctuation, and the first spelling read is the one shown. Columns with no heading are matched by position. Repeated headings are matched in order of appearance. A Source File column is added with the evidence-relative path of the workbook each row came from. If a workbook has its own Source File heading, the added column is named Source File (1). With one contributing workbook the columns are unchanged and no Source File column is added.",
        "paths": ('*/fmf/*_Followers.xlsx',),
        "output_types": "standard",
        "artifact_icon": "users",
    }
}

import os
from datetime import date, time

from openpyxl import load_workbook

from scripts.ilapfuncs import artifact_processor
from scripts.lavafuncs import sanitize_sql_name

_RESERVED = {'from', 'to', 'order', 'group', 'where', 'select', 'index', 'join', 'references',
             'check', 'default', 'add', 'table', 'column', 'create', 'insert', 'update', 'delete',
             'drop', 'values', 'set', 'primary', 'key', 'unique', 'foreign', 'constraint', 'having',
             'distinct', 'union', 'using'}


def _safe_headers(cells):
    # Dynamic headers from the spreadsheet: ensure non-empty, unique, and not SQL reserved words
    # (LAVA builds CREATE TABLE with unquoted identifiers).
    seen, out = {}, []
    for i, cell in enumerate(cells):
        name = str(cell).strip() if cell not in (None, '') else f'Column {i + 1}'
        if sanitize_sql_name(name) in _RESERVED:
            name = f'{name} Value'
        key = sanitize_sql_name(name)
        seen[key] = seen.get(key, -1) + 1
        if seen[key]:
            name = f'{name} ({seen[key]})'
        out.append(name)
    return out


def _pool_workbooks(workbooks):
    """Combine (source, headers, rows) workbooks, keeping each value under its own heading."""
    with_rows = [workbook for workbook in workbooks
                 if any(value != '' for row in workbook[2] for value in row)]
    if len(with_rows) < 2:
        chosen = with_rows or workbooks
        return (tuple(chosen[-1][1]), list(chosen[-1][2])) if chosen else ((), [])

    columns, positions, named_rows = [], {}, []
    for source, headers, rows in with_rows:
        width = max(len(headers), *(len(row) for row in rows))
        names = _safe_headers(list(headers) + [''] * (width - len(headers)))
        keys = [sanitize_sql_name(name) for name in names]
        for name, key in zip(names, keys):
            if key not in positions:
                positions[key] = len(columns)
                columns.append(name)
        named_rows.extend((source, keys, row) for row in rows)

    data_list = []
    for source, keys, row in named_rows:
        aligned = [''] * len(columns)
        for key, value in zip(keys, row):
            aligned[positions[key]] = value
        data_list.append(aligned + [source])
    source_column = _safe_headers(columns + ['Source File'])[-1]
    return tuple(columns + [source_column]), data_list


def _parse_icloud_xlsx(file_found, header_row):
    workbook = load_workbook(file_found, read_only=True, data_only=True)
    sheet = workbook.worksheets[0]
    headers, rows = [], []
    for i, row in enumerate(sheet.iter_rows(values_only=True)):
        if i < header_row:
            continue
        cells = [str(c) if isinstance(c, (date, time)) else ('' if c is None else c) for c in row]
        if i == header_row:
            headers = _safe_headers(cells)
        else:
            rows.append(cells)
    workbook.close()
    return headers, rows


@artifact_processor
def icloudFMFFollowers(context):
    workbooks, sources = [], []
    for file_found in sorted(context.get_files_found(), key=str):
        file_found = str(file_found)
        basename = os.path.basename(file_found)
        if basename.startswith('~') or basename.startswith('.'):
            continue
        sources.append(file_found)
        sheet_headers, rows = _parse_icloud_xlsx(file_found, 1)
        if sheet_headers:
            workbooks.append((context.get_relative_path(file_found), sheet_headers, rows))
    headers, data_list = _pool_workbooks(workbooks)
    return headers, data_list, '\n'.join(sources)
