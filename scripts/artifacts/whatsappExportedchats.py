__artifacts_v2__ = {
    "whatsappExportedchats": {
        "name": "Whatsapp Exported Chat",
        "description": "Lines of a WhatsApp exported chat text file (_chat.txt), one row per line, "
                       "with attached media where the file is in the export. Message text that "
                       "contains ']' is cut at that character.",
        "author": "@AlexisBrignoni",
        "creation_date": "2022-03-12",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Whatsapp Exported Chat",
        "notes": "Timestamp is the text before the first ']' on a line, with the '[' removed. A "
                 "line that continues a multi-line message has a blank Timestamp unless it contains "
                 "']', in which case the text before that character is shown there. Timestamp is "
                 "kept as text and is not converted; the date format and time zone of the export "
                 "are not established by this parser.",
        "paths": ('*/*_chat.txt',),
        "output_types": "standard",
        "artifact_icon": "message-circle",
    }
}

import os

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
        count = 0
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            for line in f:
                count += 1
                line = line.replace(chr(0x200e), '').strip()
                dividido = line.split(']')
                fecha = name = thumb = ''
                if len(dividido) > 1:
                    fecha = dividido[0].replace('[', '')
                    if ':' in dividido[1]:
                        name = dividido[1].split(':')[0]
                        mensaje = dividido[1].split(':', 1)[1]
                    else:
                        mensaje = dividido[1]
                    if '<attached: ' in mensaje:
                        attach = mensaje.split('<attached: ')[1].replace('>', '')
                        thumb = check_in_media(attach, attach)
                else:
                    mensaje = line
                if mensaje != '':
                    data_list.append((fecha, count, name, mensaje, thumb))

    data_headers = ('Timestamp', 'Count', 'Username', 'Message', ('Media', 'media'))
    return data_headers, data_list, context.get_relative_path(source_path)
