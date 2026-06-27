__artifacts_v2__ = {
    "instagramMessageReq": {  # This should match the function name exactly
        "name": "Instagram Archive - Message Request",
        "description": "Parses Instagram message requests",
        "author": "@AlexisBrignoni",
        "creation_date": "2021-08-30",
        "last_update_date": "2025-07-03",
        "requirements": "none",
        "category": "Instagram Archive",
        "notes": "",
        "paths": ('*/messages/message_requests/*'),
        "output_types": "standard",  # or ["html", "tsv", "timeline", "lava"]
        "artifact_icon": "instagram",
        "html_columns": ['Media','Reactions'],
    }
}

import os
import json

from scripts.ilapfuncs import artifact_processor, utf8_in_extended_ascii, check_in_media, convert_unix_ts_to_utc

@artifact_processor
def instagramMessageReq(context):
    files_found = context.get_files_found()
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('message_1.json'):
            
            with open(file_found, "r", encoding="utf-8") as fp:
                deserialized = json.load(fp)
        
            participants = deserialized.get('participants')
            names = ''
            for name in participants:
                names = names + f'{name["name"]}, '
            names = names.strip()[:-1]
            names = utf8_in_extended_ascii(names)[1]
            
            title  = deserialized.get('title', '')
            title = utf8_in_extended_ascii(title)[1]
            
            thread_type = deserialized.get('thread_type', '')
            
            is_still_participant = deserialized.get('is_still_participant', '')
            
            
            for x in deserialized['messages']:
                agregator_reac = ''
                media_items = []
                share_info = ''
                
                sender_name = x.get('sender_name', '')
                sender_name = utf8_in_extended_ascii(sender_name)[1]
                
                timestamp = x.get('timestamp_ms', '')
                
                share = x.get('share','')
                if share:
                    link = share.get('link','')
                    share_text = share.get('share_text','')
                    share_text = utf8_in_extended_ascii(share_text)[1]
                    content_owner = share.get('original_content_owner', '')
                    content_owner = utf8_in_extended_ascii(content_owner)[1]
                    share_info = f'Shared: {link}'
                    if share_text:
                        share_info = share_info + f'\nShared Text: {share_text}'
                    if content_owner:
                        share_info = share_info + f'\nOriginal Content Owner: {content_owner}'
                    
                
                reactions = x.get('reactions', '')
                if reactions:
                    counter = 0
                    agregator_reac = agregator_reac + ('<table>')
                    for reac in reactions:
                        if counter == 0:
                            agregator_reac = agregator_reac +('<tr>')
                        reaction = reac.get('reaction', '')
                        reaction = utf8_in_extended_ascii(reaction)[1]
                        actor = reac.get('actor', '')
                        actor = utf8_in_extended_ascii(actor)[1]
                            
                        counter = counter + 1
                        agregator_reac = agregator_reac + f'<td>{reaction}<br>{actor}</td>'
                        #hacer uno que no tenga html
                        if counter == 2:
                            counter = 0
                            agregator_reac = agregator_reac + ('</tr>')
                    if counter == 1:
                        agregator_reac = agregator_reac + ('</tr>')
                    agregator_reac = agregator_reac + ('</table><br>')
                
                timestamp = convert_unix_ts_to_utc(timestamp) if timestamp else ''
                content = x.get('content', '' )
                content = utf8_in_extended_ascii(content)[1]
                if share_info:
                    content = (content + '\n' + share_info).strip()
                type = x.get('type', '')
                is_unsent = x.get('is_unsent', '')
                
                photos = x.get('photos', '')
                if photos:
                    for pics in photos:
                        uri = pics.get('uri', '')
                        if uri:
                            ref = check_in_media(uri, os.path.basename(uri))
                            if ref:
                                media_items.append(ref)
                
                videos = x.get('videos', '')
                if videos:
                    for vids in videos:
                        uri = vids.get('uri', '')
                        if uri:
                            ref = check_in_media(uri, os.path.basename(uri))
                            if ref:
                                media_items.append(ref)
                
                data_list.append((timestamp, title, names, sender_name, content, media_items, agregator_reac, is_unsent, type, thread_type, is_still_participant, context.get_relative_path(file_found)))
    
    data_headers = (('Timestamp', 'datetime'), 'Party Account Name', 'Participants', 'Sender Account Name', 'Content', ('Media','media'), 'Reactions', 'Is Unsent', 'Type', 'Thread Type', 'Is Still Participant','Source File')
    return data_headers, data_list, 'See source path(s) below'