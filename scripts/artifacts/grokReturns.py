__artifacts_v2__ = {
    "grokAccount": {
        "name": "Grok - Account",
        "description": "Account record from the account file of an xAI (Grok) return, with the "
                       "deletion time from the account-delete-time file and the files in the "
                       "account's profile_media folder.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-10-24",
        "last_update_date": "2026-10-24",
        "requirements": "none",
        "category": "Grok (xAI) Returns",
        "notes": "xAI's README states that every record in the return is kept in UTC, and that "
                 "the deletion time is null when the account has not been deleted; Delete Time "
                 "is blank when the file holds no value. The deletion path has not been run "
                 "against a deleted account. Profile Media shows every file in the "
                 "<userId>_profile_media folder of the same account, matched by the user id in "
                 "the folder name; the README documents no field that names those files.",
        "paths": ('*/*-account.txt', '*/*-account-delete-time.txt', '*/*_profile_media/*'),
        "output_types": "standard",
        "artifact_icon": "user",
    },
    "grokMfaDevices": {
        "name": "Grok - Multi-Factor Devices",
        "description": "Registered multi-factor authentication devices from the "
                       "multi-factor-devices file of an xAI (Grok) return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-10-24",
        "last_update_date": "2026-10-24",
        "requirements": "none",
        "category": "Grok (xAI) Returns",
        "notes": "This artifact has not been run against a multi-factor device record; its "
                 "columns follow the README's field list. The README also lists totpSecret "
                 "(encrypted), webAuthnPasskey and webAuthnConfirmSkr. They are authentication "
                 "material, not account activity, and are not reported.",
        "paths": ('*/*-multi-factor-devices.txt',),
        "output_types": "standard",
        "artifact_icon": "lock",
    },
    "grokIpLogs": {
        "name": "Grok - IP Logs",
        "description": "Login IP addresses from the ip-logs file of an xAI (Grok) return, with the "
                       "first and most recent login from each address.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-10-24",
        "last_update_date": "2026-10-24",
        "requirements": "none",
        "category": "Grok (xAI) Returns",
        "notes": "First Login is createTime and Last Login is lastLoginTime, which xAI's README "
                 "describes as the first and the most recent login from the address. User ID "
                 "separates accounts when a return covers more than one, and holds one value "
                 "when it covers one.",
        "paths": ('*/*-ip-logs.txt',),
        "output_types": "standard",
        "artifact_icon": "network",
    },
    "grokSessions": {
        "name": "Grok - Sessions",
        "description": "Login sessions from the sessions file of an xAI (Grok) return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-10-24",
        "last_update_date": "2026-10-24",
        "requirements": "none",
        "category": "Grok (xAI) Returns",
        "notes": "xAI's README says Last Auth Time falls back to the creation time for older "
                 "records, so a Last Auth Time equal to Create Time is not on its own evidence "
                 "of an authentication at that moment. Start Verification Time and Verification "
                 "Time are blank when the file holds no value for them. Status is the stored "
                 "value and can be one value on every row; the README lists pending and "
                 "confirmed. User ID separates accounts when a return covers more than one, and "
                 "holds one value when it covers one.",
        "paths": ('*/*-sessions.txt',),
        "output_types": "standard",
        "artifact_icon": "login",
    },
    "grokConversationList": {
        "name": "Grok - Conversation List",
        "description": "One row per conversation from the conversations and "
                       "deleted-conversations files of an xAI (Grok) return, with its times, "
                       "title and number of responses.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-10-24",
        "last_update_date": "2026-10-24",
        "requirements": "none",
        "category": "Grok (xAI) Returns",
        "notes": "Deleted Time is header.deleteTime, present only in the deleted-conversations "
                 "file, whose README entry for it is a soft-deletion timestamp. Listed In names "
                 "the file the conversation came from. Responses counts the response objects the "
                 "file holds for the conversation. Temporary is the README's flag for a "
                 "conversation auto-deleted within 24 hours. Starred is the stored flag and can "
                 "be one value on every row. Summary, Asset IDs, Media Types and Shared With "
                 "User IDs are blank when the record holds an empty value or omits the field. X "
                 "User ID is the README's legacy X numeric user id and holds one value when the "
                 "return covers one account. User ID separates accounts when a return covers "
                 "more than one, and holds one value when it covers one. Other header fields the "
                 "README lists (anonUserId, systemPromptId, systemPromptName, leafResponseId, "
                 "rootAssetId, controller, taskResultId, teamId, sharedWithTeam) are not "
                 "reported.",
        "paths": ('*/*-conversations.txt',),
        "output_types": "standard",
        "artifact_icon": "list",
    },
    "grokConversations": {
        "name": "Grok - Conversations",
        "description": "Prompts and responses from the conversations and deleted-conversations "
                       "files of an xAI (Grok) return, one row per response, with the media "
                       "files the response names.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-10-24",
        "last_update_date": "2026-10-24",
        "requirements": "none",
        "category": "Grok (xAI) Returns",
        "notes": "Sender is the stored sender value; the README describes it as who sent the "
                 "message (human, assistant, or a model name), and the conversation view treats "
                 "human as sent by the account. Response Time is responses.createTime, which the "
                 "README describes as a BSON datetime (milliseconds since the Unix epoch). "
                 "Conversation Deleted Time is set only on rows from the deleted-conversations "
                 "file. Media shows the files in the account's <userId>_assets_media folder "
                 "whose name begins with an id the response records in fileAttachments, or that "
                 "a generatedImageUrls key names. The README does not document the folder's "
                 "naming; a generated key users/<userId>/generated/<id>/<name> is matched to a "
                 "file named <id>_<name>, the naming observed in the folder. For an id with "
                 "several files only the first of the content file, _image, _generated_video, "
                 "_original_image, _generated_video_hd, _preview_image and _last_frame_image "
                 "(the suffixes observed) is shown; Grok - Assets and Grok - Media Files list "
                 "the rest. Media is blank when the folder does not hold a file for the id. "
                 "Search Query is responses.query as stored and is blank when that value is "
                 "empty. User ID separates accounts when a return covers more than one, and "
                 "holds one value when it covers one. Thinking traces and their start and end "
                 "times, web search results, deepsearch steps, request metadata, tool responses, "
                 "card attachments, X post ids, webpage URLs, imageEditUri, selected file text, "
                 "and the manual, shared and mediaTypes values are not reported. "
                 "imageAttachments (README: base64 images attached by the user) is not reported.",
        "paths": ('*/*-conversations.txt', '*/*_assets_media/*'),
        "output_types": "standard",
        "artifact_icon": "messages",
        "data_views": {
            "conversation": {
                "conversationDiscriminatorColumn": "Conversation ID",
                "conversationLabelColumn": "Conversation Title",
                "textColumn": "Message",
                "directionColumn": "Sender",
                "directionSentValue": "human",
                "timeColumn": "Response Time",
                "senderColumn": "Sender",
                "mediaColumn": "Media",
            }
        },
    },
    "grokAssets": {
        "name": "Grok - Assets",
        "description": "Uploaded and generated assets from the asset and deleted-asset files of "
                       "an xAI (Grok) return, with the files the account's assets_media folder "
                       "holds for each asset.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-10-24",
        "last_update_date": "2026-10-24",
        "requirements": "none",
        "category": "Grok (xAI) Returns",
        "notes": "Listed In names the file the record came from. The deleted-asset file carries "
                 "no deletion time and a different field set (it adds postId and mediaKind), so "
                 "columns it lacks are blank on those rows; its File Source uses the backend "
                 "enum spelling, as the README says. On asset rows File Source is the stored "
                 "value; the README lists SELF_UPLOAD, GOOGLE_DRIVE and ONE_DRIVE, and other "
                 "values occur. Media shows every file in the account's <userId>_assets_media "
                 "folder whose name begins with the asset id, the file named by the asset's key "
                 "first; it is blank when the folder holds none. Aux Fields pairs each auxNames "
                 "entry with the auxKeys entry at the same position, as stored; deleted-asset "
                 "records carry auxKeys only, so those rows list the keys alone. The README "
                 "describes both lists only as names and storage keys of auxiliary assets. Many "
                 "auxKeys values are not storage keys (a true or false string, or other text), "
                 "and the README does not establish what those pairs mean. Last Use Time, "
                 "Deleted Time and Current Conversation ID are blank when the record omits "
                 "lastUseTime, deletedTime or currentConversationId. User ID separates accounts "
                 "when a return covers more than one, and holds one value when it covers one. "
                 "isDeleted, isLatest, isNameChanged, inlineStatus, anonUserId, "
                 "thirdPartyFileId, thirdPartyFileMimeType, assetDiff, controller, teamId, "
                 "sharedWithTeam and sharedWithUserIds are not reported.",
        "paths": ('*/*-asset.txt', '*/*_assets_media/*'),
        "output_types": "standard",
        "artifact_icon": "photo",
    },
    "grokMediaPosts": {
        "name": "Grok - Media Posts",
        "description": "Prompts for generated media from the media-posts and deleted-media-posts "
                       "files of an xAI (Grok) return, with the file the account's assets_media "
                       "folder holds for the post's media path.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-10-24",
        "last_update_date": "2026-10-24",
        "requirements": "none",
        "category": "Grok (xAI) Returns",
        "notes": "Listed In names the file the record came from and holds one value when only "
                 "one of the two files has records. The deleted-media-posts path has not been "
                 "run against a record. Media is the file mediaPath names, under the naming "
                 "observed in the folder, which the README does not document: "
                 "users/<userId>/generated/<id>/<name> as <id>_<name>, "
                 "users/<userId>/<id>/content as <id> plus the file's extension (only image "
                 "extensions observed), and imagine-public/images/<name> as <name>. It is blank "
                 "when the folder holds no such file. Media Type is the stored value, a numeric "
                 "code; the README describes the field as the type of media (e.g. image, video) "
                 "and does not map the codes. The README defines originalPrompt differently per "
                 "file: on media-posts it is the user's prompt with settings parameters "
                 "appended, on deleted-media-posts the original post's prompt for a remix. Extra "
                 "is the stored JSON object. Deleted At and Visibility are blank when the record "
                 "omits deletedAt or visibility. User ID separates accounts when a return covers "
                 "more than one, and holds one value when it covers one. mediaKind on "
                 "deleted-media-posts records is not reported.",
        "paths": ('*/*-media-posts.txt', '*/*_assets_media/*'),
        "output_types": "standard",
        "artifact_icon": "photo-ai",
    },
    "grokMediaFiles": {
        "name": "Grok - Media Files",
        "description": "Files in the assets_media folder of an xAI (Grok) return, with the record "
                       "types that name the id at the start of each file name.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-10-24",
        "last_update_date": "2026-10-24",
        "requirements": "none",
        "category": "Grok (xAI) Returns",
        "notes": "Referenced By lists each place in the same account's files where the id at the "
                 "start of the file name appears as an asset id, an asset key (key, "
                 "previewImageKey or an auxKeys entry), a deleted-asset id, key or post id, a "
                 "media post id or media path, a response fileAttachments entry or a "
                 "generatedImageUrls key. It is blank when none of those fields names the id. "
                 "Other fields are not scanned, so a blank does not show the return has no "
                 "record of the file. User ID is taken from the <userId>_assets_media folder "
                 "name and holds one value when the return covers one account.",
        "paths": ('*/*_assets_media/*', '*/*-asset.txt', '*/*-media-posts.txt',
                  '*/*-conversations.txt'),
        "output_types": "standard",
        "artifact_icon": "files",
    },
}

import json
import os
import re
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, check_in_media, convert_unix_ts_to_utc, logfunc

_UUID = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
# xAI names every file <userId>-<kind>.txt and the media folders <userId>_<name>_media.
# Twitter returns use the same <id>-<kind>.txt layout with a numeric id, so the uuid
# shape and the xai* wrapper key below are what keep this module to xAI files.
_RECORD_FILE = re.compile(r'^(' + _UUID + r')-([a-z-]+)\.txt$')
_MEDIA_DIR = re.compile(r'^(' + _UUID + r')_(assets|profile)_media$')
_ISO = re.compile(r'^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(?:\.(\d+))?(Z|[+-]\d\d:\d\d)?$')
# For an id with several files, the one shown in a single-file context.
_PRIMARY_ORDER = ('', '_image.jpg', '_generated_video.mp4', '_original_image.jpg',
                  '_generated_video_hd.mp4', '_preview_image.jpg', '_last_frame_image.jpg')


def _unwrap(text):
    '''Return the body of a PGP clear-signed message, undoing dash-escaping.'''
    lines = text.split('\n')
    if not lines or not lines[0].startswith('-----BEGIN PGP SIGNED MESSAGE-----'):
        return text
    body = []
    i = 1
    while i < len(lines) and lines[i].strip():  # armor headers (Hash: ...)
        i += 1
    for line in lines[i + 1:]:
        if line.startswith('-----BEGIN PGP SIGNATURE-----'):
            break
        body.append(line[2:] if line.startswith('- ') else line)
    return '\n'.join(body)


def _load(file_found):
    '''Parse one xAI record file into a list of records, or None when it is not one.'''
    try:
        with open(file_found, encoding='utf-8') as f:
            data = json.loads(_unwrap(f.read()))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as ex:
        logfunc(f'Grok: could not read {os.path.basename(file_found)}: {type(ex).__name__}')
        return None
    if not isinstance(data, list):
        return None
    for item in data:
        if not (isinstance(item, dict) and len(item) == 1 and next(iter(item)).startswith('xai')):
            logfunc(f'Grok: {os.path.basename(file_found)} does not hold xAI records, skipped')
            return None
    return [next(iter(item.values())) for item in data]


def _record_files(context, kind):
    '''Yield (user id, path, records) for each xAI file of the given kind.'''
    seen = set()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.isdir(file_found) or file_found in seen:
            continue
        m = _RECORD_FILE.match(os.path.basename(file_found))
        if not m or m.group(2) != kind:
            continue
        seen.add(file_found)
        records = _load(file_found)
        if records is not None:
            yield m.group(1), file_found, records


def _media_index(context, folder):
    '''Map (user id, file name) to the staged path, for files in <userId>_<folder>_media.'''
    index = {}
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.isdir(file_found):
            continue
        parent = os.path.basename(os.path.dirname(file_found))
        m = _MEDIA_DIR.match(parent)
        name = os.path.basename(file_found)
        if not m or m.group(2) != folder or name.startswith('.'):
            continue
        index[(m.group(1), name)] = file_found
    return index


def _files_by_id(index):
    '''Group an assets_media index by the uuid that starts each file name.'''
    by_id = {}
    for (user_id, name), path in index.items():
        m = re.match(_UUID, name)
        if m:
            by_id.setdefault((user_id, m.group(0)), []).append((name[len(m.group(0)):], name, path))
    return by_id


def _primary(entries):
    '''Pick the file shown for an id: the content file, then by _PRIMARY_ORDER.'''
    def rank(entry):
        suffix = entry[0]
        if suffix.startswith('.'):
            return (0, entry[1])
        return ((_PRIMARY_ORDER.index(suffix) if suffix in _PRIMARY_ORDER else len(_PRIMARY_ORDER)),
                entry[1])
    return sorted(entries, key=rank)[0]


def _key_filename(key):
    '''The assets_media file name a storage key or URL is held under, or (stem, None) for content.'''
    key = re.sub(r'^https://[^/]+/', '', key or '')
    m = re.match(r'^users/[^/]+/generated/(' + _UUID + r')/([^/]+)$', key)
    if m:
        return m.group(1) + '_' + m.group(2), None
    m = re.match(r'^users/[^/]+/(' + _UUID + r')/content$', key)
    if m:
        return None, m.group(1)
    m = re.match(r'^imagine-public/images/([^/]+)$', key)
    if m:
        return m.group(1), None
    return None, None


def _check_in(path):
    return check_in_media(path, os.path.basename(path)) if path else None


def _ts(value):
    '''Aware UTC datetime from an ISO string or a BSON date object; raw value otherwise.'''
    if isinstance(value, dict):
        date = value.get('date', value.get('$date'))
        if isinstance(date, dict):
            date = date.get('numberLong', date.get('$numberLong'))
        if isinstance(date, (int, float)) or (isinstance(date, str) and date.lstrip('-').isdigit()):
            return convert_unix_ts_to_utc(int(date) / 1000)
        value = date
    if not value or not isinstance(value, str):
        return '' if value in (None, '', {}) else json.dumps(value)
    m = _ISO.match(value.strip())
    if not m:
        return value
    base, frac, zone = m.groups()
    # Python 3.10 parses only 3 or 6 fraction digits; the return holds 4 and 5 as well.
    frac = ((frac or '') + '000000')[:6]
    zone = '+00:00' if zone in (None, 'Z') else zone
    dt = datetime.fromisoformat(f'{base}.{frac}{zone}')
    return dt.astimezone(timezone.utc)


def _text(value):
    if value is None:
        return ''
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False) if value else ''
    return value


def _lines(values):
    return '\n'.join(str(v) for v in values or [] if v not in (None, ''))


def _source(paths):
    return '\n'.join(sorted(paths))


@artifact_processor
def grokAccount(context):
    profile = _media_index(context, 'profile')
    deletes = {}
    sources = set()
    for user_id, path, records in _record_files(context, 'account-delete-time'):
        sources.add(path)
        for rec in records:
            value = rec.get('accountDeleteTime')
            if isinstance(value, dict):
                value = value.get('deleteTime')
            if value:
                deletes[user_id] = _ts(value)
    data_list = []
    for user_id, path, records in _record_files(context, 'account'):
        sources.add(path)
        for rec in records:
            acct = rec.get('account', rec)
            uid = acct.get('userId', user_id)
            media = [ref for name, p in sorted(profile.items()) if name[0] == user_id
                     for ref in [_check_in(p)] if ref]
            data_list.append((_ts(acct.get('createTime')), deletes.get(user_id, ''), media, uid,
                              acct.get('email') or '', acct.get('givenName') or '',
                              acct.get('familyName') or '', acct.get('emailDomain') or ''))
    data_headers = (('Create Time', 'datetime'), ('Delete Time', 'datetime'),
                    ('Profile Media', 'media'), 'User ID', 'Email', 'Given Name', 'Family Name',
                    'Email Domain')
    return data_headers, data_list, _source(sources)


@artifact_processor
def grokMfaDevices(context):
    data_list = []
    sources = set()
    for _user_id, path, records in _record_files(context, 'multi-factor-devices'):
        sources.add(path)
        for rec in records:
            dev = rec.get('device', rec) if isinstance(rec.get('device'), dict) else rec
            data_list.append((_ts(dev.get('createTime')), _ts(dev.get('confirmedTime')),
                              _ts(dev.get('lastUsedTime')), _text(dev.get('name')),
                              _text(dev.get('deviceType')), _text(dev.get('confirmed')),
                              _text(dev.get('deviceId')), _text(dev.get('userId'))))
    data_headers = (('Create Time', 'datetime'), ('Confirmed Time', 'datetime'),
                    ('Last Used Time', 'datetime'), 'Name', 'Device Type', 'Confirmed',
                    'Device ID', 'User ID')
    return data_headers, data_list, _source(sources)


@artifact_processor
def grokIpLogs(context):
    data_list = []
    sources = set()
    for _user_id, path, records in _record_files(context, 'ip-logs'):
        sources.add(path)
        for rec in records:
            data_list.append((_ts(rec.get('createTime')), _ts(rec.get('lastLoginTime')),
                              _text(rec.get('ipAddress')), _text(rec.get('userId'))))
    data_headers = (('First Login', 'datetime'), ('Last Login', 'datetime'), 'IP Address',
                    'User ID')
    return data_headers, data_list, _source(sources)


@artifact_processor
def grokSessions(context):
    data_list = []
    sources = set()
    for _user_id, path, records in _record_files(context, 'sessions'):
        sources.add(path)
        for rec in records:
            ses = rec.get('session', rec)
            data_list.append((_ts(ses.get('createTime')), _ts(ses.get('lastAuthTime')),
                              _ts(ses.get('expirationTime')), _ts(ses.get('startVerificationTime')),
                              _ts(ses.get('verificationTime')), _text(ses.get('status')),
                              _text(ses.get('sessionId')), _text(ses.get('userId'))))
    data_headers = (('Create Time', 'datetime'), ('Last Auth Time', 'datetime'),
                    ('Expiration Time', 'datetime'), ('Start Verification Time', 'datetime'),
                    ('Verification Time', 'datetime'), 'Status', 'Session ID', 'User ID')
    return data_headers, data_list, _source(sources)


def _conversation_files(context):
    for kind in ('conversations', 'deleted-conversations'):
        for user_id, path, records in _record_files(context, kind):
            yield kind, user_id, path, records


@artifact_processor
def grokConversationList(context):
    data_list = []
    sources = set()
    for kind, _user_id, path, records in _conversation_files(context):
        sources.add(path)
        for rec in records:
            hdr = rec.get('header') or {}
            data_list.append((_ts(hdr.get('createTime')), _ts(hdr.get('modifyTime')),
                              _ts(hdr.get('deleteTime')), _text(hdr.get('title')),
                              len(rec.get('responses') or []), _text(hdr.get('summary')),
                              _text(hdr.get('temporary')), _text(hdr.get('starred')),
                              _lines(hdr.get('assetIds')), _lines(hdr.get('mediaTypes')),
                              _lines(hdr.get('sharedWithUserIds')), _text(hdr.get('xUserId')),
                              _text(hdr.get('id')), _text(hdr.get('userId')), kind + '.txt'))
    data_headers = (('Create Time', 'datetime'), ('Modify Time', 'datetime'),
                    ('Deleted Time', 'datetime'), 'Title', 'Responses', 'Summary', 'Temporary',
                    'Starred', 'Asset IDs', 'Media Types', 'Shared With User IDs', 'X User ID',
                    'Conversation ID', 'User ID', 'Listed In')
    return data_headers, data_list, _source(sources)


@artifact_processor
def grokConversations(context):
    by_id = _files_by_id(_media_index(context, 'assets'))
    data_list = []
    sources = set()
    for kind, user_id, path, records in _conversation_files(context):
        sources.add(path)
        for rec in records:
            hdr = rec.get('header') or {}
            deleted = _ts(hdr.get('deleteTime'))
            for resp in rec.get('responses') or []:
                refs = []
                attachments = [a for a in resp.get('fileAttachments') or [] if a]
                generated = [g for g in resp.get('generatedImageUrls') or [] if g]
                for att in attachments:
                    entries = by_id.get((user_id, att))
                    if entries:
                        refs.append(_check_in(_primary(entries)[2]))
                for url in generated:
                    name, _stem = _key_filename(url)
                    m = re.match(_UUID, name or '')
                    for suffix, fname, fpath in by_id.get((user_id, m.group(0)), []) if m else []:
                        if fname == name and suffix:
                            refs.append(_check_in(fpath))
                refs = list(dict.fromkeys(r for r in refs if r))
                data_list.append((
                    _ts(resp.get('createTime')), deleted, _text(resp.get('sender')),
                    _text(hdr.get('title')), _text(resp.get('message')), refs,
                    _text(resp.get('model')), _text(resp.get('query')),
                    _text(resp.get('queryType')), _lines(attachments), _lines(generated),
                    _text(resp.get('partial')), _text(resp.get('error')), _text(resp.get('id')),
                    _text(resp.get('parentResponseId')), _text(hdr.get('id') or resp.get('conversationId')),
                    _text(hdr.get('userId')), kind + '.txt'))
    data_headers = (('Response Time', 'datetime'), ('Conversation Deleted Time', 'datetime'),
                    'Sender', 'Conversation Title', 'Message', ('Media', 'media'), 'Model',
                    'Search Query', 'Query Type', 'File Attachment IDs', 'Generated Image URLs',
                    'Partial', 'Error', 'Response ID', 'Parent Response ID', 'Conversation ID',
                    'User ID', 'Listed In')
    return data_headers, data_list, _source(sources)


@artifact_processor
def grokAssets(context):
    by_id = _files_by_id(_media_index(context, 'assets'))
    data_list = []
    sources = set()
    for kind in ('asset', 'deleted-asset'):
        for user_id, path, records in _record_files(context, kind):
            sources.add(path)
            for rec in records:
                asset_id = rec.get('assetId') or ''
                entries = by_id.get((user_id, asset_id), [])
                key_name, _stem = _key_filename(rec.get('key'))
                entries = sorted(entries, key=lambda e, k=key_name: (e[1] != k and not
                                                                     (k is None and e[0].startswith('.')),
                                                                     e[1]))
                media = [ref for _s, _n, p in entries for ref in [_check_in(p)] if ref]
                aux = '\n'.join(f'{n} = {v}' for n, v in zip(rec.get('auxNames') or [],
                                                              rec.get('auxKeys') or []))
                if kind == 'deleted-asset' and rec.get('auxKeys'):
                    aux = _lines(rec.get('auxKeys'))
                data_list.append((
                    _ts(rec.get('createTime')), _ts(rec.get('updateTime')),
                    _ts(rec.get('lastUseTime')), _ts(rec.get('deletedTime')),
                    _text(rec.get('name')), media, _text(rec.get('mimeType', rec.get('mime_type'))),
                    _text(rec.get('sizeBytes')), _text(rec.get('fileSource')),
                    _text(rec.get('isModelGenerated')), _text(rec.get('summary')),
                    _text(rec.get('width')), _text(rec.get('height')), aux,
                    _text(rec.get('sourceConversationId')), _text(rec.get('currentConversationId')),
                    _text(rec.get('responseId')), _text(rec.get('postId')),
                    _text(rec.get('mediaKind')), _text(rec.get('rootAssetId')), asset_id,
                    _text(rec.get('key')), _text(rec.get('previewImageKey')),
                    _text(rec.get('userId')), kind + '.txt'))
    data_headers = (('Create Time', 'datetime'), ('Update Time', 'datetime'),
                    ('Last Use Time', 'datetime'), ('Deleted Time', 'datetime'), 'Name',
                    ('Media', 'media'), 'MIME Type', 'Size (bytes)', 'File Source',
                    'Model Generated', 'Summary', 'Width', 'Height', 'Aux Fields',
                    'Source Conversation ID', 'Current Conversation ID', 'Response ID',
                    'Post ID', 'Media Kind', 'Root Asset ID', 'Asset ID', 'Key',
                    'Preview Image Key', 'User ID', 'Listed In')
    return data_headers, data_list, _source(sources)


@artifact_processor
def grokMediaPosts(context):
    index = _media_index(context, 'assets')
    by_id = _files_by_id(index)
    data_list = []
    sources = set()
    for kind in ('media-posts', 'deleted-media-posts'):
        for user_id, path, records in _record_files(context, kind):
            sources.add(path)
            for rec in records:
                name, stem = _key_filename(rec.get('mediaPath'))
                media_path = None
                if name:
                    media_path = index.get((user_id, name))
                elif stem:
                    content = [e for e in by_id.get((user_id, stem), []) if e[0].startswith('.')]
                    media_path = content[0][2] if content else None
                ref = _check_in(media_path)
                data_list.append((
                    _ts(rec.get('createTime')), _ts(rec.get('deletedAt')), _text(rec.get('prompt')),
                    _text(rec.get('originalPrompt')), [ref] if ref else [],
                    _text(rec.get('mediaType')), _text(rec.get('mimeType')),
                    _text(rec.get('originalRefType')), _text(rec.get('id', rec.get('postId'))),
                    _text(rec.get('originalPostId')), _text(rec.get('rootPostId')),
                    _lines(rec.get('extendedVideoPostIds')), _text(rec.get('extra')),
                    _text(rec.get('visibility')), _text(rec.get('mediaPath')),
                    _text(rec.get('userId')), kind + '.txt'))
    data_headers = (('Create Time', 'datetime'), ('Deleted At', 'datetime'), 'Prompt',
                    'Original Prompt', ('Media', 'media'), 'Media Type', 'MIME Type',
                    'Original Ref Type', 'Post ID', 'Original Post ID', 'Root Post ID',
                    'Extended Video Post IDs', 'Extra', 'Visibility', 'Media Path', 'User ID',
                    'Listed In')
    return data_headers, data_list, _source(sources)


def _referenced_ids(context):
    '''Map (user id, uuid) to the record fields of that account that name it.'''
    refs = {}

    def add(user_id, value, label):
        for uid in re.findall(_UUID, value or ''):
            if uid != user_id:
                refs.setdefault((user_id, uid), set()).add(label)
    for kind, label_id, label_key in (('asset', 'asset id', 'asset key'),
                                      ('deleted-asset', 'deleted-asset id', 'deleted-asset key')):
        for user_id, _p, records in _record_files(context, kind):
            for rec in records:
                add(user_id, rec.get('assetId'), label_id)
                for key in [rec.get('key'), rec.get('previewImageKey')] + list(rec.get('auxKeys') or []):
                    add(user_id, key, label_key)
                add(user_id, rec.get('postId'), 'deleted-asset post id')
    for kind in ('media-posts', 'deleted-media-posts'):
        for user_id, _p, records in _record_files(context, kind):
            for rec in records:
                add(user_id, rec.get('id', rec.get('postId')), kind + ' id')
                add(user_id, rec.get('mediaPath'), kind + ' media path')
    for _kind, user_id, _p, records in _conversation_files(context):
        for rec in records:
            for resp in rec.get('responses') or []:
                for att in resp.get('fileAttachments') or []:
                    add(user_id, att, 'response file attachment')
                for url in resp.get('generatedImageUrls') or []:
                    add(user_id, url, 'response generated image')
    return refs


@artifact_processor
def grokMediaFiles(context):
    index = _media_index(context, 'assets')
    refs = _referenced_ids(context)
    data_list = []
    for (user_id, name), path in sorted(index.items()):
        m = re.match(_UUID, name)
        file_id = m.group(0) if m else ''
        ref = _check_in(path)
        data_list.append((name, [ref] if ref else [], '\n'.join(sorted(refs.get((user_id, file_id), ()))),
                          file_id, os.path.getsize(path), user_id))
    data_headers = ('File Name', ('Media', 'media'), 'Referenced By', 'ID', 'Size (bytes)',
                    'User ID')
    # The folders, not each of their files, so the report's located-at line stays readable.
    return data_headers, data_list, _source({os.path.dirname(p) for p in index.values()})
