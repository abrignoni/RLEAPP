import os
import datetime
import hashlib
import json
from pathlib import Path

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen


def get_airdropdiscoverable(files_found, report_folder, seeker, wrap_text):
    # log show ./system_logs.logarchive --style ndjson --predicate 'category = "AirDrop"' > airdrop.ndjson

    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if file_found.endswith('airdrop.ndjson'):
            with open(file_found, 'r') as data:
                for y in data:
                    deserialized = json.loads(y)
                    endofdata = deserialized.get('finished', '')
                    if endofdata == 1:
                        break
                    else:
                        eventmessage = deserialized.get('eventMessage', '')
                        if 'Updated people:' in eventmessage:
                            
                            eventtimestamp = deserialized.get('timestamp', '')[0:25]
                            subsystem = deserialized.get('subsystem', '')
                            category = deserialized.get('category', '')
                            traceid = deserialized.get('traceID', '')
                            
                            #print(eventmessage)
                            separated = (eventmessage.split(','))
                            #print(separated)
                            realname = displayname = secondaryname = isme = isknown = israpport = uwbcapable = updatedp = ''
                            for x in separated:
                                
                                if '<NSOrderedCollectionDifference' in x:
                                    updatedp = x.split('(')[1]
                                    updatedp = updatedp.replace('<','')
                                elif 'Updated people' in x:
                                    updatedp = x.split(': ')[1]
                                elif 'realName' in x:
                                    realname = x.split(': ')[1]
                                elif 'displayName' in x:
                                    displayname = x.split(': ')[1]
                                elif 'secondaryName' in x:
                                    secondaryname = x.split(': ')[1]
                                elif 'isMe' in x:
                                    isme = x.split(': ')[1]
                                elif 'isKnown' in x:
                                    isknown = x.split(': ')[1]
                                elif 'isRapport' in x:
                                    israpport = x.split(': ')[1]
                                elif 'uwbCapable' in x:
                                    uwbcapable = x.split(': ')[1]
                                    uwbcapable = uwbcapable.replace('>','')
                            data_list.append((eventtimestamp, traceid, updatedp, realname, displayname, secondaryname, isme, isknown, israpport, uwbcapable))
                        
    if data_list:
        report = ArtifactHtmlReport(f'AirDrop - Discoverable')
        report.start_artifact_report(report_folder, f'AirDrop - Discoverable')
        report.add_script()
        data_headers = ('Timestamp', 'Trace ID', 'Update', 'Real Name', 'Display Name', 'Secondary Name', 'Is me?', 'Is Known?', 'Is Rapport?', 'UWC capable')
        report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
        report.end_artifact_report()

        tsvname = f'AirDrop - Discoverable'
        tsv(report_folder, data_headers, data_list, tsvname)

        tlactivity = f'AirDrop - Discoverable'
        timeline(report_folder, tlactivity, data_list, data_headers)
    else:
        logfunc(f'No AirDrop - Discoverable')


__artifacts__ = {
    "airdropdiscoverable": (
        "Airdrop Discoverable",
        ('*/airdrop.ndjson'),
        get_airdropdiscoverable)
}
