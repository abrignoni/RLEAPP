__artifacts_v2__ = {
    "discordReturnsOnlineServers": {
        "name": "Discord Online - Servers",
        "description": "Server messages from a Discord law enforcement return with media fetched "
                       "live from Discord CDN URLs (messages/servers/*.csv).",
        "author": "Kate (thekatecain)",
        "creation_date": "2024-04-09",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Discord Returns Online",
        "notes": "Media is fetched live over the network from Discord CDN URLs found in the return. "
                 "Discord CDN attachment links (cdn.discordapp.com / media.discordapp.net) are "
                 "publicly accessible without any authentication - anyone holding the URL can "
                 "retrieve the file. Downloaded bytes are embedded via check_in_embedded_media "
                 "(network requests use a 30s timeout); the original URL is preserved in the "
                 "Contents column.",
        "paths": ('*/messages/servers/*.csv',),
        "output_types": "standard",
        "artifact_icon": "server",
    }
}

import csv
import os
import urllib.parse
from datetime import datetime, timezone

import requests

from scripts.ilapfuncs import (artifact_processor, convert_unix_ts_to_utc,
                               check_in_embedded_media, logfunc)


def _discord_ts(value):
    value = (value or '').strip()
    if not value:
        return value
    if value.isdigit():
        return convert_unix_ts_to_utc(int(value))
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError:
        return value


def _fetch_embed(url, source_file):
    url = urllib.parse.unquote(url)
    try:
        resp = requests.get(url, stream=True, timeout=30)
    except requests.RequestException as exc:
        logfunc(f'Discord Online: request failed for {url}: {exc}')
        return None
    if not resp.ok:
        logfunc(f'Discord Online: HTTP {resp.status_code} for {url}')
        return None
    name = os.path.basename(urllib.parse.urlparse(url).path) or 'discord_media'
    return check_in_embedded_media(source_file, resp.content, name)


def _collect_refs(media_field, contents, source_file):
    refs = []
    media_field = (media_field or '').strip()
    if media_field.startswith('https'):
        ref = _fetch_embed(media_field, source_file)
        if ref:
            refs.append(ref)
    contents = (contents or '').strip()
    if contents.startswith('http') and ('cdn.discordapp.com' in contents
                                         or 'media.discordapp.net' in contents):
        ref = _fetch_embed(contents, source_file)
        if ref:
            refs.append(ref)
    return refs


@artifact_processor
def discordReturnsOnlineServers(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.csv') or os.path.basename(file_found).startswith('._'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)  # header
            for item in reader:
                if len(item) < 7:
                    continue
                refs = _collect_refs(item[6], item[5], file_found)
                data_list.append((_discord_ts(item[3]), item[4], item[5], refs,
                                  item[0], item[1], item[2]))

    data_headers = (('Timestamp', 'datetime'), 'Username', 'Contents', ('Attachment', 'media'),
                    'ID', 'Channel ID', 'Author ID')
    return data_headers, data_list, context.get_relative_path(source_path)
