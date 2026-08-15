__artifacts_v2__ = {
    "robloxReturnAccountIPs": {
        "name": "Roblox - IP Addresses",
        "description": "IP address log from a Roblox law enforcement return "
                       "('IP address of the account' CSV).",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "Column names ending in _utc come from the provider's own header row. "
                 "Fields mapped from a private sample; Roblox does not publish a return "
                 "format specification.",
        "paths": ('*/IP address of the account*.csv',),
        "output_types": "standard",
        "artifact_icon": "globe",
    },
    "robloxReturnChat": {
        "name": "Roblox - Chat Records",
        "description": "Chat records from a Roblox law enforcement return ('Chat records of "
                       "the Roblox user' CSV). convo_type values observed include "
                       "chat/game/public, chat/game/private, chat/app and "
                       "chat/unfiltered_threads; values are reported as delivered.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "In the reviewed sample rows arrive grouped by conversation with a fully "
                 "empty separator row between groups; empty rows are skipped. Two row "
                 "layouts were observed: most rows populate every column, others carry only "
                 "ts, text, conversation_id, user_id and request_user_id. The module reports "
                 "the user_id/name the provider recorded on each row and does not assert "
                 "anything beyond that. Fields mapped from a private sample.",
        "paths": ('*/Chat records of the Roblox user*.csv',),
        "output_types": "standard",
        "artifact_icon": "message-circle",
    },
    "robloxReturnMessages": {
        "name": "Roblox - Messages",
        "description": "Private messages from a Roblox law enforcement return ('Messages of "
                       "the Roblox user' CSV), with subject, body, author and recipient as "
                       "delivered.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "Timestamps are taken from the 'created_time (UTC seconds)' and "
                 "'updated_time (UTC seconds)' epoch columns. In the reviewed sample the "
                 "provider's human-readable 'MM/DD/YYYY hh:mm:ss' columns agreed with the "
                 "epoch columns on every row. Fields mapped from a private sample.",
        "paths": ('*/Messages of the Roblox user*.csv',),
        "output_types": "standard",
        "artifact_icon": "mail",
    },
    "robloxReturnFriends": {
        "name": "Roblox - Friend List",
        "description": "Friend list from a Roblox law enforcement return ('Friend list of "
                       "the Roblox user' CSV).",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "createdutc/updatedutc are delivered as month-first "
                 "'MM/DD/YYYY hh:mm:ss' text; the order is shown by in-file values with a "
                 "second component greater than 12 and by the provider naming the same "
                 "format month-first in the Messages CSV header of the same delivery. "
                 "Fields mapped from a private sample.",
        "paths": ('*/Friend list of the Roblox user*.csv',),
        "output_types": "standard",
        "artifact_icon": "users",
    },
    "robloxReturnFollowers": {
        "name": "Roblox - Follower & Following List",
        "description": "Follower/following relationships from a Roblox law enforcement "
                       "return ('Follower & following list of the Roblox user' CSV). Both "
                       "directions are present in one file; the provider does not document "
                       "which column follows which, so userid and followeruserid are "
                       "reported as stored.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "createdutc/updatedutc arrive as 13-digit integers. They are parsed as "
                 "Unix epoch milliseconds; that unit is inferred from the value range "
                 "(parsed values in the reviewed sample all fall inside the provider's own "
                 "stated dump window), not documented by the provider. Fields mapped from a "
                 "private sample.",
        "paths": ('*/Follower & following list of the Roblox user*.csv',),
        "output_types": "standard",
        "artifact_icon": "users",
    },
    "robloxReturnGroupWall": {
        "name": "Roblox - Group Wall Posts",
        "description": "Group wall posts from a Roblox law enforcement return ('Group wall "
                       "posts of the Roblox user' CSV).",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "createdutc/updatedutc are month-first 'MM/DD/YYYY hh:mm:ss' text; see the "
                 "Friend List artifact notes for the sourcing of that order. Fields mapped "
                 "from a private sample.",
        "paths": ('*/Group wall posts of the Roblox user*.csv',),
        "output_types": "standard",
        "artifact_icon": "users-group",
    },
    "robloxReturnDevices": {
        "name": "Roblox - Device Information",
        "description": "Device information from a Roblox law enforcement return ('Device "
                       "information of the Roblox user' CSV): device name, OS and OS "
                       "version per browser tracker id (btid).",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "Fields mapped from a private sample.",
        "paths": ('*/Device information of the Roblox user*.csv',),
        "output_types": "standard",
        "artifact_icon": "device-mobile",
    },
    "robloxReturnDeviceIDs": {
        "name": "Roblox - Device IDs",
        "description": "Device identifiers from a Roblox law enforcement return ('Device ID "
                       "of the Roblox user' CSV).",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "Fields mapped from a private sample.",
        "paths": ('*/Device ID of the Roblox user*.csv',),
        "output_types": "standard",
        "artifact_icon": "device-mobile",
    },
    "robloxReturnBTID": {
        "name": "Roblox - Browser Tracker ID",
        "description": "Browser tracker id (BTID) record from a Roblox law enforcement "
                       "return ('BTID of the Roblox user' CSV).",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "created/updated are shown exactly as delivered. Their column names carry "
                 "no timezone and the values observed were day-ambiguous, so they are not "
                 "converted. Fields mapped from a private sample.",
        "paths": ('*/BTID of the Roblox user*.csv',),
        "output_types": "standard",
        "artifact_icon": "list",
    },
    "robloxReturnAdIDs": {
        "name": "Roblox - Ad IDs",
        "description": "ad_id values from a Roblox law enforcement return. Delivered as a "
                       "single-column CSV whose header is 'ad_id'; in the reviewed sample "
                       "the file was named after the subject user id.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "The provider does not document what ad_id identifies; values are "
                 "UUID-formatted and are reported as stored. Any CSV whose header row is "
                 "exactly 'ad_id' is treated as this record type. Fields mapped from a "
                 "private sample.",
        "paths": ('*/*.csv',),
        "output_types": "standard",
        "artifact_icon": "list",
    },
    "robloxReturnUGC": {
        "name": "Roblox - User Generated Content",
        "description": "User generated content list from a Roblox law enforcement return "
                       "('User generated content of the Roblox user' CSV): one row per "
                       "asset with type, name, description and creator fields as delivered.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "asset_createdutc/asset_updatedutc/creator_createdutc are month-first "
                 "'MM/DD/YYYY hh:mm:ss' text; see the Friend List artifact notes for the "
                 "sourcing of that order. In the reviewed sample the asset_hash_id values "
                 "in this list did not match any delivered asset file name; they matched "
                 "the assethashid column of the richer asset metadata layout on every "
                 "compared row. The delivered files are named by the separate 32-character "
                 "hash carried in the *_metadata.csv files parsed by the 'Roblox - UGC "
                 "Asset Files' artifact. Fields mapped from a private sample.",
        "paths": ('*/User generated content of the Roblox user*.csv',),
        "output_types": "standard",
        "artifact_icon": "package",
    },
    "robloxReturnAssets": {
        "name": "Roblox - UGC Asset Files",
        "description": "Delivered user generated content files from a Roblox law "
                       "enforcement return: the per-type *_metadata.csv lists inside the "
                       "asset dump joined to the hash-named payload files delivered next to "
                       "them. Image payloads are embedded as media.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "The dump was observed delivered twice, once with bare hash-and-label "
                 "names (hash-IMAGE, hash-MODEL, hash-PLACE, hash-ANIMATION) and once with "
                 "extensions (.png, .rbxm, .rbxl); duplicate metadata rows are collapsed. "
                 "Two metadata header layouts were observed for the same records in one "
                 "delivery, a compact one keyed 'assetid' and a richer one keyed 'id' that "
                 "adds assettypeid, currentversionid, assethashid, assetgenres, "
                 "assetcategories and isarchived; records are merged and the richer fields "
                 "are kept where delivered. The metadata 'hash' column matched every "
                 "delivered payload file name in the reviewed sample. Several assets can "
                 "share one payload hash. Non-image payloads (Roblox binary model/place "
                 "formats) are referenced by path rather than embedded. Fields mapped from "
                 "a private sample.",
        "paths": ('*/UserId_*_metadata.csv',
                  '*/UserId_*_start_*_end_*/*',
                  "*/Images of the Roblox user*/*"),
        "output_types": "standard",
        "artifact_icon": "photo",
    },
    "robloxReturnSupportTickets": {
        "name": "Roblox - Support Tickets",
        "description": "Customer support tickets from a Roblox law enforcement return, "
                       "delivered as per-ticket JSON in Zendesk ticket-export format (one "
                       "file per ticket, named by ticket id).",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "Field meanings follow the published Zendesk Ticket API schema, which is "
                 "the structure these files carry. Any JSON file whose top level contains "
                 "via, requester and comments keys is treated as a ticket; other JSON is "
                 "skipped. Per-comment detail is in the 'Roblox - Support Ticket Comments' "
                 "artifact. Observed in a private sample.",
        "paths": ('*/*.json',),
        "output_types": "standard",
        "artifact_icon": "message",
    },
    "robloxReturnSupportTicketComments": {
        "name": "Roblox - Support Ticket Comments",
        "description": "Individual comments on customer support tickets from a Roblox law "
                       "enforcement return (Zendesk ticket-export JSON), including the "
                       "per-comment ip_address, location and latitude/longitude metadata "
                       "the export carries.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "Field meanings follow the published Zendesk Ticket Comments API schema. "
                 "Location fields are Zendesk's own per-comment metadata and are reported "
                 "as stored. The schema's per-comment attachments array was empty on every "
                 "comment in the reviewed sample and is not parsed; a return delivering "
                 "ticket attachments would need that added. Observed in a private sample.",
        "paths": ('*/*.json',),
        "output_types": "standard",
        "artifact_icon": "message",
    },
    "robloxReturnPDFDocuments": {
        "name": "Roblox - Account Documents (PDF)",
        "description": "PDF documents delivered in a Roblox law enforcement return "
                       "('Information of the account' and 'Block list of the Roblox user'). "
                       "The files are embedded for viewing; their contents are not parsed "
                       "into rows.",
        "author": "@AlexisBrignoni",
        "creation_date": "2026-08-14",
        "last_update_date": "2026-08-14",
        "requirements": "none",
        "category": "Roblox Returns",
        "notes": "In the reviewed sample these PDFs were rendered from Google Docs "
                 "(per their Producer metadata), i.e. human-assembled documents rather "
                 "than a machine export, so no stable row structure is assumed. Observed "
                 "in a private sample.",
        "paths": ('*/Information of the account*.pdf',
                  '*/Block list of the Roblox user*.pdf'),
        "output_types": "standard",
        "artifact_icon": "book",
    },
}

import csv
import json
import os
import re
import sys
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, check_in_media, logfunc

_HASH_NAME = re.compile(r'^([0-9a-f]{32})([.-])')
_META_NAME = re.compile(r'_(images|animations|models|places|audios|videos)_metadata\.csv$')

# Zendesk ticket exports observed were well under this; keeps the JSON sniff from
# loading unrelated large files matched by the broad *.json pattern.
_MAX_TICKET_JSON = 50 * 1024 * 1024


def _raise_csv_field_limit():
    try:
        csv.field_size_limit(sys.maxsize)
    except OverflowError:
        csv.field_size_limit(2 ** 31 - 1)


def _iso_ts(value):
    """ISO 8601 text as delivered (with or without fraction, trailing Z) -> aware UTC
    datetime. Empty -> None. Unparseable text is returned unchanged."""
    if not value:
        return None
    v = value.strip()
    if v.endswith('Z'):
        v = v[:-1]
    try:
        dt = datetime.fromisoformat(v)
    except ValueError:
        return value
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _mdy_ts(value):
    """Month-first 'MM/DD/YYYY hh:mm:ss' text -> aware UTC datetime. Empty -> None.
    Unparseable text is returned unchanged."""
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), '%m/%d/%Y %H:%M:%S').replace(
            tzinfo=timezone.utc)
    except ValueError:
        return value


def _sql_ts(value):
    """'YYYY-MM-DD hh:mm:ss[.fff]' text -> aware UTC datetime. Empty -> None.
    Unparseable text is returned unchanged."""
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.strip())
    except ValueError:
        return value
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _epoch_s(value):
    if not value:
        return None
    try:
        return datetime.fromtimestamp(int(value), tz=timezone.utc)
    except (ValueError, OverflowError, OSError):
        return value


def _epoch_ms(value):
    if not value:
        return None
    try:
        return datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc)
    except (ValueError, OverflowError, OSError):
        return value


def _dict_rows(file_found):
    with open(file_found, newline='', encoding='utf-8-sig', errors='backslashreplace') as f:
        yield from csv.DictReader(f)


@artifact_processor
def robloxReturnAccountIPs(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.csv'):
            continue
        source_path = file_found
        for row in _dict_rows(file_found):
            data_list.append((
                _sql_ts(row.get('first_recorded_utc', '')),
                _sql_ts(row.get('last_recorded_utc', '')),
                _sql_ts(row.get('last_observed_port_utc', '')),
                row.get('user_id', ''),
                row.get('username', ''),
                row.get('ip_address', ''),
                row.get('last_observed_port', ''),
            ))

    data_headers = (('First Recorded UTC', 'datetime'), ('Last Recorded UTC', 'datetime'),
                    ('Last Observed Port UTC', 'datetime'), 'User ID', 'Username',
                    'IP Address', 'Last Observed Port')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def robloxReturnChat(context):
    _raise_csv_field_limit()
    data_list = []
    source_path = ''
    # Low-cardinality columns repeat across a very large row count; interning keeps
    # one string object per distinct value.
    interned = {}

    def _i(value):
        return interned.setdefault(value, value)

    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.csv'):
            continue
        source_path = file_found
        with open(file_found, newline='', encoding='utf-8-sig',
                  errors='backslashreplace') as f:
            reader = csv.reader(f)
            header = next(reader, [])
            idx = {name: i for i, name in enumerate(header)}
            columns = [idx.get(name, -1) for name in (
                'ts', 'ds', 'conversation_id', 'convo_type', 'user_id', 'name',
                'text', 'is_filtered_o13', 'is_filtered_u13', 'is_rewritten',
                'request_user_id')]

            for row in reader:
                if not any(row):
                    continue    # separator row between conversation groups
                n = len(row)
                (ts, ds, conversation_id, convo_type, user_id, name, text,
                 filtered_o13, filtered_u13, rewritten, request_user_id) = (
                    row[i] if 0 <= i < n else '' for i in columns)
                data_list.append((
                    _iso_ts(ts), _i(ds), _i(conversation_id), _i(convo_type),
                    _i(user_id), _i(name), text, _i(filtered_o13), _i(filtered_u13),
                    _i(rewritten), _i(request_user_id),
                ))

    data_headers = (('Timestamp', 'datetime'), ('DS', 'date'), 'Conversation ID',
                    'Convo Type', 'User ID', 'Name', 'Text', 'Is Filtered O13',
                    'Is Filtered U13', 'Is Rewritten', 'Request User ID')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def robloxReturnMessages(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.csv'):
            continue
        source_path = file_found
        for row in _dict_rows(file_found):
            data_list.append((
                _epoch_s(row.get('created_time (UTC seconds)', '')),
                _epoch_s(row.get('updated_time (UTC seconds)', '')),
                row.get('id', ''),
                row.get('message_type_id', ''),
                row.get('subject', ''),
                row.get('body', ''),
                row.get('author_id', ''),
                row.get('author_name', ''),
                row.get('recipient_id', ''),
                row.get('recipient_name', ''),
                row.get('is_system_message', ''),
                row.get('is_read', ''),
                row.get('is_archived', ''),
            ))

    data_headers = (('Created', 'datetime'), ('Updated', 'datetime'), 'Message ID',
                    'Message Type ID (as stored)', 'Subject', 'Body', 'Author ID',
                    'Author Name', 'Recipient ID', 'Recipient Name', 'Is System Message',
                    'Is Read', 'Is Archived')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def robloxReturnFriends(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.csv'):
            continue
        source_path = file_found
        for row in _dict_rows(file_found):
            data_list.append((
                _mdy_ts(row.get('createdutc', '')),
                _mdy_ts(row.get('updatedutc', '')),
                row.get('userid', ''),
                row.get('frienduserid', ''),
            ))

    data_headers = (('Created UTC', 'datetime'), ('Updated UTC', 'datetime'),
                    'User ID', 'Friend User ID')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def robloxReturnFollowers(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.csv'):
            continue
        source_path = file_found
        for row in _dict_rows(file_found):
            data_list.append((
                _epoch_ms(row.get('createdutc', '')),
                _epoch_ms(row.get('updatedutc', '')),
                row.get('userid', ''),
                row.get('followeruserid', ''),
            ))

    data_headers = (('Created UTC', 'datetime'), ('Updated UTC', 'datetime'),
                    'User ID (userid as stored)', 'Follower User ID (followeruserid as stored)')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def robloxReturnGroupWall(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.csv'):
            continue
        source_path = file_found
        for row in _dict_rows(file_found):
            data_list.append((
                _mdy_ts(row.get('createdutc', '')),
                _mdy_ts(row.get('updatedutc', '')),
                row.get('group_wall_post_id', ''),
                row.get('group_id', ''),
                row.get('user_id', ''),
                row.get('post_text', ''),
            ))

    data_headers = (('Created UTC', 'datetime'), ('Updated UTC', 'datetime'),
                    'Group Wall Post ID', 'Group ID', 'User ID', 'Post Text')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def robloxReturnDevices(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.csv'):
            continue
        source_path = file_found
        for row in _dict_rows(file_found):
            data_list.append((
                row.get('pii_userid', ''),
                row.get('btid', ''),
                row.get('devicename', ''),
                row.get('os', ''),
                row.get('osversion', ''),
            ))

    data_headers = ('User ID', 'Browser Tracker ID (btid)', 'Device Name', 'OS',
                    'OS Version')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def robloxReturnDeviceIDs(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.csv'):
            continue
        source_path = file_found
        for row in _dict_rows(file_found):
            data_list.append((
                row.get('pii_userid', ''),
                row.get('pii_device_id', ''),
            ))

    data_headers = ('User ID', 'Device ID')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def robloxReturnBTID(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.csv'):
            continue
        source_path = file_found
        for row in _dict_rows(file_found):
            data_list.append((
                row.get('accountid', ''),
                row.get('browsertrackerid', ''),
                row.get('created', ''),
                row.get('updated', ''),
            ))

    data_headers = ('Account ID', 'Browser Tracker ID', 'Created (as stored)',
                    'Updated (as stored)')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def robloxReturnAdIDs(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.csv'):
            continue
        try:
            with open(file_found, newline='', encoding='utf-8-sig',
                      errors='backslashreplace') as f:
                reader = csv.reader(f)
                header = next(reader, [])
                if header != ['ad_id']:
                    continue
                source_path = file_found
                filename = os.path.basename(file_found)
                for row in reader:
                    if row and row[0]:
                        data_list.append((row[0], filename))
        except OSError as ex:
            logfunc(f'Error reading {file_found}: {ex}')

    data_headers = ('Ad ID (as stored)', 'Source Filename')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def robloxReturnUGC(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.csv'):
            continue
        source_path = file_found
        for row in _dict_rows(file_found):
            data_list.append((
                _mdy_ts(row.get('asset_createdutc', '')),
                _mdy_ts(row.get('asset_updatedutc', '')),
                _mdy_ts(row.get('creator_createdutc', '')),
                row.get('asset_id', ''),
                row.get('asset_type', ''),
                row.get('asset_name', ''),
                row.get('asset_description', ''),
                row.get('asset_current_version_id', ''),
                row.get('asset_hash_id', ''),
                row.get('creator_user_or_group_id', ''),
                row.get('creator_type', ''),
                row.get('creator_name', ''),
                row.get('creator_moderation_status', ''),
            ))

    data_headers = (('Asset Created UTC', 'datetime'), ('Asset Updated UTC', 'datetime'),
                    ('Creator Created UTC', 'datetime'), 'Asset ID', 'Asset Type',
                    'Asset Name', 'Asset Description', 'Asset Current Version ID',
                    'Asset Hash ID (as stored)', 'Creator User or Group ID',
                    'Creator Type', 'Creator Name', 'Creator Moderation Status')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def robloxReturnAssets(context):
    data_list = []
    source_path = ''
    metadata_files = []
    payloads = {}    # hash -> {extension or label: full path}

    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.isfile(file_found):
            continue
        basename = os.path.basename(file_found)
        if _META_NAME.search(basename):
            metadata_files.append(file_found)
            continue
        m = _HASH_NAME.match(basename)
        if m:
            payloads.setdefault(m.group(1), {})[basename[33:]] = file_found

    # Two metadata header variants were observed for the same records in one
    # delivery: a compact one starting with 'assetid' and a richer one starting
    # with 'id'. Records are merged by (kind, asset id, hash, createdutc), keeping
    # the first non-empty value delivered for each field.
    FIELDS = ('name', 'description', 'creatorid', 'assettypeid', 'currentversionid',
              'assethashid', 'assetgenres', 'assetcategories', 'isarchived',
              'updatedutc')
    merged = {}
    for file_found in metadata_files:
        asset_kind = _META_NAME.search(os.path.basename(file_found)).group(1)
        source_path = file_found
        for row in _dict_rows(file_found):
            asset_id = row.get('assetid') or row.get('id') or ''
            key = (asset_kind, asset_id, row.get('hash', ''), row.get('createdutc', ''))
            record = merged.setdefault(key, {})
            for field in FIELDS:
                if not record.get(field) and row.get(field):
                    record[field] = row[field]

    def _delivered(content_hash):
        delivered = payloads.get(content_hash, {})
        if not delivered:
            return '', None
        # Prefer the with-extensions copy; fall back to the bare hash-and-label copy.
        for suffix in ('png', 'IMAGE'):
            if suffix in delivered:
                path = delivered[suffix]
                return path, check_in_media(path, os.path.basename(path))
        named = min(delivered, key=lambda k: (k.isupper(), k))
        return delivered[named], None

    for (asset_kind, asset_id, content_hash, created), record in merged.items():
        delivered_path, media_item = _delivered(content_hash)
        data_list.append((
            _iso_ts(created),
            _iso_ts(record.get('updatedutc', '')),
            asset_kind,
            asset_id,
            record.get('name', ''),
            record.get('description', ''),
            record.get('creatorid', ''),
            record.get('assettypeid', ''),
            record.get('currentversionid', ''),
            record.get('assethashid', ''),
            record.get('assetgenres', ''),
            record.get('assetcategories', ''),
            record.get('isarchived', ''),
            content_hash,
            media_item,
            context.get_relative_path(delivered_path) if delivered_path else '',
        ))

    # Payload files delivered without a matching metadata row (for example a
    # standalone images zip) are still listed so they do not vanish from the report.
    matched_hashes = {key[2] for key in merged}
    for content_hash in sorted(set(payloads) - matched_hashes):
        delivered_path, media_item = _delivered(content_hash)
        if not source_path:
            source_path = delivered_path
        data_list.append((
            None, None, '', '', '', '', '', '', '', '', '', '', '', content_hash,
            media_item, context.get_relative_path(delivered_path),
        ))

    data_headers = (('Created UTC', 'datetime'), ('Updated UTC', 'datetime'),
                    'Asset Kind (from metadata filename)', 'Asset ID', 'Name',
                    'Description', 'Creator ID', 'Asset Type ID (as stored)',
                    'Current Version ID', 'Asset Hash ID (as stored)', 'Asset Genres',
                    'Asset Categories', 'Is Archived', 'Content Hash',
                    ('Media', 'media'), 'Delivered File')
    return data_headers, data_list, context.get_relative_path(source_path)


def _load_ticket(file_found):
    """Returns the parsed Zendesk ticket dict, or None if the file is not one."""
    try:
        if os.path.getsize(file_found) > _MAX_TICKET_JSON:
            return None
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            data = json.load(f)
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    if not {'via', 'requester', 'comments'} <= set(data):
        return None
    return data


@artifact_processor
def robloxReturnSupportTickets(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.json'):
            continue
        ticket = _load_ticket(file_found)
        if ticket is None:
            continue
        source_path = file_found
        requester = ticket.get('requester') or {}
        via = ticket.get('via') or {}
        data_list.append((
            _iso_ts(ticket.get('created_at', '')),
            _iso_ts(ticket.get('updated_at', '')),
            ticket.get('id', ''),
            ticket.get('status', ''),
            ticket.get('type', ''),
            via.get('channel', ''),
            ticket.get('subject', ''),
            requester.get('id', ''),
            requester.get('name', ''),
            requester.get('email', ''),
            _iso_ts(requester.get('created_at', '')),
            ticket.get('recipient', ''),
            len(ticket.get('comments') or []),
            ', '.join(ticket.get('tags') or []),
        ))

    data_headers = (('Created', 'datetime'), ('Updated', 'datetime'), 'Ticket ID',
                    'Status', 'Type', 'Via Channel', 'Subject', 'Requester ID',
                    'Requester Name', 'Requester Email', ('Requester Created', 'datetime'),
                    'Recipient', 'Comment Count', 'Tags')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def robloxReturnSupportTicketComments(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.json'):
            continue
        ticket = _load_ticket(file_found)
        if ticket is None:
            continue
        source_path = file_found
        for comment in ticket.get('comments') or []:
            author = comment.get('author') or {}
            via = comment.get('via') or {}
            system = ((comment.get('metadata') or {}).get('system')) or {}
            data_list.append((
                _iso_ts(comment.get('created_at', '')),
                ticket.get('id', ''),
                comment.get('id', ''),
                comment.get('type', ''),
                author.get('id', ''),
                author.get('name', ''),
                author.get('email', ''),
                comment.get('public', ''),
                via.get('channel', ''),
                system.get('ip_address', ''),
                system.get('location', ''),
                system.get('latitude', ''),
                system.get('longitude', ''),
                comment.get('plain_body', ''),
            ))

    data_headers = (('Created', 'datetime'), 'Ticket ID', 'Comment ID', 'Comment Type',
                    'Author ID', 'Author Name', 'Author Email', 'Public', 'Via Channel',
                    'IP Address', 'Location', 'Latitude', 'Longitude', 'Body')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def robloxReturnPDFDocuments(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.lower().endswith('.pdf'):
            continue
        source_path = file_found
        filename = os.path.basename(file_found)
        media_item = check_in_media(file_found, filename)
        data_list.append((filename, media_item, context.get_relative_path(file_found)))

    data_headers = ('Filename', ('Document', 'media'), 'Path')
    return data_headers, data_list, context.get_relative_path(source_path)
