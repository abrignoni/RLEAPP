__artifacts_v2__ = {
    "airdropEmails": {
        "name": "AirDrop - Email from Hash",
        "description": "Lists candidate email addresses from a wordlist whose SHA-256 begins and "
                       "ends with the hash fragments logged in the unified log (airdrop.ndjson).",
        "author": "@AlexisBrignoni",
        "creation_date": "2022-03-16",
        "last_update_date": "2026-10-09",
        "requirements": "none",
        "category": "Airdrop Emails",
        "notes": "Tests SHA-256 of each candidate email (scripts/emails/emails.txt) against the 5 "
                 "character start and end fragments the pattern Email=[xxxxx...xxxxx] matches in "
                 "the log's lines. Each distinct fragment pair that a candidate matches is "
                 "reported once, with the time and message of the first log line that held it, and "
                 "with the first wordlist candidate that matched. A match on 10 hex characters is "
                 "a candidate, not proof of the address. Timestamp is kept as text: the shared "
                 "gather_hashes_in_file helper truncates the unified-log time to 25 chars, "
                 "dropping the UTC offset, so it can't be safely typed/normalized to UTC.",
        "paths": ('*/airdrop.ndjson',),
        "output_types": "standard",
        "artifact_icon": "mail",
    }
}

import hashlib
import re
from pathlib import Path

from scripts.ilapfuncs import artifact_processor, logfunc, gather_hashes_in_file


@artifact_processor
def airdropEmails(context):
    emailslist = []
    data_list = []
    source_path = ''

    wordlist = Path(__file__).parents[1].joinpath('emails', 'emails.txt')
    with open(wordlist, encoding='utf-8') as data:
        for line in data:
            emailslist.append(line)

    regex = re.compile(r"Email=\[((\w{5}\.{3}\w{5}(, )?)+)\]")
    target_hashes = {}
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('airdrop.ndjson'):
            continue
        source_path = file_found
        target_hashes.update(gather_hashes_in_file(file_found, regex))

        for email in emailslist:
            emailcheck = email.strip()
            targettest = hashlib.sha256(emailcheck.encode()).hexdigest()
            key = (targettest[0:5].lower(), targettest[-5:].lower())
            if key in target_hashes:
                mail_hash = target_hashes.pop(key)
                mail_hash[1] = emailcheck
                data_list.append(tuple(mail_hash))
                logfunc(f'{emailcheck} matches hash fragments on {mail_hash[0]}')

    data_headers = ('Timestamp', 'Candidate Email', 'Event Message', 'Subsystem',
                    'Category', 'Trace ID')
    return data_headers, data_list, context.get_relative_path(source_path)
