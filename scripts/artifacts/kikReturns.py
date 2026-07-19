def _meta(name, paths, icon, html_columns=None):
    meta = {"name": f"Kik - {name}",
            "description": f"{name} from a Kik law enforcement return.",
            "author": "@AlexisBrignoni", "creation_date": "2021-08-17",
            "last_update_date": "2026-06-28", "requirements": "none",
            "category": "Kik Returns", "notes": "", "paths": paths,
            "output_types": "standard", "artifact_icon": icon}
    if html_columns:
        meta["html_columns"] = html_columns
    return meta


__artifacts_v2__ = {
    "kikBind": _meta("Bind", ('*/logs/bind.txt',), "log-in"),
    "kikChatPlatformSentReceived": _meta("Chat Platform Sent Received",
                                         ('*/logs/chat_platform_sent_received.txt',), "repeat"),
    "kikChatPlatformSent": _meta("Chat Platform Sent", ('*/logs/chat_platform_sent.txt',), "send"),
    "kikChatSentReceived": _meta("Chat Sent Received", ('*/logs/chat_sent_received.txt',),
                                 "message-square"),
    "kikChatSent": _meta("Chat Sent", ('*/logs/chat_sent.txt',), "message-circle"),
    "kikAbuseReport": _meta("Abuse Report", ('*/logs/*abuse',), "alert-triangle",
                            html_columns=["Data"]),
    "kikFriendAdded": _meta("Friend Added", ('*/logs/friend_added.txt',), "user-plus"),
    "kikGroupReceiveMsgPlatform": _meta("Group Receive Msg Platform",
                                        ('*/logs/group_receive_msg_platform.txt',), "download"),
    "kikGroupReceiveMsg": _meta("Group Receive Msg", ('*/logs/group_receive_msg.txt',), "users"),
    "kikGroupSendMsgPlatform": _meta("Group Send Msg Platform",
                                     ('*/logs/group_send_msg_platform.txt',), "upload"),
    "kikGroupSendMsg": _meta("Group Send Msg", ('*/logs/group_send_msg.txt',), "users"),
    "kikTextMessageData": _meta("Text Message Data",
                                ('*/content/text-msg-data/*data-text.csv',), "file-text"),
    "kikBinds": _meta("Binds", ('*/content/text-msg-data/*binds.csv',), "link"),
}

import csv
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc, check_in_media
from scripts.html_safe import esc


def utf8_in_extended_ascii(input_string, *, raise_on_unexpected=False):
    """Returns a tuple of bool (whether mis-encoded utf-8 is present) and str (the converted)."""
    output = []
    is_in_multibyte = False
    multibytes_expected = 0
    multibyte_buffer = []
    mis_encoded_utf8_present = False

    def handle_bad_data(index, character):
        if not raise_on_unexpected:
            output.extend(multibyte_buffer)
            multibyte_buffer.clear()
            output.append(character)
            nonlocal is_in_multibyte
            is_in_multibyte = False
            nonlocal multibytes_expected
            multibytes_expected = 0
        else:
            raise ValueError(f"Expected multibyte continuation at index: {index}")

    for idx, char in enumerate(input_string):
        code_point = ord(char)
        if code_point <= 0x7f or code_point > 0xf4:
            if not is_in_multibyte:
                output.append(char)
            else:
                handle_bad_data(idx, char)
        else:
            if (code_point & 0xc0) == 0x80:
                if is_in_multibyte:
                    multibyte_buffer.append(char)
                else:
                    handle_bad_data(idx, char)
            else:
                if not is_in_multibyte:
                    while (code_point & 0x80) != 0:
                        multibytes_expected += 1
                        code_point <<= 1
                    multibyte_buffer.append(char)
                    is_in_multibyte = True
                else:
                    handle_bad_data(idx, char)

        if is_in_multibyte and len(multibyte_buffer) == multibytes_expected:
            utf_8_character = bytes(ord(x) for x in multibyte_buffer).decode("utf-8")
            output.append(utf_8_character)
            multibyte_buffer.clear()
            is_in_multibyte = False
            multibytes_expected = 0
            mis_encoded_utf8_present = True

    if multibyte_buffer:
        handle_bad_data(len(input_string), "")

    return mis_encoded_utf8_present, "".join(output)


def _utf8(value):
    return utf8_in_extended_ascii(value or '')[1]


def _ts(value):
    if value in (None, ''):
        return ''
    text = str(value).strip()
    if text.isdigit():
        return convert_unix_ts_to_utc(int(text))
    try:
        dt = datetime.fromisoformat(text.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        return value


def _tab(context, basename, headers, build_row, min_len):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        base = os.path.basename(file_found)
        if base.startswith('.') or not base.startswith(basename):
            continue
        source_path = file_found
        with open(file_found, encoding='unicode_escape') as f:
            for item in csv.reader(f, delimiter='\t'):
                if len(item) < min_len:
                    continue
                data_list.append(build_row(item))
    return tuple(headers), data_list, context.get_relative_path(source_path)


@artifact_processor
def kikBind(context):
    headers = (('Timestamp', 'datetime'), 'User', 'IP', 'Port', 'Info')
    return _tab(context, 'bind.txt', headers,
                lambda item: (_ts(item[4]), item[1], item[2], item[3], item[5]), 6)


@artifact_processor
def kikChatPlatformSentReceived(context):
    headers = (('Timestamp', 'datetime'), 'User', 'Friend User', 'IP', 'APP', 'CID')
    return _tab(context, 'chat_platform_sent_received.txt', headers,
                lambda item: (_ts(item[3]), item[0], item[1], item[2], item[4], item[5]), 6)


@artifact_processor
def kikChatPlatformSent(context):
    headers = (('Timestamp', 'datetime'), 'User', 'Other User', 'App', 'IP', 'Content ID',
               ('Content', 'media'))
    return _tab(context, 'chat_platform_sent.txt', headers,
                lambda item: (_ts(item[6]), item[1], item[2], item[3], item[5], item[4],
                              check_in_media(str(item[4]), str(item[4]))), 7)


@artifact_processor
def kikChatSentReceived(context):
    headers = (('Timestamp', 'datetime'), 'User', 'Other User', 'Info 1', 'Info 2')
    return _tab(context, 'chat_sent_received.txt', headers,
                lambda item: (_ts(item[5]), item[1], item[2], item[3], item[4]), 6)


@artifact_processor
def kikChatSent(context):
    headers = (('Timestamp', 'datetime'), 'User', 'Other User', 'Info', 'IP')
    return _tab(context, 'chat_sent.txt', headers,
                lambda item: (_ts(item[5]), item[1], item[2], item[3], item[4]), 6)


@artifact_processor
def kikFriendAdded(context):
    headers = (('Timestamp', 'datetime'), 'User', 'Other User')
    return _tab(context, 'friend_added.txt', headers,
                lambda item: (_ts(item[3]), item[1], item[2]), 4)


@artifact_processor
def kikGroupReceiveMsgPlatform(context):
    headers = (('Timestamp', 'datetime'), 'User', 'Field', 'Other User', 'App', 'Info',
               'Content ID', ('Content', 'media'))
    return _tab(context, 'group_receive_msg_platform.txt', headers,
                lambda item: (_ts(item[7]), item[1], item[2], item[3], item[4], item[6], item[5],
                              check_in_media(str(item[5]), str(item[5]))), 8)


@artifact_processor
def kikGroupReceiveMsg(context):
    headers = (('Timestamp', 'datetime'), 'User', 'Value', 'Other User', 'Info 1', 'Info 2')
    return _tab(context, 'group_receive_msg.txt', headers,
                lambda item: (_ts(item[6]), item[1], item[2], item[3], item[4], item[5]), 6)


@artifact_processor
def kikGroupSendMsgPlatform(context):
    headers = (('Timestamp', 'datetime'), 'User', 'Field', 'Other User', 'App', 'IP', 'Content ID',
               ('Content', 'media'))
    return _tab(context, 'group_send_msg_platform.txt', headers,
                lambda item: (_ts(item[7]), item[1], item[2], item[3], item[4], item[6], item[5],
                              check_in_media(str(item[5]), str(item[5]))), 8)


@artifact_processor
def kikGroupSendMsg(context):
    headers = (('Timestamp', 'datetime'), 'User', 'Field 1', 'Other User', 'Field 2', 'IP')
    return _tab(context, 'group_send_msg.txt', headers,
                lambda item: (_ts(item[6]), item[1], item[2], item[3], item[4], item[5]), 7)


@artifact_processor
def kikAbuseReport(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        base = os.path.basename(file_found)
        if base.startswith('.') or not base.endswith('abuse'):
            continue
        source_path = file_found
        timestamp = report_from = aggregator = ''
        with open(file_found, encoding='unicode_escape') as f:
            for line in f:
                if line.startswith('-------Report'):
                    if aggregator != '':
                        data_list.append((_ts(timestamp), report_from, aggregator))
                        aggregator = ''
                    parts = line.split(' ')
                    report_from = parts[2] if len(parts) > 2 else ''
                    timestamp = (parts[4].strip('(') + ' ' + parts[5]) if len(parts) > 5 else ''
                else:
                    aggregator = aggregator + esc(line) + '<br>'
            if aggregator != '':
                data_list.append((_ts(timestamp), report_from, aggregator))
    data_headers = (('Timestamp', 'datetime'), 'Report From', 'Data')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def kikTextMessageData(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        base = os.path.basename(file_found)
        if base.startswith('.') or not base.endswith('data-text.csv'):
            continue
        source_path = file_found
        with open(file_found, encoding='unicode_escape') as f:
            for item in csv.reader(f, delimiter=','):
                if len(item) < 10:
                    continue
                data_list.append((_ts(item[9]), item[4], item[5], _utf8(item[3]), item[6], item[7],
                                  item[0]))
    data_headers = (('Timestamp', 'datetime'), 'Sender ID', 'Receiver ID', 'Message', 'IP', 'Port',
                    'Message ID')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def kikBinds(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        base = os.path.basename(file_found)
        if base.startswith('.') or not base.endswith('binds.csv'):
            continue
        source_path = file_found
        with open(file_found, encoding='unicode_escape') as f:
            for item in csv.reader(f, delimiter=','):
                if len(item) < 5:
                    continue
                data_list.append((_ts(item[3]), item[0], item[1], item[2], item[4]))
    data_headers = (('Timestamp', 'datetime'), 'Sender ID', 'IP', 'Port', 'Device')
    return data_headers, data_list, context.get_relative_path(source_path)
