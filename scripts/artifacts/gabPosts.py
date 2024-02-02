import os
import datetime
import csv

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen



def get_gabPosts(files_found, report_folder, seeker, wrap_text, time_offset):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.endswith('_posts.csv'):
            data_list_posts =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        created = item[3]
                        updated = item[4]
                        text = item[2]
                        inreplytoid = item[5]
                        reblogofid = item[6]
                        id = item[0]
                        uri = item[1]
                        url = item[7]
                        sensitive = item[8]
                        visibility = item[9]
                        spoilertext = item[10]
                        reply = item[11]
                        language = item[12]
                        conversationid = item[13]
                        local = item[14]
                        accountid = item[15]
                        application = item[16]
                        inreplyto = item[17]
                        pollid = item[18]
                        groupid = item[19]
                        quoteofid = item[20]
                        revisedat = item[21]
                        markdown = item[22]
                        expiresat = item[23]
                        hasquote = item[24]
                        tombsoteat = item[25]
                        
                        data_list_posts.append((created,updated,text,inreplytoid,reblogofid,id,uri,url,sensitive,visibility,spoilertext,reply,language,conversationid,local,accountid,application,inreplyto,pollid,groupid,quoteofid,revisedat,markdown,expiresat,hasquote,tombsoteat))

            if data_list_posts:
                report = ArtifactHtmlReport(f'Gab - Posts')
                report.start_artifact_report(report_folder, f'Gab - Posts')
                report.add_script()
                data_headers = ('Timestamp','Updated','Text','In Reply to ID','Reblog of ID','ID','URI','URL','Sensitive','Visibility','Spoiler Text','Reply','Language','Conversation ID','Local','Account ID','Application','In Reply To','Poll ID','Group ID','Quote of ID','Revised At','Markdown','Expires At','Has Quote','Tombstoned At')
                report.write_artifact_data_table(data_headers, data_list_posts, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Gab - Posts'
                tsv(report_folder, data_headers, data_list_posts, tsvname)
                
                tlactivity = f'Gab - Posts'
                timeline(report_folder, tlactivity, data_list_posts, data_headers)
                
                
            else:
                logfunc(f'Gab - Posts')
                
__artifacts__ = {
        "gabPosts": (
            "Gab Returns",
            ('*/*_posts.csv'),
            get_gabPosts)
}