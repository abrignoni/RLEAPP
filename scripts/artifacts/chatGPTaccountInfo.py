__artifacts_v2__ = {
    "chatGPTaccountInfo": {
        "name": "ChatGPT User Information",
        "description": "Account information for the ChatGPT user (user ID, email "
                       "address, ChatGPT Plus status and phone number), parsed from "
                       "the user.json file of a ChatGPT data export.",
        "author": "@upintheairsheep2",
        "creation_date": "2023-08-02",
        "last_update_date": "2026-07-09",
        "requirements": "none",
        "category": "ChatGPT",
        "notes": "",
        "paths": ('*/user.json',),
        "output_types": "standard",
        "artifact_icon": "user",
    }
}

import json
import os

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def chatGPTaccountInfo(context):
    data_list = []
    source_path = ''
    parsed = set()
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'user.json':
            continue
        real_path = os.path.realpath(file_found)
        if real_path in parsed:
            continue
        parsed.add(real_path)
        source_path = file_found

        with open(file_found, encoding='utf-8', mode='r') as f:
            data = json.load(f)

        # user.json holds a single JSON object; accept a list of them too.
        accounts = data if isinstance(data, list) else [data]
        for account in accounts:
            data_list.append((
                account.get('id', ''),
                account.get('email', ''),
                account.get('chatgpt_plus_user', ''),
                account.get('phone_number', ''),
            ))

    data_headers = (
        'User ID',
        'User Email Address',
        'Does this user use ChatGPT Plus?',
        ('User Phone Number', 'phonenumber'),
    )
    return data_headers, data_list, context.get_relative_path(source_path)
