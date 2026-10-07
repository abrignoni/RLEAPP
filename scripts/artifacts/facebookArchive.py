__artifacts_v2__ = {
    "facebookArchiveAccountActivity": {
        "name": "Facebook Archive - Account Activity",
        "description": "Account activity events from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from security_and_login_information/account_activity.json in a Facebook Download "
                 "Your Information (DYI) JSON export. One row per entry in account_activity_v2 of the "
                 "first matching file; when the input holds more than one export only the first file "
                 "found is read. Timestamp is the entry's Unix seconds value. Action, IP Address, City, "
                 "Region, Country, Site, User Agent, Datr Cookie and Port are the fields the export "
                 "records for the event, reported as stored. How the export derives City, Region and "
                 "Country is not established here, and they are not shown to be a device location. "
                 "Field mapping was done against a private sample; no sample data is recorded for it.",
        "paths": ('*/security_and_login_information/account_activity.json',),
        "output_types": "standard",
        "artifact_icon": "brand-facebook",
    },
    "facebookArchiveLogins": {
        "name": "Facebook Archive - Logins and Logouts",
        "description": "Login and logout events from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from security_and_login_information/logins_and_logouts.json, one row per entry "
                 "in account_accesses_v2. Timestamp is Unix seconds. Action, Site and IP Address are "
                 "reported as stored. When the input holds more than one export only the first file "
                 "found is read. Field mapping was done against a private sample; no sample data is "
                 "recorded for it.",
        "paths": ('*/security_and_login_information/logins_and_logouts.json',),
        "output_types": "standard",
        "artifact_icon": "login",
    },
    "facebookArchiveIpActivity": {
        "name": "Facebook Archive - IP Address Activity",
        "description": "IP address activity from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from security_and_login_information/ip_address_activity.json, one row per entry "
                 "in used_ip_address_v2. Timestamp is Unix seconds. IP, Action and User Agent are "
                 "reported as stored. When the input holds more than one export only the first file "
                 "found is read. Field mapping was done against a private sample; no sample data is "
                 "recorded for it.",
        "paths": ('*/security_and_login_information/ip_address_activity.json',),
        "output_types": "standard",
        "artifact_icon": "world",
    },
    "facebookArchiveActiveSessions": {
        "name": "Facebook Archive - Active Sessions",
        "description": "Active sessions from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from security_and_login_information/where_you_re_logged_in.json, one row per "
                 "entry in active_sessions_v2. Created and Updated are Unix seconds. IP Address, "
                 "Device, Location, App, Session Type, User Agent and Datr Cookie are reported as "
                 "stored. What places a session in that list is not established here. When the input "
                 "holds more than one export only the first file found is read. Field mapping was done "
                 "against a private sample; no sample data is recorded for it.",
        "paths": ('*/security_and_login_information/where_you_re_logged_in.json',),
        "output_types": "standard",
        "artifact_icon": "devices",
    },
    "facebookArchiveAdminRecords": {
        "name": "Facebook Archive - Account Record Details",
        "description": "Account change records from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from security_and_login_information/record_details.json, one row per entry in "
                 "admin_records_v2. Event names the recorded account change. Session Created is Unix "
                 "seconds, with the Session IP, User Agent and Datr Cookie the export attached to the "
                 "event. Change Details joins the entry's extra_info fields (for example old and new "
                 "name, email, phone number or vanity) as label: value pairs. A field with an empty "
                 "value is left out, and a value that is not text (a number, a list or a nested object) "
                 "is shown blank after its label. When the input holds more than one export only the "
                 "first file found is read. Field mapping was done against a private sample; no sample "
                 "data is recorded for it.",
        "paths": ('*/security_and_login_information/record_details.json',),
        "output_types": "standard",
        "artifact_icon": "history",
    },
    "facebookArchiveRegistration": {
        "name": "Facebook Archive - Registration Information",
        "description": "Registration information from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from security_and_login_information/registration_information.json. Registered is "
                 "the file's top level Unix seconds timestamp. Label and Value are the export's own "
                 "registration label_values pairs, one row each, reported as stored, except that a "
                 "value that is not text (a number, a list or a nested object) is shown blank; the "
                 "labels are in the language of the export. FBID is the account identifier the file "
                 "records. When the input holds more than one export only the first file found is read. "
                 "Field mapping was done against a private sample; no sample data is recorded for it.",
        "paths": ('*/security_and_login_information/registration_information.json',),
        "output_types": "standard",
        "artifact_icon": "user-plus",
    },
    "facebookArchiveSearches": {
        "name": "Facebook Archive - Search History",
        "description": "Search history from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from logged_information/search/your_search_history.json, one row per entry in "
                 "searches_v2. Timestamp is Unix seconds. Search is the text values the entry carries "
                 "in its data array, joined; Title is the entry's own title, reported as stored. When "
                 "the input holds more than one export only the first file found is read. Field mapping "
                 "was done against a private sample; no sample data is recorded for it.",
        "paths": ('*/logged_information/search/your_search_history.json',),
        "output_types": "standard",
        "artifact_icon": "search",
    },
    "facebookArchiveProfileVisits": {
        "name": "Facebook Archive - Profile Visits",
        "description": "Profile visits from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from logged_information/interactions/profile_visits.json, one row per entry. "
                 "Timestamp is Unix seconds. Details joins the entry's label_values pairs as label: "
                 "value, reported as stored, except that a timestamp_value is shown as a UTC date and "
                 "time and a value that is not text (a number, a list or a nested object) is shown "
                 "blank after its label; the labels are in the language of the export. When the input "
                 "holds more than one export only the first file found is read. Field mapping was done "
                 "against a private sample; no sample data is recorded for it.",
        "paths": ('*/logged_information/interactions/profile_visits.json',),
        "output_types": "standard",
        "artifact_icon": "eye",
    },
    "facebookArchivePrimaryLocation": {
        "name": "Facebook Archive - Primary Location",
        "description": "Primary location from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from logged_information/location/primary_location.json. How the platform arrives "
                 "at this location is not established here, and it is not shown to be a device GPS fix. "
                 "Label and Value are the export's own label_values pairs, flattened one row each, "
                 "reported as stored; the labels are in the language of the export. Only items that "
                 "carry a value or a dict give a row, and a value that is not text (a number, a list or "
                 "a nested object) is shown blank. When the input holds more than one export only the "
                 "first file found is read. Field mapping was done against a private sample; no sample "
                 "data is recorded for it.",
        "paths": ('*/logged_information/location/primary_location.json',),
        "output_types": "standard",
        "artifact_icon": "map-pin",
    },
    "facebookArchiveProfileInformation": {
        "name": "Facebook Archive - Profile Information",
        "description": "Profile information from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from personal_information/profile_information/profile_information.json, from the "
                 "profile_v2 object. Full Name, First Name, Middle Name, Last Name, Emails, Birthday, "
                 "Gender, Pronoun, Current City, Hometown and Relationship Status are the account "
                 "profile fields, reported as stored. Emails joins the addresses in the emails list of "
                 "the profile's emails object; any other list in that object is not read. Birthday is "
                 "the stored year, month and day. When the input holds more than one export only the "
                 "first file found is read. Field mapping was done against a private sample; no sample "
                 "data is recorded for it.",
        "paths": ('*/personal_information/profile_information/profile_information.json',),
        "output_types": "standard",
        "artifact_icon": "user",
    },
    "facebookArchiveDevices": {
        "name": "Facebook Archive - Devices",
        "description": "Devices from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from personal_information/profile_information/your_devices.json, one row per "
                 "entry. Details joins the entry's label_values pairs as label: value, reported as "
                 "stored, except that a timestamp_value is shown as a UTC date and time and a value "
                 "that is not text (a number, a list or a nested object) is shown blank after its "
                 "label; the labels are in the language of the export. When the input holds more than "
                 "one export only the first file found is read. Field mapping was done against a "
                 "private sample; no sample data is recorded for it.",
        "paths": ('*/personal_information/profile_information/your_devices.json',),
        "output_types": "standard",
        "artifact_icon": "device-mobile",
    },
    "facebookArchiveFriends": {
        "name": "Facebook Archive - Friends",
        "description": "Friends from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from connections/friends/your_friends.json, one row per entry in friends_v2. "
                 "Timestamp is Unix seconds; what event it marks is not established here. Name is the "
                 "friend's name as stored. When the input holds more than one export only the first "
                 "file found is read. Field mapping was done against a private sample; no sample data "
                 "is recorded for it.",
        "paths": ('*/connections/friends/your_friends.json',),
        "output_types": "standard",
        "artifact_icon": "users",
    },
    "facebookArchiveFriendRequests": {
        "name": "Facebook Archive - Friend Requests",
        "description": "Received and rejected friend requests from a Facebook DYI export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from connections/friends/received_friend_requests.json (received_requests_v2) and "
                 "connections/friends/rejected_friend_requests.json (rejected_requests_v2). Kind says "
                 "which file the row came from. Timestamp is Unix seconds. Name is stored as recorded. "
                 "Field mapping was done against a private sample; no sample data is recorded for it.",
        "paths": ('*/connections/friends/received_friend_requests.json',
                  '*/connections/friends/rejected_friend_requests.json'),
        "output_types": "standard",
        "artifact_icon": "user-plus",
    },
    "facebookArchiveComments": {
        "name": "Facebook Archive - Comments",
        "description": "Comments from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Codex",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-10-07",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from your_facebook_activity/comments_and_reactions/comments.json. Each truthy "
                 "comment object in an entry's data array gives one row, in stored array order; "
                 "repeated comment items are retained. An entry with no truthy comment object gives one "
                 "row with empty Comment and Author, preserving the existing entry fallback. Timestamp "
                 "uses the outer comments_v2 entry's timestamp as Unix seconds, not a separately read "
                 "comment timestamp; its event meaning is not established here. Comment, Author and "
                 "Title use the existing text repair, which leaves non-text values blank. Title is the "
                 "outer entry's own title. When the input holds more than one export only the first "
                 "file found is read. Field mapping was done against a private sample; no sample data "
                 "is recorded for it. Original parser and historical sample observations credited to "
                 "@AlexisBrignoni, Claude.",
        "paths": ('*/your_facebook_activity/comments_and_reactions/comments.json',),
        "output_types": "standard",
        "artifact_icon": "message-2",
    },
    "facebookArchiveReactions": {
        "name": "Facebook Archive - Likes and Reactions",
        "description": "Likes and reactions from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from your_facebook_activity/comments_and_reactions/likes_and_reactions.json, one "
                 "row per entry. Timestamp is Unix seconds. Details joins the entry's label_values "
                 "pairs as label: value, reported as stored, except that a timestamp_value is shown as "
                 "a UTC date and time and a value that is not text (a number, a list or a nested "
                 "object) is shown blank after its label; the labels are in the language of the export. "
                 "When the input holds more than one export only the first file found is read. Field "
                 "mapping was done against a private sample; no sample data is recorded for it.",
        "paths": ('*/your_facebook_activity/comments_and_reactions/likes_and_reactions.json',),
        "output_types": "standard",
        "artifact_icon": "thumb-up",
    },
    "facebookArchivePosts": {
        "name": "Facebook Archive - Posts",
        "description": "Post entries (title, text, place and external link) from the "
                       "your_posts__check_ins__photos_and_videos files of a Facebook DYI export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from "
                 "your_facebook_activity/posts/your_posts__check_ins__photos_and_videos_*.json, one row "
                 "per post entry. Timestamp is Unix seconds. Title and Post text are reported as "
                 "stored. Place and Coordinates are read from an entry's place attachment when present, "
                 "reported as stored. A place attached to a post is not shown to be where the post was "
                 "made. External URL is read from an external_context attachment when present. Field "
                 "mapping was done against a private sample; no sample data is recorded for it.",
        "paths": ('*/your_facebook_activity/posts/your_posts__check_ins__photos_and_videos_*.json',),
        "output_types": "standard",
        "artifact_icon": "note",
    },
    "facebookArchiveMessages": {
        "name": "Facebook Archive - Messages",
        "description": "Messenger threads from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read only from the files named message_1.json under your_facebook_activity/messages "
                 "in a Facebook Download Your Information (DYI) export; any further numbered message "
                 "file of a thread is not read. The read is not limited to particular folders under "
                 "messages. This is the DYI message shape (participants as name objects, title, and "
                 "messages with sender_name, timestamp_ms and content), which is distinct from the "
                 "camelCase Messenger export that the Facebook Messenger module reads. The Facebook and "
                 "Instagram DYI message trees have the same layout and are told apart by the "
                 "your_facebook_activity path, so this artifact reads only the Facebook side. Timestamp "
                 "is Unix milliseconds. Sender and message text are repaired from the export's "
                 "Latin-1-escaped UTF-8. Thread is the thread title where present, otherwise the thread "
                 "folder name. Participants lists the thread's members. Media renders the photos, "
                 "videos, gifs, audio, files and stickers a message carries, resolved from each item's "
                 "uri relative to the export root and checked in from disk. Reactions joins each "
                 "reaction with the actor who left it. Direction is not asserted because the export "
                 "does not mark which participant is the account owner. Field mapping was done against "
                 "a private sample; no sample data is recorded for it.",
        "paths": ('*/your_facebook_activity/messages/*',),
        "output_types": "standard",
        "artifact_icon": "brand-messenger",
        "html_columns": ['Media', 'Reactions'],
        "data_views": {
            "conversation": {
                "conversationDiscriminatorColumn": "Thread",
                "conversationLabelColumn": "Thread",
                "timeColumn": "Timestamp",
                "senderColumn": "Sender",
                "textColumn": "Message",
                "mediaColumn": "Media",
            }
        },
    },
    "facebookArchivePayments": {
        "name": "Facebook Archive - Payment History",
        "description": "Payment history from a Facebook Download Your Information export",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-22",
        "last_update_date": "2026-09-22",
        "requirements": "none",
        "category": "Facebook Archive",
        "notes": "Read from your_facebook_activity/facebook_payments/payment_history.json, one row per "
                 "payment in payments_v2.payments; when that list is empty one row is written holding "
                 "only Preferred Currency, which is not a payment. The fields of each payment are "
                 "joined as label: value; a value that is not text (a number, a list or a nested "
                 "object) is shown blank after its label. The payment record schema was not exercised "
                 "on the tested export, where the payment list was empty. Preferred Currency is the "
                 "account's stored currency. When the input holds more than one export only the first "
                 "file found is read. Field mapping was done against a private sample; no sample data "
                 "is recorded for it.",
        "paths": ('*/your_facebook_activity/facebook_payments/payment_history.json',),
        "output_types": "standard",
        "artifact_icon": "credit-card",
    },
}

import json
import os

from scripts.ilapfuncs import (artifact_processor, utf8_in_extended_ascii,
                               convert_unix_ts_to_utc, check_in_media)
from scripts.html_safe import esc

_MSG_MEDIA_KEYS = ('photos', 'videos', 'gifs', 'audio_files', 'files')


def _load(file_found):
    try:
        with open(file_found, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def _fix(value):
    """Repair Facebook DYI's Latin-1-escaped UTF-8 text, tolerant of non-strings."""
    if not isinstance(value, str) or not value:
        return value if isinstance(value, str) else ''
    try:
        return utf8_in_extended_ascii(value)[1]
    except (UnicodeDecodeError, UnicodeEncodeError, IndexError, TypeError):
        return value


def _ts(value):
    return convert_unix_ts_to_utc(value) if value else ''


def _pairs(label_values):
    """Join a DYI label_values list into 'label: value' text, mojibake-repaired."""
    out = []
    for item in label_values or []:
        label = _fix(item.get('label', ''))
        if 'value' in item:
            out.append(f"{label}: {_fix(item.get('value', ''))}")
        elif 'timestamp_value' in item:
            out.append(f"{label}: {_ts(item.get('timestamp_value'))}")
        elif 'dict' in item:
            inner = '; '.join(f"{_fix(d.get('label',''))}={_fix(d.get('value',''))}"
                              for d in item.get('dict') or [])
            out.append(f"{label}: {inner}")
        elif 'vec' in item:
            inner = ', '.join(_fix(d.get('value', '')) for d in item.get('vec') or [])
            out.append(f"{label}: {inner}")
    return '\n'.join(out)


def _first_file(context):
    for file_found in context.get_files_found():
        return str(file_found)
    return ''


@artifact_processor
def facebookArchiveAccountActivity(context):
    data_headers = (
        ('Timestamp', 'datetime'), 'Action', 'IP Address', 'City', 'Region', 'Country',
        'Site', 'User Agent', 'Datr Cookie', 'Port', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    for row in (loaded or {}).get('account_activity_v2', []):
        data_list.append((
            _ts(row.get('timestamp')), _fix(row.get('action', '')), row.get('ip_address', ''),
            _fix(row.get('city', '')), _fix(row.get('region', '')), _fix(row.get('country', '')),
            _fix(row.get('site_name', '')), _fix(row.get('user_agent', '')),
            row.get('datr_cookie', ''), row.get('port', ''),
            context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchiveLogins(context):
    data_headers = (('Timestamp', 'datetime'), 'Action', 'Site', 'IP Address', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    for row in (loaded or {}).get('account_accesses_v2', []):
        data_list.append((
            _ts(row.get('timestamp')), _fix(row.get('action', '')), _fix(row.get('site', '')),
            row.get('ip_address', ''), context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchiveIpActivity(context):
    data_headers = (('Timestamp', 'datetime'), 'IP', 'Action', 'User Agent', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    for row in (loaded or {}).get('used_ip_address_v2', []):
        data_list.append((
            _ts(row.get('timestamp')), row.get('ip', ''), _fix(row.get('action', '')),
            _fix(row.get('user_agent', '')), context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchiveActiveSessions(context):
    data_headers = (
        ('Created', 'datetime'), ('Updated', 'datetime'), 'IP Address', 'Device', 'Location',
        'App', 'Session Type', 'User Agent', 'Datr Cookie', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    for row in (loaded or {}).get('active_sessions_v2', []):
        data_list.append((
            _ts(row.get('created_timestamp')), _ts(row.get('updated_timestamp')),
            row.get('ip_address', ''), _fix(row.get('device', '')), _fix(row.get('location', '')),
            _fix(row.get('app', '')), _fix(row.get('session_type', '')),
            _fix(row.get('user_agent', '')), row.get('datr_cookie', ''),
            context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchiveAdminRecords(context):
    data_headers = (
        ('Session Created', 'datetime'), 'Event', 'Session IP', 'User Agent', 'Datr Cookie',
        'Change Details', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    for row in (loaded or {}).get('admin_records_v2', []):
        session = row.get('session') or {}
        extra = row.get('extra_info') or {}
        details = '\n'.join(f"{key}: {_fix(value)}" for key, value in extra.items() if value)
        data_list.append((
            _ts(session.get('created_timestamp')), _fix(row.get('event', '')),
            session.get('ip_address', ''), _fix(session.get('user_agent', '')),
            session.get('datr_cookie', ''), details, context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchiveRegistration(context):
    data_headers = (('Registered', 'datetime'), 'Label', 'Value', 'FBID', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    if isinstance(loaded, dict):
        registered = _ts(loaded.get('timestamp'))
        fbid = loaded.get('fbid', '')
        for item in loaded.get('label_values', []):
            data_list.append((
                registered, _fix(item.get('label', '')), _fix(item.get('value', '')),
                fbid, context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchiveSearches(context):
    data_headers = (('Timestamp', 'datetime'), 'Search', 'Title', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    for row in (loaded or {}).get('searches_v2', []):
        text = ' '.join(_fix(d.get('text', '')) for d in row.get('data') or [] if d.get('text'))
        data_list.append((
            _ts(row.get('timestamp')), text, _fix(row.get('title', '')),
            context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchiveProfileVisits(context):
    data_headers = (('Timestamp', 'datetime'), 'Details', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    entries = loaded if isinstance(loaded, list) else []
    for row in entries:
        data_list.append((
            _ts(row.get('timestamp')), _pairs(row.get('label_values')),
            context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchivePrimaryLocation(context):
    data_headers = ('Label', 'Value', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    if isinstance(loaded, dict):
        for item in loaded.get('label_values', []):
            label = _fix(item.get('label', ''))
            if 'value' in item:
                data_list.append((label, _fix(item.get('value', '')),
                                  context.get_relative_path(file_found)))
            for inner in item.get('dict') or []:
                data_list.append((f"{label} / {_fix(inner.get('label',''))}",
                                  _fix(inner.get('value', '')),
                                  context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchiveProfileInformation(context):
    data_headers = (
        'Full Name', 'First Name', 'Middle Name', 'Last Name', 'Emails', 'Birthday', 'Gender',
        'Pronoun', 'Current City', 'Hometown', 'Relationship Status', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    profile = (loaded or {}).get('profile_v2') if isinstance(loaded, dict) else None
    if profile:
        name = profile.get('name') or {}
        emails = '; '.join(profile.get('emails', {}).get('emails', []) or [])
        birthday = profile.get('birthday') or {}
        bday = ''
        if birthday.get('year') or birthday.get('month') or birthday.get('day'):
            bday = f"{birthday.get('year','')}-{birthday.get('month','')}-{birthday.get('day','')}"
        gender = profile.get('gender') or {}
        data_list.append((
            _fix(name.get('full_name', '')), _fix(name.get('first_name', '')),
            _fix(name.get('middle_name', '')), _fix(name.get('last_name', '')), emails, bday,
            _fix(gender.get('gender_option', '')), _fix(gender.get('pronoun', '')),
            _fix((profile.get('current_city') or {}).get('name', '')),
            _fix((profile.get('hometown') or {}).get('name', '')),
            _fix((profile.get('relationship') or {}).get('status', '')),
            context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchiveDevices(context):
    data_headers = ('Details', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    entries = loaded if isinstance(loaded, list) else []
    for row in entries:
        data_list.append((_pairs(row.get('label_values')), context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchiveFriends(context):
    data_headers = (('Timestamp', 'datetime'), 'Name', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    for row in (loaded or {}).get('friends_v2', []):
        data_list.append((
            _ts(row.get('timestamp')), _fix(row.get('name', '')),
            context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchiveFriendRequests(context):
    data_headers = (('Timestamp', 'datetime'), 'Kind', 'Name', 'Source File')
    data_list = []
    source_paths = []
    for file_found in context.get_files_found():
        file_found = str(file_found)
        name = os.path.basename(file_found.replace('\\', '/'))
        loaded = _load(file_found)
        if not isinstance(loaded, dict):
            continue
        if name.startswith('received'):
            kind, key = 'Received', 'received_requests_v2'
        else:
            kind, key = 'Rejected', 'rejected_requests_v2'
        rows = 0
        for row in loaded.get(key, []):
            data_list.append((
                _ts(row.get('timestamp')), kind, _fix(row.get('name', '')),
                context.get_relative_path(file_found)))
            rows += 1
        if rows:
            source_paths.append(file_found)
    return data_headers, data_list, '\n'.join(source_paths)


@artifact_processor
def facebookArchiveComments(context):
    data_headers = (('Timestamp', 'datetime'), 'Comment', 'Author', 'Title', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    for row in (loaded or {}).get('comments_v2', []):
        emitted = False
        for data in row.get('data') or []:
            comment = data.get('comment') or {}
            if comment:
                data_list.append((
                    _ts(row.get('timestamp')), _fix(comment.get('comment', '')),
                    _fix(comment.get('author', '')), _fix(row.get('title', '')),
                    context.get_relative_path(file_found)))
                emitted = True
        if not emitted:
            data_list.append((
                _ts(row.get('timestamp')), '', '', _fix(row.get('title', '')),
                context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchiveReactions(context):
    data_headers = (('Timestamp', 'datetime'), 'Details', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    entries = loaded if isinstance(loaded, list) else []
    for row in entries:
        data_list.append((
            _ts(row.get('timestamp')), _pairs(row.get('label_values')),
            context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


@artifact_processor
def facebookArchivePosts(context):
    data_headers = (
        ('Timestamp', 'datetime'), 'Title', 'Post', 'Place', 'Coordinates', 'External URL',
        'Source File')
    data_list = []
    source_paths = []
    for file_found in context.get_files_found():
        file_found = str(file_found)
        loaded = _load(file_found)
        entries = loaded if isinstance(loaded, list) else []
        rows = 0
        for row in entries:
            post_text = ''
            place = ''
            coords = ''
            url = ''
            for data in row.get('data') or []:
                if data.get('post'):
                    post_text = _fix(data.get('post', ''))
            for attach in row.get('attachments') or []:
                for data in attach.get('data') or []:
                    if data.get('place'):
                        placed = data['place']
                        place = _fix(placed.get('name', ''))
                        coord = placed.get('coordinate') or {}
                        if coord.get('latitude') is not None:
                            coords = f"{coord.get('latitude')}, {coord.get('longitude')}"
                    if data.get('external_context'):
                        url = data['external_context'].get('url', '')
            data_list.append((
                _ts(row.get('timestamp')), _fix(row.get('title', '')), post_text, place, coords,
                url, context.get_relative_path(file_found)))
            rows += 1
        if rows:
            source_paths.append(file_found)
    return data_headers, data_list, '\n'.join(source_paths)


@artifact_processor
def facebookArchivePayments(context):
    data_headers = ('Preferred Currency', 'Payment Details', 'Source File')
    data_list = []
    file_found = _first_file(context)
    loaded = _load(file_found) if file_found else None
    payments = (loaded or {}).get('payments_v2') if isinstance(loaded, dict) else None
    if payments:
        currency = _fix(payments.get('preferred_currency', ''))
        rows = payments.get('payments') or []
        if rows:
            for row in rows:
                details = '\n'.join(f"{key}: {_fix(value)}" for key, value in row.items())
                data_list.append((currency, details, context.get_relative_path(file_found)))
        else:
            data_list.append((currency, '', context.get_relative_path(file_found)))
    return data_headers, data_list, file_found


def _thread_media(message, export_root):
    """Resolve a DYI message's media items to on-disk paths and check them in.

    Returns a list of checked-in media references, which the report renders as a
    media column without interpolating anything unescaped into markup.
    """
    refs = []
    items = []
    for key in _MSG_MEDIA_KEYS:
        for item in message.get(key) or []:
            if isinstance(item, dict) and item.get('uri'):
                items.append(item['uri'])
    sticker = message.get('sticker')
    if isinstance(sticker, dict) and sticker.get('uri'):
        items.append(sticker['uri'])
    for uri in items:
        media_path = os.path.join(export_root, uri.replace('/', os.sep))
        if os.path.exists(media_path):
            ref = check_in_media(media_path, os.path.basename(media_path))
            if ref:
                refs.append(ref)
    return refs


def _reactions(message):
    out = []
    for reaction in message.get('reactions') or []:
        if isinstance(reaction, dict):
            out.append(f"{esc(_fix(reaction.get('actor', '')))}: "
                       f"{esc(_fix(reaction.get('reaction', '')))}")
    return '<br>'.join(out)


@artifact_processor
def facebookArchiveMessages(context):
    data_headers = (
        ('Timestamp', 'datetime'), 'Sender', 'Thread', 'Message', ('Media', 'media'),
        'Participants', 'Reactions', 'Source File')
    data_list = []
    source_paths = []
    for file_found in context.get_files_found():
        file_found = str(file_found)
        normalized = file_found.replace('\\', '/')
        if os.path.basename(normalized) != 'message_1.json':
            continue
        marker = '/your_facebook_activity/'
        if marker not in normalized:
            continue
        loaded = _load(file_found)
        if not isinstance(loaded, dict):
            continue
        messages = loaded.get('messages')
        if not isinstance(messages, list):
            continue
        export_root = file_found[:file_found.replace('\\', '/').index(marker)]
        participants = ', '.join(
            _fix(p.get('name', '')) for p in loaded.get('participants') or []
            if isinstance(p, dict))
        thread = _fix(loaded.get('title', '')) or os.path.basename(os.path.dirname(normalized))
        rows = 0
        for message in messages:
            timestamp = message.get('timestamp_ms')
            data_list.append((
                convert_unix_ts_to_utc(timestamp / 1000) if timestamp else '',
                _fix(message.get('sender_name', '')), thread, _fix(message.get('content', '')),
                _thread_media(message, export_root), participants, _reactions(message),
                context.get_relative_path(file_found)))
            rows += 1
        if rows:
            source_paths.append(file_found)
    return data_headers, data_list, '\n'.join(source_paths)
