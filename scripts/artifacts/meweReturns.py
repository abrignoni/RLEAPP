__artifacts_v2__ = {
    "meweContacts": {
        "name": "MeWe Contacts",
        "description": "This parses the Contacts list from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "creation_date": "2024-05-13",
        "last_update_date": "2024-05-13",
        "requirements": "none",
        "category": "MeWe",
        "notes": "",
        "paths": ('**/mewe-content/contacts.txt',),
        "output_types": "standard",
        "artifact_icon": "users",
    },
    "meweDevices": {
        "name": "MeWe Devices",
        "description": "This parses the Device list from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "creation_date": "2024-05-13",
        "last_update_date": "2024-05-13",
        "requirements": "none",
        "category": "MeWe",
        "notes": "",
        "paths": ('**/mewe-content/devices.txt',),
        "output_types": "standard",
        "artifact_icon": "devices",
    },
    "meweEmails": {
        "name": "MeWe Email Accounts",
        "description": "This parses the Email account list from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "creation_date": "2024-05-13",
        "last_update_date": "2024-05-13",
        "requirements": "none",
        "category": "MeWe",
        "notes": "",
        "paths": ('**/mewe-content/emails.txt',),
        "output_types": "standard",
        "artifact_icon": "mail",
    },
    "meweGroupmemberships": {
        "name": "MeWe Group Memberships",
        "description": "This parses the Group Membership list from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "creation_date": "2024-05-13",
        "last_update_date": "2024-05-13",
        "requirements": "none",
        "category": "MeWe",
        "notes": "",
        "paths": ('**/mewe-content/group-memberships.txt',),
        "output_types": "standard",
        "artifact_icon": "users-group",
    },
    "meweProfile": {
        "name": "MeWe Profile",
        "description": "This parses the User Profile from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "creation_date": "2024-05-15",
        "last_update_date": "2024-05-15",
        "requirements": "none",
        "category": "MeWe",
        "notes": "",
        "paths": ('**/mewe-content/profile.txt', '**/mewe-content/photos/*.jpg'),
        "output_types": "standard",
        "artifact_icon": "user",
    },
    "meweGroupChat": {
        "name": "MeWe Group Chat",
        "description": "This parses the Group Chat Posts from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "creation_date": "2024-05-15",
        "last_update_date": "2024-05-15",
        "requirements": "none",
        "category": "MeWe",
        "notes": "",
        "paths": ('**/mewe-content/groupChat.txt', '**/mewe-content/photos/*.jpg'),
        "output_types": "standard",
        "artifact_icon": "message",
    },
    "mewePosts": {
        "name": "MeWe Posts",
        "description": "This parses the Posts from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "creation_date": "2024-05-15",
        "last_update_date": "2024-05-15",
        "requirements": "none",
        "category": "MeWe",
        "notes": "",
        "paths": ('**/mewe-content/posts.txt', '**/mewe-content/photos/*.jpg'),
        "output_types": "standard",
        "artifact_icon": "note",
    },
    "meweUserChat": {
        "name": "MeWe Chat Posts",
        "description": "This parses the User Chat Posts from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "creation_date": "2024-05-16",
        "last_update_date": "2024-05-16",
        "requirements": "none",
        "category": "MeWe",
        "notes": "",
        "paths": ('**/mewe-content/userChat.txt', '**/mewe-content/photos/*.jpg', '**/mewe-content/documents/**'),
        "output_types": "standard",
        "artifact_icon": "message-2",
    },
    "meweLoginStats": {
        "name": "MeWe Login Stats",
        "description": "This parses the User Login Stats from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "creation_date": "2024-05-16",
        "last_update_date": "2024-05-16",
        "requirements": "none",
        "category": "MeWe",
        "notes": "",
        "paths": ('**/mewe-content/logins/stats.txt',),
        "output_types": "standard",
        "artifact_icon": "login",
    },
    "meweLoginLogs": {
        "name": "MeWe Login Logs",
        "description": "This parses the User Login Logs from a MeWe warrant return.",
        "author": "Troy Schnack (@TheBaldJedi)",
        "creation_date": "2024-05-16",
        "last_update_date": "2024-05-16",
        "requirements": "none",
        "category": "MeWe",
        "notes": "",
        "paths": ('**/mewe-content/logins/logs.txt',),
        "output_types": "standard",
        "artifact_icon": "login",
    },
}

import csv
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, check_in_media


def _kv(field):
    '''Return the value from a "key: value" field. Uses a single split so
    values that themselves contain ": " (timestamps, IPv6, URLs) are kept
    whole -- the original lstrip()/split(': ') logic truncated those.'''
    field = str(field)
    if ': ' in field:
        return field.split(': ', 1)[1].strip()
    return field.strip()


def _mewe_ts(value):
    '''Parse a MeWe ISO-8601 timestamp to an aware UTC datetime.
    Naive values are assumed UTC (warrant-return convention); unparseable
    values are kept verbatim.'''
    if not value:
        return ''
    try:
        dt = datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return value
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


@artifact_processor
def meweLoginLogs(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.txt'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', mode='r', errors='backslashreplace') as f:
            for item in csv.reader(f, delimiter=','):
                if len(item) < 2:
                    continue
                data_list.append((_mewe_ts(_kv(item[0])), _kv(item[1])))

    data_headers = (('Login Date', 'datetime'), 'IP Address')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def meweLoginStats(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.txt'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', mode='r', errors='backslashreplace') as f:
            for item in csv.reader(f, delimiter=','):
                if len(item) < 2:
                    continue
                data_list.append((_kv(item[0]), _kv(item[1])))

    data_headers = ('IP Address', 'Total Logins From IP')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def meweUserChat(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.txt'):
            continue
        source_path = file_found
        date_created = chat_text = sender_id = thread_id = chat_type = recipient_id = document_id = image_id = ''
        media_refs = []
        with open(file_found, encoding='utf-8', mode='r', errors='backslashreplace') as f:
            for line in f:
                if 'date_created:' in line:
                    date_created = _mewe_ts(_kv(line))
                elif 'text:' in line:
                    chat_text = _kv(line)
                elif 'sender_id:' in line:
                    sender_id = _kv(line)
                elif 'threadId:' in line:
                    thread_id = _kv(line)
                elif 'chatThreadType:' in line:
                    chat_type = _kv(line)
                elif 'recipientUsersId' in line:
                    recipient_id = _kv(line)
                elif 'document_id:' in line:
                    document_id = _kv(line)
                    ref = check_in_media(document_id, document_id)
                    if ref:
                        media_refs.append(ref)
                elif 'image_id:' in line:
                    image_id = _kv(line)
                    ref = check_in_media(image_id, image_id)
                    if ref:
                        media_refs.append(ref)
                elif '---------------' in line:
                    data_list.append((date_created, chat_text, sender_id, thread_id, chat_type,
                                      recipient_id, document_id, image_id, media_refs))
                    date_created = chat_text = sender_id = thread_id = chat_type = recipient_id = document_id = image_id = ''
                    media_refs = []

    data_headers = (('Created Date', 'datetime'), 'Text', 'Sender ID', 'Thread ID', 'Chat Type',
                    'Recipient ID', 'Attached Filename', 'Photo Filename', ('Media', 'media'))
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def mewePosts(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.txt'):
            continue
        source_path = file_found
        date_created = chat_text = image_id = ''
        media_ref = ''
        with open(file_found, encoding='utf-8', mode='r', errors='backslashreplace') as f:
            for line in f:
                if 'date_created:' in line:
                    date_created = _mewe_ts(_kv(line))
                elif 'text:' in line:
                    chat_text = _kv(line)
                elif 'image_id:' in line:
                    image_id = _kv(line)
                    media_ref = check_in_media(image_id, image_id)
                elif '---------------' in line:
                    data_list.append((date_created, chat_text, image_id, media_ref))
                    date_created = chat_text = image_id = ''
                    media_ref = ''

    data_headers = (('Created Date', 'datetime'), 'Text', 'Image ID', ('Media', 'media'))
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def meweGroupChat(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.txt'):
            continue
        source_path = file_found
        date_created = chat_text = sender_id = thread_id = chat_type = image_id = ''
        media_ref = ''
        with open(file_found, encoding='utf-8', mode='r', errors='backslashreplace') as f:
            for line in f:
                if 'date_created' in line:
                    date_created = _mewe_ts(_kv(line))
                elif 'text:' in line:
                    chat_text = _kv(line)
                elif 'sender_id:' in line:
                    sender_id = _kv(line)
                elif 'threadId' in line:
                    thread_id = _kv(line)
                elif 'chatThreadType' in line:
                    chat_type = _kv(line)
                elif 'image_id:' in line:
                    image_id = _kv(line)
                    media_ref = check_in_media(image_id, image_id)
                elif '---------------' in line:
                    data_list.append((date_created, chat_text, sender_id, thread_id, chat_type, image_id, media_ref))
                    date_created = chat_text = sender_id = thread_id = chat_type = image_id = ''
                    media_ref = ''

    data_headers = (('Created Date', 'datetime'), 'Text', 'Sender ID', 'Thread ID', 'Chat Type',
                    'Image ID', ('Media', 'media'))
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def meweProfile(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.txt'):
            continue
        source_path = file_found
        userid = first_name = last_name = email = time_zone = profile_text = is_banned = url_page = cover_image = profile_image = ''
        date_registered = last_seen = ''
        cover_ref = profile_ref = ''
        with open(file_found, encoding='utf-8', mode='r', errors='backslashreplace') as f:
            for line in f:
                if 'user_id:' in line:
                    userid = _kv(line)
                elif 'date_registered:' in line:
                    date_registered = _mewe_ts(_kv(line))
                elif 'first_name' in line:
                    first_name = _kv(line)
                elif 'last_name' in line:
                    last_name = _kv(line)
                elif 'email' in line:
                    email = _kv(line)
                elif 'last_seen_login' in line:
                    last_seen = _mewe_ts(_kv(line))
                elif 'registration_time_zone' in line:
                    time_zone = _kv(line)
                elif 'profile_text' in line:
                    profile_text = _kv(line)
                elif 'is_banned' in line:
                    is_banned = _kv(line)
                elif 'url' in line:
                    url_page = _kv(line)
                elif 'cover_image' in line:
                    cover_image = _kv(line)
                    cover_ref = check_in_media(cover_image, cover_image)
                elif 'profile_image' in line:
                    profile_image = _kv(line)
                    profile_ref = check_in_media(profile_image, profile_image)
                elif '---------------' in line:
                    data_list.append((userid, date_registered, first_name, last_name, email, last_seen,
                                      time_zone, profile_text, is_banned, url_page, cover_image, cover_ref,
                                      profile_image, profile_ref))
                    userid = first_name = last_name = email = time_zone = profile_text = is_banned = url_page = cover_image = profile_image = ''
                    date_registered = last_seen = ''
                    cover_ref = profile_ref = ''

    data_headers = ('User ID', ('Date Registered', 'datetime'), 'First Name', 'Last Name', 'Email',
                    ('Last Seen', 'datetime'), 'Registration TimeZone', 'Profile Text', 'Is Banned',
                    'MeWe URL', 'Cover Filename', ('Cover Media', 'media'), 'Profile Filename',
                    ('Profile Media', 'media'))
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def meweGroupmemberships(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.txt'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', mode='r', errors='backslashreplace') as f:
            for item in csv.reader(f, delimiter=','):
                if len(item) < 2:
                    continue
                data_list.append((_kv(item[0]), _kv(item[1])))

    data_headers = ('Group ID', 'Group Name')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def meweEmails(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.txt'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', mode='r', errors='backslashreplace') as f:
            for item in csv.reader(f):
                if len(item) < 2:
                    continue
                data_list.append((_mewe_ts(_kv(item[1])), _kv(item[0])))

    data_headers = (('Created Date', 'datetime'), 'Email Account')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def meweDevices(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.txt'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', mode='r', errors='backslashreplace') as f:
            for item in csv.reader(f):
                if len(item) < 4:
                    continue
                device_id = _kv(item[0])
                vendor_device_id = _kv(item[1])
                device_type = _kv(item[2])
                timestamp = _mewe_ts(_kv(item[3]))
                data_list.append((device_type, timestamp, device_id, vendor_device_id))

    data_headers = ('Device Type', ('Created Timestamp', 'datetime'), 'Device ID', 'Vendor Device ID')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def meweContacts(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.txt'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', mode='r', errors='backslashreplace') as f:
            for item in csv.reader(f, delimiter=','):
                if len(item) < 2:
                    continue
                data_list.append((_kv(item[0]), _kv(item[1])))

    data_headers = ('User ID', 'Username')
    return data_headers, data_list, context.get_relative_path(source_path)
