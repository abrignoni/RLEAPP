__artifacts_v2__ = {
    "gooReturnsact": {
        "name": "Google Returns - Access Log Activities",
        "description": "Access Log Activities from a Google law enforcement return "
                       "(Access Log Activity/Activities*.csv).",
        "author": "@AlexisBrignoni",
        "creation_date": "2022-05-29",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Google Returns",
        "notes": "Dynamic-schema CSV: headers are read from the file's first row (with the first "
                 "column moved to the end, as in the original) and made LAVA-safe. This parses the "
                 "same source as the Takeout 'Google Access Log Activities' artifact.",
        "paths": ('*/Access Log Activity/Activities*.csv',),
        "output_types": "standard",
        "artifact_icon": "activity",
    }
}

import csv
import os

from scripts.ilapfuncs import artifact_processor
from scripts.lavafuncs import sanitize_sql_name

_RESERVED = {'from', 'to', 'order', 'group', 'where', 'select', 'index', 'join', 'references',
             'check', 'default', 'add', 'table', 'column', 'create', 'insert', 'update', 'delete',
             'drop', 'values', 'set', 'primary', 'key', 'unique', 'foreign', 'constraint', 'having',
             'distinct', 'union', 'using'}


def _safe_headers(cells):
    seen, out = {}, []
    for i, cell in enumerate(cells):
        name = str(cell).strip() if cell not in (None, '') else f'Column {i + 1}'
        if sanitize_sql_name(name) in _RESERVED:
            name = f'{name} Value'
        key = name.lower()
        seen[key] = seen.get(key, -1) + 1
        if seen[key]:
            name = f'{name} ({seen[key]})'
        out.append(name)
    return out


@artifact_processor
def gooReturnsact(context):
    headers, data_list, source_path = [], [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.csv') or os.path.basename(file_found).startswith('.'):
            continue
        source_path = file_found
        file_headers = None
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            for item in csv.reader(f, delimiter=','):
                if not item:
                    continue
                item = item[1:] + item[:1]  # original moves the first column to the end
                if file_headers is None:
                    file_headers = _safe_headers(item)
                    continue
                row = item + [''] * len(file_headers)
                data_list.append(tuple(row[:len(file_headers)]))
        if file_headers:
            headers = file_headers

    return tuple(headers), data_list, context.get_relative_path(source_path)
