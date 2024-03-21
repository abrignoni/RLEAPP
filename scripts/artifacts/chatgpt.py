__artifacts_v2__ = {
    "chatgpt": {
        "name": "ChatGPT",
        "description": "Parses user's ChatGPT data export. Parser includes conversations, user info, and others. This parser is based on a research project",
        "author": "Evangelos Dragonas (@theAtropos4n6)",
        "version": "1.0.1",
        "date": "2024-02-10",
        "requirements": "",
        "category": "ChatGPT",
        "paths": (
            '**/conversations.json', 
            '**/chat.html',
            '**/message_feedback.json',
            '**/model_comparisons.json',
            '**/shared_conversations.json',
            '**/user.json',
        ),
        "function": "get_chatgpt"
    }
}



import json
import os
from pathlib import Path
from datetime import datetime
from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, convert_utc_human_to_timezone,convert_ts_int_to_timezone,convert_ts_human_to_utc,is_platform_windows


def get_chatgpt(files_found, report_folder, seeker, wrap_text, time_offset):
    conversations_metadata = []
    conversations_messages = []
    draft_messages = []
    account_list = []
    account_list_files_found = []
    voice_list = []
    photo_list = []
    for file_found in files_found:
        file_found = str(file_found)
        #counter += 1 
        file_name = os.path.basename(file_found)
        if file_name.endswith('conversations.json') and 'shared_' not in file_name:
            with open(file_found, 'r', encoding='utf-8') as file:
                data = json.load(file)
                conversations_metadata = []
                conversations_messages = []
                for conversations in data:
                    conversation_title = conversations.get("title","")
                    conversation_id = conversations.get("id","")
                    create_time = convert_ts_int_to_timezone(int(conversations.get("create_time", 0)),time_offset)
                    update_time = convert_ts_int_to_timezone(int(conversations.get("update_time", 0)),time_offset)
                    moderation_results = conversations.get("moderation_results","")
                    plugin_ids = conversations.get("plugin_ids","")
                    gizmo_id = conversations.get("gizmo_id","")
                    is_archived = conversations.get("is_archived","")
                    conversations_metadata.append((create_time,update_time,conversation_title,conversation_id,moderation_results,plugin_ids,gizmo_id,is_archived))

                    if isinstance(conversations.get("mapping"), dict):
                        for messageId, message_details in conversations.get("mapping", {}).items():
                            message_id = message_details.get("id")
                            if message_details.get("message"):
                                msg_content = message_details.get("message")
                                author_role = msg_content.get("author", "").get("role", "")
                                author_name = msg_content.get("author", "").get("name", "")
                                author_metadata = msg_content.get("author", "").get("metadata", "")
                                msg_create_time = convert_ts_int_to_timezone(int(msg_content.get("create_time", 0)),time_offset) if msg_content.get("create_time") is not None else ""
                                msg_update_time = convert_ts_int_to_timezone(int(msg_content.get("update_time", 0)),time_offset) if msg_content.get("update_time") is not None else ""
                                content_type = msg_content.get("content", "").get("content_type", "")
                                content_language = msg_content.get("content", "").get("language", "")
                                content_text = msg_content.get("content", "").get("text", "")
                                content_parts = msg_content.get("content", "").get("parts", "")
                                status = msg_content.get("status", "")
                                end_turn = msg_content.get("end_turn", "")
                                weight = msg_content.get("weight", "")
                                is_visually_hidden_from_conversation = msg_content.get("metadata", False).get("is_visually_hidden_from_conversation", "")
                                if isinstance(msg_content.get("metadata").get("user_context_message_data", ""), dict):
                                    about_user_message = msg_content.get("metadata").get("user_context_message_data", "").get("about_user_message", "")
                                    about_model_message = msg_content.get("metadata").get("user_context_message_data", "").get("about_model_message", "")
                                else:
                                    about_user_message = ""
                                    about_model_message = ""
                                voice_mode_message = msg_content.get("metadata", False).get("voice_mode_message", "")
                                rest_metadata = msg_content.get("metadata", False)
                                recipient = msg_content.get("recipient", "")
                                conversations_messages.append((msg_create_time,msg_update_time,message_id,conversation_title,conversation_id,author_role,author_name,content_parts,about_user_message,about_model_message,content_type,content_language,content_text,rest_metadata,status,voice_mode_message,author_metadata,is_visually_hidden_from_conversation,end_turn,weight,recipient))
                                
                                # create_time_msg = convert_utc_human_to_timezone(convert_ts_int_to_utc(int(msg_create_time)), time_offset)
                                # print(create_time_msg)
                            #parsing collected conversations metadata
                if len(conversations_metadata) > 0:
                    description = f'Metadata from ChatGPT conversations'
                    report = ArtifactHtmlReport(f'ChatGPT - Conversations Metadata')
                    report.start_artifact_report(report_folder, f'ChatGPT - Conversations Metadata', description)
                    report.add_script()
                    data_headers = ('Creation Time','Modification Date','Title','Conversation ID','Moderation Results','Plugin IDs','Gizmo ID','Is Archived') 
                    report.write_artifact_data_table(data_headers, conversations_metadata, file_found, html_escape=False)
                    report.end_artifact_report()
                    
                    tsvname = f'ChatGPT - Conversations Metadata'
                    tsv(report_folder, data_headers, conversations_metadata, tsvname)

                    tlactivity = f'ChatGPT - Conversations Metadata'
                    timeline(report_folder, tlactivity, conversations_metadata, data_headers)
                else:
                    logfunc(f'No ChatGPT - Conversations Metadata available')

                #parsing collected conversations metadata
                if len(conversations_messages) > 0:
                    description = f'User conversations with ChatGPT'
                    report = ArtifactHtmlReport(f'ChatGPT - Conversations')
                    report.start_artifact_report(report_folder, f'ChatGPT - Conversations', description)
                    report.add_script()
                    data_headers = ('Creation Time','Modification Date','Message ID','Conversation Title','Conversation ID','Author (Role)','Author (Name)','Parts','Custom Instructions (User)','Custom Instructions (Model)','Content Type','Language','Text','Rest Metadata','Status','Voice Chat','Author (Metadata)','Is Visually Hidden From Conversation','End Turn','Weight','Recipient')
                    report.write_artifact_data_table(data_headers, conversations_messages, file_found, html_escape=False)
                    report.end_artifact_report()
                    
                    tsvname = f'ChatGPT - Conversations'
                    tsv(report_folder, data_headers, conversations_messages, tsvname)

                    tlactivity = f'ChatGPT - Conversations'
                    timeline(report_folder, tlactivity, conversations_messages, data_headers)
                else:
                    logfunc(f'No ChatGPT - Conversations available')
        
        if file_name.endswith('shared_conversations.json'):
            with open(file_found, 'r', encoding='utf-8') as file:
                data = json.load(file)
                shared_conversations_metadata = []
                for conversations in data:
                    conversation_title = conversations.get("title","")
                    share_id = conversations.get("id","")
                    conversation_anonymous = conversations.get("is_anonymous",False)
                    conversation_id = conversations.get("conversation_id","")
                    shared_conversations_metadata.append((share_id,conversation_id,conversation_title,conversation_anonymous))

                if len(shared_conversations_metadata) > 0:
                    description = f'Metadata from ChatGPT shared conversations'
                    report = ArtifactHtmlReport(f'ChatGPT - Shared Conversations')
                    report.start_artifact_report(report_folder, f'ChatGPT - Shared Conversations', description)
                    report.add_script()
                    data_headers = ('Share ID','Conversation ID','Title','Is Anonymous') 
                    report.write_artifact_data_table(data_headers, shared_conversations_metadata, file_found, html_escape=False)
                    report.end_artifact_report()
                    
                    tsvname = f'ChatGPT - Shared Conversations'

                    tsv(report_folder, data_headers, shared_conversations_metadata, tsvname)
                else:
                    logfunc(f'No ChatGPT - Shared Conversations available')

        if file_name.endswith('user.json'):
            with open(file_found, 'r', encoding='utf-8') as file:
                data = json.load(file)
                user = []
                user_id = data.get("id","")
                email = data.get("email","")
                chatgpt_plus_user = data.get("chatgpt_plus_user",False)
                user.append((user_id,email,chatgpt_plus_user))

                if len(user) > 0:
                    description = f'ChatGPT user info'
                    report = ArtifactHtmlReport(f'ChatGPT - User')
                    report.start_artifact_report(report_folder, f'ChatGPT - User', description)
                    report.add_script()
                    data_headers = ('User ID','Email','Is ChatGPT Plus User') 
                    report.write_artifact_data_table(data_headers, user, file_found, html_escape=False)
                    report.end_artifact_report()
                    
                    tsvname = f'ChatGPT - User'
                    tsv(report_folder, data_headers, user, tsvname)
                else:
                    logfunc(f'No ChatGPT - User available')

        if file_name.endswith('message_feedback.json'):
            with open(file_found, 'r', encoding='utf-8') as file:
                data = json.load(file)
                message_feedback = []
                for feedback in data:
                    msg_id = feedback.get("id","")
                    conv_id = feedback.get("conversation_id","")
                    user_id = feedback.get("user_id","")
                    rating = feedback.get("rating","")
                    formatted_timestamp = feedback.get("create_time","").split('T')[0] + ' ' + feedback.get("create_time","").split('T')[1].split('.')[0] #converts iso format to ilapp function's desired input
                    create_time = convert_utc_human_to_timezone(convert_ts_human_to_utc(formatted_timestamp), time_offset)
                    workspace_id = feedback.get("workspace_id","")
                    content = feedback.get("content","")
                    storage_protocol = feedback.get("storage_protocol","")
                    message_feedback.append((create_time,user_id,msg_id,conv_id,rating,workspace_id,content,storage_protocol))

                if len(message_feedback) > 0:
                    description = f'ChatGPT message feedback'
                    report = ArtifactHtmlReport(f'ChatGPT - Message Feedback')
                    report.start_artifact_report(report_folder, f'ChatGPT - Message Feedback', description)
                    report.add_script()
                    data_headers = ('Creation Time','User ID','Message ID','Conversation ID','Rating','Workspace ID','Content','Storage Protocol') 
                    report.write_artifact_data_table(data_headers, message_feedback, file_found, html_escape=False)
                    report.end_artifact_report()
                    
                    tsvname = f'ChatGPT - Message Feedback'
                    tsv(report_folder, data_headers, message_feedback, tsvname)
                else:
                    logfunc(f'No ChatGPT - Message Feedback available')

        if file_name.endswith('chat.html'):
            pass 
        if file_name.endswith('model_comparisons.json'):
            pass 