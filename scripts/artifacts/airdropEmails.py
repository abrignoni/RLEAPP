import os
import datetime
import hashlib
import json
from pathlib import Path

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen


def get_airdropEmails(files_found, report_folder, seeker, wrap_text):
    # log show ./system_logs.logarchive --style ndjson --predicate 'category = "AirDrop"' > airdrop.ndjson

    emailslist = []
    data_list = []

    p = Path(__file__).parents[1]
    my_path = Path(p).joinpath('emails')
    emails = Path(my_path).joinpath('emails.txt')

    with open(emails, 'r') as data:
        for x in data:
            emailslist.append(x)

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
                        if 'Email=[' in eventmessage:
                            targetstart = (eventmessage.split('[')[1].split(',')[0][0:5]).lower()
                            targetend = (eventmessage.split('[')[1].split(',')[0][8:13]).lower()
                            eventtimestamp = deserialized.get('timestamp', '')[0:25]
                            subsystem = deserialized.get('subsystem', '')
                            category = deserialized.get('category', '')
                            traceid = deserialized.get('traceID', '')

                            if (targetstart, targetend) not in target_hashes:
                                logfunc(f"Add {targetstart}...{targetend} to target list")
                                target_hashes[(targetstart, targetend)] = (
                                eventtimestamp, None, eventmessage, subsystem, category, traceid)

        for email in emailslist:
            emailcheck = email.strip()
            print('Testing email' + str(emailcheck) + ' for target...')

            targettest = hashlib.sha256(emailcheck.encode())
            starthashcheck = targettest.hexdigest()[0:5]
            endhashcheck = targettest.hexdigest()[-5:]

            if (starthashcheck.lower(), endhashcheck.lower()) in target_hashes:
                target_hashes[(starthashcheck, endhashcheck)][1] = emailcheck
                data_list.append(target_hashes[(starthashcheck, endhashcheck)][1])
                logfunc(emailcheck + ' matches hash fragments on ' + target_hashes[(starthashcheck, endhashcheck)][0])

    if data_list:
        report = ArtifactHtmlReport(f'AirDrop - Email from Hash ')
        report.start_artifact_report(report_folder, f'AirDrop - Email from Hash')
        report.add_script()
        data_headers = ('Timestamp', 'Email', 'Event Message', 'Subsystem', 'Category', 'Trace ID')
        report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
        report.end_artifact_report()

        tsvname = f'AirDrop - Email from Hash'
        tsv(report_folder, data_headers, data_list, tsvname)

        tlactivity = f'AirDrop - Email from Hash'
        timeline(report_folder, tlactivity, data_list, data_headers)
    else:
        logfunc(f'No AirDrop - Email from Hash')


__artifacts__ = {
    "airdropEmails": (
        "Airdrop Emails",
        ('*/airdrop.ndjson'),
        get_airdropEmails)
}
