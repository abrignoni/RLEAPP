def _meta(name, paths, icon):
    return {"name": f"Gab - {name}",
            "description": f"{name} from a Gab law enforcement return.",
            "author": "@AlexisBrignoni", "creation_date": "2024-02-02",
            "last_update_date": "2026-06-28", "requirements": "none",
            "category": "Gab Returns", "notes": "", "paths": paths,
            "output_types": "standard", "artifact_icon": icon}


__artifacts_v2__ = {
    "gabPosts": _meta("Posts", ('*/*_posts.csv',), "message-square"),
    "gabAccountInfo": _meta("Account Info", ('*/*_account_info.csv',), "user"),
    "gabBlocks": _meta("Blocks", ('*/*_blocks.csv',), "slash"),
    "gabFollowers": _meta("Followers", ('*/*_followers.csv',), "users"),
    "gabFollowing": _meta("Following", ('*/*_following.csv',), "users"),
    "gabLikes": _meta("Likes", ('*/*_likes.csv',), "thumbs-up"),
    "gabMentions": _meta("Mentions", ('*/*_mentions.csv',), "at-sign"),
    "gabReplies": _meta("Replies", ('*/*_replies.csv',), "corner-up-left"),
    "gabSessionActivations": _meta("Session Activations", ('*/*_session_activations.csv',), "key"),
}

import csv
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


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


def _process(context, suffix, headers, build_row, min_len):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith(suffix):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)  # header row
            for item in reader:
                if len(item) < min_len:
                    continue
                data_list.append(build_row(item))
    return tuple(headers), data_list, context.get_relative_path(source_path)


@artifact_processor
def gabPosts(context):
    headers = (('Timestamp', 'datetime'), ('Updated', 'datetime'), 'Text', 'In Reply to ID',
               'Reblog of ID', 'ID', 'URI', 'URL', 'Sensitive', 'Visibility', 'Spoiler Text',
               'Reply', 'Language', 'Conversation ID', 'Local', 'Account ID', 'Application',
               'In Reply To', 'Poll ID', 'Group ID', 'Quote of ID', 'Revised At', 'Markdown',
               'Expires At', 'Has Quote', 'Tombstoned At')

    def build(item):
        return (_ts(item[3]), _ts(item[4]), _utf8(item[2]), item[5], item[6], item[0], item[1],
                item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14],
                item[15], item[16], item[17], item[18], item[19], item[20], item[21], item[22],
                item[23], item[24], item[25])

    return _process(context, '_posts.csv', headers, build, 26)


@artifact_processor
def gabAccountInfo(context):
    headers = ('Timestamp', 'Updated', 'Username', 'ID', 'Note', 'Display Name', 'Avatar Filename',
               'Avatar Content Type', 'Avatar File Size', 'Avatar Updated At', 'Header File Name',
               'Header Content Type', 'Header File Size', 'Header Updated At', 'Locked', 'Memorial',
               'Is Pro', 'Is Verified', 'Is Donor', 'Is Investor', 'Is Flagged', 'Weighted TSV',
               'Domain', 'Secret', 'Remote URL', 'Salmon URL', 'Hub URL', 'URI', 'URL',
               'Avatar Remote URL', 'Subscription', 'Header Remote URL', 'Last Web Fingered At',
               'Inbox URL', 'Outbox URL', 'Shared Inbox URL', 'Followers URL', 'Protocol',
               'Moved To Account ID', 'Featured Collection URL', 'Fields', 'Actor Type',
               'Discoverable', 'Also Known As', 'Silenced At', 'Suspended At', 'Pro Expires At',
               'Spam Flag')
    headers = (('Timestamp', 'datetime'), ('Updated', 'datetime')) + headers[2:]

    def build(item):
        return (_ts(item[7]), _ts(item[8]), item[1], item[0], item[9], item[10], item[13],
                item[14], item[15], item[16], item[17], item[18], item[19], item[20], item[23],
                item[31], item[40], item[42], item[43], item[44], item[45], item[47], item[2],
                item[3], item[4], item[5], item[6], item[11], item[12], item[21], item[22],
                item[24], item[25], item[26], item[27], item[28], item[29], item[30], item[32],
                item[33], item[34], item[35], item[36], item[37], item[38], item[39], item[41],
                item[46])

    return _process(context, '_account_info.csv', headers, build, 48)


@artifact_processor
def gabBlocks(context):
    headers = (('Timestamp', 'datetime'), 'Account ID', 'Target Account ID', 'Blocked')

    def build(item):
        return (_ts(item[0]), item[1], item[2], item[3])

    return _process(context, '_blocks.csv', headers, build, 4)


@artifact_processor
def gabFollowers(context):
    return _process(context, '_followers.csv', ('Username',), lambda item: (item[0],), 1)


@artifact_processor
def gabFollowing(context):
    return _process(context, '_following.csv', ('Username',), lambda item: (item[0],), 1)


def _likes_mentions(context, suffix):
    headers = (('Created At', 'datetime'), 'ID', 'URI', ('Post Created At', 'datetime'), 'Text',
               'URL', 'Account ID')

    def build(item):
        return (_ts(item[0]), item[1], item[2], _ts(item[3]), _utf8(item[4]), item[5], item[6])

    return _process(context, suffix, headers, build, 7)


@artifact_processor
def gabLikes(context):
    return _likes_mentions(context, '_likes.csv')


@artifact_processor
def gabMentions(context):
    return _likes_mentions(context, '_mentions.csv')


@artifact_processor
def gabReplies(context):
    headers = (('Timestamp', 'datetime'), ('updated_at', 'datetime'), 'id', 'uri', 'text',
               'in_reply_to_id', 'reblog_of_id', 'url', 'sensitive', 'visibility', 'spoiler_text',
               'reply', 'language', 'conversation_id', 'local', 'account_id', 'application_id',
               'in_reply_to_account_id', 'poll_id', 'group_id', 'quote_of_id', 'revised_at',
               'markdown', 'expires_at', 'has_quote', 'tombstoned_at')

    def build(item):
        return (_ts(item[3]), _ts(item[4]), item[0], item[1], item[2], item[5], item[6], item[7],
                item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15],
                item[16], item[17], item[18], item[19], item[20], item[21], item[22], item[23],
                item[24], item[25])

    return _process(context, '_replies.csv', headers, build, 26)


@artifact_processor
def gabSessionActivations(context):
    headers = (('Created At', 'datetime'), ('Updated At', 'datetime'), 'ID', 'Session ID',
               'User Agent', 'IP', 'Access Token ID', 'User ID', 'Web Push Subscription ID')

    def build(item):
        return (_ts(item[2]), _ts(item[3]), item[0], item[1], item[4], item[5], item[6], item[7],
                item[8])

    return _process(context, '_session_activations.csv', headers, build, 9)
