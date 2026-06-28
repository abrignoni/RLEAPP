__artifacts_v2__ = {
    "snapArchiveFriends": {
        "name": "Snapchat Archive - Friends", "description": "Friends from a Snapchat data archive (friends.json).",
        "author": "@AlexisBrignoni", "creation_date": "2023-12-11", "last_update_date": "2026-06-28",
        "requirements": "none", "category": "Snapchat Archive", "notes": "",
        "paths": ('*/friends.json',), "output_types": "standard", "artifact_icon": "users",
    },
    "snapArchiveFriendRequestsSent": {
        "name": "Snapchat Archive - Friend Requests Sent", "description": "Friend requests sent from a Snapchat data archive (friends.json).",
        "author": "@AlexisBrignoni", "creation_date": "2023-12-11", "last_update_date": "2026-06-28",
        "requirements": "none", "category": "Snapchat Archive", "notes": "",
        "paths": ('*/friends.json',), "output_types": "standard", "artifact_icon": "user-plus",
    },
    "snapArchiveBlockedUsers": {
        "name": "Snapchat Archive - Blocked Users", "description": "Blocked users from a Snapchat data archive (friends.json).",
        "author": "@AlexisBrignoni", "creation_date": "2023-12-11", "last_update_date": "2026-06-28",
        "requirements": "none", "category": "Snapchat Archive", "notes": "",
        "paths": ('*/friends.json',), "output_types": "standard", "artifact_icon": "user-x",
    },
    "snapArchiveDeletedFriends": {
        "name": "Snapchat Archive - Deleted Friends", "description": "Deleted friends from a Snapchat data archive (friends.json).",
        "author": "@AlexisBrignoni", "creation_date": "2023-12-11", "last_update_date": "2026-06-28",
        "requirements": "none", "category": "Snapchat Archive", "notes": "",
        "paths": ('*/friends.json',), "output_types": "standard", "artifact_icon": "user-minus",
    },
    "snapArchiveHiddenFriendSuggestions": {
        "name": "Snapchat Archive - Hidden Friend Suggestions", "description": "Hidden friend suggestions from a Snapchat data archive (friends.json).",
        "author": "@AlexisBrignoni", "creation_date": "2023-12-11", "last_update_date": "2026-06-28",
        "requirements": "none", "category": "Snapchat Archive", "notes": "",
        "paths": ('*/friends.json',), "output_types": "standard", "artifact_icon": "eye-off",
    },
    "snapArchiveIgnoredSnapchatters": {
        "name": "Snapchat Archive - Ignored Snapchatters", "description": "Ignored Snapchatters from a Snapchat data archive (friends.json).",
        "author": "@AlexisBrignoni", "creation_date": "2023-12-11", "last_update_date": "2026-06-28",
        "requirements": "none", "category": "Snapchat Archive", "notes": "",
        "paths": ('*/friends.json',), "output_types": "standard", "artifact_icon": "user-x",
    },
    "snapArchivePendingRequests": {
        "name": "Snapchat Archive - Pending Requests", "description": "Pending requests from a Snapchat data archive (friends.json).",
        "author": "@AlexisBrignoni", "creation_date": "2023-12-11", "last_update_date": "2026-06-28",
        "requirements": "none", "category": "Snapchat Archive", "notes": "",
        "paths": ('*/friends.json',), "output_types": "standard", "artifact_icon": "clock",
    },
    "snapArchiveShortcuts": {
        "name": "Snapchat Archive - Shortcuts", "description": "Shortcuts from a Snapchat data archive (friends.json).",
        "author": "@AlexisBrignoni", "creation_date": "2023-12-11", "last_update_date": "2026-06-28",
        "requirements": "none", "category": "Snapchat Archive", "notes": "",
        "paths": ('*/friends.json',), "output_types": "standard", "artifact_icon": "bookmark",
    }
}

import json
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc

_MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
           'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
_HEADERS = (('Timestamp', 'datetime'), ('Last Modified Timestamp', 'datetime'), 'Username',
            'Display Name', 'Source')


def _snap_ts(value):
    value = (value or '').strip()
    if not value:
        return value
    cleaned = value.replace(' UTC', '').strip()
    if cleaned.isdigit():
        return convert_unix_ts_to_utc(int(cleaned))
    try:
        dt = datetime.fromisoformat(cleaned.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        pass
    try:
        parts = value.split(' ')
        return datetime(int(parts[-1]), _MONTHS[parts[1]], int(parts[2]),
                        *(int(x) for x in parts[3].split(':')), tzinfo=timezone.utc)
    except (IndexError, KeyError, ValueError):
        return value


def _friend_section(context, key):
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).startswith('friends.json'):
            continue
        with open(file_found, encoding='utf-8') as fp:
            data = json.load(fp)
        rows = [(_snap_ts(it.get('Creation Timestamp', '')),
                 _snap_ts(it.get('Last Modified Timestamp', '')), it.get('Username', ''),
                 it.get('Display Name', ''), it.get('Source', '')) for it in data.get(key, [])]
        return _HEADERS, rows, context.get_relative_path(file_found)
    return _HEADERS, [], ''


@artifact_processor
def snapArchiveFriends(context):
    return _friend_section(context, 'Friends')


@artifact_processor
def snapArchiveFriendRequestsSent(context):
    return _friend_section(context, 'Friend Requests Sent')


@artifact_processor
def snapArchiveBlockedUsers(context):
    return _friend_section(context, 'Blocked Users')


@artifact_processor
def snapArchiveDeletedFriends(context):
    return _friend_section(context, 'Deleted Friends')


@artifact_processor
def snapArchiveHiddenFriendSuggestions(context):
    return _friend_section(context, 'Hidden Friend Suggestions')


@artifact_processor
def snapArchiveIgnoredSnapchatters(context):
    return _friend_section(context, 'Ignored Snapchatters')


@artifact_processor
def snapArchivePendingRequests(context):
    return _friend_section(context, 'Pending Requests')


@artifact_processor
def snapArchiveShortcuts(context):
    return _friend_section(context, 'Shortcuts')
