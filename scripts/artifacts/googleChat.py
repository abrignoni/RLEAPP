__artifacts_v2__ = {
    "googleChat": {
        "name": "Google Chat - Messages",
        "description": "Parses Google Chat messages from Takeout",
        "author": "@KevinPagano3 & John Hyla {jfhyla@gmail.com}",
        "creation_date": "2022-03-08",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": ('*/Google Chat/Groups/*/**',),
        "output_types": "standard",
        "html_columns": ["Group Members"],
        "artifact_icon": "message-square",
    }
}

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from scripts.ilapfuncs import artifact_processor, check_in_media

_MONTHS = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
           'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}


def _parse_gchat_date(value):
    # Two Google formats, both UTC:
    #   "Tuesday, 7 February 2021 at 17:13:43 UTC"      (24h, no AM/PM)
    #   "Wednesday, January 4, 2023 at 10:59:50 AM UTC" (12h with AM/PM)
    value = value.strip()
    try:
        parts = value.split(', ')
        if len(parts) == 3:
            month_name, day = parts[1].split(' ')[0], parts[1].split(' ')[1]
            tail = parts[2].split(' ')
            year, time_token = tail[0], tail[2]
            ampm = tail[3] if len(tail) > 3 else ''
        elif len(parts) == 2:
            left, right = parts[1].split(' at ')
            day, month_name, year = left.split(' ')[0], left.split(' ')[1], left.split(' ')[2]
            rtok = right.split(' ')
            time_token = rtok[0]
            ampm = rtok[1] if len(rtok) > 1 and rtok[1] in ('AM', 'PM') else ''
        else:
            return value
        hour, minute, second = (int(x) for x in time_token.split(':'))
        if ampm == 'PM' and hour < 12:
            hour += 12
        elif ampm == 'AM' and hour == 12:
            hour = 0
        return datetime(int(year), _MONTHS[month_name], int(day), hour, minute, second,
                        tzinfo=timezone.utc)
    except (ValueError, KeyError, IndexError):
        return value


@artifact_processor
def googleChat(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'messages.json':
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as f:
            data = json.load(f)

        members = []
        group_info_file = os.path.join(os.path.dirname(file_found), 'group_info.json')
        if Path(group_info_file).is_file():
            with open(group_info_file, encoding='utf-8') as fg:
                group_data = json.load(fg)
            for member in group_data.get('members', []):
                members.append(member.get('name', '') + ' - ' + member.get('email', ''))
        members_html = '<br>'.join(members)

        for chat_message in data.get('messages', []):
            created_date = chat_message.get('created_date', '')
            deleted_date = chat_message.get('deleted_date', '')
            date_str = created_date or deleted_date
            if not date_str:
                continue
            creator = chat_message.get('creator', {})
            sender_name = creator.get('name', '') if created_date else 'deleted'
            sender_email = creator.get('email', '')
            sender_user_type = creator.get('user_type', '')
            created_dt = _parse_gchat_date(date_str)
            message_text = chat_message.get('text', '')

            attachments = []
            for att in chat_message.get('attached_files', []):
                export_name = att.get('export_name', '')
                if export_name:
                    ref = check_in_media(export_name, export_name)
                    if ref:
                        attachments.append(ref)

            data_list.append((created_dt, sender_name, sender_email, sender_user_type,
                              members_html, message_text, attachments))

    data_headers = (('Created Timestamp', 'datetime'), 'Sender Name', 'Sender Email', 'Sender Type',
                    'Group Members', 'Message', ('Attachment', 'media'))
    return data_headers, data_list, context.get_relative_path(source_path)
