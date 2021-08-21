import os
import datetime
import json

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_instagramProfchanges(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('profile_changes.json'):
            data_list = []
            
            with open(file_found, "rb") as fp:
                deserialized = json.load(fp)
                
            for x in deserialized['profile_profile_change']:
                aggregator = ''
                if x.get('title'):
                    #print(x)
                    for a, b in x.items():
                        
                        if a == 'title':
                            title = b
                        if a == 'media_map_data':
                            if b:
                                for y, z in b.items():
                                    for c, d in z.items():
                                        if d:
                                            if 'timestamp' in c:
                                                if d > 0:
                                                    d = (datetime.datetime.fromtimestamp(int(d)).strftime('%Y-%m-%d %H:%M:%S'))
                                        ''' use seek function in the future
                                        if c == 'uri':
                                            thumb = 'get file to show'
                                        else:
                                            thumb = ''
                                        '''
                                        aggregator = aggregator + f'{y} - {c} - {d} <br>'
                        if a == 'string_map_data':
                            for y, z in b.items():
                                for c, d in z.items():
                                    if d:
                                        if 'timestamp' in c:
                                            if d > 0:
                                                d = (datetime.datetime.fromtimestamp(int(d)).strftime('%Y-%m-%d %H:%M:%S'))
                                        aggregator = aggregator + f'{y} - {c} - {d} <br>'
                                        
                data_list.append((title, aggregator))
                                
            if data_list:
                report = ArtifactHtmlReport('Instagram Archive - Profile Changes')
                report.start_artifact_report(report_folder, 'Instagram Archive - Profile Changes')
                report.add_script()
                data_headers = ('Title', 'Items')

                report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Items'])
                report.end_artifact_report()
                
                tsvname = f'Instagram Archive - Profile Changes'
                tsv(report_folder, data_headers, data_list, tsvname)
                
            else:
                logfunc('No Instagram Archive - Profile Changes data available')
                
        