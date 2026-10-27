__artifacts_v2__ = {
    "takeoutSearchContributionsStreaming": {
        "name": "Google Search Contributions - Streaming Providers",
        "description": "Entries of Streaming video providers.json in the Search Contributions "
                       "folder of a Google Takeout: provider name and published time. What action "
                       "created an entry is not established here.",
        "author": "@Jadoo4QFan, @AlexisBrignoni, Codex",
        "creation_date": "2025-07-23",
        "last_update_date": "2026-10-04",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Mixed time columns use text storage and do not populate timeline/date filters. Published values that are ISO 8601 strings with a Z or an offset are converted "
                 "to timezone-aware UTC; unparseable values are kept verbatim as text. A value "
                 "with no Z or offset is retained as stored text.",
        "paths": ('*/Search Contributions/Streaming video providers.json',),
        "output_types": "standard",
        "artifact_icon": "device-tv",
    },
    "takeoutSearchContributionsReviews": {
        "name": "Google Search Contributions - Reviews",
        "description": "Entries of Reviews.json in the Search Contributions folder of a Google Takeout: search query, star rating, comment, published and updated times.",
        "author": "@Jadoo4QFan, @AlexisBrignoni, Codex",
        "creation_date": "2025-07-23",
        "last_update_date": "2026-10-04",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Mixed time columns use text storage and do not populate timeline/date filters. Published and Updated values that are ISO 8601 strings with a Z or an offset are "
                 "converted to timezone-aware UTC; unparseable values are kept verbatim as text. A "
                 "value with no Z or offset is retained as stored text.",
        "paths": ('*/Search Contributions/Reviews.json',),
        "output_types": "standard",
        "artifact_icon": "star",
    },
    "takeoutSearchContributionsWatched": {
        "name": "Google Search Contributions - Watched",
        "description": "Entries of Watched.json in the Search Contributions folder of a Google Takeout: search query and published time. What action created an entry is not established here.",
        "author": "@Jadoo4QFan, @AlexisBrignoni, Codex",
        "creation_date": "2025-07-23",
        "last_update_date": "2026-10-04",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Mixed time columns use text storage and do not populate timeline/date filters. Published values that are ISO 8601 strings with a Z or an offset are converted "
                 "to timezone-aware UTC; unparseable values are kept verbatim as text. A value "
                 "with no Z or offset is retained as stored text.",
        "paths": ('*/Search Contributions/Watched.json',),
        "output_types": "standard",
        "artifact_icon": "eye",
    },
    "takeoutSearchContributionsThumbs": {
        "name": "Google Search Contributions - Thumbs",
        "description": "Entries of Thumbs.json in the Search Contributions folder of a Google Takeout: search query, thumbs rating, published and updated times.",
        "author": "@Jadoo4QFan, @AlexisBrignoni, Codex",
        "creation_date": "2025-07-23",
        "last_update_date": "2026-10-04",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Mixed time columns use text storage and do not populate timeline/date filters. Published and Updated values that are ISO 8601 strings with a Z or an offset are "
                 "converted to timezone-aware UTC; unparseable values are kept verbatim as text. A "
                 "value with no Z or offset is retained as stored text.",
        "paths": ('*/Search Contributions/Thumbs.json',),
        "output_types": "standard",
        "artifact_icon": "thumb-up",
    }
}

import json
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, logfunc


def _iso_to_utc(value):
    # Takeout Search Contributions timestamps are ISO 8601 UTC strings
    # (e.g. "2023-05-01T12:34:56.789Z"). Anything unparseable stays as text.
    if not value:
        return value
    try:
        dt = datetime.fromisoformat(value.strip().replace('Z', '+00:00'))
        return value if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except (ValueError, AttributeError):
        return value


def _load_items(context, target_name):
    items = []
    source_path = ''
    seen = set()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != target_name:
            continue
        real_path = os.path.realpath(file_found)
        if real_path in seen:
            continue
        seen.add(real_path)
        with open(file_found, encoding='utf-8', mode='r') as f:
            try:
                data = json.loads(f.read())
            except json.JSONDecodeError:
                logfunc(f'Error decoding JSON from file: {os.path.basename(file_found)}')
                continue
        source_path = file_found
        if isinstance(data, list):
            items.extend(data)
    return items, source_path


@artifact_processor
def takeoutSearchContributionsStreaming(context):
    data_list = []
    items, source_path = _load_items(context, 'Streaming video providers.json')
    for item in items:
        provider_name = item.get('Provider Name', '')
        published = _iso_to_utc(item.get('Published', ''))
        data_list.append((published, provider_name))

    data_headers = ('Published Timestamp', 'Provider Name')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def takeoutSearchContributionsReviews(context):
    data_list = []
    items, source_path = _load_items(context, 'Reviews.json')
    for item in items:
        published = _iso_to_utc(item.get('Published', ''))
        updated = _iso_to_utc(item.get('Updated', ''))
        comment = item.get('Review Comment', '')
        rating = item.get('Review Star Rating', '')
        query = item.get('Search Query', '')
        data_list.append((published, updated, query, rating, comment))

    data_headers = ('Published Timestamp', 'Updated Timestamp',
                    'Search Query', 'Star Rating', 'Comment')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def takeoutSearchContributionsWatched(context):
    data_list = []
    items, source_path = _load_items(context, 'Watched.json')
    for item in items:
        published = _iso_to_utc(item.get('Published', ''))
        query = item.get('Search Query', '')
        data_list.append((published, query))

    data_headers = ('Published Timestamp', 'Search Query')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def takeoutSearchContributionsThumbs(context):
    data_list = []
    items, source_path = _load_items(context, 'Thumbs.json')
    for item in items:
        published = _iso_to_utc(item.get('Published', ''))
        updated = _iso_to_utc(item.get('Updated', ''))
        query = item.get('Search Query', '')
        rating = item.get('Thumbs Rating', '')
        data_list.append((published, updated, query, rating))

    data_headers = ('Published Timestamp', 'Updated Timestamp',
                    'Search Query', 'Thumbs Rating')
    return data_headers, data_list, context.get_relative_path(source_path)
