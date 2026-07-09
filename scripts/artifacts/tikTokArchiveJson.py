# Module Description: Parses all TikTok data from "Download My Data" export (JSON files)
# Author: @upintheairsheep and @Jadoo4QFan
# Date: 2025-06-15
# Artifact version: 1.0
# Requirements: none
# Note: Gemini Code Assist was used during the script's development, however the code was then heavily tested against real exports.

import json
import os
from datetime import datetime, timezone

from scripts.ilapfuncs import artifact_processor, convert_unix_ts_to_utc

# Every artifact in this module reads the same TikTok "Download My Data" JSON
# export. Both the old (user_data.json) and new (user_data_tiktok.json)
# filenames are supported.
_PATHS = ('*/user_data.json', '*/user_data_tiktok.json')
_FILENAMES = ('user_data.json', 'user_data_tiktok.json')

__artifacts_v2__ = {}


def _load(file_found):
    with open(file_found, encoding='utf-8', mode='r') as f:
        return json.loads(f.read())


def _tt_ts(value):
    '''Best-effort convert a TikTok timestamp to an aware UTC datetime.
    Handles epoch seconds/ms (numeric), "YYYY-MM-DD HH:MM:SS" and ISO-8601
    strings (all UTC in the export). Unparseable/empty values are kept
    verbatim so the LAVA datetime column stores them as text.'''
    if value in (None, '', 'N/A'):
        return ''
    s = str(value).strip()
    if not s:
        return ''
    if s.isdigit():
        return convert_unix_ts_to_utc(s)
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S'):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    try:
        dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return value


def _register(key, name, icon, headers, extractor):
    '''Build and register a context-form @artifact_processor for one report
    section of the TikTok export.'''
    def fn(context):
        data_list = []
        source_path = ''
        for file_found in context.get_files_found():
            file_found = str(file_found)
            if os.path.basename(file_found) not in _FILENAMES:
                continue
            source_path = file_found
            data = _load(file_found)
            data_list.extend(extractor(data))
        return headers, data_list, context.get_relative_path(source_path)

    fn.__name__ = key
    fn.__qualname__ = key
    globals()[key] = artifact_processor(fn)
    __artifacts_v2__[key] = {
        "name": name,
        "description": f"Parses the '{name}' section of the TikTok 'Download My Data' JSON export.",
        "author": "@upintheairsheep and @Jadoo4QFan",
        "creation_date": "2025-06-15",
        "last_update_date": "2025-06-15",
        "requirements": "none",
        "category": "TikTok",
        "notes": "Gemini Code Assist was used during the script's development, however the code was then heavily tested against real exports.",
        "paths": _PATHS,
        "output_types": "standard",
        "artifact_icon": icon,
    }


def _roots(data):
    '''Return the frequently used top-level containers (new schema names with
    fallbacks to the old names).'''
    return {
        'activity': data.get('Your Activity', data.get('Activity', {})),
        'app_settings': data.get('App Settings', {}),
        'comment': data.get('Comment', {}),
        'video': data.get('Post', data.get('Video', {})),
        'profile': data.get('Profile', {}),
        'live': data.get('Tiktok Live', {}),
        'shop': data.get('TikTok Shop', data.get('Tiktok Shopping', {})),
        'location_review': data.get('Location Review', {}),
        'ads': data.get('Ads and data', {}),
        'dm': data.get('Direct Message', data.get('Direct Messages', {})),
    }


def _x_favorite_effects(data):
    rows = []
    section = _roots(data)['activity'].get('Favorite Effects', {})
    for effect in section.get('FavoriteEffectsList', []):
        rows.append((effect.get('EffectLink', effect.get('Link', '')), _tt_ts(effect.get('Date', ''))))
    return rows


def _x_blocked_users(data):
    rows = []
    section = _roots(data)['app_settings'].get('Block List', _roots(data)['app_settings'].get('Block', {}))
    for user in section.get('BlockList', []):
        rows.append((user.get('UserName', ''), _tt_ts(user.get('Date', ''))))
    return rows


def _x_video_history(data):
    rows = []
    activity = _roots(data)['activity']
    section = activity.get('Watch History', activity.get('Video Browsing History', {}))
    for video in section.get('VideoList', []):
        rows.append((video.get('Link', ''), _tt_ts(video.get('Date', '')), video.get('timepertiktok', 0)))
    return rows


def _x_comments(data):
    rows = []
    comment_root = _roots(data)['comment']
    location = None
    if 'Comments' in comment_root and 'CommentsList' in comment_root['Comments']:
        location = comment_root['Comments'].get('CommentsList', [])
    elif 'CommentsList' in comment_root:
        location = comment_root.get('CommentsList', [])
    if location:
        for item in location:
            text = item.get('comment', item.get('Comment', ''))
            date_val = item.get('date', item.get('Date', ''))
            rows.append((text, _tt_ts(date_val)))
    return rows


def _x_favorite_hashtags(data):
    rows = []
    for hashtag in _roots(data)['activity'].get('Favorite Hashtags', {}).get('FavoriteHashtagList', []):
        rows.append((hashtag.get('Link', ''), _tt_ts(hashtag.get('Date', ''))))
    return rows


def _x_favorite_sounds(data):
    rows = []
    for sound in _roots(data)['activity'].get('Favorite Sounds', {}).get('FavoriteSoundList', []):
        rows.append((sound.get('Link', ''), _tt_ts(sound.get('Date', ''))))
    return rows


def _x_favorite_videos(data):
    rows = []
    for video in _roots(data)['activity'].get('Favorite Videos', {}).get('FavoriteVideoList', []):
        rows.append((video.get('Link', ''), _tt_ts(video.get('Date', ''))))
    return rows


def _x_followers(data):
    rows = []
    activity = _roots(data)['activity']
    section = activity.get('Follower', activity.get('Follower List', {}))
    for follower in section.get('FansList', []):
        rows.append((follower.get('UserName', ''), _tt_ts(follower.get('Date', ''))))
    return rows


def _x_following(data):
    rows = []
    activity = _roots(data)['activity']
    section = activity.get('Following', activity.get('Following List', {}))
    for user in section.get('Following', []):
        rows.append((user.get('UserName', ''), _tt_ts(user.get('Date', ''))))
    return rows


def _x_hashtags_used(data):
    rows = []
    for hashtag in _roots(data)['activity'].get('Hashtag', {}).get('HashtagList', []):
        rows.append((hashtag.get('HashtagName', ''), hashtag.get('HashtagLink', '')))
    return rows


def _x_liked_videos(data):
    rows = []
    activity = _roots(data)['activity']
    if 'Like List' in activity:
        for item in activity['Like List'].get('ItemFavoriteList', []):
            link_val = item.get('link', item.get('Link', ''))
            date_val = item.get('date', item.get('Date', ''))
            rows.append((link_val, _tt_ts(date_val)))
    return rows


def _x_login_history(data):
    rows = []
    for login in _roots(data)['activity'].get('Login History', {}).get('LoginHistoryList', []):
        rows.append((
            _tt_ts(login.get('Date', '')),
            login.get('IP', ''),
            login.get('DeviceModel', ''),
            login.get('DeviceSystem', ''),
            login.get('NetworkType', ''),
            login.get('Carrier', ''),
        ))
    return rows


def _x_search_history(data):
    rows = []
    activity = _roots(data)['activity']
    section = activity.get('Searches', activity.get('Search History', {}))
    for search in section.get('SearchList', []):
        rows.append((search.get('SearchTerm', ''), _tt_ts(search.get('Date', ''))))
    return rows


def _x_share_history(data):
    rows = []
    for share in _roots(data)['activity'].get('Share History', {}).get('ShareHistoryList', []):
        rows.append((
            _tt_ts(share.get('Date', '')),
            share.get('SharedContent', ''),
            share.get('Link', ''),
            share.get('Method', ''),
        ))
    return rows


def _x_status_info(data):
    rows = []
    for status in _roots(data)['activity'].get('Status', {}).get('Status List', []):
        rows.append((
            status.get('Resolution', ''),
            status.get('App Version', ''),
            status.get('IDFA', ''),
            status.get('GAID', ''),
            status.get('Android ID', ''),
            status.get('IDFV', ''),
            status.get('Web ID', ''),
        ))
    return rows


def _x_uploaded_videos(data):
    rows = []
    video_root = _roots(data)['video']
    container = video_root.get('Posts', video_root.get('Videos', {}))
    if container and 'VideoList' in container:
        for item in container.get('VideoList', []):
            rows.append((
                _tt_ts(item.get('Date', '')),
                item.get('Link', ''),
                item.get('Likes', ''),
                item.get('WhoCanView', ''),
                item.get('AllowComments', ''),
                item.get('AllowStitches', ''),
                item.get('AllowDuets', ''),
                item.get('AllowStickers', ''),
                item.get('AllowSharingToStory', ''),
                item.get('ContentDisclosure', ''),
                item.get('AIGeneratedContent', ''),
                item.get('Sound', ''),
                item.get('Location', ''),
                item.get('Title', ''),
                item.get('AddYoursText', ''),
            ))
    return rows


def _x_off_tiktok_activity(data):
    rows = []
    section = _roots(data)['ads'].get('Off TikTok Activity', {}).get('OffTikTokActivityDataList', [])
    for item in section:
        rows.append((_tt_ts(item.get('TimeStamp', '')), item.get('Source', ''), item.get('Event', '')))
    return rows


def _x_direct_messages(data):
    rows = []
    dm_root = _roots(data)['dm']
    intermediate = dm_root.get('Direct Messages', dm_root.get('Chat History', {}))
    container = intermediate.get('ChatHistory', {})
    for chat_key, messages in container.items():
        chat_with_user = chat_key.replace('Chat History with ', '').rstrip(':')
        for message in messages:
            rows.append((_tt_ts(message.get('Date', '')), chat_with_user, message.get('From', ''), message.get('Content', '')))
    return rows


def _x_profile_auto_fill(data):
    rows = []
    profile_root = _roots(data)['profile']
    section = profile_root.get('Autofill', profile_root.get('Auto Fill', {}))
    if section:
        rows.append((
            section.get('PhoneNumber', 'N/A'),
            section.get('Email', 'N/A'),
            section.get('FirstName', 'N/A'),
            section.get('LastName', 'N/A'),
            section.get('Address', 'N/A'),
            section.get('ZipCode', 'N/A'),
            section.get('Unit', 'N/A'),
            section.get('City', 'N/A'),
            section.get('State', 'N/A'),
            section.get('Country', 'N/A'),
        ))
    return rows


def _x_profile_information(data):
    rows = []
    profile_root = _roots(data)['profile']
    container = profile_root.get('Profile Info', profile_root.get('Profile Information', {}))
    profile_map = container.get('ProfileMap', {})
    if profile_map:
        rows.append((
            profile_map.get('userName', ''),
            profile_map.get('bioDescription', ''),
            profile_map.get('birthDate', ''),
            profile_map.get('emailAddress', ''),
            profile_map.get('telephoneNumber', ''),
            profile_map.get('likesReceived', ''),
            profile_map.get('profilePhoto', ''),
            profile_map.get('profileVideo', ''),
        ))
    return rows


def _x_ai_moji(data):
    rows = []
    section = _roots(data)['profile'].get('AI-Moji', {})
    if section:
        rows.append((_tt_ts(section.get('CreateDate', '')), json.dumps(section.get('AIMojiList', {}), ensure_ascii=False)))
    return rows


def _x_watch_live_history(data):
    rows = []
    section = _roots(data)['live'].get('Watch Live History', {}).get('WatchLiveMap', {})
    for live_id, live_data in section.items():
        if live_id == "-1" and not live_data.get('Link'):
            continue
        rows.append((live_id, _tt_ts(live_data.get('WatchTime', '')), live_data.get('Link', '')))
    return rows


def _x_watch_live_interactions(data):
    rows = []
    section = _roots(data)['live'].get('Watch Live History', {}).get('WatchLiveMap', {})
    for live_id, live_data in section.items():
        if live_id == "-1" and not live_data.get('Link'):
            continue
        watch_time = _tt_ts(live_data.get('WatchTime', ''))
        for comment in (live_data.get('Comments', []) or []):
            rows.append((live_id, watch_time, 'Comment', _tt_ts(comment.get('CommentTime', '')), comment.get('CommentContent', '')))
        for question in (live_data.get('Questions', []) or []):
            rows.append((live_id, watch_time, 'Question', _tt_ts(question.get('QuestionTime', '')), question.get('QuestionContent', '')))
    return rows


def _x_watch_live_settings(data):
    rows = []
    container = _roots(data)['live'].get('Watch Live Settings', {})
    if container:
        settings_map = container.get('WatchLiveSettingsMap', {})
        rows.append((
            settings_map.get('app', 'N/A'),
            settings_map.get('web', 'N/A'),
            _tt_ts(container.get('MostRecentModificationTimeInApp', '')),
            _tt_ts(container.get('MostRecentModificationTimeInWeb', '')),
        ))
    return rows


def _flatten_settings(settings_map, empty_list_value=""):
    rows = []
    for key, value in settings_map.items():
        if isinstance(value, dict):
            value_str = "; ".join(f"{k}: {v}" for k, v in value.items())
        elif isinstance(value, list):
            value_str = ", ".join(map(str, value)) if value else empty_list_value
        else:
            value_str = str(value) if value is not None else empty_list_value
        rows.append((key, value_str))
    return rows


def _x_app_settings(data):
    return _flatten_settings(_roots(data)['app_settings'].get('Settings', {}).get('SettingsMap', {}))


def _x_go_live_settings(data):
    return _flatten_settings(_roots(data)['live'].get('Go Live Settings', {}).get('SettingsMap', {}), empty_list_value="N/A")


def _x_go_live_history(data):
    rows = []
    for event in _roots(data)['live'].get('Go Live History', {}).get('GoLiveList', []):
        muted = event.get('MutedList')
        muted_str = ", ".join(map(str, muted)) if isinstance(muted, list) else str(muted)
        rows.append((
            _tt_ts(event.get('LiveStartTime', '')),
            _tt_ts(event.get('LiveEndTime', '')),
            event.get('LiveDuration', ''),
            event.get('RoomId', ''),
            event.get('RoomTitle', ''),
            event.get('CoverUri', ''),
            event.get('ReplayUrl', ''),
            event.get('TotalEarning', ''),
            event.get('TotalLike', ''),
            event.get('TotalView', ''),
            event.get('TotalGifter', ''),
            event.get('QualitySetting', ''),
            muted_str,
        ))
    return rows


def _x_shop_communication_history(data):
    rows = []
    shop_root = _roots(data)['shop']
    container = shop_root.get('Communication With Shops', shop_root.get('Communication History', {}))
    for shop_name_key, messages in container.get('CommunicationHistories', {}).items():
        if isinstance(messages, list):
            for message in messages:
                rows.append((
                    _tt_ts(message.get('send_time', '')),
                    message.get('shop_name', shop_name_key),
                    message.get('direction', ''),
                    message.get('content', ''),
                ))
    # Placeholder sub-sections whose internal structure is not defined are
    # surfaced as raw JSON so nothing is silently dropped.
    placeholders = (
        ('Current Payment Information', 'PayCard', 'Current Payment Information'),
        ('Customer Support History', 'CustomerSupportHistories', 'Customer Support History'),
        ('Order Dispute History', 'OrderDisputeHistories', 'Order Dispute History'),
        ('Order History', 'OrderHistories', 'Order History'),
        ('Product Reviews', 'ProductReviewHistories', 'Product Reviews History'),
        ('Returns and Refunds History', 'ReturnAndRefundHistories', 'Returns and Refunds History'),
    )
    for section_key, inner_key, label in placeholders:
        payload = shop_root.get(section_key, {}).get(inner_key, {})
        if payload:
            rows.append((label, "See JSON", "N/A", json.dumps(payload, ensure_ascii=False)))
    return rows


def _x_shop_product_browsing(data):
    rows = []
    for item in _roots(data)['shop'].get('Product Browsing History', {}).get('ProductBrowsingHistories', []):
        rows.append((_tt_ts(item.get('browsing_date', '')), item.get('shop_name', ''), item.get('product_name', '')))
    return rows


def _x_shop_saved_addresses(data):
    rows = []
    for address in _roots(data)['shop'].get('Saved Address Information', {}).get('SavedAddress', []):
        rows.append((address.get('receiver_name', ''), address.get('masked_phone_number', ''), address.get('adress_info', '')))
    return rows


def _x_shop_shopping_cart(data):
    rows = []
    for item in _roots(data)['shop'].get('Shopping Cart List', {}).get('ShoppingCart', []):
        rows.append((_tt_ts(item.get('CreateTime', '')), item.get('ShopName', ''), item.get('ProductName', ''), item.get('SkuCount', '')))
    return rows


def _x_shop_vouchers(data):
    rows = []
    for voucher in _roots(data)['shop'].get('Vouchers', {}).get('Vouchers', []):
        rows.append((
            _tt_ts(voucher.get('ReceivedDate', '')),
            voucher.get('VoucherId', ''),
            voucher.get('VoucherName', 'N/A'),
            voucher.get('VoucherText', ''),
            voucher.get('Status', ''),
        ))
    return rows


def _x_usage_data_third_party(data):
    rows = []
    for item in _roots(data)['ads'].get('Usage Data From Third-Party Apps And Websites', {}).get('UsageDataList', []):
        rows.append((_tt_ts(item.get('TimeStamp', '')), item.get('Source', ''), item.get('Event', '')))
    return rows


def _x_sent_gifts(data):
    rows = []
    activity = _roots(data)['activity']
    purchases = activity.get('Purchases', activity.get('Purchase History', {}))
    for gift in purchases.get('SendGifts', {}).get('SendGifts', []):
        rows.append((_tt_ts(gift.get('Date', '')), gift.get('GiftAmount', ''), gift.get('UserName', '')))
    return rows


def _x_bought_gifts(data):
    rows = []
    activity = _roots(data)['activity']
    purchases = activity.get('Purchases', activity.get('Purchase History', {}))
    for gift in purchases.get('BuyGifts', {}).get('BuyGifts', []):
        rows.append((_tt_ts(gift.get('Date', '')), gift.get('Price', '')))
    return rows


def _x_ads_configuration(data):
    rows = []
    ads = _roots(data)['ads']
    ad_interests = ads.get('Ad Interests', {}).get('AdInterestCategories', '')
    if ad_interests:
        rows.append(('Ad Interest Categories', ad_interests))
    partners = ads.get('Ads Based On Data Received From Partners', {})
    if partners.get('DataPartnerList', ''):
        rows.append(('Data Partner List', partners.get('DataPartnerList', '')))
    if partners.get('AdvertiserList', ''):
        rows.append(('Advertiser List', partners.get('AdvertiserList', '')))
    return rows


def _x_most_recent_location(data):
    rows = []
    location = _roots(data)['activity'].get('Most Recent Location Data', {}).get('LocationData', {})
    if location:
        rows.append((_tt_ts(location.get('Date', '')), location.get('GpsData', 'N/A'), location.get('LastRegion', 'N/A')))
    return rows


def _x_activity_summary(data):
    rows = []
    container = _roots(data)['activity'].get('Your Activity', {})
    summary = container.get('Activity Summary', {}).get('ActivitySummaryMap', {})
    if summary:
        rows.append((
            summary.get('videosCommentedOnSinceAccountRegistration', 0),
            summary.get('videosSharedSinceAccountRegistration', 0),
            summary.get('videosWatchedToTheEndSinceAccountRegistration', 0),
        ))
    return rows


def _x_location_reviews(data):
    rows = []
    for review in _roots(data)['location_review'].get('Location Reviews', {}).get('ReviewsList', []):
        rows.append((
            review.get('PlaceName', ''),
            _tt_ts(review.get('Date', '')),
            review.get('Rating', ''),
            review.get('Status', ''),
            review.get('Likes', ''),
            review.get('ReviewText', ''),
        ))
    return rows


def _x_recently_deleted_posts(data):
    rows = []
    for post in _roots(data)['video'].get('Recently Deleted Posts', {}).get('PostList', []):
        rows.append((json.dumps(post, ensure_ascii=False),))
    return rows


_register('tikTokFavoriteEffects', 'TikTok Favorite Effects', 'star',
          ('Link', ('Date', 'datetime')), _x_favorite_effects)
_register('tikTokBlockedUsers', 'TikTok Blocked Users', 'user-off',
          ('Username', ('Date', 'datetime')), _x_blocked_users)
_register('tikTokVideoHistory', 'TikTok Video History', 'history',
          ('URL', ('Date', 'datetime'), 'Time Per TikTok (s)'), _x_video_history)
_register('tikTokComments', 'TikTok Comments', 'message',
          ('Comment', ('Date', 'datetime')), _x_comments)
_register('tikTokFavoriteHashtags', 'TikTok Favorite Hashtags', 'hash',
          ('Link', ('Date', 'datetime')), _x_favorite_hashtags)
_register('tikTokFavoriteSounds', 'TikTok Favorite Sounds', 'music',
          ('Link', ('Date', 'datetime')), _x_favorite_sounds)
_register('tikTokFavoriteVideos', 'TikTok Favorite Videos', 'heart',
          ('Link', ('Date', 'datetime')), _x_favorite_videos)
_register('tikTokFollowers', 'TikTok Followers', 'users',
          ('Username', ('Date', 'datetime')), _x_followers)
_register('tikTokFollowing', 'TikTok Following', 'users',
          ('Username', ('Date', 'datetime')), _x_following)
_register('tikTokHashtagsUsed', 'TikTok Hashtags Used', 'hash',
          ('Hashtag Name', 'URL'), _x_hashtags_used)
_register('tikTokLikedVideos', 'TikTok Liked Videos', 'heart',
          ('Link', ('Date', 'datetime')), _x_liked_videos)
_register('tikTokLoginHistory', 'TikTok Login History', 'login',
          (('Date', 'datetime'), 'IP Address', 'Device Model', 'OS', 'Network Type', 'Carrier'), _x_login_history)
_register('tikTokSearchHistory', 'TikTok Search History', 'search',
          ('Search Term', ('Date', 'datetime')), _x_search_history)
_register('tikTokShareHistory', 'TikTok Share History', 'share',
          (('Date', 'datetime'), 'Content Type', 'URL', 'Method'), _x_share_history)
_register('tikTokStatusInfo', 'TikTok Status Info', 'info-circle',
          ('Screen Resolution', 'App Version', 'IDFA', 'GAID', 'Android ID', 'IDFV', 'Web ID'), _x_status_info)
_register('tikTokUploadedVideos', 'TikTok Uploaded Videos', 'video',
          (('Date Uploaded', 'datetime'), 'Direct URL', 'Like Count', 'Who Can View', 'Allow Comments',
           'Allow Stitches', 'Allow Duets', 'Allow Stickers', 'Allow Sharing To Story', 'Content Disclosure',
           'AI Generated Content', 'Sound', 'Location', 'Title', 'Add Yours Text'), _x_uploaded_videos)
_register('tikTokOffTikTokActivity', 'TikTok Off-TikTok Activity', 'external-link',
          (('Timestamp', 'datetime'), 'Source', 'Event'), _x_off_tiktok_activity)
_register('tikTokDirectMessages', 'TikTok Direct Messages', 'message-2',
          (('Date', 'datetime'), 'Chat With', 'Sender', 'Content'), _x_direct_messages)
_register('tikTokProfileAutoFill', 'TikTok Profile Auto Fill', 'forms',
          (('Phone Number', 'phonenumber'), 'Email', 'First Name', 'Last Name', 'Address', 'Zip Code',
           'Unit', 'City', 'State', 'Country'), _x_profile_auto_fill)
_register('tikTokProfileInformation', 'TikTok Profile Information', 'user',
          ('Username', 'Bio Description', 'Birth Date', 'Email Address', ('Telephone Number', 'phonenumber'),
           'Likes Received', 'Profile Photo URL', 'Profile Video URL'), _x_profile_information)
_register('tikTokAiMoji', 'TikTok AI-Moji', 'mood-smile',
          (('Create Date', 'datetime'), 'AI Moji List (JSON)'), _x_ai_moji)
_register('tikTokWatchLiveHistory', 'TikTok Watch Live History', 'device-tv',
          ('Live ID', ('Watch Time', 'datetime'), 'Link'), _x_watch_live_history)
_register('tikTokWatchLiveSettings', 'TikTok Watch Live Settings', 'settings',
          ('App Setting', 'Web Setting', ('App Mod Time', 'datetime'), ('Web Mod Time', 'datetime')), _x_watch_live_settings)
_register('tikTokWatchLiveInteractions', 'TikTok Watch Live Interactions', 'messages',
          ('Live ID', ('Live Watch Time', 'datetime'), 'Interaction Type', ('Interaction Time', 'datetime'), 'Content'), _x_watch_live_interactions)
_register('tikTokAppSettings', 'TikTok App Settings', 'settings',
          ('Setting Name', 'Setting Value'), _x_app_settings)
_register('tikTokGoLiveSettings', 'TikTok Go Live Settings', 'settings',
          ('Setting Name', 'Setting Value'), _x_go_live_settings)
_register('tikTokShopCommunicationHistory', 'TikTok Shop Communication History', 'shopping-cart',
          (('Send Time', 'datetime'), 'Shop Name', 'Direction', 'Content (Encrypted)'), _x_shop_communication_history)
_register('tikTokShopProductBrowsingHistory', 'TikTok Shop Product Browsing History', 'shopping-cart',
          (('Browsing Date', 'datetime'), 'Shop Name', 'Product Name'), _x_shop_product_browsing)
_register('tikTokShopSavedAddresses', 'TikTok Shop Saved Addresses', 'map-pin',
          ('Receiver Name', 'Masked Phone Number', 'Address Info'), _x_shop_saved_addresses)
_register('tikTokShopShoppingCart', 'TikTok Shop Shopping Cart', 'shopping-cart',
          (('Create Time', 'datetime'), 'Shop Name', 'Product Name', 'SKU Count'), _x_shop_shopping_cart)
_register('tikTokShopVouchers', 'TikTok Shop Vouchers', 'ticket',
          (('Received Date', 'datetime'), 'Voucher ID', 'Voucher Name', 'Voucher Text', 'Status'), _x_shop_vouchers)
_register('tikTokUsageDataThirdParty', 'TikTok Usage Data (Third-Party)', 'external-link',
          (('Timestamp', 'datetime'), 'Source', 'Event'), _x_usage_data_third_party)
_register('tikTokSentGifts', 'TikTok Purchase History - Sent Gifts', 'gift',
          (('Date', 'datetime'), 'Gift Amount', 'To Username'), _x_sent_gifts)
_register('tikTokBoughtGifts', 'TikTok Purchase History - Bought Gifts', 'gift',
          (('Date', 'datetime'), 'Price'), _x_bought_gifts)
_register('tikTokAdsConfiguration', 'TikTok Ads Configuration', 'ad',
          ('Setting Name', 'Setting Value'), _x_ads_configuration)
_register('tikTokGoLiveHistory', 'TikTok Go Live History', 'device-tv',
          (('Start Time', 'datetime'), ('End Time', 'datetime'), 'Duration', 'Room ID', 'Room Title', 'Cover URI',
           'Replay URL', 'Total Earning', 'Total Likes', 'Total Views', 'Total Gifters', 'Quality Setting', 'Muted List'), _x_go_live_history)
_register('tikTokMostRecentLocation', 'TikTok Most Recent Location Data', 'map-pin',
          (('Date', 'datetime'), 'GPS Data', 'Last Region'), _x_most_recent_location)
_register('tikTokActivitySummary', 'TikTok Your Activity Summary', 'chart-bar',
          ('Videos Commented On', 'Videos Shared', 'Videos Watched to End'), _x_activity_summary)
_register('tikTokLocationReviews', 'TikTok Location Reviews', 'map-pin',
          ('Place Name', ('Date', 'datetime'), 'Rating', 'Status', 'Likes', 'Review Text'), _x_location_reviews)
_register('tikTokRecentlyDeletedPosts', 'TikTok Recently Deleted Posts', 'trash',
          ('Post Data (JSON)',), _x_recently_deleted_posts)
