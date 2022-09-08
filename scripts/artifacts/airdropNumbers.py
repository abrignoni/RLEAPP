# Base code comes from:
# https://github.com/043a7e/airdropmsisdn

import hashlib
import json
import time
from enum import Enum
from pathlib import Path
import locale

locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

from scripts import ilapfuncs
from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, logdevinfo


class COUNTRY(Enum):
    US = "us"
    DE = "de"


COUNTRY_CODE = {COUNTRY.US: '1', COUNTRY.DE: '49'}
MIN_LEN = {COUNTRY.US: 7, COUNTRY.DE: 7}
MAX_LEN = {COUNTRY.US: 7, COUNTRY.DE: 10}
AREACODE_FILE = {COUNTRY.US: 'areacodes_us.txt', COUNTRY.DE: 'areacodes_de.txt'}


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def _get_line_count(file):
    with open(file, 'rb') as fp:
        return sum(buffer.count(b'\n') for buffer in _count_generator(fp.raw.read))


def get_airdropNumbers(files_found, report_folder, seeker, wrap_text):
    # log show ./system_logs.logarchive --style ndjson --predicate 'category = "AirDrop"' > airdrop.ndjson
    selected_country = COUNTRY.DE
    areacodelist = []
    data_list = []

    p = Path(__file__).parents[1]
    my_path = Path(p).joinpath('areacodes')
    areacodes = Path(my_path).joinpath(AREACODE_FILE[selected_country])

    with open(areacodes, 'r') as data:
        for x in data:
            areacodelist.append(x)

    target_hashes = {}
    for file_found in files_found:
        file_found = str(file_found)

        if file_found.endswith('airdrop.ndjson'):
            factor = 100 / _get_line_count(file_found)
            with open(file_found, 'r') as data:
                for i, x in enumerate(data):
                    ilapfuncs.GuiWindow.SetProgressBar(int(factor * i))
                    if 'Phone=[' in x or ():
                        deserialized = json.loads(x)
                        eventmessage = deserialized.get('eventMessage', '')
                        phonehash = eventmessage.split(',')[1].strip()
                        if len(phonehash) >= 21:
                            targetstart = phonehash[7:12]
                            targetend = phonehash[15:20]
                            eventtimestamp = deserialized.get('timestamp', '')[0:25]
                            subsystem = deserialized.get('subsystem', '')
                            category = deserialized.get('category', '')
                            traceid = deserialized.get('traceID', '')

                            # We assume same hash equals same phone
                            if (targetstart, targetend) not in target_hashes:
                                logfunc(f"Add {targetstart}...{targetend} to target list")
                                target_hashes[(targetstart, targetend)] = [eventtimestamp, None, eventmessage,
                                                                           subsystem, category, traceid]

    for i in range(MIN_LEN[selected_country], MAX_LEN[selected_country]):
        logfunc(f"Searching for len {i}")
        factor = int(10 ** i / 100)
        for areacode in areacodelist:
            areacode = areacode.strip()
            logfunc('Searching area code ' + str(areacode) + ' for target...')
            ilapfuncs.GuiWindow.SetProgressBar(0)
            off = 0
            start_time = time.time()
            for line in range(10 ** i):

                # Performance measuring
                if 60.0 < (time.time() - start_time) < 60.2:
                    logfunc(f"Current Speed: {(line - off) / 60}nr/s")
                    off = line
                    start_time = time.time()

                if line % factor == 0:
                    ilapfuncs.GuiWindow.SetProgressBar(int(line / factor))

                targetphone = COUNTRY_CODE[selected_country] + str(areacode) + str(line).zfill(i)
                targettest = hashlib.sha256(targetphone.encode())
                starthashcheck = targettest.hexdigest()[0:5]
                endhashcheck = targettest.hexdigest()[-5:]
                if (starthashcheck, endhashcheck) in target_hashes:
                    logfunc(f"Found phone {targetphone} for hash {starthashcheck}....{endhashcheck}")
                    phone_hash = target_hashes.pop((starthashcheck, endhashcheck))
                    phone_hash[1] = targetphone
                    data_list.append(phone_hash)
                if not target_hashes:
                    logfunc("No target hashes left")
                    break

    if data_list:
        report = ArtifactHtmlReport(f'AirDrop - Phone Number from Hash ')
        report.start_artifact_report(report_folder, f'AirDrop - Phone Number from Hash')
        report.add_script()
        data_headers = ['Timestamp', 'Target Phone', 'Event Message', 'Subsystem', 'Category', 'Trace ID']
        report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
        report.end_artifact_report()

        tsvname = f'AirDrop - Phone Number from Hash'
        tsv(report_folder, data_headers, data_list, tsvname)

        tlactivity = f'AirDrop - Phone Number from Hash'
        timeline(report_folder, tlactivity, data_list, data_headers)
    else:
        logfunc(f'No AirDrop - Phone Number from Hash')


__artifacts__ = {
    "airdropNumbers": (
        "Airdrop Numbers",
        ('*/airdrop.ndjson'),
        get_airdropNumbers)
}
