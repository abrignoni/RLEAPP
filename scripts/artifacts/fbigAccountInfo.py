__artifacts_v2__ = {
    "fbigAccountInfo": {
        "name": "Facebook Instagram Returns - Account and Report Information",
        "description": "Account and report information parsed from a Facebook/Instagram law enforcement return (records.html / preservation).",
        "author": "@AlexisBrignoni",
        "creation_date": "2023-07-01",
        "last_update_date": "2026-06-27",
        "requirements": "none",
        "category": "Facebook - Instagram Returns",
        "notes": "Flat Key/Value table; date/phone values stay as raw text (the Value column is heterogeneous and can't be column-typed).",
        "paths": ('*/records.html', '*/preservation*.html', '*/linked_media/profile_picture_*.jpg'),
        "output_types": "standard",
        "artifact_icon": "info",
    }
}

import os

from bs4 import BeautifulSoup

from scripts.ilapfuncs import artifact_processor, check_in_media


def _texts(soup, prop_id, skip):
    """(enumerate index, most_inner text) for each 'div_table inner' at/after `skip`."""
    out = []
    for section in soup.find_all('div', {'id': prop_id}):
        for index, div in enumerate(section.find_all('div', class_='div_table inner')):
            if index < skip:
                continue
            inner = div.find('div', class_='most_inner')
            out.append((index, inner.get_text() if inner else ''))
    return out


@artifact_processor
def fbigAccountInfo(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        basename = os.path.basename(file_found)
        if not (basename.startswith('records.html') or basename.startswith('preservation')):
            continue
        source_path = file_found
        with open(file_found, encoding='utf-8') as fp:
            soup = BeautifulSoup(fp, 'lxml')

        param_keys = ['Service', 'Target', 'Account Identifier', 'Account Type',
                      'Meta Business Records Report Generated',
                      'Meta Business Records Report Date Range']
        for index, text in _texts(soup, 'property-request_parameters', 0):
            data_list.append((param_keys[index] if index < len(param_keys) else '', text, None))

        for _, text in _texts(soup, 'property-name', 2):
            data_list.append(('Name Provided by Account Holder', text, None))
        for _, text in _texts(soup, 'property-emails', 1):
            data_list.append(('Registered Email Address', text, None))
        for _, text in _texts(soup, 'property-vanity', 1):
            data_list.append(('Vanity Name', text, None))
        for _, text in _texts(soup, 'property-registration_date', 1):
            data_list.append(('Account Registration/Creation Date', text, None))
        for _, text in _texts(soup, 'property-registration_ip', 1):
            data_list.append(('Registration IP', text, None))
        for index, text in _texts(soup, 'property-account_end_date', 1):
            data_list.append(('Account Still Active' if index == 2 else 'Account Data', text, None))
        for _, text in _texts(soup, 'property-phone_numbers', 1):
            data_list.append(('Phone Number', text, None))

        pairs = [text for _, text in _texts(soup, 'property-privacy_settings', 2)]
        for i in range(0, len(pairs) - 1, 2):
            data_list.append((pairs[i], pairs[i + 1], None))

        for _, text in _texts(soup, 'property-popular_block', 2):
            data_list.append(('Blocked from showing media in Instagram explorer page', text, None))
        for _, text in _texts(soup, 'property-gender', 1):
            data_list.append(('Gender', text, None))
        for _, text in _texts(soup, 'property-date_of_birth', 1):
            data_list.append(('Date of Birth', text, None))
        for _, text in _texts(soup, 'property-website', 1):
            data_list.append(('Website', text, None))
        for _, text in _texts(soup, 'property-profile_picture', 2):
            data_list.append(('Profile Picture', text, check_in_media(text, text)))

    data_headers = ('Key', 'Value', ('Media', 'media'))
    return data_headers, data_list, context.get_relative_path(source_path)
