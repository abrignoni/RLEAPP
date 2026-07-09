__artifacts_v2__ = {
    "chatgptConversationsMetadata": {
        "name": "ChatGPT - Conversations Metadata",
        "description": "Metadata from ChatGPT conversations parsed from a ChatGPT data export (conversations.json). This parser is based on a research project.",
        "author": "Evangelos Dragonas (@theAtropos4n6)",
        "creation_date": "2024-07-09",
        "last_update_date": "2024-07-09",
        "requirements": "none",
        "category": "ChatGPT",
        "notes": "Latest validation date: 9 July 2024.",
        "paths": ('**/conversations.json',),
        "output_types": "standard",
        "artifact_icon": "message-2",
    },
    "chatgptConversations": {
        "name": "ChatGPT - Conversations",
        "description": "User conversations with ChatGPT parsed from a ChatGPT data export (conversations.json). This parser is based on a research project.",
        "author": "Evangelos Dragonas (@theAtropos4n6)",
        "creation_date": "2024-07-09",
        "last_update_date": "2024-07-09",
        "requirements": "none",
        "category": "ChatGPT",
        "notes": "Latest validation date: 9 July 2024.",
        "paths": ('**/conversations.json',),
        "output_types": "standard",
        "artifact_icon": "messages",
    },
    "chatgptSharedConversations": {
        "name": "ChatGPT - Shared Conversations",
        "description": "Metadata from ChatGPT shared conversations parsed from a ChatGPT data export (shared_conversations.json).",
        "author": "Evangelos Dragonas (@theAtropos4n6)",
        "creation_date": "2024-07-09",
        "last_update_date": "2024-07-09",
        "requirements": "none",
        "category": "ChatGPT",
        "notes": "Latest validation date: 9 July 2024.",
        "paths": ('**/shared_conversations.json',),
        "output_types": "standard",
        "artifact_icon": "share",
    },
    "chatgptMessageFeedback": {
        "name": "ChatGPT - Message Feedback",
        "description": "ChatGPT message feedback parsed from a ChatGPT data export (message_feedback.json).",
        "author": "Evangelos Dragonas (@theAtropos4n6)",
        "creation_date": "2024-07-09",
        "last_update_date": "2024-07-09",
        "requirements": "none",
        "category": "ChatGPT",
        "notes": "Latest validation date: 9 July 2024.",
        "paths": ('**/message_feedback.json',),
        "output_types": "standard",
        "artifact_icon": "message-report",
    },
}

import json
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc


def _flat(value):
    '''Serialize dict/list values so they store cleanly as text.'''
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return value


def _iso_to_utc(value):
    '''Parse an ISO-8601 timestamp string to an aware UTC datetime; keep raw on failure.'''
    if not value:
        return ''
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        return value
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


@artifact_processor
def chatgptConversationsMetadata(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'conversations.json':
            continue
        source_path = file_found
        with open(file_found, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for conversation in data:
            create_time = convert_unix_ts_to_utc(conversation.get("create_time")) if conversation.get("create_time") else ''
            update_time = convert_unix_ts_to_utc(conversation.get("update_time")) if conversation.get("update_time") else ''
            data_list.append((
                create_time,
                update_time,
                conversation.get("title", ""),
                conversation.get("id", ""),
                _flat(conversation.get("moderation_results", "")),
                _flat(conversation.get("plugin_ids", "")),
                conversation.get("gizmo_id", ""),
                conversation.get("is_archived", ""),
            ))

    data_headers = (
        ('Creation Time', 'datetime'),
        ('Modification Date', 'datetime'),
        'Title', 'Conversation ID', 'Moderation Results', 'Plugin IDs',
        'Gizmo ID', 'Is Archived',
    )
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def chatgptConversations(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'conversations.json':
            continue
        source_path = file_found
        with open(file_found, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for conversation in data:
            conversation_title = conversation.get("title", "")
            conversation_id = conversation.get("id", "")
            if not isinstance(conversation.get("mapping"), dict):
                continue
            for _message_id, message_details in conversation.get("mapping", {}).items():
                message_id = message_details.get("id")
                msg_content = message_details.get("message")
                if not msg_content:
                    continue
                author = msg_content.get("author", "") or {}
                author_role = author.get("role", "") if isinstance(author, dict) else ""
                author_name = author.get("name", "") if isinstance(author, dict) else ""
                author_metadata = author.get("metadata", "") if isinstance(author, dict) else ""
                msg_create_time = convert_unix_ts_to_utc(msg_content.get("create_time")) if msg_content.get("create_time") is not None else ""
                msg_update_time = convert_unix_ts_to_utc(msg_content.get("update_time")) if msg_content.get("update_time") is not None else ""
                content = msg_content.get("content", "") or {}
                content_type = content.get("content_type", "") if isinstance(content, dict) else ""
                content_language = content.get("language", "") if isinstance(content, dict) else ""
                content_text = content.get("text", "") if isinstance(content, dict) else ""
                content_parts = content.get("parts", "") if isinstance(content, dict) else ""
                status = msg_content.get("status", "")
                end_turn = msg_content.get("end_turn", "")
                weight = msg_content.get("weight", "")
                metadata = msg_content.get("metadata", False) or {}
                is_visually_hidden = metadata.get("is_visually_hidden_from_conversation", "") if isinstance(metadata, dict) else ""
                user_context = metadata.get("user_context_message_data", "") if isinstance(metadata, dict) else ""
                if isinstance(user_context, dict):
                    about_user_message = user_context.get("about_user_message", "")
                    about_model_message = user_context.get("about_model_message", "")
                else:
                    about_user_message = ""
                    about_model_message = ""
                voice_mode_message = metadata.get("voice_mode_message", "") if isinstance(metadata, dict) else ""
                recipient = msg_content.get("recipient", "")
                data_list.append((
                    msg_create_time, msg_update_time, message_id, conversation_title,
                    conversation_id, author_role, author_name, _flat(content_parts),
                    about_user_message, about_model_message, content_type, content_language,
                    content_text, _flat(metadata), status, voice_mode_message,
                    _flat(author_metadata), is_visually_hidden, end_turn, weight, recipient,
                ))

    data_headers = (
        ('Creation Time', 'datetime'),
        ('Modification Date', 'datetime'),
        'Message ID', 'Conversation Title', 'Conversation ID', 'Author (Role)',
        'Author (Name)', 'Parts', 'Custom Instructions (User)', 'Custom Instructions (Model)',
        'Content Type', 'Language', 'Text', 'Rest Metadata', 'Status', 'Voice Chat',
        'Author (Metadata)', 'Is Visually Hidden From Conversation', 'End Turn', 'Weight',
        'Recipient',
    )
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def chatgptSharedConversations(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'shared_conversations.json':
            continue
        source_path = file_found
        with open(file_found, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for conversation in data:
            data_list.append((
                conversation.get("id", ""),
                conversation.get("conversation_id", ""),
                conversation.get("title", ""),
                conversation.get("is_anonymous", False),
            ))

    data_headers = ('Share ID', 'Conversation ID', 'Title', 'Is Anonymous')
    return data_headers, data_list, context.get_relative_path(source_path)


@artifact_processor
def chatgptMessageFeedback(context):
    data_list = []
    source_path = ''
    for file_found in context.get_files_found():
        file_found = str(file_found)
        if os.path.basename(file_found) != 'message_feedback.json':
            continue
        source_path = file_found
        with open(file_found, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for feedback in data:
            data_list.append((
                _iso_to_utc(feedback.get("create_time", "")),
                feedback.get("user_id", ""),
                feedback.get("id", ""),
                feedback.get("conversation_id", ""),
                feedback.get("rating", ""),
                feedback.get("workspace_id", ""),
                _flat(feedback.get("content", "")),
                feedback.get("storage_protocol", ""),
            ))

    data_headers = (
        ('Creation Time', 'datetime'),
        'User ID', 'Message ID', 'Conversation ID', 'Rating', 'Workspace ID',
        'Content', 'Storage Protocol',
    )
    return data_headers, data_list, context.get_relative_path(source_path)
