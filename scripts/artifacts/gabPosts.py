import os
import datetime
import csv

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, media_to_html, kmlgen

def utf8_in_extended_ascii(input_string, *, raise_on_unexpected=False):
    """Returns a tuple of bool (whether mis-encoded utf-8 is present) and str (the converted string)"""
    output = []  # individual characters, join at the end
    is_in_multibyte = False  # True if we're currently inside a utf-8 multibyte character
    multibytes_expected = 0
    multibyte_buffer = []
    mis_encoded_utf8_present = False
    
    def handle_bad_data(index, character):
        if not raise_on_unexpected: # not raising, so we dump the buffer into output and append this character
            output.extend(multibyte_buffer)
            multibyte_buffer.clear()
            output.append(character)
            nonlocal is_in_multibyte
            is_in_multibyte = False
            nonlocal multibytes_expected
            multibytes_expected = 0
        else:
            raise ValueError(f"Expected multibyte continuation at index: {index}")
            
    for idx, c in enumerate(input_string):
        code_point = ord(c)
        if code_point <= 0x7f or code_point > 0xf4:  # ASCII Range data or higher than you get for mis-encoded utf-8:
            if not is_in_multibyte:
                output.append(c)  # not in a multibyte, valid ascii-range data, so we append
            else:
                handle_bad_data(idx, c)
        else:  # potentially utf-8
            if (code_point & 0xc0) == 0x80:  # continuation byte
                if is_in_multibyte:
                    multibyte_buffer.append(c)
                else:
                    handle_bad_data(idx, c)
            else:  # start-byte
                if not is_in_multibyte:
                    assert multibytes_expected == 0
                    assert len(multibyte_buffer) == 0
                    while (code_point & 0x80) != 0:
                        multibytes_expected += 1
                        code_point <<= 1
                    multibyte_buffer.append(c)
                    is_in_multibyte = True
                else:
                    handle_bad_data(idx, c)
                    
        if is_in_multibyte and len(multibyte_buffer) == multibytes_expected:  # output utf-8 character if complete
            utf_8_character = bytes(ord(x) for x in multibyte_buffer).decode("utf-8")
            output.append(utf_8_character)
            multibyte_buffer.clear()
            is_in_multibyte = False
            multibytes_expected = 0
            mis_encoded_utf8_present = True
        
    if multibyte_buffer:  # if we have left-over data
        handle_bad_data(len(input_string), "")
    
    return mis_encoded_utf8_present, "".join(output)

def get_gabPosts(files_found, report_folder, seeker, wrap_text):

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
                        text = utf8_in_extended_ascii(text)[1]
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
                logfunc(f'No Gab - Posts')
                
        
        if filename.endswith('_account_info.csv'):
            data_list_posts =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        created = item[7]
                        updated = item[8]
                        username = item[1]
                        id = item[0]
                        note = item[9]
                        displayname = item[10]
                        avatarfilename = item[13]
                        avatarcontenttype = item[14]
                        avatarfilesize = item[15]
                        avatarupdatedat = item[16]
                        headerfilename = item[17]
                        headercontenttype = item[18]
                        headerfilesize = item[19]
                        headerupdatedat = item[20]
                        locked = item[23]
                        memorial = item[31]
                        ispro = item[40]
                        isverified = item[42]
                        isdonor = item[43]
                        isinvestor = item[44]
                        isflagged = item[45]
                        weightedtsv = item[47]
                        domain = item[2]
                        secret = item[3]
                        remoteurl = item[4]
                        salmonurl = item[5]
                        hubyurl = item[6]
                        uri = item[11]
                        url = item[12]
                        avatarremoteurl = item[21]
                        subscription = item[22]
                        headerremoteurl = item[24]
                        lastwebfingeredat = item[25]
                        inboxurl = item[26]
                        outboxurl = item[27]
                        sharedinboxurl = item[28]
                        followersurl = item[29]
                        protocol = item[30]
                        movedtoaccountid = item[32]
                        featuredcollectionurl = item[33]
                        fields = item[34]
                        actortype = item[35]
                        discoverable = item[36]
                        alsoknownas = item[37]
                        silencedat = item[38]
                        suspendedat = item[39]
                        proexpiresat = item[41]
                        spamflag = item[46]
                        
                        data_list_posts.append((created,updated,username,id,note,displayname,avatarfilename,avatarcontenttype,avatarfilesize,avatarupdatedat,headerfilename,headercontenttype,headerfilesize,headerupdatedat,locked,memorial,ispro,isverified,isdonor,isinvestor,isflagged,weightedtsv,domain,secret,remoteurl,salmonurl,hubyurl,uri,url,avatarremoteurl,subscription,headerremoteurl,lastwebfingeredat,inboxurl,outboxurl,sharedinboxurl,followersurl,protocol,movedtoaccountid,featuredcollectionurl,fields,actortype,discoverable,alsoknownas,silencedat,suspendedat,proexpiresat,spamflag))
                        
            if data_list_posts:
                report = ArtifactHtmlReport(f'Gab - Account Info')
                report.start_artifact_report(report_folder, f'Gab - Account Info')
                report.add_script()
                data_headers = ('Timestamp','Updated','Username','ID','Note','Display Name','Avatar Filename','Avatar Content Type','Avatar File Size','Avatar Updated At','Header File Name','Header Content Type','Header File Size','Header Updated At','Locked','Memorial','Is Pro','Is Verified','Is Donor','Is Investor','Is Flagged','Weighted TSV','Domain','Secret','Remote URL','Salmon URL','Hub URL','URI','URL','Avatar Remote URL','Subscription','Header Remote URL','Last Web Fingered At','Inbox URL','Outbox URL','Shared Inbox URL','Followers URL','Protocol','Moved To Account ID','Featured Collection URL','Fields','Actor Type','Discoverable','Also Known As','Silenced At','Suspended At','Pro Expires At','Spam Flag')
                report.write_artifact_data_table(data_headers, data_list_posts, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Gab - Account Info'
                tsv(report_folder, data_headers, data_list_posts, tsvname)
                
                tlactivity = f'Gab - Account Info'
                timeline(report_folder, tlactivity, data_list_posts, data_headers)
                
                
            else:
                logfunc(f'No Gab - Account Info')

        if filename.endswith('_blocks.csv'):
            data_list_posts =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        createdatt = item[0]
                        accountidd = item[1]
                        targetaccountt = item[2]
                        blocked = item[3]
                        
                        
                        data_list_posts.append((createdatt,accountidd,targetaccountt,blocked,))
                        
            if data_list_posts:
                report = ArtifactHtmlReport(f'Gab - Blocks')
                report.start_artifact_report(report_folder, f'Gab - Blocks')
                report.add_script()
                data_headers = ('Timestamp','Account ID','Target Account ID','Blocked')
                report.write_artifact_data_table(data_headers, data_list_posts, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Gab - Blocks'
                tsv(report_folder, data_headers, data_list_posts, tsvname)
                
                tlactivity = f'Gab - Blocks'
                timeline(report_folder, tlactivity, data_list_posts, data_headers)
                
                
            else:
                logfunc(f'No Gab - Blocks')
                
        if filename.endswith('_followers.csv'):
            data_list_posts =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        username = item[0]
                        
                        data_list_posts.append((username,))
                        
            if data_list_posts:
                report = ArtifactHtmlReport(f'Gab - Followers')
                report.start_artifact_report(report_folder, f'Gab - Followers')
                report.add_script()
                data_headers = ('Username',)
                report.write_artifact_data_table(data_headers, data_list_posts, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Gab - Followers'
                tsv(report_folder, data_headers, data_list_posts, tsvname)
                
                #tlactivity = f'Gab - Followers'
                #timeline(report_folder, tlactivity, data_list_posts, data_headers)
                
                
            else:
                logfunc(f'No Gab - Blocks')
                
        if filename.endswith('_following.csv'):
            data_list_posts =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        username = item[0]
                        
                        data_list_posts.append((username,))
                        
            if data_list_posts:
                report = ArtifactHtmlReport(f'Gab - Following')
                report.start_artifact_report(report_folder, f'Gab - Following')
                report.add_script()
                data_headers = ('Username',)
                report.write_artifact_data_table(data_headers, data_list_posts, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Gab - Following'
                tsv(report_folder, data_headers, data_list_posts, tsvname)
                
                #tlactivity = f'Gab - Followers'
                #timeline(report_folder, tlactivity, data_list_posts, data_headers)
                
                
            else:
                logfunc(f'No Gab - Blocks')
                
        if filename.endswith('_likes.csv'):
            data_list_posts =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        createdat1 = item[0]
                        id = item[1]
                        uri = item[2]
                        createdat2 = item[3]
                        text = item[4]
                        text = utf8_in_extended_ascii(text)[1]
                        url = item[5]
                        accountid = item[6]
                        data_list_posts.append((createdat1,id,uri,createdat2,text,url,accountid))
                        
            if data_list_posts:
                report = ArtifactHtmlReport(f'Gab - Likes')
                report.start_artifact_report(report_folder, f'Gab - Likes')
                report.add_script()
                data_headers = ('Created At','ID','URI','Created At','Text','URL','Account ID')
                report.write_artifact_data_table(data_headers, data_list_posts, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Gab - Likes'
                tsv(report_folder, data_headers, data_list_posts, tsvname)
                
                #tlactivity = f'Gab - Followers'
                #timeline(report_folder, tlactivity, data_list_posts, data_headers)
                
                
            else:
                logfunc(f'No Gab - Likes')

        if filename.endswith('_mentions.csv'):
            data_list_posts =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        createdat1 = item[0]
                        id = item[1]
                        uri = item[2]
                        createdat2 = item[3]
                        text = item[4]
                        text = utf8_in_extended_ascii(text)[1]
                        url = item[5]
                        accountid = item[6]
                        data_list_posts.append((createdat1,id,uri,createdat2,text,url,accountid))
                        
            if data_list_posts:
                report = ArtifactHtmlReport(f'Gab - Mentions')
                report.start_artifact_report(report_folder, f'Gab - Mentions')
                report.add_script()
                data_headers = ('Created At','ID','URI','Created At','Text','URL','Account ID')
                report.write_artifact_data_table(data_headers, data_list_posts, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Gab - Mentions'
                tsv(report_folder, data_headers, data_list_posts, tsvname)
                
                #tlactivity = f'Gab - Followers'
                #timeline(report_folder, tlactivity, data_list_posts, data_headers)
                
                
            else:
                logfunc(f'No Gab - Mentions')

        if filename.endswith('_replies.csv'):
            data_list_posts =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        created_at = item[3]
                        updated_at = item[4]
                        id = item[0]
                        uri = item[1]
                        text = item[2]
                        in_reply_to_id = item[5]
                        reblog_of_id  = item[6]
                        url = item[7]
                        sensitive = item[8]
                        visibility = item[9]
                        spoiler_text = item[10]
                        reply = item[11]
                        language = item[12]
                        conversation_id	= item[13]
                        local  = item[14]
                        account_id = item[15]	
                        application_id = item[16]	
                        in_reply_to_account_id = item[17]	
                        poll_id = item[18]	
                        group_id = item[19]	
                        quote_of_id = item[20]	
                        revised_at = item[21]	
                        markdown = item[22]	
                        expires_at = item[23]	
                        has_quote = item[24]	
                        tombstoned_at = item[25]
                        
                        data_list_posts.append((created_at,updated_at,id,uri,text,	in_reply_to_id,reblog_of_id,url,sensitive,visibility,spoiler_text,reply,language,conversation_id,local,account_id,application_id,in_reply_to_account_id,poll_id,group_id,quote_of_id,revised_at,markdown,	expires_at,has_quote,tombstoned_at))
                        
            if data_list_posts:
                report = ArtifactHtmlReport(f'Gab - Replies')
                report.start_artifact_report(report_folder, f'Gab - Replies')
                report.add_script()
                data_headers = ('Timestamp','updated_at','id','uri','text',	'in_reply_to_id','reblog_of_id','url','sensitive','visibility','spoiler_text','reply','language','conversation_id','local','account_id','application_id','in_reply_to_account_id','poll_id','group_id','quote_of_id','revised_at','markdown','expires_at','has_quote','tombstoned_at')
                report.write_artifact_data_table(data_headers, data_list_posts, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Gab - Replies'
                tsv(report_folder, data_headers, data_list_posts, tsvname)
                
                #tlactivity = f'Gab - Followers'
                #timeline(report_folder, tlactivity, data_list_posts, data_headers)
                
                
            else:
                logfunc(f'No Gab - Replies')
                
        if filename.endswith('_session_activations.csv'):
            data_list_posts =[]
            with open(file_found, 'r', errors='backslashreplace') as f:
                for line in f:
                    delimited = csv.reader(f, delimiter=',')
                    for item in delimited:
                        createdat = item[2]
                        updatedat = item[3]
                        id = item[0]
                        sessionid = item[1]
                        useragent = item[4]
                        ip = item[5]
                        accesstoken = item[6]
                        userid = item[7]
                        webpushsubid = item[8]
                        data_list_posts.append((createdat,updatedat,id,sessionid,useragent,ip,accesstoken,userid,webpushsubid))
                        
            if data_list_posts:
                report = ArtifactHtmlReport(f'Gab - Session Activations')
                report.start_artifact_report(report_folder, f'Gab - Session Activations')
                report.add_script()
                data_headers = ('Created At','Updated At','ID','Session ID','User Agent','IP','Access Token ID','User ID','Web Push Subscription ID')
                report.write_artifact_data_table(data_headers, data_list_posts, file_found, html_no_escape=['Media'])
                report.end_artifact_report()
                
                tsvname = f'Gab - Session Activations'
                tsv(report_folder, data_headers, data_list_posts, tsvname)
                
                #tlactivity = f'Gab - Followers'
                #timeline(report_folder, tlactivity, data_list_posts, data_headers)
                
                
            else:
                logfunc(f'Gab - Session Activations')
                
                
__artifacts__ = {
        "gabPosts": (
            "Gab Returns",
            ('*/*_posts.csv','*/*_account_info.csv','*/*_blocks.csv','*/*_followers.csv','*/*_likes.csv','*/*_mentions.csv','*/*_replies.csv','*/*_session_activations.csv'),
            get_gabPosts)
}
