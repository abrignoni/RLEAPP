# Module Description: Parses all TikTok data from "Download My Data" export (JSON files)
# Author: @upintheairsheep and @Jadoo4QFan
# Date: 2025-06-15
# Artifact version: 1.0
# Requirements: none
# Note: Gemini Code Assist was used during the script's development, however the code was then heavily tested against real exports.

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_tikTokData(files_found, report_folder, seeker, wrap_text):
    # Initialize all data lists
    favorite_effects = []
    blocked_users = []
    video_history = []
    comments = []
    favorite_hashtags = []
    favorite_sounds = []
    favorite_videos = []
    followers = []
    following = []
    hashtags_used = []
    liked_videos = []
    login_history = []
    search_history = []
    share_history = []
    status_info = []
    uploaded_videos = []
    off_tiktok_activity = []
    direct_messages = []
    profile_auto_fill = []
    profile_information = []
    watch_live_history = []
    watch_live_interactions = [] # For comments and questions
    app_settings_general = []
    tiktok_go_live_settings = []
    shop_communication_history = []
    shop_product_browsing_history = []
    shop_saved_addresses = []
    shop_shopping_cart = []
    shop_vouchers = []
    usage_data_third_party = []
    purchase_history_send_gifts = []
    purchase_history_buy_gifts = []
    ads_configuration = [] # For Ad Interests, DataPartnerList, AdvertiserList
    live_go_live_history = []

    for file_found in files_found:
        file_found = str(file_found)
        # Support both old and new TikTok data export filenames
        if not os.path.basename(file_found) in ('user_data.json', 'user_data_tiktok.json'):
            continue

        with open(file_found, encoding='utf-8', mode='r') as f:
            data = json.loads(f.read())

        # Get top-level structures from data
        activity_data = data.get('Activity', {})
        app_settings_data = data.get('App Settings', {})
        comment_data_root = data.get('Comment', {}) # 'Comment' is a top-level key in schema
        video_data_root = data.get('Video', {})     # 'Video' is a top-level key in schema
        profile_data_root = data.get('Profile', {}) # Profile is a top-level key
        tiktok_live_data_root = data.get('Tiktok Live', {}) # TikTok Live is a top-level key
        tiktok_shop_data_root = data.get('Tiktok Shopping', {}) # TikTok Shopping is a top-level key

        # Process each data type
        if 'Favorite Effects' in activity_data:
            for effect in activity_data['Favorite Effects'].get('FavoriteEffectsList', []):
                favorite_effects.append((effect.get('EffectLink', ''), effect.get('Date', ''))) # Changed 'Link' to 'EffectLink'

        if 'Block' in app_settings_data: # Changed from data to app_settings_data
            for user in app_settings_data['Block'].get('BlockList', []):
                blocked_users.append((user.get('UserName', ''), user.get('Date', '')))

        if 'Video Browsing History' in activity_data: # Changed from data to activity_data
            for video in activity_data['Video Browsing History'].get('VideoList', []):
                video_history.append((video.get('Link', ''), video.get('Date', '')))
        
        # Comments - handles old and new schema for field names and structure
        comments_list_location = None
        if 'Comments' in comment_data_root and 'CommentsList' in comment_data_root['Comments']:
            comments_list_location = comment_data_root['Comments'].get('CommentsList', [])
        elif 'CommentsList' in comment_data_root: # Fallback for older structure
            comments_list_location = comment_data_root.get('CommentsList', [])

        if comments_list_location:
            for comment_item in comments_list_location:
                # Try new schema field names first (lowercase), then old (capitalized)
                text = comment_item.get('comment', comment_item.get('Comment', ''))
                date_val = comment_item.get('date', comment_item.get('Date', ''))
                comments.append((text, date_val))

        if 'Favorite Hashtags' in activity_data: # Changed from data to activity_data
            for hashtag in activity_data['Favorite Hashtags'].get('FavoriteHashtagList', []):
                favorite_hashtags.append((hashtag.get('Link', ''), hashtag.get('Date', '')))

        if 'Favorite Sounds' in activity_data: # Changed from data to activity_data
            for sound in activity_data['Favorite Sounds'].get('FavoriteSoundList', []):
                favorite_sounds.append((sound.get('Link', ''), sound.get('Date', '')))

        if 'Favorite Videos' in activity_data: # Changed from data to activity_data
            for video in activity_data['Favorite Videos'].get('FavoriteVideoList', []):
                favorite_videos.append((video.get('Link', ''), video.get('Date', '')))

        if 'Follower List' in activity_data: # Changed from data to activity_data
            for follower in activity_data['Follower List'].get('FansList', []):
                followers.append((follower.get('UserName', ''), follower.get('Date', '')))

        if 'Following List' in activity_data: # Changed from data to activity_data
            for following_user in activity_data['Following List'].get('Following', []):
                following.append((following_user.get('UserName', ''), following_user.get('Date', '')))

        if 'Hashtag' in activity_data: # Changed from data to activity_data
            for hashtag in activity_data['Hashtag'].get('HashtagList', []):
                hashtags_used.append((hashtag.get('HashtagName', ''), hashtag.get('HashtagLink', '')))

        # Liked Videos - handles old and new schema for field names
        if 'Like List' in activity_data: # Changed from data to activity_data
            item_favorite_list = activity_data['Like List'].get('ItemFavoriteList', [])
            for video_item in item_favorite_list:
                link_val = video_item.get('link', video_item.get('Link', '')) # New 'link', old 'Link'
                date_val = video_item.get('date', video_item.get('Date', '')) # New 'date', old 'Date'
                liked_videos.append((link_val, date_val))

        if 'Login History' in activity_data: # Changed from data to activity_data
            for login in activity_data['Login History'].get('LoginHistoryList', []):
                login_history.append((
                    login.get('Date', ''),
                    login.get('IP', ''),
                    login.get('DeviceModel', ''),
                    login.get('DeviceSystem', ''),
                    login.get('NetworkType', ''),
                    login.get('Carrier', '')
                ))
        
        # Purchase History (New based on schema)
        purchase_history_data = activity_data.get('Purchase History', {})
        # SendGifts
        send_gifts_list = purchase_history_data.get('SendGifts', {}).get('SendGifts', [])
        if send_gifts_list: # Check if not None or empty
            for gift in send_gifts_list:
                purchase_history_send_gifts.append((gift.get('Date', ''), gift.get('GiftAmount', ''), gift.get('UserName', '')))
        
        # BuyGifts
        buy_gifts_list = purchase_history_data.get('BuyGifts', {}).get('BuyGifts', [])
        if buy_gifts_list: # Check if not None or empty
            for gift in buy_gifts_list:
                purchase_history_buy_gifts.append((gift.get('Date', ''), gift.get('Price', '')))

        if 'Search History' in activity_data: # Changed from data to activity_data
            for search in activity_data['Search History'].get('SearchList', []):
                search_history.append((search.get('SearchTerm', ''), search.get('Date', '')))

        if 'Share History' in activity_data: # Changed from data to activity_data
            for share in activity_data['Share History'].get('ShareHistoryList', []):
                share_history.append((
                    share.get('Date', ''),
                    share.get('SharedContent', ''),
                    share.get('Link', ''),
                    share.get('Method', '')
                ))

        if 'Status' in activity_data: # Changed from data to activity_data
            for status in activity_data['Status'].get('Status List', []):
                status_info.append((
                    status.get('Resolution', ''),
                    status.get('App Version', ''),
                    status.get('IDFA', ''),
                    status.get('GAID', ''),
                    status.get('Android ID', ''),
                    status.get('IDFV', ''),
                    status.get('Web ID', '')
                ))

        # Updated for 'Video' section based on schema: data['Video']['Videos']['VideoList']
        # and field name changes
        if 'Videos' in video_data_root:
            video_list_container = video_data_root['Videos']
            if 'VideoList' in video_list_container:
                for video_item in video_list_container.get('VideoList', []):
                    uploaded_videos.append((
                        video_item.get('Date', ''),
                        video_item.get('Link', ''),
                        video_item.get('Likes', ''),
                        video_item.get('WhoCanView', ''),
                        video_item.get('AllowComments', ''),
                        video_item.get('AllowStitches', ''),
                        video_item.get('AllowDuets', ''),
                        video_item.get('AllowStickers', ''),
                        video_item.get('AllowSharingToStory', ''),
                        video_item.get('ContentDisclosure', ''),
                        video_item.get('AIGeneratedContent', ''),
                        video_item.get('Sound', ''),
                        video_item.get('Location', ''),
                        video_item.get('Title', ''),
                        video_item.get('AddYoursText', '')
                    ))

        # Off TikTok Activity (New based on schema)
        ads_data = data.get('Ads and data', {})
        off_tiktok_activity_list = ads_data.get('Off TikTok Activity', {}).get('OffTikTokActivityDataList', [])
        for item in off_tiktok_activity_list:
            off_tiktok_activity.append((
                item.get('TimeStamp', ''),
                item.get('Source', ''),
                item.get('Event', '')
            ))

        # Ads and data - Ad Interests, Ads Based On Data Received From Partners (New based on schema)
        # ads_data is already defined
        ad_interests_cat = ads_data.get('Ad Interests', {}).get('AdInterestCategories', '')
        if ad_interests_cat:
            ads_configuration.append(('Ad Interest Categories', ad_interests_cat))
        
        ads_based_on_partners_data = ads_data.get('Ads Based On Data Received From Partners', {})
        data_partner_list_str = ads_based_on_partners_data.get('DataPartnerList', '')
        if data_partner_list_str:
            ads_configuration.append(('Data Partner List', data_partner_list_str))
        advertiser_list_str = ads_based_on_partners_data.get('AdvertiserList', '')
        if advertiser_list_str:
            ads_configuration.append(('Advertiser List', advertiser_list_str))

        # Usage Data From Third-Party Apps And Websites (New based on schema)
        # ads_data is already defined above for Off TikTok Activity
        usage_data_list = ads_data.get('Usage Data From Third-Party Apps And Websites', {}).get('UsageDataList', [])
        if usage_data_list: # Check if not None or empty
            for item in usage_data_list:
                usage_data_third_party.append((
                    item.get('TimeStamp', ''),
                    item.get('Source', ''),
                    item.get('Event', '')
                ))
        # Direct Messages (New based on schema)
        dm_root = data.get('Direct Messages', {})
        chat_history_container = dm_root.get('Chat History', {}).get('ChatHistory', {})
        for chat_key, messages_list in chat_history_container.items():
            # Extract target user from chat_key like "Chat History with USERNAME:"
            chat_with_user = chat_key.replace('Chat History with ', '').rstrip(':')
            for message in messages_list:
                direct_messages.append((message.get('Date', ''), chat_with_user, message.get('From', ''), message.get('Content', '')))

        # Profile - Auto Fill
        auto_fill_data = profile_data_root.get('Auto Fill', {})
        if auto_fill_data: # Check if auto_fill_data is not empty
            profile_auto_fill.append((
                auto_fill_data.get('PhoneNumber', 'N/A'),
                auto_fill_data.get('Email', 'N/A'),
                auto_fill_data.get('FirstName', 'N/A'),
                auto_fill_data.get('LastName', 'N/A'),
                auto_fill_data.get('Address', 'N/A'),
                auto_fill_data.get('ZipCode', 'N/A'),
                auto_fill_data.get('Unit', 'N/A'),
                auto_fill_data.get('City', 'N/A'),
                auto_fill_data.get('State', 'N/A'),
                auto_fill_data.get('Country', 'N/A')
            ))

        # Profile - Profile Information
        profile_info_container = profile_data_root.get('Profile Information', {})
        profile_map = profile_info_container.get('ProfileMap', {})
        if profile_map: # Check if profile_map is not empty
            profile_information.append((
                profile_map.get('userName', ''),
                profile_map.get('bioDescription', ''),
                profile_map.get('birthDate', ''),
                profile_map.get('emailAddress', ''),
                profile_map.get('telephoneNumber', ''),
                profile_map.get('likesReceived', ''),
                profile_map.get('profilePhoto', ''),
                profile_map.get('profileVideo', '')
            ))

        # TikTok Live - Watch Live History
        watch_live_history_map = tiktok_live_data_root.get('Watch Live History', {}).get('WatchLiveMap', {})
        for live_id, live_data in watch_live_history_map.items():
            if live_id == "-1" and not live_data.get('Link'): # Skip placeholder/empty entries
                continue
            
            watch_live_history.append((
                live_id,
                live_data.get('WatchTime', ''),
                live_data.get('Link', '')
            ))

            # Process Comments from this Live session
            comments_list = live_data.get('Comments', [])
            if comments_list: # Check if comments_list is not None
                for comment in comments_list:
                    watch_live_interactions.append((live_id, live_data.get('WatchTime', ''), 'Comment', comment.get('CommentTime', ''), comment.get('CommentContent', '')))
            
            # Process Questions from this Live session
            questions_list = live_data.get('Questions', [])
            if questions_list: # Check if questions_list is not None
                for question in questions_list:
                    watch_live_interactions.append((live_id, live_data.get('WatchTime', ''), 'Question', question.get('QuestionTime', ''), question.get('QuestionContent', '')))
        
        # App Settings - General Settings
        settings_map = app_settings_data.get('Settings', {}).get('SettingsMap', {})
        if settings_map:
            for key, value in settings_map.items():
                if isinstance(value, dict):
                    # Flatten nested dictionaries for simplicity in the report
                    value_str_parts = []
                    for sub_key, sub_value in value.items():
                        value_str_parts.append(f"{sub_key}: {sub_value}")
                    value_str = "; ".join(value_str_parts)
                elif isinstance(value, list):
                    value_str = ", ".join(map(str, value))
                else:
                    value_str = str(value) if value is not None else ""
                app_settings_general.append((key, value_str))

        # TikTok Live - Go Live Settings
        go_live_settings_map = tiktok_live_data_root.get('Go Live Settings', {}).get('SettingsMap', {})
        if go_live_settings_map:
            for key, value in go_live_settings_map.items():
                if isinstance(value, dict):
                    # Flatten nested dictionaries for simplicity in the report
                    value_str_parts = []
                    for sub_key, sub_value in value.items():
                        value_str_parts.append(f"{sub_key}: {sub_value}")
                    value_str = "; ".join(value_str_parts)
                elif isinstance(value, list):
                    value_str = ", ".join(map(str, value)) if value else "N/A" # Handle empty lists
                else:
                    value_str = str(value) if value is not None else "N/A"
                tiktok_go_live_settings.append((key, value_str))
        
        # TikTok Live - Go Live History (New based on schema)
        go_live_list = tiktok_live_data_root.get('Go Live History', {}).get('GoLiveList', [])
        if go_live_list: # Check if not None or empty
            for live_event in go_live_list:
                muted_list_val = live_event.get('MutedList')
                muted_list_str = ", ".join(map(str, muted_list_val)) if isinstance(muted_list_val, list) else str(muted_list_val)
                live_go_live_history.append((
                    live_event.get('LiveStartTime', ''),
                    live_event.get('LiveEndTime', ''),
                    live_event.get('LiveDuration', ''),
                    live_event.get('RoomId', ''),
                    live_event.get('RoomTitle', ''),
                    live_event.get('CoverUri', ''),
                    live_event.get('ReplayUrl', ''),
                    live_event.get('TotalEarning', ''),
                    live_event.get('TotalLike', ''),
                    live_event.get('TotalView', ''),
                    live_event.get('TotalGifter', ''),
                    live_event.get('QualitySetting', ''),
                    muted_list_str
                ))

        # TikTok Shopping - Communication History
        comm_history_map = tiktok_shop_data_root.get('Communication History', {}).get('CommunicationHistories', {})
        for shop_name_key, messages in comm_history_map.items():
            if isinstance(messages, list):
                for message in messages:
                    shop_communication_history.append((
                        message.get('send_time', ''),
                        shop_name_key, # shop_name is also in message, but key is more direct
                        message.get('direction', ''),
                        message.get('content', '') 
                    ))

        # TikTok Shopping - Product Browsing History
        product_browsing_list = tiktok_shop_data_root.get('Product Browsing History', {}).get('ProductBrowsingHistories', [])
        if product_browsing_list: # Check if not None
            for item in product_browsing_list:
                shop_product_browsing_history.append((
                    item.get('browsing_date', ''),
                    item.get('shop_name', ''),
                    item.get('product_name', '')
                ))

        # TikTok Shopping - Saved Address Information
        saved_address_list = tiktok_shop_data_root.get('Saved Address Information', {}).get('SavedAddress', [])
        if saved_address_list: # Check if not None
            for address in saved_address_list:
                shop_saved_addresses.append((address.get('receiver_name', ''), address.get('masked_phone_number', ''), address.get('adress_info', '')))

        # TikTok Shopping - Shopping Cart List
        shopping_cart_list = tiktok_shop_data_root.get('Shopping Cart List', {}).get('ShoppingCart', [])
        if shopping_cart_list: # Check if not None
            for item in shopping_cart_list:
                shop_shopping_cart.append((item.get('CreateTime', ''), item.get('ShopName', ''), item.get('ProductName', ''), item.get('SkuCount', '')))
        
        # TikTok Shopping - Vouchers
        vouchers_list = tiktok_shop_data_root.get('Vouchers', {}).get('Vouchers', [])
        if vouchers_list: # Check if not None
            for voucher in vouchers_list:
                shop_vouchers.append((voucher.get('ReceivedDate', ''), voucher.get('VoucherId', ''), voucher.get('VoucherName', 'N/A'), voucher.get('VoucherText', ''), voucher.get('Status', '')))
    # Generate reports for each data type
    def generate_report(title, data_list, headers, tsvname, tlactivity):
        if data_list:
            report = ArtifactHtmlReport(title)
            report.start_artifact_report(report_folder, title)
            report.add_script()
            report.write_artifact_data_table(headers, data_list, file_found)
            report.end_artifact_report()
            
            tsv(report_folder, headers, data_list, tsvname)
            timeline(report_folder, tlactivity, data_list, headers)
        else:
            logfunc(f'No {title} data available')

    # Generate all reports
    generate_report('TikTok Favorite Effects', favorite_effects, 
                   ['Link', 'Date'], 'TikTok Favorite Effects', 'TikTok Favorite Effects')
    
    generate_report('TikTok Blocked Users', blocked_users,
                   ['Username', 'Date'], 'TikTok Blocked Users', 'TikTok Blocked Users')
    
    generate_report('TikTok Video History', video_history,
                   ['URL', 'Date'], 'TikTok Video History', 'TikTok Video History')
    
    generate_report('TikTok Comments', comments,
                   ['Comment', 'Date'], 'TikTok Comments', 'TikTok Comments')
    
    generate_report('TikTok Favorite Hashtags', favorite_hashtags,
                   ['Link', 'Date'], 'TikTok Favorite Hashtags', 'TikTok Favorite Hashtags')
    
    generate_report('TikTok Favorite Sounds', favorite_sounds,
                   ['Link', 'Date'], 'TikTok Favorite Sounds', 'TikTok Favorite Sounds')
    
    generate_report('TikTok Favorite Videos', favorite_videos,
                   ['Link', 'Date'], 'TikTok Favorite Videos', 'TikTok Favorite Videos')
    
    generate_report('TikTok Followers', followers,
                   ['Username', 'Date'], 'TikTok Followers', 'TikTok Followers')
    
    generate_report('TikTok Following', following,
                   ['Username', 'Date'], 'TikTok Following', 'TikTok Following')
    
    generate_report('TikTok Hashtags Used', hashtags_used,
                   ['Hashtag Name', 'URL'], 'TikTok Hashtags Used', 'TikTok Hashtags Used')
    
    generate_report('TikTok Liked Videos', liked_videos,
                   ['Link', 'Date'], 'TikTok Liked Videos', 'TikTok Liked Videos')
    
    generate_report('TikTok Login History', login_history,
                   ['Date', 'IP Address', 'Device Model', 'OS', 'Network Type', 'Carrier'],
                   'TikTok Login History', 'TikTok Login History')
    
    generate_report('TikTok Search History', search_history,
                   ['Search Term', 'Date'], 'TikTok Search History', 'TikTok Search History')
    
    generate_report('TikTok Share History', share_history,
                   ['Date', 'Content Type', 'URL', 'Method'],
                   'TikTok Share History', 'TikTok Share History')
    
    generate_report('TikTok Status Info', status_info,
                   ['Screen Resolution', 'App Version', 'IDFA', 'GAID', 'Android ID', 'IDFV', 'Web ID'],
                   'TikTok Status Info', 'TikTok Status Info')
    
    generate_report('TikTok Uploaded Videos', uploaded_videos,
                   ['Date Uploaded', 'Direct URL', 'Like Count', 'Who Can View', 'Allow Comments', 'Allow Stitches', 'Allow Duets', 
                    'Allow Stickers', 'Allow Sharing To Story', 'Content Disclosure', 'AI Generated Content', 'Sound', 'Location', 'Title', 'Add Yours Text'],
                   'TikTok Uploaded Videos', 'TikTok Uploaded Videos')
    
    generate_report('TikTok Off-TikTok Activity', off_tiktok_activity,
                   ['Timestamp', 'Source', 'Event'],
                   'TikTok Off-TikTok Activity', 'TikTok Off-TikTok Activity')

    generate_report('TikTok Direct Messages', direct_messages,
                   ['Date', 'Chat With', 'From', 'Content'],
                   'TikTok Direct Messages', 'TikTok Direct Messages')

    generate_report('TikTok Profile Auto Fill', profile_auto_fill,
                   ['Phone Number', 'Email', 'First Name', 'Last Name', 'Address', 'Zip Code', 'Unit', 'City', 'State', 'Country'],
                   'TikTok Profile Auto Fill', 'TikTok Profile Auto Fill')

    generate_report('TikTok Profile Information', profile_information,
                   ['Username', 'Bio Description', 'Birth Date', 'Email Address', 'Telephone Number', 'Likes Received', 'Profile Photo URL', 'Profile Video URL'],
                   'TikTok Profile Information', 'TikTok Profile Information')

    generate_report('TikTok Watch Live History', watch_live_history,
                   ['Live ID', 'Watch Time', 'Link'],
                   'TikTok Watch Live History', 'TikTok Watch Live History')
    
    generate_report('TikTok Watch Live Interactions', watch_live_interactions,
                   ['Live ID', 'Live Watch Time', 'Interaction Type', 'Interaction Time', 'Content'],
                   'TikTok Watch Live Interactions', 'TikTok Watch Live Interactions')

    generate_report('TikTok App Settings', app_settings_general,
                   ['Setting Name', 'Setting Value'],
                   'TikTok App Settings', 'TikTok App Settings')

    generate_report('TikTok Go Live Settings', tiktok_go_live_settings,
                   ['Setting Name', 'Setting Value'],
                   'TikTok Go Live Settings', 'TikTok Go Live Settings')

    generate_report('TikTok Shop Communication History', shop_communication_history,
                   ['Send Time', 'Shop Name', 'Direction', 'Content (Encrypted)'],
                   'TikTok Shop Communication History', 'TikTok Shop Communication History')

    generate_report('TikTok Shop Product Browsing History', shop_product_browsing_history,
                   ['Browsing Date', 'Shop Name', 'Product Name'],
                   'TikTok Shop Product Browsing History', 'TikTok Shop Product Browsing History')

    generate_report('TikTok Shop Saved Addresses', shop_saved_addresses,
                   ['Receiver Name', 'Masked Phone Number', 'Address Info'],
                   'TikTok Shop Saved Addresses', 'TikTok Shop Saved Addresses')

    generate_report('TikTok Shop Shopping Cart', shop_shopping_cart,
                   ['Create Time', 'Shop Name', 'Product Name', 'SKU Count'],
                   'TikTok Shop Shopping Cart', 'TikTok Shop Shopping Cart')

    generate_report('TikTok Shop Vouchers', shop_vouchers,
                   ['Received Date', 'Voucher ID', 'Voucher Name', 'Voucher Text', 'Status'],
                   'TikTok Shop Vouchers', 'TikTok Shop Vouchers')

    generate_report('TikTok Usage Data (Third-Party)', usage_data_third_party,
                   ['Timestamp', 'Source', 'Event'],
                   'TikTok Usage Data (Third-Party)', 'TikTok Usage Data (Third-Party)')

    generate_report('TikTok Purchase History - Sent Gifts', purchase_history_send_gifts,
                   ['Date', 'Gift Amount', 'To Username'],
                   'TikTok Purchase History - Sent Gifts', 'TikTok Purchase History - Sent Gifts')

    generate_report('TikTok Purchase History - Bought Gifts', purchase_history_buy_gifts,
                   ['Date', 'Price'],
                   'TikTok Purchase History - Bought Gifts', 'TikTok Purchase History - Bought Gifts')
    
    generate_report('TikTok Ads Configuration', ads_configuration,
                   ['Setting Name', 'Setting Value'],
                   'TikTok Ads Configuration', 'TikTok Ads Configuration')

    generate_report('TikTok Go Live History', live_go_live_history,
                   ['Start Time', 'End Time', 'Duration', 'Room ID', 'Room Title', 'Cover URI', 'Replay URL', 'Total Earning', 'Total Likes', 'Total Views', 'Total Gifters', 'Quality Setting', 'Muted List'],
                   'TikTok Go Live History', 'TikTok Go Live History')

    # ToDo in the future: Many items, such as POI Reviews and Recently Deleted Posts are not in any dataset I have access to, mostly TikTok Shop-related. Income Plus Wallet Transactions, Live Watch Settings, Current Payment Information, Customer Support History, Order Dispute History, Product Review History, Return and Refund History, Order History.

__artifacts__ = {
    "tikTokData": (
        "TikTok Download Your Data Export",
        ('*/user_data.json', '*/user_data_tiktok.json'), # Added user_data_tiktok.json
        get_tikTokData)
}
