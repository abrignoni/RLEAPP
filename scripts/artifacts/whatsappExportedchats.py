__artifacts_v2__ = {
    "whatsappExportedchats": {
        "name": "Whatsapp Exported Chat",
        "description": "Messages from a WhatsApp exported chat text file (_chat.txt), with "
                       "continuation lines kept in the preceding message and attached media "
                       "where the file is in the export.",
        "author": "@AlexisBrignoni, Codex",
        "creation_date": "2022-03-12",
        "last_update_date": "2026-10-04",
        "requirements": "none",
        "category": "Whatsapp Exported Chat",
        "notes": "Bracketed numeric date/time prefixes identify message starts. Timestamp is kept as "
                 "printed text; its date order and time zone are not established. Count is the "
                 "starting line number. Text before the first recognised message is retained "
                 "with a blank timestamp and username. Brackets inside message text are kept.",
        "paths": ('*/*_chat.txt',),
        "output_types": "standard",
        "artifact_icon": "message-circle",
    }
}

import os
import re

from scripts.ilapfuncs import artifact_processor, check_in_media


@artifact_processor
def whatsappExportedchats(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('_chat.txt') or os.path.basename(file_found).startswith('.'):
            continue
        source_path = file_found
        pending = None
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            for count, line in enumerate(f, start=1):
                line = line.replace(chr(0x200e), '').rstrip('\r\n')
                match = re.match(
                    r'^\[(\d{1,4}[/.-]\d{1,2}[/.-]\d{1,4},?\s+'
                    r'\d{1,2}:\d{2}(?::\d{2})?[^\]]*)\]\s?(.*)$', line)
                if match:
                    if pending is not None:
                        data_list.append(tuple(pending))
                    fecha, message = match.groups()
                    name, separator, mensaje = message.partition(': ')
                    if not separator:
                        name, mensaje = '', message
                    thumb = ''
                    attached = re.search(r'<attached: ([^>]+)>', mensaje)
                    if attached:
                        attach = attached.group(1)
                        thumb = check_in_media(attach, attach)
                    pending = [fecha, count, name, mensaje, thumb]
                elif pending is not None:
                    pending[3] += '\n' + line
                elif line:
                    pending = ['', count, '', line, '']
        if pending is not None:
            data_list.append(tuple(pending))

    data_headers = ('Timestamp', 'Count', 'Username', 'Message', ('Media', 'media'))
    return data_headers, data_list, context.get_relative_path(source_path)
