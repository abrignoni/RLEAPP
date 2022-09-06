# Base code comes from:
# https://github.com/043a7e/airdropmsisdn

import os
import datetime
import hashlib
import json
from pathlib import Path

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen


def get_airdropNumbers(files_found, report_folder, seeker, wrap_text):
    # log show ./system_logs.logarchive --style ndjson --predicate 'category = "AirDrop"' > airdrop.ndjson
    COUNTRY_CODE = '1'
    MIN_LEN = 7
    MAX_LEN = 10

    areacodelist = []
    data_list = []

    p = Path(__file__).parents[1]
    my_path = Path(p).joinpath('areacodes')
    areacodes = Path(my_path).joinpath('areacodes.txt')

    with open(areacodes, 'r') as data:
        for x in data:
            areacodelist.append(x)

    target_hashes = {}
    for file_found in files_found:
        file_found = str(file_found)

        filename = os.path.basename(file_found)

        if file_found.endswith('airdrop.ndjson'):
            with open(file_found, 'r') as data:
                for x in data:
                    deserialized = json.loads(x)
                    endofdata = deserialized.get('finished', '')
                    if endofdata == 1:
                        break
                    else:
                        eventmessage = deserialized.get('eventMessage', '')
                        if 'Phone=[' in eventmessage:
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
                                    target_hashes[(targetstart, targetend)] = (eventtimestamp, None, eventmessage, subsystem, category, traceid)

    for areacode in areacodelist:
        areacode = areacode.strip()
        line = '0'
        print('Searching area code ' + str(areacode) + ' for target...')
        for i in range(MIN_LEN, MAX_LEN):
            for line in range(10 ** i):

                targetphone = COUNTRY_CODE + str(areacode) + str(line).zfill(7)
                targettest = hashlib.sha256(targetphone.encode())
                starthashcheck = targettest.hexdigest()[0:5]
                endhashcheck = targettest.hexdigest()[-5:]
                if (starthashcheck, endhashcheck) in target_hashes:
                    logfunc(f"Found phone {targetphone} for hash {starthashcheck}....{endhashcheck}")
                    target_hashes[(starthashcheck, endhashcheck)][1] = targetphone
                    data_list.append(target_hashes[(starthashcheck, endhashcheck)][1])

    if data_list:
        report = ArtifactHtmlReport(f'AirDrop - Phone Number from Hash ')
        report.start_artifact_report(report_folder, f'AirDrop - Phone Number from Hash')
        report.add_script()
        data_headers = ('Timestamp', 'Target Phone', 'Event Message', 'Subsystem', 'Category', 'Trace ID')
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
