__artifacts_v2__ = {
    "fbigFollowers": {
        "name": "Facebook Instagram Returns - Followers",
        "description": "Accounts following the account holder, with the time each follow started, from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per record of the Followers section of records.html and every preservation_N.html; Snapshot File names the file. "
                 "Per the provider's embedded definition the section lists all the accounts following the account holder at the time of production, and Time is when an account started following the account holder. "
                 "Follower is reported as stored, 'username (Instagram: numeric id) [display name]' on the tested return, and its three parts are also split into their own columns; Display Name is blank when the stored value carries no bracketed part. "
                 "Each snapshot file is a separate capture and can list a different set of followers: on the return this was built against, one snapshot listed 92 followers and the other two listed 3.",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "users",
    },
    "fbigFollowing": {
        "name": "Facebook Instagram Returns - Following",
        "description": "Accounts listed in the Following section, with the time each follow started, from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per record of the Following section of records.html and every preservation_N.html; Snapshot File names the file. "
                 "Per the provider's embedded definition the section lists all the accounts the account holder is following at the time of production, and Time is when the account holder started following an account. "
                 "Following is reported as stored, 'username (Instagram: numeric id) [display name]' on the tested return, and its three parts are also split into their own columns. "
                 "Records split across the return's page breaks are rejoined before reporting; on the tested return the row count of each file equalled the number of 'Following' field labels inside the section's list (the section heading carries the same label and is not a record).",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "user-check",
    },
    "fbigIncoFollow": {
        "name": "Facebook Instagram Returns - Incoming Follow Requests",
        "description": "Accounts awaiting approval to follow the account holder, from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per entry of the Incoming Follow Requests section of records.html and every preservation_N.html; Snapshot File names the file. "
                 "Per the provider's embedded definition the section lists the accounts awaiting approval to follow the account holder. The section carries no time. "
                 "Requester is reported as stored, 'username (Instagram: numeric id) [display name]' on the tested return, and its three parts are also split into their own columns.",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "user-plus",
    },
    "fbigSearches": {
        "name": "Facebook Instagram Returns - Searches",
        "description": "Search records from the Searches section of a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2023-06-30",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per record of the Searches section of records.html and every preservation_N.html. "
                 "Per the provider's embedded definition the section returns a list of accounts, tags, or places searched for from the account, Timestamp is the most recent time the item was searched for and clicked on, and Type is the type of search conducted. "
                 "The section held no records on the return this was built against, so the field layout is taken from that definition and is unexercised: Time is read from a Time or Timestamp field, Type from a Type field, and every other field of the record lands in Details as 'label: value'.",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "search",
    },
}

from scripts.ilapfuncs import artifact_processor
from scripts import meta_records as mr


def _account_rows(context, section, label):
    data_list = []
    sources = mr.records_files(context.get_files_found())
    for path in sources:
        rec = mr.load(path)
        for record in rec.records(section):
            stored = mr.text(record, label)
            username, ig_id, display = mr.parse_account(stored)
            data_list.append((mr.parse_ts(mr.text(record, 'Time')), stored, username, ig_id, display, rec.name))
    return data_list, sources


@artifact_processor
def fbigFollowers(context):
    data_list, sources = _account_rows(context, 'followers', 'Follower')
    data_headers = (('Time', 'datetime'), 'Follower', 'Follower Username', 'Follower Instagram ID',
                    'Follower Display Name', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def fbigFollowing(context):
    data_list, sources = _account_rows(context, 'following', 'Following')
    data_headers = (('Time', 'datetime'), 'Following', 'Following Username', 'Following Instagram ID',
                    'Following Display Name', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def fbigIncoFollow(context):
    data_list = []
    sources = mr.records_files(context.get_files_found())
    for path in sources:
        rec = mr.load(path)
        entries = []
        for record in rec.records('incoming_follow_requests'):
            entries.extend(item.value for item in record if isinstance(item.value, str))
        if not entries:
            value = rec.text('incoming_follow_requests')
            if value.strip() != mr.NO_RECORDS:
                entries = mr.lines(value)
        for stored in entries:
            username, ig_id, display = mr.parse_account(stored)
            data_list.append((stored, username, ig_id, display, rec.name))
    data_headers = ('Requester', 'Requester Username', 'Requester Instagram ID', 'Requester Display Name',
                    'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def fbigSearches(context):
    data_list = []
    sources = mr.records_files(context.get_files_found())
    for path in sources:
        rec = mr.load(path)
        for record in rec.records('searches'):
            raw = mr.text(record, 'Timestamp') or mr.text(record, 'Time')
            details = [f'{item.label}: {item.value}' for item in record
                       if isinstance(item.value, str) and item.label not in ('Timestamp', 'Time', 'Type')]
            details.extend(mr.flatten([item for item in record if not isinstance(item.value, str)]))
            when = mr.parse_ts(raw)
            if raw and not when:
                details.append(f'Time (as stored): {raw}')
            data_list.append((when, mr.text(record, 'Type'), '\n'.join(details), rec.name))
    data_headers = (('Time', 'datetime'), 'Type', 'Details', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)
