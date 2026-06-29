def _meta(name, basename, icon, html_columns=None):
    meta = {"name": f"Reddit - {name}",
            "description": f"{name} from a Reddit law enforcement return ({basename}).",
            "author": "@AlexisBrignoni", "creation_date": "2023-04-22",
            "last_update_date": "2026-06-28", "requirements": "none",
            "category": "Reddit Returns", "notes": "Source File column preserves the per-account "
            "path (username/email) the original encoded in the report title.",
            "paths": (f'**/{basename}',), "output_types": "standard", "artifact_icon": icon}
    if html_columns:
        meta["html_columns"] = html_columns
    return meta


__artifacts_v2__ = {
    "redditChatHistory": _meta("Chat History", "chat_history.csv", "message-circle"),
    "redditCommentVotes": _meta("Comment Votes", "comment_votes.csv", "thumbs-up"),
    "redditComments": _meta("Comments", "comments.csv", "message-square"),
    "redditDrafts": _meta("Drafts", "drafts.csv", "edit"),
    "redditGildedComments": _meta("Gilded Comments", "gilded_comments.csv", "award"),
    "redditGildedPosts": _meta("Gilded Posts", "gilded_posts.csv", "award"),
    "redditHiddenPosts": _meta("Hidden Posts", "hidden_posts.csv", "eye-off"),
    "redditIpLogs": _meta("IP Logs", "ip_logs.csv", "globe"),
    "redditRegistrationIp": _meta("Registration IP", "ip_logs.csv", "user-check"),
    "redditLinkedPhone": _meta("Linked Phone", "linked_phone_number.csv", "phone"),
    "redditLiveStreamPosts": _meta("Live Stream Posts", "live_stream_posts.csv", "video"),
    "redditMessages": _meta("Messages", "messages.csv", "mail"),
    "redditPollVotes": _meta("Poll Votes", "poll_votes.csv", "bar-chart-2"),
    "redditPostVotes": _meta("Post Votes", "post_votes.csv", "arrow-up"),
    "redditPosts": _meta("Posts", "posts.csv", "file-text"),
    "redditGoldInformation": _meta("Reddit Gold Info", "reddit_gold_information.csv", "star"),
    "redditSavedComments": _meta("Saved Comments", "saved_comments.csv", "bookmark"),
    "redditSavedPosts": _meta("Saved Posts", "saved_posts.csv", "bookmark"),
    "redditScheduledPosts": _meta("Scheduled Posts", "scheduled_posts.csv", "clock"),
    "redditStatistics": _meta("Statistics", "statistics.csv", "activity"),
    "redditUserPreferences": _meta("User Prefs", "user_preferences.csv", "settings"),
}

import csv
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


def _ts(value):
    if value in (None, ''):
        return ''
    text = str(value).replace('UTC', '').strip()
    if not text:
        return ''
    if text.isdigit():
        return convert_unix_ts_to_utc(int(text))
    try:
        dt = datetime.fromisoformat(text.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        return value


def _csv(context, basename, headers, build_row, min_len):
    data_list, source_path = [], ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        base = os.path.basename(file_found)
        if base.startswith('.') or not base.startswith(basename):
            continue
        source_path = file_found
        rel = context.get_relative_path(file_found)
        with open(file_found, encoding='unicode_escape') as f:
            reader = csv.reader(f)
            next(reader, None)  # header row
            for row in reader:
                if len(row) < min_len:
                    continue
                built = build_row(row)
                if built is not None:
                    data_list.append(built + (rel,))
    return tuple(headers) + ('Source File',), data_list, context.get_relative_path(source_path)


@artifact_processor
def redditChatHistory(context):
    headers = (('Created At', 'datetime'), ('Updated At', 'datetime'), 'Username', 'Message',
               'Message ID', 'Conversation Type', 'Channel', 'Channel Name', 'Subreddit')
    return _csv(context, 'chat_history.csv', headers,
                lambda r: (_ts(r[1]), _ts(r[2]), r[3], r[4], r[0], r[8], r[5], r[7], r[6]), 9)


@artifact_processor
def redditCommentVotes(context):
    return _csv(context, 'comment_votes.csv', ('ID', 'Permalink', 'Direction'),
                lambda r: (r[0], r[1], r[2]), 3)


@artifact_processor
def redditComments(context):
    headers = (('Timestamp', 'datetime'), 'IP', 'Body', 'Permalink', 'ID', 'Subreddit', 'Gildings',
               'Link', 'Parent', 'Media')
    return _csv(context, 'comments.csv', headers,
                lambda r: (_ts(r[2]), r[3], r[8], r[1], r[0], r[4], r[5], r[6], r[7], r[9]), 10)


@artifact_processor
def redditDrafts(context):
    headers = (('Created', 'datetime'), ('Modified', 'datetime'), 'ID', 'Title', 'Body', 'Kind',
               'Spoiler', 'NSFW', 'Original Content', 'Content Category', 'Flair ID', 'Flair Text',
               'Send Replies', 'Subreddit', 'Is Public Link')
    return _csv(context, 'drafts.csv', headers,
                lambda r: (_ts(r[4]), _ts(r[5]), r[0], r[1], r[2], r[3], r[6], r[7], r[8], r[9],
                           r[10], r[11], r[12], r[13], r[14]), 15)


@artifact_processor
def redditGildedComments(context):
    return _csv(context, 'gilded_comments.csv', ('ID', 'Permalink', 'Award ID', 'Quantity'),
                lambda r: (r[0], r[1], r[2], r[3]), 4)


@artifact_processor
def redditGildedPosts(context):
    return _csv(context, 'gilded_posts.csv', ('ID', 'Permalink', 'Award ID', 'Quantity'),
                lambda r: (r[0], r[1], r[2], r[3]), 4)


@artifact_processor
def redditHiddenPosts(context):
    return _csv(context, 'hidden_posts.csv', ('ID', 'Permalink'), lambda r: (r[0], r[1]), 2)


@artifact_processor
def redditIpLogs(context):
    headers = (('Timestamp', 'datetime'), 'IP')
    return _csv(context, 'ip_logs.csv', headers,
                lambda r: None if r[0] == 'registration ip' else (_ts(r[0]), r[1]), 2)


@artifact_processor
def redditRegistrationIp(context):
    return _csv(context, 'ip_logs.csv', ('Key', 'Value'),
                lambda r: ('Registration IP', r[1]) if r[0] == 'registration ip' else None, 2)


@artifact_processor
def redditLinkedPhone(context):
    return _csv(context, 'linked_phone_number.csv', (('Number', 'phonenumber'),),
                lambda r: (r[0],), 1)


@artifact_processor
def redditLiveStreamPosts(context):
    # original called filename(row[1]) -- a str is not callable, so this report crashed; fixed.
    return _csv(context, 'live_stream_posts.csv', ('Post URL', 'Filename'),
                lambda r: (r[0], r[1]), 2)


@artifact_processor
def redditMessages(context):
    headers = (('Timestamp', 'datetime'), 'IP', 'To User', 'From User', 'Subject', 'Body',
               'Permalink', 'Thread ID', 'ID')
    return _csv(context, 'messages.csv', headers,
                lambda r: (_ts(r[3]), r[4], r[6], r[5], r[7], r[8], r[1], r[2], r[0]), 9)


@artifact_processor
def redditPollVotes(context):
    headers = ('Post ID', 'User Selection', 'Text', 'Image URL', 'Is Prediction', 'Stake Amount')
    return _csv(context, 'poll_votes.csv', headers,
                lambda r: (r[0], r[1], r[2], r[3], r[4], r[5]), 6)


@artifact_processor
def redditPostVotes(context):
    return _csv(context, 'post_votes.csv', ('ID', 'Permalink', 'Direction'),
                lambda r: (r[0], r[1], r[2]), 3)


@artifact_processor
def redditPosts(context):
    headers = (('Timestamp', 'datetime'), 'IP', 'ID', 'Title', 'URL', 'Body', 'Permalink',
               'Subreddit', 'Gildings')
    return _csv(context, 'posts.csv', headers,
                lambda r: (_ts(r[2]), r[3], r[0], r[6], r[7], r[8], r[1], r[4], r[5]), 9)


@artifact_processor
def redditGoldInformation(context):
    headers = (('Timestamp', 'datetime'), 'Processor', 'Transaction ID', 'Cost', 'Payer Email')
    return _csv(context, 'reddit_gold_information.csv', headers,
                lambda r: (_ts(r[2]), r[0], r[1], r[3], r[4]), 5)


@artifact_processor
def redditSavedComments(context):
    return _csv(context, 'saved_comments.csv', ('ID', 'Permalink'), lambda r: (r[0], r[1]), 2)


@artifact_processor
def redditSavedPosts(context):
    return _csv(context, 'saved_posts.csv', ('ID', 'Permalink'), lambda r: (r[0], r[1]), 2)


@artifact_processor
def redditScheduledPosts(context):
    headers = ('Scheduled Post ID', 'Subreddit', 'Title', 'Body', 'URL',
               ('Submission Time', 'datetime'), 'Recurrence')
    return _csv(context, 'scheduled_posts.csv', headers,
                lambda r: (r[0], r[1], r[2], r[3], r[4], _ts(r[5]), r[6]), 7)


@artifact_processor
def redditStatistics(context):
    return _csv(context, 'statistics.csv', ('Key', 'Value'), lambda r: (r[0], r[1]), 2)


@artifact_processor
def redditUserPreferences(context):
    # original never appended to data_list, so this report was always empty; fixed.
    return _csv(context, 'user_preferences.csv', ('Key', 'Value'), lambda r: (r[0], r[1]), 2)
