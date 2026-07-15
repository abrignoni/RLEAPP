__artifacts_v2__ = {
    "instagramInfotoadv": {
        "name": "Instagram Archive - Info Submitted to Adv",
        "description": "Parses information submitted to advertisers from an Instagram data archive",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-21",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ("*/ads_and_businesses/information_you've_submitted_to_advertisers.json"),
        "output_types": "standard",
        "artifact_icon": "brand-instagram",
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor


@artifact_processor
def instagramInfotoadv(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found).startswith("information_you've_submitted_to_advertisers.json"):
            source_path = file_found
            with open(file_found, 'r', encoding='utf-8') as fp:
                deserialized = json.load(fp)

            for x in deserialized['ig_lead_gen_info']:
                label = x.get('label', '')
                value = x.get('value', '')
                data_list.append((label, value))

    data_headers = ('Label', 'Value')
    return data_headers, data_list, context.get_relative_path(source_path)
