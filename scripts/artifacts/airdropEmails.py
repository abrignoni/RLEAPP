import os
import datetime
import hashlib
import json
import re
from pathlib import Path

from scripts.artifact_report import ArtifactHtmlReport
from scripts.artifacts.airdropNumbers import gather_hashes_in_file
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

    regex = re.compile(r"Email=\[(?P<start>\w{5})\.{3}(?P<end>\w{5})]")
    target_hashes = {}
    for file_found in files_found:
        file_found = str(file_found)

        if file_found.endswith('airdrop.ndjson'):
            target_hashes.update(gather_hashes_in_file(file_found, regex))

        for email in emailslist:
            emailcheck = email.strip()
            logfunc('Testing email' + str(emailcheck) + ' for target...')

            targettest = hashlib.sha256(emailcheck.encode()).hexdigest()
            starthashcheck = targettest[0:5]
            endhashcheck = targettest[-5:]

            if (starthashcheck.lower(), endhashcheck.lower()) in target_hashes:
                mail_hash = target_hashes.pop((starthashcheck, endhashcheck))
                mail_hash[1] = emailcheck
                data_list.append(mail_hash)
                logfunc(emailcheck + ' matches hash fragments on ' + mail_hash[0])

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
