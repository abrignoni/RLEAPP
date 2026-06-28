__artifacts_v2__ = {
    "airdropRealname": {
        "name": "AirDrop - Real Name from Hash",
        "description": "Recovers sender real names from AirDrop partial hashes in the unified log "
                       "(airdrop.ndjson) by testing a candidate name wordlist.",
        "author": "Rex",
        "creation_date": "2022-09-10",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Airdrop Real Names",
        "notes": "Tests SHA-256 of each candidate name (scripts/names/realnames.txt) against the "
                 "partial hashes AirDrop writes to the unified log. Timestamp is kept as text: the "
                 "shared gather_hashes_in_file helper truncates the unified-log time to 25 chars, "
                 "dropping the UTC offset, so it can't be safely typed/normalized to UTC.",
        "paths": ('*/airdrop.ndjson',),
        "output_types": "standard",
        "artifact_icon": "user",
    }
}

import hashlib
import re
from pathlib import Path

from scripts.ilapfuncs import artifact_processor, logfunc, gather_hashes_in_file


@artifact_processor
def airdropRealname(context):
    namelist = []
    data_list = []
    source_path = ''

    wordlist = Path(__file__).parents[1].joinpath('names', 'realnames.txt')
    with open(wordlist, encoding='utf-8') as data:
        for line in data:
            namelist.append(line)

    regex = re.compile(r"realName: (\w{10})")
    target_hashes = {}
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('airdrop.ndjson'):
            continue
        source_path = file_found
        target_hashes.update(gather_hashes_in_file(file_found, regex))

        for name in namelist:
            namecheck = name.strip()
            targettest = hashlib.sha256(namecheck.encode()).hexdigest()
            key = (targettest[0:5].lower(), targettest[-5:].lower())
            if key in target_hashes:
                name_hash = target_hashes.pop(key)
                name_hash[1] = namecheck
                data_list.append(tuple(name_hash))
                logfunc(f'{namecheck} matches hash fragments on {name_hash[0]}')

    data_headers = ('Timestamp', 'Realname', 'Event Message', 'Subsystem', 'Category', 'Trace ID')
    return data_headers, data_list, context.get_relative_path(source_path)
