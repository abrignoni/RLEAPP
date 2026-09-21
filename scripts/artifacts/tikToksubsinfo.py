__artifacts_v2__ = {
    "tikToksubsinfo": {
        "name": "TikTok - Subscriber Info",
        "description": "Subscriber/registration information from a TikTok law enforcement return "
                       "((Subscriber information).pdf).",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-09-29",
        "last_update_date": "2026-09-21",
        "requirements": "pypdf",
        "category": "TikTok Returns",
        "notes": "Source File column added so per-subscriber provenance (originally encoded in the "
                 "report title) survives when multiple returns are merged into one table. The PDF's "
                 "text is read with pypdf, and each field is taken from a line holding its label, a "
                 "colon and the value. A field whose label and value are not extracted onto the same "
                 "line is left blank. Checked only on constructed PDFs made with ReportLab and with "
                 "Chrome's print to PDF, not on a real TikTok return.",
        "paths": ('*/*/*(Subscriber information).pdf',),
        "output_types": "standard",
        "artifact_icon": "user",
    }
}

import os
from datetime import datetime, timezone

from pypdf import PdfReader

from scripts.ilapfuncs import artifact_processor


def _to_utc(value):
    value = (value or '').strip()
    if not value:
        return value
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        return value


@artifact_processor
def tikToksubsinfo(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        filename = os.path.basename(file_found)
        if filename.startswith('~') or filename.startswith('.') or not filename.endswith('.pdf'):
            continue
        source_path = file_found

        text = ''
        for page in PdfReader(file_found).pages:
            text += (page.extract_text() or '') + '\n'

        username = registrationmethod = phone = ''
        registrationdate = registrationip = registrationdeviceinfo = ''
        for line in text.split('\n'):
            line = line.strip()
            if ':' not in line:
                continue
            key, _, rest = line.partition(':')  # split on FIRST colon so values keep their colons
            key = key.strip().lower()
            rest = rest.strip()
            if 'username' in key:
                username = rest
            elif 'registration method' in key:
                registrationmethod = rest
            elif 'phone' in key:
                phone = rest
            elif 'registration date' in key:
                registrationdate = rest
            elif 'registration ip' in key:
                registrationip = rest
            elif 'registration device info' in key:
                registrationdeviceinfo = rest

        data_list.append((_to_utc(registrationdate), username, registrationmethod, phone,
                          registrationip, registrationdeviceinfo,
                          context.get_relative_path(file_found)))

    data_headers = (('Registration Date', 'datetime'), 'Username', 'Registration Method',
                    ('Phone', 'phonenumber'), 'Registration IP', 'Registration Device Info',
                    'Source File')
    return data_headers, data_list, context.get_relative_path(source_path)
