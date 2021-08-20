# To add a new artifact module, import it here as shown below:
#     from scripts.artifacts.fruitninja import get_fruitninja
# Also add the grep search for that module using the same name
# to the 'tosearch' data structure.

import traceback

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

from scripts.ilapfuncs import *

# GREP searches for each module
# Format is Key='modulename', Value=Tuple('Module Pretty Name', 'regex_term')
#   regex_term can be a string or a list/tuple of strings
# Here modulename must match the get_xxxxxx function name for that module. 
# For example: If modulename='profit', function name must be get_profit(..)
# Don't forget to import the module above!!!!

tosearch = {
    'kikReturns':('Kik Returns', ('*/logs/*.txt','*/logs/*','*/content/*')),
    'kikProfilepic':('Kik Returns', ('*profile-pic.jpg')),
    'icloudReturnsAcc':('iCloud Returns', ('*/Account/*_AccountDetails.xlsx')),
    'icloudMsgsInCloud':('iCloud Returns', ('*/Messagesinicloud/*MessagesInICloud.*')),
    'icloudReturnsLogs':('iCloud Returns', ('*/LOG/*_iCloudLogs.xlsx')),
    'icloudQueryLogs':('iCloud Returns', ('*/LOG/*_IDS_QueryLogs.xlsx')),
    'icloudBookmarks':('iCloud Returns', ('*/Bookmarks/*_iCloud_Bookmarks.xlsx')),
    'icloudFMFFollowers':('iCloud Returns', ('*/fmf/*_Followers.xlsx')),
    'icloudFMFFollowing':('iCloud Returns', ('*/fmf/*_Following.xlsx')),
    'instagramAccinfo':('Instagram Archive', ('*/account_information/account_information.json'))
    
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
    