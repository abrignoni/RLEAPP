import os
import datetime
import hashlib
import json
import re
from pathlib import Path

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, gather_hashes_in_file


def get_airdropRealnames(files_found, report_folder, seeker, wrap_text):
    # log show ./system_logs.logarchive --style ndjson --predicate 'category = "AirDrop"' > airdrop.ndjson

    namelist = []
    data_list = []

    p = Path(__file__).parents[1]
    my_path = Path(p).joinpath('names')
    names = Path(my_path).joinpath('realnames.txt')

    with open(names, 'r') as data:
        for x in data:
            namelist.append(x)

    regex = re.compile(r"realName: (\w{10})")
    target_hashes = {}
    for file_found in files_found:
        file_found = str(file_found)

        if file_found.endswith('airdrop.ndjson'):
            target_hashes.update(gather_hashes_in_file(file_found, regex))

        for email in namelist:
            namecheck = email.strip()
            logfunc('Testing name ' + str(namecheck) + ' for target...')

            targettest = hashlib.sha256(namecheck.encode()).hexdigest()
            starthashcheck = targettest[0:5]
            endhashcheck = targettest[-5:]

            if (starthashcheck.lower(), endhashcheck.lower()) in target_hashes:
                mail_hash = target_hashes.pop((starthashcheck, endhashcheck))
                mail_hash[1] = namecheck
                data_list.append(mail_hash)
                logfunc(namecheck + ' matches hash fragments on ' + mail_hash[0])

    if data_list:
        report = ArtifactHtmlReport(f'AirDrop - Realname from Hash ')
        report.start_artifact_report(report_folder, f'AirDrop - Realname from Hash')
        report.add_script()
        data_headers = ('Timestamp', 'Realname', 'Event Message', 'Subsystem', 'Category', 'Trace ID')
        report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
        report.end_artifact_report()

        tsvname = f'AirDrop - Realname from Hash'
        tsv(report_folder, data_headers, data_list, tsvname)

        tlactivity = f'AirDrop - Realname from Hash'
        timeline(report_folder, tlactivity, data_list, data_headers)
    else:
        logfunc(f'No AirDrop - Realname from Hash')


__artifacts__ = {
    "airdropRealname": (
        "Airdrop Real Names",
        ('*/airdrop.ndjson'),
        get_airdropRealnames)
}
