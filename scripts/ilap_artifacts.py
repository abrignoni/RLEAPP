# To add a new artifact module, import it here as shown below:
#     from scripts.artifacts.fruitninja import get_fruitninja
# Also add the grep search for that module using the same name
# to the 'tosearch' data structure.

import traceback

from scripts.artifacts.chromeExtensions import get_chromeExtensions
from scripts.artifacts.chromeHistory import get_chromeHistory
from scripts.artifacts.kikReturns import get_kikReturns
from scripts.artifacts.kikProfilepic import get_kikProfilepic
from scripts.artifacts.icloudReturnsAcc import get_icloudReturnsAcc
from scripts.artifacts.icloudMsgsInCloud import get_icloudMsgsInCloud
from scripts.artifacts.icloudReturnsLogs import get_icloudReturnsLogs
from scripts.artifacts.icloudQueryLogs import get_icloudQueryLogs
from scripts.artifacts.icloudBookmarks import get_icloudBookmarks
from scripts.artifacts.icloudFMFFollowers import get_icloudFMFFollowers
from scripts.artifacts.icloudFMFFollowing import get_icloudFMFFollowing
from scripts.artifacts.instagramAccinfo import get_instagramAccinfo
from scripts.artifacts.instagramDevices import get_instagramDevices
from scripts.artifacts.instagramDevicescam import get_instagramDevicescam
from scripts.artifacts.instagramInfotoadv import get_instagramInfotoadv
from scripts.artifacts.instagramLogin import get_instagramLogin
from scripts.artifacts.instagramPersinfo import get_instagramPersinfo
from scripts.artifacts.instagramProfchanges import get_instagramProfchanges
from scripts.artifacts.instagramPosts import get_instagramPosts
from scripts.artifacts.playStoreDevices import get_playStoreDevices
from scripts.artifacts.playStoreInstalls import get_playStoreInstalls
from scripts.artifacts.playStoreLibrary import get_playStoreLibrary
from scripts.artifacts.playStorePurchaseHistory import get_playStorePurchaseHistory
from scripts.artifacts.playStoreSubscriptions import get_playStoreSubscriptions

from scripts.ilapfuncs import *

# GREP searches for each module
# Format is Key='modulename', Value=Tuple('Module Pretty Name', 'regex_term')
#   regex_term can be a string or a list/tuple of strings
# Here modulename must match the get_xxxxxx function name for that module. 
# For example: If modulename='profit', function name must be get_profit(..)
# Don't forget to import the module above!!!!

tosearch = {
    'chromeExtensions':('Google Takeout Archive', ('*/Chrome/Extensions.json')),
    'chromeHistory':('Google Takeout Archive', ('*/Chrome/BrowserHistory.json')),
    'kikReturns':('Kik Returns', ('*/logs/*.txt','*/logs/*','*/content/*')),
    'kikProfilepic':('Kik Returns', ('*profile-pic.jpg')),
    'icloudReturnsAcc':('iCloud Returns', ('*/Account/*_AccountDetails.xlsx')),
    'icloudMsgsInCloud':('iCloud Returns', ('*/Messagesinicloud/*MessagesInICloud.*')),
    'icloudReturnsLogs':('iCloud Returns', ('*/LOG/*_iCloudLogs.xlsx')),
    'icloudQueryLogs':('iCloud Returns', ('*/LOG/*_IDS_QueryLogs.xlsx')),
    'icloudBookmarks':('iCloud Returns', ('*/Bookmarks/*_iCloud_Bookmarks.xlsx')),
    'icloudFMFFollowers':('iCloud Returns', ('*/fmf/*_Followers.xlsx')),
    'icloudFMFFollowing':('iCloud Returns', ('*/fmf/*_Following.xlsx')),
    'instagramAccinfo':('Instagram Archive', ('*/account_information/account_information.json')),
    'instagramDevices':('Instagram Archive', ('*/device_information/devices.json')),
    'instagramDevicescam':('Instagram Archive', ('*/device_information/camera_information.json')),
    'instagramInfotoadv':('Instagram Archive', ("*/ads_and_businesses/information_you've_submitted_to_advertisers.json")),
    'instagramLogin':('Instagram Archive', ('*/login_and_account_creation/login_activity.json')),
    'instagramPersinfo':('Instagram Archive', ('*/account_information/personal_information.json', '*/media/other/*.jpg')),
    'instagramProfchanges':('Instagram Archive', ('*/account_information/profile_changes.json')),
    'instagramPosts':('Instagram Takeout Archive', ('*/content/posts_1.json', '*/media/posts/*')),
    'playStoreDevices':('Google Takeout Archive', ('*/Google Play Store/Devices.json')),
    'playStoreInstalls':('Google Takeout Archive', ('*/Google Play Store/Installs.json')),
    'playStoreLibrary':('Google Takeout Archive', ('*/Google Play Store/Library.json')),
    'playStorePurchaseHistory':('Google Takeout Archive', ('*/Google Play Store/Purchase History.json')),
    'playStoreSubscriptions':('Google Takeout Archive', ('*/Google Play Store/Subscriptions.json')),
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
    