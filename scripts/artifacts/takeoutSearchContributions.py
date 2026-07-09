__artifacts_v2__ = {
    "takeoutSearchContributionsStreaming": {
        "name": "Google Search Contributions - Streaming Providers",
        "description": "User-reported information about streaming providers that the user is "
                       "subscribed to.",
        "author": "@Jadoo4QFan",
        "creation_date": "2025-07-23",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Published/Updated values are ISO 8601 UTC ('Z') strings in the Takeout JSON "
                 "and are converted to timezone-aware UTC; unparseable values are kept "
                 "verbatim as text.",
        "paths": ('*/Search Contributions/Streaming video providers.json',),
        "output_types": "standard",
        "artifact_icon": "tv",
    },
    "takeoutSearchContributionsReviews": {
        "name": "Google Search Contributions - Reviews",
        "description": "Reviews for movies, TV shows, music albums, etc.",
        "author": "@Jadoo4QFan",
        "creation_date": "2025-07-23",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Published/Updated values are ISO 8601 UTC ('Z') strings in the Takeout JSON "
                 "and are converted to timezone-aware UTC; unparseable values are kept "
                 "verbatim as text.",
        "paths": ('*/Search Contributions/Reviews.json',),
        "output_types": "standard",
        "artifact_icon": "star",
    },
    "takeoutSearchContributionsWatched": {
        "name": "Google Search Contributions - Watched",
        "description": "Movies and TV shows that the user reported as already watched.",
        "author": "@Jadoo4QFan",
        "creation_date": "2025-07-23",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Published/Updated values are ISO 8601 UTC ('Z') strings in the Takeout JSON "
                 "and are converted to timezone-aware UTC; unparseable values are kept "
                 "verbatim as text.",
        "paths": ('*/Search Contributions/Watched.json',),
        "output_types": "standard",
        "artifact_icon": "eye",
    },
    "takeoutSearchContributionsThumbs": {
        "name": "Google Search Contributions - Thumbs",
        "description": "Thumb ratings for movies, TV shows, music albums, etc.",
        "author": "@Jadoo4QFan",
        "creation_date": "2025-07-23",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "Published/Updated values are ISO 8601 UTC ('Z') strings in the Takeout JSON "
                 "and are converted to timezone-aware UTC; unparseable values are kept "
                 "verbatim as text.",
        "paths": ('*/Search Contributions/Thumbs.json',),
        "output_types": "standard",
        "artifact_icon": "thumbs-up",
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
        return datetime.fromisoformat(value.strip().replace('Z', '+00:00')).astimezone(timezone.utc)
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

    data_headers = (('Published Timestamp', 'datetime'), 'Provider Name')
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

    data_headers = (('Published Timestamp', 'datetime'), ('Updated Timestamp', 'datetime'),
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

    data_headers = (('Published Timestamp', 'datetime'), 'Search Query')
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

    data_headers = (('Published Timestamp', 'datetime'), ('Updated Timestamp', 'datetime'),
                    'Search Query', 'Thumbs Rating')
    return data_headers, data_list, context.get_relative_path(source_path)
