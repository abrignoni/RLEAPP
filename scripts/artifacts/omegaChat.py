__artifacts_v2__ = {
    "omegaChatAccount": {
        "name": "Omega Chat Account",
        "description": "Parses Omega Chat Account information from an Omega Chat "
                       "legal return (hicht.json).",
        "author": "Heather Charpentier (@charpy4n6)",
        "creation_date": "2024-09-03",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Omega Chat",
        "notes": "",
        "paths": ('*/hicht.json',),
        "output_types": "standard",
        "artifact_icon": "user",
    },
    "omegaChatMessages": {
        "name": "Omega Chat Messages",
        "description": "Parses Omega Chat Messages from an Omega Chat legal "
                       "return (hicht.json).",
        "author": "Alexis Brigs Brignoni",
        "creation_date": "2024-09-03",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Omega Chat",
        "notes": "",
        "paths": ('*/hicht.json',),
        "output_types": "standard",
        "artifact_icon": "message-circle",
    },
    "omegaChatUsers": {
        "name": "Omega Chat Users",
        "description": "Parses Omega Chat Users from an Omega Chat legal "
                       "return (hicht.json).",
        "author": "Heather Charpentier (@charpy4n6)",
        "creation_date": "2024-09-03",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "Omega Chat",
        "notes": "",
        "paths": ('*/hicht.json',),
        "output_types": "standard",
        "artifact_icon": "users",
    },
}

import json
import os

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc

# The return is a single flattened JSON array: most values in a record are
# integer indexes that point back into the top-level array, where the actual
# value is stored.


def _hicht_files(context):
    # Basename filter plus realpath dedupe so the same return file found
    # through several search paths is only parsed once.
    parsed = set()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'hicht.json':
            continue
        real_path = os.path.realpath(file_found)
        if real_path in parsed:
            continue
        parsed.add(real_path)
        yield file_found


def _load_json(file_path):
    with open(file_path, encoding='utf-8') as f:
        return json.loads(f.read())


@artifact_processor
def omegaChatAccount(context):
    data_headers = (
        ('Created At', 'datetime'), 'MBX UID', 'First Name', 'Birthday',
        'Latitude', 'Longitude', 'City', 'Region', 'Nation', 'Gender', 'Age')
    data_list = []
    source_path = ''

    for file_found in _hicht_files(context):
        source_path = file_found
        data = _load_json(file_found)

        users = data[8]
        for user in users:
            userdata = data[int(user)]

            actcreatedat = userdata.get('created_timestamp', 'Unknown')
            if actcreatedat != 'Unknown':
                actcreatedat = convert_unix_ts_to_utc(actcreatedat)

            actno = data[int(userdata['mbx_uid'])]
            fname = data[int(userdata['first_name'])]
            bdate = data[int(userdata['birthday'])]
            lat = userdata.get('lat', 'Unknown')
            lon = userdata.get('lon', 'Unknown')
            cit = data[int(userdata['city'])]
            reg = data[int(userdata['region'])]
            nat = data[int(userdata['nation'])]
            gen = data[int(userdata['gender'])]
            age = userdata.get('age', 'Unknown')

            data_list.append((actcreatedat, actno, fname, bdate, lat, lon,
                              cit, reg, nat, gen, age))

    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def omegaChatMessages(context):
    data_headers = (
        ('Created At', 'datetime'), 'First Name', 'Content', 'Translate')
    data_list = []
    source_path = ''

    for file_found in _hicht_files(context):
        source_path = file_found
        data = _load_json(file_found)

        dictofusers = {}
        listofusers = data[2]
        for user in listofusers:
            userdata = data[int(user)]
            dictofusers[userdata['id']] = userdata

        listofconvs = data[3]
        for conv in listofconvs:
            conversation_md = data[int(conv)]
            convcreatedat = convert_unix_ts_to_utc(conversation_md['createdAt'])

            content = data[int(conversation_md['content'])]

            conversation = data[int(conversation_md['conversation'])]
            userdata = dictofusers[int(conversation['user_id'])]
            fname = data[int(userdata['first_name'])]

            translate = conversation_md.get('translate')
            if translate is not None:
                translate = data[int(translate)]

            data_list.append((convcreatedat, fname, content, translate))

    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def omegaChatUsers(context):
    data_headers = (
        'MBX UID', 'First Name', 'Birthday', 'Latitude', 'Longitude',
        'City', 'Region', 'Nation', 'Gender', 'Age')
    data_list = []
    source_path = ''

    for file_found in _hicht_files(context):
        source_path = file_found
        data = _load_json(file_found)

        listofusers = data[2]
        for user in listofusers:
            userdata = data[int(user)]

            actno = data[int(userdata['mbx_uid'])]
            fname = data[int(userdata['first_name'])]
            bdate = data[int(userdata['birthday'])]
            lat = data[int(userdata['lat'])]
            lon = data[int(userdata['lon'])]
            cit = data[int(userdata['city'])]
            reg = data[int(userdata['region'])]
            nat = data[int(userdata['nation'])]
            gen = data[int(userdata['gender'])]
            age = userdata.get('age', 'Unknown')

            data_list.append((actno, fname, bdate, lat, lon, cit, reg, nat,
                              gen, age))

    return data_headers, data_list, context.get_relative_path(source_path)
