# Base code comes from:
# https://github.com/043a7e/airdropmsisdn

__artifacts_v2__ = {
    "airdropNumbers": {
        "name": "AirDrop - Phone Number from Hash",
        "description": "Recovers sender phone numbers from AirDrop partial hashes in the unified "
                       "log (airdrop.ndjson) by brute-forcing candidate numbers per area code.",
        "author": "@AlexisBrignoni",
        "creation_date": "2022-03-15",
        "last_update_date": "2026-06-28",
        "requirements": "none",
        "category": "Airdrop Numbers",
        "notes": "Brute-forces every candidate number for each area code in "
                 "scripts/areacodes/areacodes_us.txt and SHA-256s it against AirDrop's partial "
                 "hashes. This is compute-heavy (up to 10^7 hashes per area code). Timestamp is "
                 "kept as text: the shared gather_hashes_in_file helper truncates the unified-log "
                 "time to 25 chars, dropping the UTC offset, so it can't be safely normalized.",
        "paths": ('*/airdrop.ndjson',),
        "output_types": "standard",
        "artifact_icon": "phone",
    }
}

import hashlib
import re
import time
from enum import Enum
from pathlib import Path

from scripts.ilapfuncs import artifact_processor, logfunc, gather_hashes_in_file


class COUNTRY(Enum):
    US = "us"
    DE = "de"


COUNTRY_CODE = {COUNTRY.US: '1', COUNTRY.DE: '49'}
MIN_LEN = {COUNTRY.US: 7, COUNTRY.DE: 7}
MAX_LEN = {COUNTRY.US: 7, COUNTRY.DE: 10}
AREACODE_FILE = {COUNTRY.US: 'areacodes_us.txt', COUNTRY.DE: 'areacodes_de.txt'}


@artifact_processor
def airdropNumbers(context):
    selected_country = COUNTRY.US
    areacodelist = []
    data_list = []
    source_path = ''

    areacodes = Path(__file__).parents[1].joinpath('areacodes', AREACODE_FILE[selected_country])
    with open(areacodes, encoding='utf-8') as data:
        for line in data:
            areacodelist.append(line)

    regex = re.compile(r"Phone=\[((\w{5}\.{3}\w{5}(, )?)+)\]")
    target_hashes = {}
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if not file_found.endswith('airdrop.ndjson'):
            continue
        source_path = file_found
        target_hashes.update(gather_hashes_in_file(file_found, regex))

    for i in range(MIN_LEN[selected_country], MAX_LEN[selected_country] + 1):
        logfunc(f"Searching for len {i}")
        for areacode in areacodelist:
            areacode = areacode.strip()
            logfunc('Searching area code ' + str(areacode) + ' for target...')
            off = 0
            start_time = time.time()
            for line in range(10 ** i):
                if 60.0 < (time.time() - start_time) < 60.2:
                    logfunc(f"Current Speed: {(line - off) / 60}nr/s")
                    off = line
                    start_time = time.time()

                targetphone = f"{COUNTRY_CODE[selected_country]}{areacode}{line:0{i}d}"
                targettest = hashlib.sha256(targetphone.encode()).hexdigest()
                key = (targettest[:5], targettest[-5:])
                if key in target_hashes:
                    logfunc(f"Found phone {targetphone} for hash {key[0]}....{key[1]}")
                    phone_hash = list(target_hashes[key])
                    phone_hash[1] = targetphone
                    data_list.append(tuple(phone_hash))
                if not target_hashes:
                    logfunc("No target hashes left")
                    break

    data_headers = ('Timestamp', ('Target Phone', 'phonenumber'), 'Event Message', 'Subsystem',
                    'Category', 'Trace ID')
    return data_headers, data_list, context.get_relative_path(source_path)
