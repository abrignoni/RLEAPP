# To add a new artifact module, import it here as shown below:
#     from scripts.artifacts.fruitninja import get_fruitninja
# Also add the grep search for that module using the same name
# to the 'tosearch' data structure.

import traceback

from scripts.artifacts.airdropEmails import get_airdropEmails
from scripts.artifacts.airdropNumbers import get_airdropNumbers
from scripts.artifacts.chromeExtensions import get_chromeExtensions
from scripts.artifacts.chromeHistory import get_chromeHistory
from scripts.artifacts.coinbaseArchive import get_coinbaseArchive
from scripts.artifacts.discordReturnsfriends import get_discordReturnsfriends
from scripts.artifacts.discordReturnsdms import get_discordReturnsdms
from scripts.artifacts.discordReturnsser import get_discordReturnsser
from scripts.artifacts.discordReturnsserver import get_discordReturnsserver
from scripts.artifacts.discordReturnsunkn import get_discordReturnsunkn
from scripts.artifacts.googleChat import get_googleChat
from scripts.artifacts.googleFi_UserInfoRecords import get_googleFi_UserInfoRecords
from scripts.artifacts.gooReturnsact import get_gooReturnsact
from scripts.artifacts.gooReturnsrec import get_gooReturnsrec
from scripts.artifacts.googleReturnsmbox import get_googleReturnsmbox
from scripts.artifacts.googlePayTransactions import get_googlePayTransactions
from scripts.artifacts.googleProfile import get_googleProfile
from scripts.artifacts.googleTasks import get_googleTasks
from scripts.artifacts.fbigUnifiedmessaging import get_fbigUnifiedmessaging
from scripts.artifacts.icloudReturnsAcc import get_icloudReturnsAcc
from scripts.artifacts.icloudMsgsInCloud import get_icloudMsgsInCloud
from scripts.artifacts.icloudReturnsLogs import get_icloudReturnsLogs
from scripts.artifacts.icloudReturnsphotolibrary import get_icloudReturnsphotolibrary
from scripts.artifacts.icloudQueryLogs import get_icloudQueryLogs
from scripts.artifacts.icloudBookmarks import get_icloudBookmarks
from scripts.artifacts.icloudFMFFollowers import get_icloudFMFFollowers
from scripts.artifacts.icloudFMFFollowing import get_icloudFMFFollowing
from scripts.artifacts.instagramAccinfo import get_instagramAccinfo
from scripts.artifacts.instagramAdsclicked import get_instagramAdsclicked
from scripts.artifacts.instagramAdsviewed import get_instagramAdsviewed
from scripts.artifacts.instagramBlocked import get_instagramBlocked
from scripts.artifacts.instagramDevices import get_instagramDevices
from scripts.artifacts.instagramDevicescam import get_instagramDevicescam
from scripts.artifacts.instagramFollowers import get_instagramFollowers
from scripts.artifacts.instagramFollowing import get_instagramFollowing
from scripts.artifacts.instagramInfotoadv import get_instagramInfotoadv
from scripts.artifacts.instagramInterests import get_instagramInterests
from scripts.artifacts.instagramLikedcomm import get_instagramLikedcomm
from scripts.artifacts.instagramLogin import get_instagramLogin
from scripts.artifacts.instagramLogout import get_instagramLogout
from scripts.artifacts.instagramMessages import get_instagramMessages
from scripts.artifacts.instagramMessageReq import get_instagramMessageReq
from scripts.artifacts.instagramMusicheard import get_instagramMusicheard
from scripts.artifacts.instagramNointerest import get_instagramNointerest
from scripts.artifacts.instagramPasswordchange import get_instagramPasswordchange
from scripts.artifacts.instagramPending import get_instagramPending
from scripts.artifacts.instagramPersinfo import get_instagramPersinfo
from scripts.artifacts.instagramPrivacychange import get_instagramPrivacychange
from scripts.artifacts.instagramProfchanges import get_instagramProfchanges
from scripts.artifacts.instagramPolls import get_instagramPolls
from scripts.artifacts.instagramPosts import get_instagramPosts
from scripts.artifacts.instagramPostcom import get_instagramPostcom
from scripts.artifacts.instagramPostsviewed import get_instagramPostsviewed
from scripts.artifacts.instagramRecentreq import get_instagramRecentreq
from scripts.artifacts.instagramRemovedsug import get_instagramRemovedsug
from scripts.artifacts.instagramSavedposts import get_instagramSavedposts
from scripts.artifacts.instagramSearches import get_instagramSearches
from scripts.artifacts.instagramStories import get_instagramStories
from scripts.artifacts.instagramVideoswatched import get_instagramVideoswatched
from scripts.artifacts.instagramSuggestedviewed import get_instagramSuggestedviewed
from scripts.artifacts.kikReturns import get_kikReturns
from scripts.artifacts.kikProfilepic import get_kikProfilepic
from scripts.artifacts.msftheadReturn import get_msftheadReturn
from scripts.artifacts.netflixArchive import get_netflixArchive
from scripts.artifacts.playStoreDevices import get_playStoreDevices
from scripts.artifacts.playStoreInstalls import get_playStoreInstalls
from scripts.artifacts.playStoreLibrary import get_playStoreLibrary
from scripts.artifacts.playStorePurchaseHistory import get_playStorePurchaseHistory
from scripts.artifacts.playStoreReviews import get_playStoreReviews
from scripts.artifacts.playStoreSubscriptions import get_playStoreSubscriptions
from scripts.artifacts.snapChatsubsinfo import get_snapChatsubsinfo
from scripts.artifacts.snapchatMemimg import get_snapchatMemimg
from scripts.artifacts.snapChathistory import get_snapChathistory
from scripts.artifacts.snapChatmemo import get_snapChatmemo
from scripts.artifacts.snapchatConv import get_snapchatConv
from scripts.artifacts.tikTokipdata import get_tikTokipdata
from scripts.artifacts.tikTokvideometa import get_tikTokvideometa
from scripts.artifacts.tikToksubsinfo import get_tikToksubsinfo
from scripts.artifacts.takeoutAccessLogActivity import get_takeoutAccessLogActivity
from scripts.artifacts.takeoutGoogleFit import get_takeoutGoogleFit
from scripts.artifacts.takeoutLocationHistory import get_takeoutLocationHistory
from scripts.artifacts.takeoutRecords import get_takeoutRecords
from scripts.artifacts.takeoutSavedLinks import get_takeoutSavedLinks
from scripts.artifacts.twitterReturns import get_twitterReturns
from scripts.artifacts.twitterReturnsTip import get_twitterReturnsTip
from scripts.artifacts.whatsappExportedchats import get_whatsappExportedchats
from scripts.artifacts.youtubeSubscriptions import get_youtubeSubscriptions


from scripts.ilapfuncs import *

# GREP searches for each module
# Format is Key='modulename', Value=Tuple('Module Pretty Name', 'regex_term')
#   regex_term can be a string or a list/tuple of strings
# Here modulename must match the get_xxxxxx function name for that module. 
# For example: If modulename='profit', function name must be get_profit(..)
# Don't forget to import the module above!!!!

tosearch = {
    'airdropEmails':('Airdrop Emails', ('*/airdrop.ndjson')),
    'airdropNumbers':('Airdrop Numbers', ('*/airdrop.ndjson')),
    'chromeExtensions':('Google Takeout Archive', ('*/Chrome/Extensions.json')),
    'chromeHistory':('Google Takeout Archive', ('*/Chrome/BrowserHistory.json')),
    'coinbaseArchive':('Coinbase Archive', ('**/coinbase_data.json')),
    'discordReturnsfriends':('Discord Returns', ('*/relationships_*.csv')),
    'discordReturnsdms':('Discord Returns', ('*/attachments/*.*', '*/messages/dms/*.csv')),
    'discordReturnsser':('Discord Returns', ('*/servers/*.json')),
    'discordReturnsserver':('Discord Returns', ('*/attachments/*.*', '*/messages/servers/*.csv')),
    'discordReturnsunkn':('Discord Returns', ('*/attachments/*.*', '*/messages/unknown/*.csv')),
    'googleChat':('Google Takeout Archive', ('*/Google Chat/Groups/*/messages.json', '*/Google Chat/Groups/*/group_info.json')),
    'googleFi_UserInfoRecords':('Google Takeout Archive', ('*/Google Fi/User Info*/GoogleFi.UserInfo.Records.txt')),
    'gooReturnsact':('Google Returns', ('*/Access Log Activity/Activities*.csv')),
    'gooReturnsrec':('Google Returns', ('*/Location History/Records.json')),
    'googleReturnsmbox':('Google Returns MBOXes',('*/*.Mail.MessageContent_*/Mail/All mail Including Spam and Trash.mbox')),
    'googlePayTransactions':('Google Takeout Archive', ('*/Google Pay/Google transactions/transactions_*.csv')),
    'googleProfile':('Google Takeout Archive', ('*/Profile/Profile.json','*/Profile/ProfilePhoto.jpg')),
    'googleTasks':('Google Takeout Archive', ('*/Tasks/Tasks.json')),
    'fbigUnifiedmessaging':('Facebook - Instagram Returns', ('*/index.html', '*/preservation-1.html', '*/linked_media/*')),
    'icloudReturnsAcc':('iCloud Returns', ('*/Account/*_AccountDetails.xlsx')),
    'icloudMsgsInCloud':('iCloud Returns', ('*/Messagesinicloud/*MessagesInICloud.*')),
    'icloudMsgsInCloud':('iCloud Returns', ('*/Messagesinicloud/*MessagesInICloud*', '*/Messages/MessagesInICloud*')),
    'icloudReturnsLogs':('iCloud Returns', ('*/LOG/*_iCloudLogs.xlsx')),
    'icloudQueryLogs':('iCloud Returns', ('*/LOG/*_IDS_QueryLogs.xlsx')),
    'icloudBookmarks':('iCloud Returns', ('*/Bookmarks/*_iCloud_Bookmarks.xlsx')),
    'icloudFMFFollowers':('iCloud Returns', ('*/fmf/*_Followers.xlsx')),
    'icloudFMFFollowing':('iCloud Returns', ('*/fmf/*_Following.xlsx')),
    'icloudReturnsphotolibrary':('iCloud Returns', ('*/*/cloudphotolibrary/*')),
    'instagramAccinfo':('Instagram Archive', ('*/account_information/account_information.json')),
    'instagramAdsclicked':('Instagram Archive', ('*/ads_and_content/ads_clicked.json')),
    'instagramAdsviewed':('Instagram Archive', ('*/ads_and_content/ads_viewed.json')),
    'instagramBlocked':('Instagram Archive', ('*/followers_and_following/blocked_accounts.json')),
    'instagramDevices':('Instagram Archive', ('*/device_information/devices.json')),
    'instagramDevicescam':('Instagram Archive', ('*/device_information/camera_information.json')),
    'instagramFollowers':('Instagram Archive', ('*/followers_and_following/followers.json')),
    'instagramFollowing':('Instagram Archive', ('*/followers_and_following/following.json')),
    'instagramInfotoadv':('Instagram Archive', ("*/ads_and_businesses/information_you've_submitted_to_advertisers.json")),
    'instagramInterests':('Instagram Archive', ("*/information_about_you/ads_interests.json")),
    'instagramLikedcomm':('Instagram Archive', ('*/likes/liked_comments.json')),
    'instagramLogin':('Instagram Archive', ('*/login_and_account_creation/login_activity.json')),
    'instagramLogout':('Instagram Archive', ('*/login_and_account_creation/logout_activity.json')),
    'instagramMessages':('Instagram Archive', ('*/messages/inbox/*')),
    'instagramMessageReq':('Instagram Archive', ('*/messages/message_requests/*')),
    'instagramMusicheard':('Instagram Archive', ('*/ads_and_content/music_heard_in_stories.json')),
    'instagramNointerest':('Instagram Archive', ('*/ads_and_content/*re_not_interested_in.json')),
    'instagramPasswordchange':('Instagram Archive', ('*/login_and_account_creation/password_change_activity.json')),
    'instagramPending':('Instagram Archive', ('*/followers_and_following/pending_follow_requests.json')),
    'instagramPersinfo':('Instagram Archive', ('*/account_information/personal_information.json', '*/media/other/*.jpg')),
    'instagramPrivacychange':('Instagram Archive', ('*/login_and_account_creation/account_privacy_changes.json')),
    'instagramProfchanges':('Instagram Archive', ('*/account_information/profile_changes.json')),
    'instagramPolls':('Instagram Archive', ('*/story_sticker_interactions/polls.json')),
    'instagramPosts':('Instagram Archive', ('*/content/posts_1.json', '*/media/posts/*')),
    'instagramPostcom':('Instagram Archive', ('*/comments/post_comments.json')),
    'instagramPostsviewed':('Instagram Archive', ('*/ads_and_content/posts_viewed.json')),
    'instagramRecentreq':('Instagram Archive', ('*/followers_and_following/recent_follow_requests.json')),
    'instagramRemovedsug':('Instagram Archive', ('*/followers_and_following/removed_suggestions.json')),
    'instagramSavedposts':('Instagram Archive', ('*/saved/saved_posts.json')),
    'instagramSearches':('Instagram Archive', ('*/recent_searches/account_searches.json')),
    'instagramStories':('Instagram Archive', ('*/content/stories.json', '*/media/stories/*')),
    'instagramSuggestedviewed':('Instagram Archive', ('*/ads_and_content/suggested_accounts_viewed.json')),
    'instagramVideoswatched':('Instagram Archive', ('*/ads_and_content/videos_watched.json')),
    'kikReturns':('Kik Returns', ('*/logs/*.txt','*/logs/*','*/content/*')),
    'kikProfilepic':('Kik Returns', ('*profile-pic.jpg')),
    'msftheadReturn':('Microsoft Returns', ('*.eml_hdr.eml')),
    'netflixArchive':('Netflix Archive', ('**/Profiles.csv', '**/BillingHistory.csv', '**/IpAddressesLogin.csv', '**/IpAddressesStreaming.csv', '**/Devices.csv', '**/ViewingActivity.csv', '**/SearchHistory.csv', '**/AccountDetails.csv', '**/MessagesSentByNetflix.csv')),
    'playStoreDevices':('Google Takeout Archive', ('*/Google Play Store/Devices.json')),
    'playStoreInstalls':('Google Takeout Archive', ('*/Google Play Store/Installs.json')),
    'playStoreLibrary':('Google Takeout Archive', ('*/Google Play Store/Library.json')),
    'playStorePurchaseHistory':('Google Takeout Archive', ('*/Google Play Store/Purchase History.json')),
    'playStoreReviews':('Google Takeout Archive', ('*/Google Play Store/Reviews.json')),
    'playStoreSubscriptions':('Google Takeout Archive', ('*/Google Play Store/Subscriptions.json')),
    'snapchatConv':('Snapchat Returns', ('*/conversations.csv', '*/*.*')),
    'snapChatsubsinfo':('Snapchat Returns', ('*/subscriber_information.csv')),
    'snapChathistory':('Snapchat Archive', ('*/chat_history.json')),
    'snapchatMemimg':('Snapchat Returns', ('*/memories*.jpg','*/memories*.mp4')),
    'snapChatmemo':('Snapchat Returns', ('*/memories.csv','*/memories*.jpg','*/memories*.mp4')),
    'tikTokipdata':('TikTok Returns', ('*/*/*- IP Data.xlsx')),
    'tikToksubsinfo':('TikTok Returns', ('*/*/*(Subscriber information).pdf')),
    'tikTokvideometa':('TikTok Returns', ('*/*/*- video metadata.xlsx', '*/*/*/Video Content/*')),
    'takeoutAccessLogActivity':('Google Takeout Archive', ('*/Access Log Activity/*.csv')),
    'takeoutGoogleFit':('Google Takeout Archive', ('*/Fit/Daily activity metrics/Daily activity metrics.csv')),
    'takeoutLocationHistory':('Google Takeout Archive', ('*/Location History/Location History.json')),
    'takeoutRecords':('Google Takeout Archive', ('*/Location History/Records.json')),
    'takeoutSavedLinks':('Google Takeout Archive', ('*/Saved/*.csv')),
    'twitterReturns':('Twitter Returns',('*/*/*','*/*.txt')),
    'twitterReturnsTip':('Twitter Returns',('*/*.jpg','*/*.mp4','*/*.txt')),
    'youtubeSubscriptions':('Google Takeout Archive', ('*/YouTube and YouTube Music/subscriptions/subscriptions.csv')),
    'whatsappExportedchats':('Whatsapp Exported Chat', ('*/*.*')),
    
    
}
slash = '\\' if is_platform_windows() else '/'

def process_artifact(files_found, artifact_func, artifact_name, seeker, report_folder_base, wrap_text):
    ''' Perform the common setup for each artifact, ie, 
        1. Create the report folder for it
        2. Fetch the method (function) and call it
        3. Wrap processing function in a try..except block

        Args:
            files_found: list of files that matched regex

            artifact_func: method to call

            artifact_name: Pretty name of artifact

            seeker: FileSeeker object to pass to method
            
            wrap_text: whether the text data will be wrapped or not using textwrap.  Useful for tools that want to parse the data.
    '''
    logfunc('{} [{}] artifact executing'.format(artifact_name, artifact_func))
    report_folder = os.path.join(report_folder_base, artifact_name) + slash
    try:
        if os.path.isdir(report_folder):
            pass
        else:
            os.makedirs(report_folder)
    except Exception as ex:
        logfunc('Error creating {} report directory at path {}'.format(artifact_name, report_folder))
        logfunc('Reading {} artifact failed!'.format(artifact_name))
        logfunc('Error was {}'.format(str(ex)))
        return
    try:
        method = globals()['get_' + artifact_func]
        method(files_found, report_folder, seeker, wrap_text)
    except Exception as ex:
        logfunc('Reading {} artifact had errors!'.format(artifact_name))
        logfunc('Error was {}'.format(str(ex)))
        logfunc('Exception Traceback: {}'.format(traceback.format_exc()))
        return

    logfunc('{} [{}] artifact completed'.format(artifact_name, artifact_func))
    