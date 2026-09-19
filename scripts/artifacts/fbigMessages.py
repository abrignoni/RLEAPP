__artifacts_v2__ = {
    "fbigUnifiedMessages": {
        "name": "Facebook Instagram Returns - Unified Messaging",
        "description": "Direct messages with their attachments rendered inline, from the Unified Messages section of a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2021-08-31",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per message record of every Thread block in the Unified Messages section of records.html and every preservation_N.html; Snapshot File names the file, and a message that appears in two snapshots is reported once per snapshot. "
                 "Direction is 'Outgoing' when the numeric Instagram id in the message's Author equals the request parameter Target (the account's numeric identifier per the provider's embedded definitions) and 'Incoming' otherwise; it is blank when Target is not numeric or the Author carries no id. On the return this was built against, the messages whose Author id equalled Target were exactly the messages whose Author username equalled the Vanity Name printed in the same snapshot file, in all three snapshots. "
                 "Thread ID is the identifier printed at the head of the Thread block, parentheses removed. Conversation is that identifier followed by the snapshot file in parentheses, and it is what LAVA's conversation view groups on, so each snapshot's copy of a thread is its own conversation. The tested return carried two threads in all three snapshots, and for each the three snapshots held the same messages when matched on Sent, Direction, Author Instagram ID and Linked Media File, so grouping by Thread ID alone showed each of those messages three times. "
                 "The copies were not all identical: preservation_1.html, which printed a different Vanity Name from the other two snapshots, also printed a different Author on 60 messages of one thread and 61 of the other and a different Body on 6, and each snapshot printed its own Attachment URL for every message carrying one. "
                 "Body is reported as stored; per the provider's definition it is the text of the communication or a description of the content type sent. On the tested return the Body of a message carrying an attachment or a share was a sentence of the form '<name> sent a ...' on every such message in two snapshots and on 2,549 of 2,587 in the third. "
                 "Media renders every linked_media file named by the message's Attachments blocks; the attachment columns join one value per attachment with ' | ' when a message carries more than one (19 messages of one snapshot on the tested return). Attachment Name (as stored) is the text the provider prints at the head of each Attachments block (an identifier in parentheses, preceded on some records by a file name, on the tested return; the provider does not define it). "
                 "Share Date Created is kept as text because the provider printed 'Unknown' on most share records of the tested return. Call Missed and Call Duration come from a Call Record block; the provider defines Duration as the length of the call in seconds. Subscription Event Type and Users come from a Subscription Event block (an account joining or leaving the thread). "
                 "A record with a Body but no Author or Sent is reported with those columns blank; the tested return held fourteen across its three snapshots, each printed directly after a subscription event message. Disappearing Message and Disappearing Duration are reported as stored, and a message lacking the Disappearing Message field leaves that column blank (15 of 803 message records in one snapshot of the tested return). "
                 "Records, and single fields, split across the return's page breaks are rejoined before reporting; on the tested return the row count of each file equalled the number of 'Author' labels in its source text plus its records without an Author. "
                 "Author is the username part of the stored Author value; the numeric id is in Author Instagram ID, and no message Author on the tested return carried a bracketed display name, which is why there is no display name column here. Audio attachments are named '.mp3' and labelled audio/mpeg by the provider but are ISO-BMFF files with a single sound track on the tested return; the report types them by their track handlers so they render as audio rather than video. Thread-level fields (participants, read receipts, AI) are in the Thread Participants artifact; every attachment is also listed one per row in the Message Attachments artifact, and calls in the Calls artifact.",
        "paths": ('*/records.html', '*/preservation*.html', '*/linked_media/*'),
        "output_types": "standard",
        "artifact_icon": "message",
        "data_views": {
            "conversation": {
                "conversationDiscriminatorColumn": "Conversation",
                "conversationLabelColumn": "Conversation",
                "textColumn": "Body",
                "directionColumn": "Direction",
                # Not 'Sent': the LAVA writer rewrites any conversation view value equal to a
                # column name into that column's SQL name, and 'Sent' is the time column here.
                "directionSentValue": "Outgoing",
                "timeColumn": "Sent",
                "senderColumn": "Author",
                "mediaColumn": "Media",
            }
        },
    },
    "fbigThreadParticipants": {
        "name": "Facebook Instagram Returns - Thread Participants",
        "description": "Per-thread participants, settings and message span from the Unified Messages section of a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2021-08-31",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per Thread block of the Unified Messages section of records.html and every preservation_N.html; Snapshot File names the file. "
                 "Current Participants and Past Participants are reported as stored, one entry per line. On the tested return the first line of each was a 'YYYY-MM-DD HH:MM:SS UTC' timestamp and the following lines were accounts as 'username (Instagram: numeric id)'; the provider's embedded definition describes the participants ('account holders included in conversation thread' and 'previously subscribed') but does not say what that leading timestamp marks, so no meaning is assigned to it. "
                 "AI and Read Receipts are the thread-level values as stored; per the definition AI is whether the thread includes messages generated by generative AI and Read Receipts is the thread-level read receipt setting. "
                 "Messages counts the message records of the thread in that snapshot, and First Sent and Last Sent are the earliest and latest Sent values among them.",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "users",
    },
    "fbigMessageAttachments": {
        "name": "Facebook Instagram Returns - Message Attachments",
        "description": "Message attachments, one per row with its linked media file, from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-19",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per Attachments block of every message in the Unified Messages section of records.html and every preservation_N.html, plus one row per file in the return's linked_media folder that no snapshot file references (Sent, Author and Thread ID blank, Linked Media File naming the file). "
                 "On the return this was built against every one of the 1,549 files in linked_media was referenced by at least one snapshot file, so the unreferenced-file rows are unexercised. "
                 "Type is the attachment type as stored (a MIME type such as audio/mpeg, video/mp4 or image/jpeg on the tested return), Size the size as stored, Product Type as stored (PERMANENT, REPLAYABLE or VIEW ONCE on the tested return; the provider does not define these values), URL the provider's link to the content, and Attachment Name (as stored) the text printed at the head of the block. "
                 "The same file is referenced from records.html and from a preservation snapshot when both carry the message, so it appears once per snapshot. Audio attachments are named '.mp3' and labelled audio/mpeg by the provider but are ISO-BMFF files with a single sound track on the tested return (all 648 of them; every '.mp4' carried a video track); Media types them by their track handlers so they render as audio rather than video.",
        "paths": ('*/records.html', '*/preservation*.html', '*/linked_media/*'),
        "output_types": "standard",
        "artifact_icon": "paperclip",
    },
    "fbigCalls": {
        "name": "Facebook Instagram Returns - Calls",
        "description": "Call records found inside message threads (missed flag and duration), from a Meta (Instagram) law enforcement return.",
        "author": "@AlexisBrignoni, Claude",
        "creation_date": "2026-09-19",
        "last_update_date": "2026-09-19",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "One row per message record carrying a Call Record block, from the Unified Messages section of records.html and every preservation_N.html; Snapshot File names the file. "
                 "Per the provider's embedded definition a Call Record indicates a call was made through a conversation thread, Missed whether the call was missed, and Duration the length of the call in seconds; the definition also lists a Type (the method in which the call was placed), which the tested return did not carry and which lands in Other Fields when present. "
                 "Direction and Author are computed as in the Unified Messaging artifact. Body is the provider's text for the call event as stored. On the tested return every call record sat in one thread, so Thread ID was uniform.",
        "paths": ('*/records.html', '*/preservation*.html'),
        "output_types": "standard",
        "artifact_icon": "phone",
    },
}

import os

from scripts.ilapfuncs import artifact_processor, check_in_media, logfunc
from scripts import meta_records as mr


def _sources(context):
    return mr.records_files(context.get_files_found())


def _threads(rec):
    """(thread id, header records, message records) per Thread block of a snapshot."""
    for record in rec.records('unified_messages'):
        for thread in mr.subs(record, 'Thread'):
            thread_id = thread.text.strip().strip('()').strip()
            headers, messages = [], []
            for block in thread.value:
                if any(item.label in ('Author', 'Sent', 'Body') for item in block):
                    messages.append(block)
                else:
                    headers.append(block)
            yield thread_id, headers, messages


def _direction(author, target_id):
    author_id = mr.account_id(author)
    if not target_id or not author_id:
        return ''
    return 'Outgoing' if author_id == target_id else 'Incoming'


def _attachments(message):
    """One dict per Attachments block of a message."""
    out = []
    for block in mr.subs(message, 'Attachments'):
        for group in block.value:
            names = mr.linked_media_files(group)
            out.append({
                'Type': mr.text(group, 'Type'),
                'Size': mr.text(group, 'Size'),
                'Product Type': mr.text(group, 'Product Type'),
                'URL': mr.text(group, 'URL') or mr.text(group, 'Url'),
                'Name': block.text,
                'files': names,
            })
    return out


def _register(context, names):
    return mr.register_media(context, names)


def _joined(attachments, key):
    return ' | '.join(a[key] for a in attachments if a[key])


@artifact_processor
def fbigUnifiedMessages(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for thread_id, _, messages in _threads(rec):
            for message in messages:
                author = mr.text(message, 'Author')
                username, author_id, _ = mr.parse_account(author)
                attachments = _attachments(message)
                files = [name for a in attachments for name in a['files']]
                shares = [group for block in mr.subs(message, 'Share') for group in block.value]
                calls = [group for block in mr.subs(message, 'Call Record') for group in block.value]
                events = [group for block in mr.subs(message, 'Subscription Event') for group in block.value]
                data_list.append((
                    mr.parse_ts(mr.text(message, 'Sent')),
                    _direction(author, rec.target_id),
                    username or author,
                    f'{thread_id} ({rec.name})',
                    mr.text(message, 'Body'),
                    _register(context, files) or None,
                    thread_id,
                    _joined(attachments, 'Type'), _joined(attachments, 'Size'),
                    _joined(attachments, 'Product Type'), _joined(attachments, 'URL'),
                    _joined(attachments, 'Name'), '\n'.join(files),
                    ' | '.join(mr.text(s, 'Date Created') for s in shares),
                    ' | '.join(mr.text(s, 'Text') for s in shares),
                    ' | '.join(mr.text(s, 'Url') or mr.text(s, 'URL') for s in shares),
                    ' | '.join(mr.text(c, 'Missed') for c in calls),
                    ' | '.join(mr.text(c, 'Duration') for c in calls),
                    ' | '.join(mr.text(e, 'Type') for e in events),
                    ' | '.join(mr.text(e, 'Users') for e in events),
                    mr.text(message, 'Disappearing Message'), mr.text(message, 'Disappearing Duration'),
                    author_id, rec.name))
    data_headers = (('Sent', 'datetime'), 'Direction', 'Author', 'Conversation', 'Body', ('Media', 'media'),
                    'Thread ID', 'Attachment Type', 'Attachment Size', 'Attachment Product Type', 'Attachment URL',
                    'Attachment Name (as stored)', 'Linked Media File', 'Share Date Created (as stored)',
                    'Share Text', 'Share URL', 'Call Missed', 'Call Duration', 'Subscription Event Type',
                    'Subscription Event Users', 'Disappearing Message', 'Disappearing Duration',
                    'Author Instagram ID', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def fbigThreadParticipants(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for thread_id, headers, messages in _threads(rec):
            values = {}
            for block in headers:
                for item in block:
                    if isinstance(item.value, str):
                        values[item.label] = item.value
            sent = [mr.parse_ts(mr.text(m, 'Sent')) for m in messages]
            sent = [s for s in sent if s]
            data_list.append((min(sent) if sent else '', max(sent) if sent else '', thread_id,
                              values.get('Current Participants', ''), values.get('Past Participants', ''),
                              values.get('AI', ''), values.get('Read Receipts', ''), len(messages), rec.name))
    data_headers = (('First Sent', 'datetime'), ('Last Sent', 'datetime'), 'Thread ID', 'Current Participants',
                    'Past Participants', 'AI', 'Read Receipts', 'Messages', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def fbigMessageAttachments(context):
    data_list = []
    sources = _sources(context)
    referenced = set()
    for path in sources:
        rec = mr.load(path)
        for thread_id, _, messages in _threads(rec):
            for message in messages:
                author = mr.text(message, 'Author')
                for attachment in _attachments(message):
                    referenced.update(os.path.basename(n) for n in attachment['files'])
                    data_list.append((mr.parse_ts(mr.text(message, 'Sent')), _direction(author, rec.target_id),
                                      mr.parse_account(author)[0] or author, thread_id,
                                      _register(context, attachment['files']) or None, attachment['Type'],
                                      attachment['Size'], attachment['Product Type'], attachment['URL'],
                                      attachment['Name'], '\n'.join(attachment['files']), rec.name))
        for section in ('photos', 'videos', 'archived_stories', 'profile_picture'):
            for record in rec.records(section):
                referenced.update(os.path.basename(n) for n in mr.linked_media_files(record))
    orphans = 0
    for file_found in context.get_files_found():
        file_found = str(file_found)
        parent = os.path.basename(os.path.dirname(file_found))
        if parent != 'linked_media' or not os.path.isfile(file_found):
            continue
        name = os.path.basename(file_found)
        if name in referenced:
            continue
        orphans += 1
        ref = check_in_media(file_found, name, force_type=mr.media_type_hint(file_found))
        data_list.append(('', '', '', '', ref, '', '', '', '', '', f'linked_media/{name}', ''))
    if orphans:
        logfunc(f'Message Attachments: {orphans} linked_media file(s) not referenced by any records file')
    data_headers = (('Sent', 'datetime'), 'Direction', 'Author', 'Thread ID', ('Media', 'media'), 'Type', 'Size',
                    'Product Type', 'URL', 'Attachment Name (as stored)', 'Linked Media File', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)


@artifact_processor
def fbigCalls(context):
    data_list = []
    sources = _sources(context)
    for path in sources:
        rec = mr.load(path)
        for thread_id, _, messages in _threads(rec):
            for message in messages:
                calls = [group for block in mr.subs(message, 'Call Record') for group in block.value]
                if not calls:
                    continue
                author = mr.text(message, 'Author')
                for call in calls:
                    other = [f'{item.label}: {item.value}' for item in call
                             if isinstance(item.value, str) and item.label not in ('Missed', 'Duration')]
                    data_list.append((mr.parse_ts(mr.text(message, 'Sent')), _direction(author, rec.target_id),
                                      mr.parse_account(author)[0] or author, thread_id, mr.text(message, 'Body'),
                                      mr.text(call, 'Missed'), mr.text(call, 'Duration'), '\n'.join(other),
                                      rec.name))
    data_headers = (('Sent', 'datetime'), 'Direction', 'Author', 'Thread ID', 'Body', 'Missed', 'Duration',
                    'Other Fields', 'Snapshot File')
    return data_headers, data_list, '\n'.join(sources)
