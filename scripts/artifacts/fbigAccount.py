__artifacts_v2__ = {
    "fbigAccountInfo": {
        "name": "Facebook Instagram Returns - Account and Report Information",
        "description": "Request parameters and account profile fields from a Meta (Instagram) law enforcement return, one Key/Value row per field and snapshot file.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2023-07-01",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "Reads records.html and every preservation_N.html in the return (the Meta business-records archive format, div.t.o/div.t.i/div.m/div.p blocks; see scripts/meta_records.py). "
                 "Each snapshot file is reported separately, named in the Snapshot File column, because a preservation is a separate capture with its own Generated time and its own contents. "
                 "Sections carried: request parameters (Service, Internal Ticket Number, Target, Account Identifier, Account Type, Generated, Date Range), Name, Registered Email Addresses, Vanity Name, Registration Date, Registration IP, Account Closure Date, Account Read Receipts, Phone Numbers, Privacy Settings, Popular Block, Gender, Date Of Birth, Website, About Me, Linked Accounts, Threads Registration Date and Profile Picture. "
                 "Values are reported as stored, including the provider's 'No responsive records' placeholder, so a checked-and-empty field is visible. "
                 "The provider's own field definitions are embedded in the return beside each section; per those definitions the request parameter Target is the account's numeric identifier and Vanity is the username. "
                 "On the return this was built against (one Instagram account, three snapshot files) the messages whose Author id equalled Target were exactly the messages whose Author username equalled the Vanity Name, in all three snapshots, while Account Identifier held a non-numeric value on two of the three files; Target is therefore the field the message artifacts use to tell the account's own messages from everyone else's. "
                 "Timestamps in this table are kept as text because the Value column is heterogeneous; the provider prints them as 'YYYY-MM-DD HH:MM:SS UTC'.",
        "paths": ('*/records.html', '*/preservation*.html', '*/linked_media/*'),
        "output_types": "standard",
        "artifact_icon": "info-circle",
    },
    "fbigAccountChanges": {
        "name": "Facebook Instagram Returns - Account Changes",
        "description": "Name, email, username, phone number, password and account status changes from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-19",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per change record in the Name Changes, Email Changes, Vanity Changes, Phone Number Changes, Password Changes and Account Status History sections, from records.html and every preservation_N.html. "
                 "Change Type names the section. Old Value and New Value are taken from the record's 'Old ...' and 'New ...' fields; a section whose record carries a single value (Email, Status) reports it as New Value; every other field of the record goes to Details as 'label: value'. "
                 "Only Vanity Changes carried a record on the return this was built against, so the other five sections are handled from the provider's embedded field definitions and are unexercised. "
                 "A time that does not parse as 'YYYY-MM-DD HH:MM:SS UTC' is left blank in the Time column and kept in Details. The final column holds the provider's own flag for the change as stored (one value on the tested return's rows).",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "edit",
    },
    "fbigIpaddresses": {
        "name": "Facebook Instagram Returns - Account IP Addresses",
        "description": "IP address activity records (time, address with source port, action) from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2024-08-07",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per record of the Ip Addresses section of records.html and every preservation_N.html; Snapshot File names the file. "
                 "IP Address is reported as stored: per the provider's embedded definition the source port, when available, follows the address after a colon, and IPv6 addresses are printed in brackets. "
                 "Action is the provider's own event name as stored (four distinct values on the tested return: v1_profile_changed, media_upload, v1_user_block and v1_logout); no meaning beyond the name is asserted. "
                 "Records split across the return's page breaks are rejoined before reporting: on the return this was built against, the page break fell inside the Time field of a record on six occasions in one file, and the row count equalled the number of 'IP Address' labels in the source text.",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "globe",
    },
    "fbigDevices": {
        "name": "Facebook Instagram Returns - Devices",
        "description": "Device identifiers and the accounts seen on them, from the Devices section of a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per record of the Devices section of records.html and every preservation_N.html. "
                 "Per the provider's embedded definition: Type is the model number of the device, Id an identifier associated with the device, Active whether Instagram was accessed by the device, and User the Instagram accounts seen on the device ID. "
                 "A record can carry several User fields; they are joined one per line. On the return this was built against Type was the word 'UUID' on every record, Id an identifier reported as stored, and Users was filled on a minority of records (5 of 28, 3 of 26 and 5 of 28 across the three snapshots). "
                 "The richer per-device history (family device id, first and last seen, OS, associated users) is in the Devices Info artifact.",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "device-mobile",
    },
    "fbigDevicesInfo": {
        "name": "Facebook Instagram Returns - Devices Info",
        "description": "Per-device records (family device id, first and last seen, OS, identifiers, associated accounts) from the Devices Info section of a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-19",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per Device block of the Devices Info section of records.html and every preservation_N.html. "
                 "The provider prints a device's fields in groups separated by spacers (two groups per device on every Device block of the tested return); all groups of one Device block are merged into the one row. "
                 "Column names are the provider's field labels. Per its embedded definition, Family Device Id is the identifier shared by all Meta apps on the same physical device, Family Device First Seen and Last Seen are when that identifier was first and last seen, App Scoped Device IDs are app-specific device identifiers, and Associated Users are the Instagram accounts associated with the device. "
                 "App Scoped Device IDs, Family ID History and Push Tokens are lists and are joined one entry per line; Associated Users is reported as stored. Fields the definition lists but the tested return did not carry (Hardware ID, the connection fields, Reactivated Users) would land in Other Fields as 'label: value'; Push Tokens, carried by two snapshots of the tested return and absent from the definition, is reported as stored. "
                 "Blocked Status, Is Tablet and Active are reported as stored.",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "devices",
    },
    "fbigEncryptedConnectionInfo": {
        "name": "Facebook Instagram Returns - Encrypted Connection Info",
        "description": "Devices recorded for end-to-end encrypted features, from the Encrypted Connection Info section of a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-19",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per record of the Encrypted Connection Info section of records.html and every preservation_N.html. "
                 "Per the provider's embedded definition this section describes the device the account holder used to access end-to-end encrypted features, and can also reflect opening the app from a non-running state, receiving push notifications, or sharing through the iOS share sheet or Android chat bubble. "
                 "The return this was built against carried Device Type, Device Manufacturer, Device Model and Device Os Version; the definition also lists Current Connected IP, Current Connected Port, Device OS Build Number, Last Active Time, Last Connected IP and Online Since, which are reported in Other Fields as 'label: value' when present and are unexercised.",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "lock",
    },
    "fbigPrivacyBlocks": {
        "name": "Facebook Instagram Returns - Privacy Blocks",
        "description": "Block relationships (blocker and blocked account) from the Privacy Blocks section of a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-19",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per record of the Privacy Blocks section of records.html and every preservation_N.html. "
                 "Per the provider's embedded definition the section lists any account that has blocked the account holder, with Blocker the account holder who blocked and Blocked the account holder who was blocked. "
                 "Both are reported as stored ('username [display name] (numeric id)' on the tested return) with the username and numeric id also split into their own columns. No time is recorded in this section. On the tested return the Blocked account was the same account on every row, consistent with the definition (accounts that have blocked the account holder).",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "ban",
    },
}

from scripts.ilapfuncs import artifact_processor, logfunc
from scripts import meta_records as mr

TIME_LABELS = ('Time', 'Timestamp', 'Date', 'Date Created')


def _sources(context):
    return mr.records_files(context.get_files_found())


def _adder(data_list, snapshot):
    def add(key, value, media=None):
        data_list.append((key, value, media, snapshot))
    return add


def _time_and_rest(record):
    """(datetime, raw time text, remaining fields) for a change-style record."""
    for label in TIME_LABELS:
        raw = mr.text(record, label)
        if raw:
            rest = [f for f in record if f.label != label]
            return mr.parse_ts(raw), raw, rest
    return '', '', list(record)


@artifact_processor
def fbigAccountInfo(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        add = _adder(data_list, rec.name)

        for item in rec.fields('request_parameters'):
            if isinstance(item.value, str):
                add(item.label, item.value)
        for record in rec.records('name'):
            for item in record:
                if isinstance(item.value, str):
                    add(f'Name ({item.label})', item.value)
        if not rec.records('name') and rec.has('name'):
            add('Name', rec.text('name'))
        for line in mr.lines(rec.text('emails')) or [rec.text('emails')]:
            add('Registered Email Address', line)
        add('Vanity Name', rec.text('vanity'))
        add('Registration Date', rec.text('registration_date'))
        add('Registration IP', rec.text('registration_ip'))
        closure = rec.records('account_end_date')
        for record in closure:
            for item in record:
                if isinstance(item.value, str):
                    add(f'Account Closure Date: {item.label}', item.value)
        if not closure and rec.has('account_end_date'):
            add('Account Closure Date', rec.text('account_end_date'))
        add('Account Read Receipts', rec.text('account_read_receipts'))
        for line in mr.lines(rec.text('phone_numbers')) or [rec.text('phone_numbers')]:
            add('Phone Number', line)
        settings = rec.records('privacy_settings')
        for record in settings:
            add(f"Privacy Setting: {mr.text(record, 'Name')}", mr.text(record, 'Value'))
        if not settings and rec.has('privacy_settings'):
            add('Privacy Settings', rec.text('privacy_settings'))
        blocks = rec.records('popular_block')
        for record in blocks:
            add('Popular Block (Explore page)', mr.text(record, 'Blocked'))
        if not blocks and rec.has('popular_block'):
            add('Popular Block (Explore page)', rec.text('popular_block'))
        add('Gender', rec.text('gender'))
        add('Date Of Birth', rec.text('date_of_birth'))
        add('Website', rec.text('website'))
        add('About Me', rec.text('about_me'))
        linked = rec.records('linked_accounts')
        for record in linked:
            add('Linked Account', ' | '.join(f'{f.label}: {f.value}' for f in record if isinstance(f.value, str)))
        if not linked and rec.has('linked_accounts'):
            add('Linked Account', rec.text('linked_accounts'))
        if rec.has('threads_registration_date'):
            add('Threads Registration Date', rec.text('threads_registration_date'))
        pictures = mr.linked_media_files(rec.records('profile_picture')[0]) if rec.records('profile_picture') else []
        for name in pictures:
            add('Profile Picture', name, mr.register_media(context, [name]) or None)
        if not pictures and rec.has('profile_picture'):
            add('Profile Picture', rec.text('profile_picture'))
    data_headers = ('Key', 'Value', ('Media', 'media'), 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


CHANGE_SECTIONS = (
    ('name_changes', 'Name Change'),
    ('email_changes', 'Email Change'),
    ('vanity_changes', 'Vanity (Username) Change'),
    ('phone_number_changes', 'Phone Number Change'),
    ('password_changes', 'Password Change'),
    ('account_status_history', 'Account Status Change'),
)


@artifact_processor
def fbigAccountChanges(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for section, change_type in CHANGE_SECTIONS:
            for record in rec.records(section):
                when, raw, rest = _time_and_rest(record)
                old = new = user_initiated = ''
                details = []
                for item in rest:
                    if not isinstance(item.value, str):
                        details.extend(mr.flatten([item]))
                    elif item.label.startswith('Old'):
                        old = item.value
                    elif item.label.startswith('New') or item.label in ('Email', 'Status'):
                        new = item.value
                    elif item.label == 'User Initiated':
                        user_initiated = item.value
                    else:
                        details.append(f'{item.label}: {item.value}')
                if raw and not when:
                    details.append(f'Time (as stored): {raw}')
                data_list.append((when, change_type, old, new, '\n'.join(details), user_initiated, rec.name))
    data_headers = (('Time', 'datetime'), 'Change Type', 'Old Value', 'New Value', 'Details',
                    'User Initiated', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def fbigIpaddresses(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for record in rec.records('ip_addresses'):
            data_list.append((mr.parse_ts(mr.text(record, 'Time')), mr.text(record, 'IP Address'),
                              mr.text(record, 'Action'), rec.name))
    data_headers = (('Time', 'datetime'), 'IP Address', 'Action', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def fbigDevices(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for record in rec.records('devices'):
            users = '\n'.join(mr.texts(record, 'User'))
            data_list.append((mr.text(record, 'Type'), mr.text(record, 'Id'), mr.text(record, 'Active'),
                              users, rec.name))
    data_headers = ('Type', 'Id', 'Active', 'Users', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


DEVICE_INFO_COLUMNS = ('Family Device Id', 'Device Type', 'Manufacturer', 'Os Type', 'Os Version',
                       'Is Tablet', 'Active', 'Blocked Status', 'Android Id', 'Advertiser Id',
                       'Hardware Id', 'User Agent', 'Associated Users')
DEVICE_INFO_LISTS = ('App Scoped Device IDs', 'Family ID History', 'Push Tokens')


def _merge_block(block):
    """Every field of a multi-group block as one ordered list."""
    merged = []
    for record in block:
        merged.extend(record)
    return merged


@artifact_processor
def fbigDevicesInfo(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for record in rec.records('devices_info'):
            for device in mr.subs(record, 'Device'):
                fields = _merge_block(device.value)
                row = {}
                lists = {name: [] for name in DEVICE_INFO_LISTS}
                other = []
                for item in fields:
                    if item.label in DEVICE_INFO_LISTS:
                        if isinstance(item.value, list):
                            lists[item.label].extend(' | '.join(mr.flatten(sub)) for sub in item.value)
                        else:
                            lists[item.label].extend(mr.lines(item.value))
                    elif item.label in ('Family Device First Seen', 'Family Device Last Seen'):
                        row[item.label] = item.value if isinstance(item.value, str) else ''
                    elif item.label in DEVICE_INFO_COLUMNS and isinstance(item.value, str):
                        row[item.label] = item.value
                    else:
                        other.extend(mr.flatten([item]))
                first_seen = mr.parse_ts(row.get('Family Device First Seen', ''))
                last_seen = mr.parse_ts(row.get('Family Device Last Seen', ''))
                data_list.append((first_seen, last_seen) + tuple(row.get(c, '') for c in DEVICE_INFO_COLUMNS)
                                 + tuple('\n'.join(lists[name]) for name in DEVICE_INFO_LISTS)
                                 + ('\n'.join(other), rec.name))
    data_headers = (('Family Device First Seen', 'datetime'), ('Family Device Last Seen', 'datetime')) \
        + DEVICE_INFO_COLUMNS + DEVICE_INFO_LISTS + ('Other Fields', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


ECI_COLUMNS = ('Device Type', 'Device Manufacturer', 'Device Model', 'Device Os Version')


@artifact_processor
def fbigEncryptedConnectionInfo(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for record in rec.records('encrypted_connection_info'):
            row = {item.label: item.value for item in record if isinstance(item.value, str)}
            other = [f'{item.label}: {item.value}' for item in record
                     if isinstance(item.value, str) and item.label not in ECI_COLUMNS]
            other.extend(mr.flatten([item for item in record if not isinstance(item.value, str)]))
            data_list.append(tuple(row.get(c, '') for c in ECI_COLUMNS) + ('\n'.join(other), rec.name))
    data_headers = ECI_COLUMNS + ('Other Fields', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def fbigPrivacyBlocks(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for record in rec.records('privacy_blocks'):
            blocker, blocked = mr.text(record, 'Blocker'), mr.text(record, 'Blocked')
            blocker_user, blocker_id, _ = mr.parse_account(blocker)
            blocked_user, blocked_id, _ = mr.parse_account(blocked)
            data_list.append((blocker, blocker_user, blocker_id, blocked, blocked_user, blocked_id, rec.name))
    if not data_list:
        logfunc('Privacy Blocks: no block records in the return files read')
    data_headers = ('Blocker', 'Blocker Username', 'Blocker Instagram ID', 'Blocked', 'Blocked Username',
                    'Blocked Instagram ID', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)
