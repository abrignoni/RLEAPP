__artifacts_v2__ = {
    "discordReturnsser": {
        "name": "Discord - Server Metadata",
        "description": "Server metadata from a Discord law enforcement return (servers/*.json).",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-12-04",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Discord Returns",
        "notes": "",
        "paths": ('*/servers/*.json',),
        "output_types": "standard",
        "html_columns": ["Channels"],
        "artifact_icon": "server",
    }
}

import json

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def discordReturnsser(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('.json'):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8', errors='backslashreplace') as f:
            data = json.load(f)

        channels = data.get('channels', '')
        channels_agg = ('<br>'.join(f'{k}: {v}' for k, v in channels.items())
                        if isinstance(channels, dict) else '')
        data_list.append((data.get('name', ''), data.get('description', ''), channels_agg,
                          data.get('banner', ''), data.get('icon', ''), data.get('id', ''),
                          data.get('owner_id', ''), data.get('preferred_locale', ''),
                          data.get('region', ''), data.get('threads', '')))

    data_headers = ('Name', 'Description', 'Channels', 'Banner', 'Icon ID', 'ID', 'Owner ID',
                    'Preferred Locale', 'Region', 'Threads')
    return data_headers, data_list, context.get_relative_path(source_path)
