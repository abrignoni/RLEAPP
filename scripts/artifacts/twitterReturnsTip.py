__artifacts_v2__ = {
    'twitterDirectMessages': {
        'name': 'Twitter Returns - Direct Messages',
        'description': (
            'Direct messages from the direct-messages file of a Twitter law enforcement return. '
            'String values are decoded as the JSON string printed on each line, keeping commas, '
            'double quotes and colons. Only the first media URL, reaction and URL of a message '
            'are read. Reaction Timestamp is read from the first reaction when its labelled '
            'timestamp field is present.'
        ),
        'author': '@AlexisBrignoni, Codex',
        'creation_date': '2022-06-12',
        'last_update_date': '2026-10-09',
        'requirements': 'none',
        'category': 'Twitter Returns',
        'notes': (
            'Time columns preserve mixed values as text and do not populate timeline/date '
            'filters.'
        ),
        'paths': ('**/*-direct-messages.txt',),
        'output_types': 'standard',
        'artifact_icon': 'message-circle',
    },
    'twitterAccountCreationIp': {
        'name': 'Twitter Returns - Account Creation IP',
        'description': 'Account Creation IP from a Twitter law enforcement return.',
        'author': '@AlexisBrignoni, Codex',
        'creation_date': '2022-06-12',
        'last_update_date': '2026-10-09',
        'requirements': 'none',
        'category': 'Twitter Returns',
        'notes': (
            'Time columns preserve mixed values as text and do not populate timeline/date '
            'filters.'
        ),
        'paths': ('**/*-account-creation-ip.txt',),
        'output_types': 'standard',
        'artifact_icon': 'globe',
    },
    'twitterAccountSuspension': {
        'name': 'Twitter Returns - Account Suspension',
        'description': 'Account Suspension from a Twitter law enforcement return.',
        'author': '@AlexisBrignoni, Codex',
        'creation_date': '2022-06-12',
        'last_update_date': '2026-10-09',
        'requirements': 'none',
        'category': 'Twitter Returns',
        'notes': (
            'Time columns preserve mixed values as text and do not populate timeline/date '
            'filters.'
        ),
        'paths': ('**/*-account-suspension.txt',),
        'output_types': 'standard',
        'artifact_icon': 'alert-octagon',
    },
    'twitterAccount': {
        'name': 'Twitter Returns - Account',
        'description': (
            'Account details from the account file of a Twitter law enforcement return. String '
            'values are decoded as the JSON string printed on each line, keeping commas, double '
            'quotes and colons.'
        ),
        'author': '@AlexisBrignoni, Codex',
        'creation_date': '2022-06-12',
        'last_update_date': '2026-10-09',
        'requirements': 'none',
        'category': 'Twitter Returns',
        'notes': (
            'Time columns preserve mixed values as text and do not populate timeline/date '
            'filters.'
        ),
        'paths': ('**/*-account.txt',),
        'output_types': 'standard',
        'artifact_icon': 'user',
    },
    'twitterAgeInfo': {
        'name': 'Twitter Returns - Age Info',
        'description': 'Age Info from a Twitter law enforcement return.',
        'author': '@AlexisBrignoni, Codex',
        'creation_date': '2022-06-12',
        'last_update_date': '2026-10-09',
        'requirements': 'none',
        'category': 'Twitter Returns',
        'notes': (
            'Time columns preserve mixed values as text and do not populate timeline/date '
            'filters.'
        ),
        'paths': ('**/*-ageinfo.txt',),
        'output_types': 'standard',
        'artifact_icon': 'calendar',
    },
    'twitterBlock': {
        'name': 'Twitter Returns - Block',
        'description': 'Block from a Twitter law enforcement return.',
        'author': '@AlexisBrignoni, Codex',
        'creation_date': '2022-06-12',
        'last_update_date': '2026-10-09',
        'requirements': 'none',
        'category': 'Twitter Returns',
        'notes': (
            'Time columns preserve mixed values as text and do not populate timeline/date '
            'filters.'
        ),
        'paths': ('**/*-block.txt',),
        'output_types': 'standard',
        'artifact_icon': 'slash',
    },
    'twitterDeviceToken': {
        'name': 'Twitter Returns - Device Token',
        'description': 'Device Token from a Twitter law enforcement return.',
        'author': '@AlexisBrignoni, Codex',
        'creation_date': '2022-06-12',
        'last_update_date': '2026-10-09',
        'requirements': 'none',
        'category': 'Twitter Returns',
        'notes': (
            'Time columns preserve mixed values as text and do not populate timeline/date '
            'filters.'
        ),
        'paths': ('**/*-device-token.txt',),
        'output_types': 'standard',
        'artifact_icon': 'smartphone',
    },
    'twitterFollower': {
        'name': 'Twitter Returns - Follower',
        'description': 'Follower from a Twitter law enforcement return.',
        'author': '@AlexisBrignoni, Codex',
        'creation_date': '2022-06-12',
        'last_update_date': '2026-10-09',
        'requirements': 'none',
        'category': 'Twitter Returns',
        'notes': (
            'Time columns preserve mixed values as text and do not populate timeline/date '
            'filters.'
        ),
        'paths': ('**/*-follower.txt',),
        'output_types': 'standard',
        'artifact_icon': 'users',
    },
    'twitterFollowing': {
        'name': 'Twitter Returns - Following',
        'description': 'Following from a Twitter law enforcement return.',
        'author': '@AlexisBrignoni, Codex',
        'creation_date': '2022-06-12',
        'last_update_date': '2026-10-09',
        'requirements': 'none',
        'category': 'Twitter Returns',
        'notes': (
            'Time columns preserve mixed values as text and do not populate timeline/date '
            'filters.'
        ),
        'paths': ('**/*-following.txt',),
        'output_types': 'standard',
        'artifact_icon': 'users',
    },
    'twitterIpAudit': {
        'name': 'Twitter Returns - IP Audit',
        'description': 'IP Audit from a Twitter law enforcement return.',
        'author': '@AlexisBrignoni, Codex',
        'creation_date': '2022-06-12',
        'last_update_date': '2026-10-09',
        'requirements': 'none',
        'category': 'Twitter Returns',
        'notes': (
            'Time columns preserve mixed values as text and do not populate timeline/date '
            'filters.'
        ),
        'paths': ('**/*-ip-audit.txt',),
        'output_types': 'standard',
        'artifact_icon': 'log-in',
    },
    'twitterLike': {
        'name': 'Twitter Returns - Like',
        'description': (
            'Liked tweets from the like file of a Twitter law enforcement return. Tweet ID, Full '
            'Text and Expanded URL are decoded from JSON string fields in the line-oriented '
            'return, preserving punctuation and escaped text. Records with malformed or '
            'non-string fields are skipped and logged.'
        ),
        'author': '@AlexisBrignoni, Codex',
        'creation_date': '2022-06-12',
        'last_update_date': '2026-10-09',
        'requirements': 'none',
        'category': 'Twitter Returns',
        'notes': (
            'Time columns preserve mixed values as text and do not populate timeline/date '
            'filters.'
        ),
        'paths': ('**/*-like.txt',),
        'output_types': 'standard',
        'artifact_icon': 'heart',
    },
    'twitterMute': {
        'name': 'Twitter Returns - Mute',
        'description': 'Mute from a Twitter law enforcement return.',
        'author': '@AlexisBrignoni, Codex',
        'creation_date': '2022-06-12',
        'last_update_date': '2026-10-09',
        'requirements': 'none',
        'category': 'Twitter Returns',
        'notes': (
            'Time columns preserve mixed values as text and do not populate timeline/date '
            'filters.'
        ),
        'paths': ('**/*-mute.txt',),
        'output_types': 'standard',
        'artifact_icon': 'volume-x',
    },
    'twitterTweet': {
        'name': 'Twitter Returns - Tweet',
        'description': (
            'Tweets from the tweet file of a Twitter law enforcement return. Full Text is decoded '
            'as the JSON string printed on its line, keeping commas, double quotes and colons. '
            'created_at is converted using its printed offset. Each distinct media_url file name '
            "of a tweet is looked up once among the return's media files. Video is linked only "
            'for a variant listed at bitrate 2176000.'
        ),
        'author': '@AlexisBrignoni, Codex',
        'creation_date': '2022-06-12',
        'last_update_date': '2026-10-09',
        'requirements': 'none',
        'category': 'Twitter Returns',
        'notes': (
            'Time columns preserve mixed values as text and do not populate timeline/date '
            'filters.'
        ),
        'paths': ('**/*-tweet.txt',),
        'output_types': 'standard',
        'artifact_icon': 'twitter',
    },
}

import os
import json
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, check_in_media, logfunc


def timestamps(line):
    """Read the printed ISO time without discarding its offset."""
    value = line.split(':', 1)[1].strip().rstrip(',')
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return value.strip('"')


def _to_utc(value):
    if value in (None, ''):
        return ''
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc) if value.tzinfo else value.isoformat(sep=' ')
    text = str(value).strip()
    try:
        dt = datetime.fromisoformat(text.replace('Z', '+00:00'))
        return value if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        return value


def _value(line):
    """Return the value printed after a line's first colon.

    A JSON string is decoded whole, so commas, double quotes and colons inside
    it are kept. Any other value is returned as printed.
    """
    payload = line.partition(':')[2].strip()
    try:
        value, end = json.JSONDecoder().raw_decode(payload)
    except ValueError:
        value, end = None, 0
    if isinstance(value, str) and payload[end:].strip() in ('', ','):
        return value
    return line.split(': ')[1].replace('"', '').replace(',', '').strip()


def _two_field(context, suffix, key_a, key_b, headers):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).endswith(suffix):
            continue
        source_path = file_found
        value_a = ''
        with open(file_found, encoding='utf-8') as f:
            for line in f:
                if key_a in line:
                    value_a = _value(line)
                elif key_b in line:
                    data_list.append((value_a, _value(line)))
    return tuple(headers), data_list, context.get_relative_path(source_path)


@artifact_processor
def twitterAccountCreationIp(context):
    return _two_field(context, '-account-creation-ip.txt', '"accountId"', '"userCreationIp"',
                      ('Account ID', 'User Creation IP'))


@artifact_processor
def twitterBlock(context):
    return _two_field(context, '-block.txt', '"accountId"', '"userLink"',
                      ('Account ID', 'User Link'))


@artifact_processor
def twitterFollower(context):
    return _two_field(context, '-follower.txt', '"accountId"', '"userLink"',
                      ('Account ID', 'User Link'))


@artifact_processor
def twitterFollowing(context):
    return _two_field(context, '-following.txt', '"accountId"', '"userLink"',
                      ('Account ID', 'User Link'))


@artifact_processor
def twitterMute(context):
    return _two_field(context, '-mute.txt', '"accountId"', '"userLink"',
                      ('Account ID', 'User Link'))


@artifact_processor
def twitterAccountSuspension(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).endswith('-account-suspension.txt'):
            continue
        source_path = file_found
        timestamp = ''
        with open(file_found, encoding='utf-8') as f:
            for line in f:
                if '"timeStamp"' in line:
                    timestamp = timestamps(line)
                elif '"action"' in line:
                    data_list.append((_to_utc(timestamp), _value(line)))
    data_headers = ('Timestamp', 'Action')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def twitterAccount(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).endswith('-account.txt'):
            continue
        source_path = file_found
        email = timestamp = accountid = cvia = usern = accdn = ''
        with open(file_found, encoding='utf-8') as f:
            for line in f:
                if '"createdAt"' in line:
                    timestamp = timestamps(line)
                elif '"accountId"' in line:
                    accountid = _value(line)
                elif '"email" :' in line:
                    email = _value(line)
                elif '"createdVia"' in line:
                    cvia = _value(line)
                elif '"username"' in line:
                    usern = _value(line)
                elif '"accountDisplayName"' in line:
                    accdn = _value(line)
        data_list.append((_to_utc(timestamp), accountid, email, cvia, usern, accdn))
    data_headers = ('Created At', 'Account ID', 'Email', 'Created Via', 'Username',
                    'Account Display Name')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def twitterAgeInfo(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).endswith('-ageinfo.txt'):
            continue
        source_path = file_found
        age = ''
        with open(file_found, encoding='utf-8') as f:
            for line in f:
                if '"age" :' in line:
                    line = line.strip()
                    if line.endswith(']'):
                        age = ''
                    else:
                        age = next(f).replace('"', '').strip()
                elif '"birthDate"' in line:
                    birth = line.split(': ')[1].replace('"', '').strip()
                    data_list.append((birth, age))
    data_headers = ('Birthdate', 'Age')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def twitterDeviceToken(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).endswith('-device-token.txt'):
            continue
        source_path = file_found
        token = lastseen = clientappid = clientappname = ''
        with open(file_found, encoding='utf-8') as f:
            for line in f:
                if '"token" :' in line:
                    token = _value(line)
                elif '"lastSeenAt"' in line:
                    lastseen = timestamps(line)
                elif '"clientApplicationId"' in line:
                    clientappid = _value(line)
                elif '"clientApplicationName"' in line:
                    clientappname = _value(line)
                elif '"createdAt"' in line:
                    data_list.append((_to_utc(timestamps(line)), _to_utc(lastseen), clientappid,
                                      clientappname, token))
    data_headers = ('Created At', 'Last Seen At',
                    'Client Application ID', 'Client Application Name', 'Token')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def twitterIpAudit(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).endswith('-ip-audit.txt'):
            continue
        source_path = file_found
        accid = timestampt = ''
        with open(file_found, encoding='utf-8') as f:
            for line in f:
                if '"accountId"' in line:
                    accid = _value(line)
                elif '"createdAt"' in line:
                    timestampt = timestamps(line)
                elif '"loginIp"' in line:
                    data_list.append((_to_utc(timestampt), _value(line), accid))
    data_headers = ('Created At', 'Login IP', 'Account ID')
    return data_headers, data_list, context.get_relative_path(source_path)


def _like_string(line):
    """Decode a complete string field, allowing only its structural trailing comma."""
    _, separator, payload = line.partition(':')
    if not separator:
        raise ValueError('Missing field separator')
    value, end = json.JSONDecoder().raw_decode(payload.lstrip())
    if not isinstance(value, str) or payload.lstrip()[end:].strip() not in ('', ','):
        raise ValueError('Expected one JSON string field')
    return value


@artifact_processor
def twitterLike(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).endswith('-like.txt'):
            continue
        source_path = file_found
        tweetid = fulltxt = ''
        invalid = False
        with open(file_found, encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                field = line.partition(':')[0].strip()
                if field not in ('"tweetId"', '"fullText"', '"expandedUrl"'):
                    continue
                if field == '"tweetId"':
                    tweetid = fulltxt = ''
                    invalid = False
                try:
                    value = _like_string(line)
                except ValueError:
                    invalid = True
                    logfunc(f'Twitter Like: skipped invalid string field at '
                            f'{context.get_relative_path(file_found)}:{line_number}')
                else:
                    if field == '"tweetId"':
                        tweetid = value
                    elif field == '"fullText"':
                        fulltxt = value
                    elif not invalid:
                        data_list.append((tweetid, fulltxt, value))
                if field == '"expandedUrl"':
                    tweetid = fulltxt = ''
                    invalid = False
    data_headers = ('Tweet ID', 'Full Text', 'Expanded URL')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def twitterDirectMessages(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).endswith('-direct-messages.txt'):
            continue
        source_path = file_found
        convoid = idc = sid = rid = text = thumb = mediaurl = ''
        url = expanded = display = rtimestamp = rsenderid = reactkey = reventid = timestamp = ''
        with open(file_found, encoding='utf-8') as f:
            for line in f:
                if '**** conversationId:' in line:
                    convoid = line.split(': ')[1].replace('*', '').strip()
                elif '"id" :' in line:
                    idc = _value(line)
                elif '"senderId" :' in line:
                    sid = _value(line)
                elif '"recipientId" :' in line:
                    rid = _value(line)
                elif '"text" :' in line:
                    text = _value(line)
                elif '"createdAt" :' in line:
                    timestamp = timestamps(line)
                elif '"mediaUrls" :' in line:
                    line = line.strip()
                    if line.endswith('[ ],'):
                        mediaurl = thumb = ''
                    else:
                        mediaurl = next(f).replace('"', '').strip()
                        if 'ton' in mediaurl:
                            thumb = check_in_media(mediaurl.split('/')[-1], mediaurl.split('/')[-1])
                        elif 'video' in mediaurl:
                            ident = mediaurl.split('/')[-1].split('?')[0]
                            thumb = check_in_media(ident, ident)
                        else:
                            thumb = ''
                elif '"reactions" :' in line:
                    line = line.strip()
                    if line.endswith('[ ],'):
                        reactkey = rsenderid = reventid = rtimestamp = ''
                    else:
                        next(f)
                        rsenderid = _value(next(f))
                        reactkey = _value(next(f))
                        reventid = _value(next(f))
                        extraline = next(f)
                        if 'timestamp' in extraline.lower() or 'createdat' in extraline.lower():
                            rtimestamp = timestamps(extraline)
                elif '"urls" :' in line:
                    line = line.strip()
                    if line.endswith(']'):
                        url = expanded = display = ''
                    else:
                        next(f)
                        url = _value(next(f))
                        expanded = _value(next(f))
                        extraline = next(f)
                        if extraline != '':
                            display = _value(extraline)
                    data_list.append((_to_utc(timestamp), _to_utc(rtimestamp), convoid, sid, rid, text, thumb, mediaurl,
                                      url, expanded, display, rsenderid,
                                      reactkey, reventid, idc))
                    timestamp = sid = rid = text = mediaurl = url = expanded = display = ''
                    rtimestamp = rsenderid = reactkey = reventid = idc = thumb = ''
    data_headers = ('Created At', 'Reaction Timestamp', 'Conversation ID', 'Sender ID', 'Recipient ID',
                    'Text', ('Media', 'media'), 'Media URL', 'URL', 'Expanded URL', 'Display URL',
                    'Reaction Sender ID', 'Reaction',
                    'Reaction Event ID', 'ID')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def twitterTweet(context):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not os.path.basename(file_found).endswith('-tweet.txt'):
            continue
        source_path = file_found
        msgbase = 0
        media_seen = set()
        media_refs, video_ref = [], ''
        createdat = fulltext = ''
        with open(file_found, encoding='utf-8') as f:
            for line in f:
                if '**** id: ' in line:
                    if msgbase == 0:
                        msgbase = 1
                    else:
                        data_list.append((_to_utc(_tweet_date(createdat)), fulltext, media_refs,
                                          video_ref))
                        media_seen = set()
                        fulltext = ''
                        media_refs, video_ref = [], ''
                elif "-----END PGP SIGNATURE-----" in line:
                    if createdat != '':
                        data_list.append((_to_utc(_tweet_date(createdat)), fulltext, media_refs,
                                          video_ref))
                elif '"created_at" : ' in line:
                    createdat = _value(line)
                elif '"full_text" : ' in line:
                    fulltext = _value(line)
                elif '"media_url" : ' in line:
                    # The same media_url is printed under entities and again under
                    # extended_entities, so each file name is looked up once per tweet.
                    ident = _value(line).split('/')[-1].split('.')[0]
                    if ident and ident not in media_seen:
                        media_seen.add(ident)
                        ref = check_in_media(ident, ident)
                        if ref:
                            media_refs.append(ref)
                elif '"bitrate" : "2176000"' in line:
                    next(f)
                    videomedia = next(f).split('/')[-1].split('?')[0].replace('"', '').strip()
                    video_ref = check_in_media(videomedia, videomedia)
    data_headers = ('Timestamp', 'Full Text', ('Media', 'media'), ('Video', 'media'))
    return data_headers, data_list, context.get_relative_path(source_path)


def _tweet_date(createdat):
    try:
        return datetime.strptime(createdat.replace("'", '').strip(), '%a %b %d %H:%M:%S %z %Y').astimezone(timezone.utc)
    except ValueError:
        return createdat
