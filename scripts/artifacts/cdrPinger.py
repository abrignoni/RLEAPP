__artifacts_v2__ = {
    "cdrPinger": {
        "name": "Pinger - CDR",
        "description": "Call detail records from a Pinger law enforcement return (xlsx).",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-18",
        "last_update_date": "2026-11-23",
        "requirements": "openpyxl",
        "category": "Pinger",
        "notes": "When more than one workbook contributes rows, each value is placed under the column whose heading matches its own. Headings are matched ignoring case and punctuation, and the first spelling read is the one shown. Columns with no heading are matched by position. Repeated headings are matched in order of appearance. A Source File column is added with the evidence-relative path of the workbook each row came from. If a workbook has its own Source File heading, the added column takes a numbered name such as Source File (1). With one contributing workbook the columns are unchanged and no Source File column is added.",
        "paths": ('*/*CDR.xlsx',),
        "output_types": "standard",
        "artifact_icon": "phone-call",
    }
}

import os
from datetime import date, time

from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from scripts.ilapfuncs import artifact_processor
from scripts.lavafuncs import sanitize_sql_name

_RESERVED = {'from', 'to', 'order', 'group', 'where', 'select', 'index', 'join', 'references',
             'check', 'default', 'add', 'table', 'column', 'create', 'insert', 'update', 'delete',
             'drop', 'values', 'set', 'primary', 'key', 'unique', 'foreign', 'constraint', 'having',
             'distinct', 'union', 'using'}


def _safe_headers(cells):
    seen, used, out = {}, set(), []
    for i, cell in enumerate(cells):
        name = ('' if cell is None else str(cell).strip()) or f'Column {i + 1}'
        if sanitize_sql_name(name) in _RESERVED:
            name = f'{name} Value'
        key = sanitize_sql_name(name)
        seen[key] = seen.get(key, -1) + 1
        count = seen[key]
        unique = f'{name} ({count})' if count else name
        while sanitize_sql_name(unique) in used:
            count += 1
            unique = f'{name} ({count})'
        used.add(sanitize_sql_name(unique))
        out.append(unique)
    return out


def _heading_keys(cells):
    """Identify each heading by its own text and occurrence, or by position when it has none."""
    seen, keys = {}, []
    for i, cell in enumerate(cells):
        text = '' if cell is None else str(cell).strip()
        if not text:
            keys.append(('position', i))
            continue
        text = sanitize_sql_name(text).strip('_') or text
        seen[text] = seen.get(text, -1) + 1
        keys.append(('heading', text, seen[text]))
    return keys


def _pool_workbooks(workbooks):
    """Combine (source, headers, heading_keys, rows) workbooks, keeping values under their headings."""
    with_rows = [workbook for workbook in workbooks
                 if any(value != '' for row in workbook[3] for value in row)]
    if len(with_rows) < 2:
        chosen = with_rows or workbooks
        return (tuple(chosen[-1][1]), list(chosen[-1][3])) if chosen else ((), [])

    columns, positions, keyed_rows = [], {}, []
    for source, headers, heading_keys, rows in with_rows:
        width = max(len(headers), *(len(row) for row in rows))
        names = list(headers) + [f'Column {i + 1}' for i in range(len(headers), width)]
        keys = list(heading_keys) + [('position', i) for i in range(len(headers), width)]
        for name, key in zip(names, keys):
            if key not in positions:
                positions[key] = len(columns)
                columns.append(name)
        keyed_rows.extend((source, keys, row) for row in rows)

    data_list = []
    for source, keys, row in keyed_rows:
        aligned = [''] * len(columns)
        for key, value in zip(keys, row):
            aligned[positions[key]] = value
        data_list.append(aligned + [source])
    return tuple(_safe_headers(columns + ['Source File'])), data_list


def _parse_xlsx(file_found, header_row):
    workbook = load_workbook(file_found, read_only=True, data_only=True)
    sheet = workbook.worksheets[0]
    headers, heading_keys, rows = [], [], []
    for i, row in enumerate(sheet.iter_rows(values_only=True)):
        if i < header_row:
            continue
        cells = [str(c) if isinstance(c, (date, time)) else ('' if c is None else c) for c in row]
        if i == header_row:
            headers = _safe_headers(cells)
            heading_keys = _heading_keys(cells)
        else:
            rows.append(cells)
    workbook.close()
    return headers, heading_keys, rows


@artifact_processor
def cdrPinger(context):
    workbooks, sources = [], []
    for file_found in sorted(context.get_files_found(), key=str):
        file_found = str(file_found)
        basename = os.path.basename(file_found)
        if basename.startswith('~') or basename.startswith('.'):
            continue
        try:
            sheet_headers, heading_keys, rows = _parse_xlsx(file_found, 1)
        except (InvalidFileException, KeyError):
            continue
        sources.append(file_found)
        if sheet_headers:
            workbooks.append((context.get_relative_path(file_found), sheet_headers, heading_keys, rows))
    headers, data_list = _pool_workbooks(workbooks)
    return headers, data_list, '\n'.join(sources)
