# Module Description: Parses Refresh Token Login data from a Chase Bank PDF return
# Author: infosec.exchange/@abrignoni
# Date: 2022-12-29
# Artifact version: 0.0.1
# Requirements: none

# Update Author: Shawn Ramsey (ramseys1990)
# Github: https://github.com/ramseys1990
# Updated 2024-02-08
# Artfact version: 0.0.2

# TODO: Process other items of interest such as 
# TODO: Rebuild this artifact to process other items that may be of interest such as:
#
# TODO: GATEWAY ExtAcct_Verification_Reminder
# TODO: GATEWAY CIS Profile Synchronized
# TODO: GATEWAY CIS Update Trigger
# TODO: GATEWAY Payment Sent for ACH Off-Us Service (ExternalTransferExtract)
# TODO: AUTH Failed Logon Mobile (all mobile channels) **** This doesn't appear to be of any interest)
# TODO: GATEWAY Xfer-MemoFunder-Fail, Xfer-MemoFunder-NSF, Xfer-MemoFunder-LastNSF
# TODO: PAYMENTS QuickPayAccept
import os

# Updated to use pypdf vs PyPDF2 as PyPDF2 is deprecated
from pypdf import PdfReader
from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, kmlgen

# Class to maintain information on the User
# TODO: Finish building out some of the information placeholders
class AccountInfo:
    def __init__(self, username, name = "", dob = "0000-00-00", ssn = 0):
        self.username = username
        self.name = name
        self.dob = dob
        self.ssn = ssn
        self.address1 = ""
        self.address2 = ""
        self.city_state_zip = ""
        self.city = ""
        self.state = ""
        self.zip = 0
        self.country = ""

        self.tempList = []
        self.refreshTokenLoginLists = []
        self.refreshTokenDict = {
            'TIMESTAMP':"",
            'USERNAME':"",
            'APPLICATIONID':"",
            'COMMENTS':"",
            'DEVAPPINSTALL':"",
            'DEVAPPVER':"",
            'DEVID':"",
            'DEVLOCALE':"",
            'DEVOSVER':"",
            'DEV_MDL_VER':"",
            'DVC_ID':"",
            'DVC_MAK':"",
            'DVC_MDL':"",
            'DVC_NAME':"",
            'DVC_OS':"",
            'ENC_DVC_ID':"",
            'ERR_CD':"",
            'ERR_DESC':"",
            'GEOLAT':"",
            'GEOLON':"",
            'GEOTS':"",
            'INPT_DID':"",
            'LANGUAGE':"",
            'MLWR_SC':"",
            'RT_SC':"",
            'STS':"",
            'TKN_TP':"",
            'USR_AGNT_DVC_NM':"",
            'SERVERID':"",
            'CHANNELID':"",
            'SLOTCODE':"",
            'DEVICE_TRUST_LEVEL':"",
            'FAILED_DVC_TRUST_RULE':"",
        }

    def add_username(self, username):
        self.username.append(username)
    
    def add_latitude(self, latitude):
        self.latitude.append(latitude)
    
    def add_longitude(self, longitude):
        self.longitude.append(longitude)
    
    def add_device_id(self, device_id):
        self.device_id.append(device_id)
    
    def add_ip_address(self, ip_address):
        self.ip_address.append(ip_address)

    def add_ssn(self, ssn):
        self.ssn = ssn
    
    def add_account(self, account_number, account_type):
        self.account.append((account_number, account_type))
    
    def add_address1(self, address):
        self.address1 = address

    def add_address2(self, address):
        self.address2 = address

    def add_city(self, city):
        self.city = city

    def add_state(self, state):
        self.state = state

    def add_zip(self, zip):
        self.zip = zip

    def add_country(self, country):
        self.country = country

    def add_creation_date(self, creation_date):
        self.creation_date = creation_date

    def add_phone_number(self, phone_number):
        self.phone_number.append(phone_number)
    
    def add_w_phone(self, phone_number):
        self.w_phone = phone_number

    def add_h_phone(self, phone_number):
        self.h_phone = phone_number

    def add_dob(self, dob):
        self.dob = dob
    
    def add_email(self, email):
        self.email = email
    
    def add_name(self, name):
        self.name = name

    # TODO: Generate a full, proper address from the gathered information
    # TODO: Perform some validation here?
    def get_city_state_zip(self):
        string = self.city + ", " + self.state + " " + self.zip + " " + self.country
        return string 
    
    def get_username(self):
        return self.username
    
    def generateRefreshTokenList_old(self):
        for key, value in self.refreshTokenDict.items():
            self.tempList.append(value)
        return self.tempList
    
    def generateRefreshTokenList(self, dList):
        tempList = []
        for key, value in dList.items():
            tempList.append(value)
        return tempList

    def stashRefreshTokenList(self, tList):
        self.refreshTokenLoginLists.append(tList)

    def get_blank_RefreshTokenDict(self):
        return self.refreshTokenDict


# Originally from Todd Gamblin on stack overflow but modified to allow an optional starting index.
def find_nth(haystack: str, needle: str, n: int, start: int = 0) -> int:

    start = haystack.find(needle, start)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def get_chaseReturnsRTL(files_found, report_folder, seeker, wrap_text, time_offset):
    account_list = []
    data_list = []
    
    for file_found in files_found:
        file_found = str(file_found)
        filename = os.path.basename(file_found)
        
        pdfFileObj = open(file_found,'rb')
        pdfmagic = pdfFileObj.read(4)
        # TODO: Fix this, this needs to verify that it is a correct PDF file
#        if (pdfmagic!='%PDF'):
#            return
        pdfReader= PdfReader(pdfFileObj)
        x = len(pdfReader.pages)
        #x=pdfreader.numPages
        
        text = ''
        index = 0
        accountDataNeeded = True

        for page in range(x):
            pageObj=pdfReader.pages[page]
            text = text.replace('\n', '' ) + pageObj.extract_text()
            
        while index < len(text):

            # If this is true, then this is the first time we've reached User Data or
            # it means we have exhausted all of our Refresh Token Login Headers and are now at a new user.
            if text.find('User Data', index) < text.find('Refresh Token Login', index):

                # If this is true, then we are looking for User Data and we have one to process, otherwise, we're done.
                if text.find('User Data', index) > -1:

                    # Lets position ourselves to start grabbing our User Data
                    userIndex = text.find('User Data', index)

                    # No User Data Found, has the format been changed or is this a valid Chase Return?
                    if userIndex == -1:
                        break

                    # Set our startPoint
                    startPoint = userIndex
                    endPoint = text.find('Combined Events', startPoint)
                    subtext = text[startPoint:endPoint]

                    # Grab the User ID:
                    grabText = subtext[(subtext.find('User ID: ')) + 9:(subtext.find('E-mail'))]

                    # Check to see if we have any accounts being processed, if not, we have our first one and we will add it to the list.
                    # If there are accounts already, check them to make sure this is not a new one to add and process.
                    # TODO: Split this out to maintain the AccountInfo class instances
                    if len(account_list) > 0:
                        for account in account_list:
                            if account.get_username() != grabText:
                                logfunc("Located a username: " + str(grabText) + "... Processing now!")
                                account_list.append(AccountInfo(grabText))
                                accountDataNeeded = True
                                break
                            else:
                                # Account is already being processed, we can't pull account info right now
                                continue
                    else:
                        # This is our first account to process
                        logfunc("Located a username: " + str(grabText) + "... Processing now!")
                        account_list.append(AccountInfo(grabText))
                        accountDataNeeded = True

                if accountDataNeeded:
                    # Create the AccountInfo object to store everything in
                    account = AccountInfo(grabText)

                    # Grab the Email Address:
                    account.add_email(subtext[(subtext.find('E-mail Address: ')) + 16:(subtext.find('Customer'))])

                    # Grab the Name:
                    account.add_name(subtext[(subtext.find('Name: ')) + 6:(subtext.find('Address 1'))])

                    # Grab the Address1:
                    account.add_address1(subtext[(subtext.find('Address 1: ')) + 11:(subtext.find('Address 2'))])

                    # Grab the Address2:
                    account.add_address2(subtext[(subtext.find('Address 2: ')) + 11:(subtext.find('City:'))])

                    # Grab the City:
                    account.add_city(subtext[(subtext.find('City: ')) + 6:(subtext.find('State:'))])

                    # Grab the State:
                    account.add_state(subtext[(subtext.find('State: ')) + 7:(subtext.find('Zip:'))])

                    # Grab the Zip:
                    account.add_zip(subtext[(subtext.find('Zip: ')) + 5:(subtext.find('Country Code:'))])

                    # Grab the Country Code:
                    account.add_country(subtext[(subtext.find('Country Code: ')) + 14:(subtext.find('W. Phone:'))])

                    # Grab the Work Phone:
                    account.add_w_phone(subtext[(subtext.find('W. Phone: ')) + 10:(subtext.find('H. Phone:'))])

                    # Grab the Home Phone:
                    account.add_h_phone(subtext[(subtext.find('H. Phone: ')) + 10:(subtext.find('Combined Events'))])

                    # Set accountDataNeeded to False since we've obtained it (will be set to true when we find a new account)
                    accountDataNeeded = False

            # Check to see if we're looking at a Refresh Token Login Header
            index = text.find('Refresh Token Login', index)
            if index == -1:
                break
            tempList = account.get_blank_RefreshTokenDict()

            startPoint = index
            # This is the First / in the date of the next box... After the refresh token login, there are 2 / for the date of event, the 3rd one is the next event
            # We also need to subtract 2 because we have 2 characters before this /

            endPoint = find_nth(text, '/', 3, index) - 2

            index = endPoint
            subtext = text[startPoint:endPoint]
            templist = []

            # We search for the / after the Refresh Token Login Header to get us as close to the time as possible (this appears to be a fixed length on here?)
            # We then subtract 2 to give us the beginning of the date.
            # If you would rather only  have the time, you can search for the 2nd occurence and add 6 to get past the year and space.
            # For the end, we search for the next , due to the timestamp being ended with this
            timestampStart = find_nth(subtext, '/', 1) - 2
            timestampEnd = find_nth(subtext, ',', 1, timestampStart)
            timestamp = subtext[timestampStart:timestampEnd]            
            
            # Adding 20 to this gets us past Refresh Token Login Header
            # After refresh token, the next identifiable item is a / in the date below the Refresh Token Login Header
            # We will grab this index and subtract 2 from this to isolate the username
            usernameStart = subtext.find('Refresh Token Login ') + 20
            usernameEnd = find_nth(subtext, '/', 1) - 2
            username = subtext[usernameStart:usernameEnd]

            tempList.update({'TIMESTAMP':timestamp})
            tempList.update({'USERNAME':username})
            
            testList = subtext.split(', ')

            # Lets process through each item
            # TODO: Rewrite this to not make it so long
            # TODO: This can be made much more concise but this is a good way to see how its working through each item
            for item in testList:
                lineItem = item.split(' - ')
                if len(lineItem) > 1:
                    if lineItem[0] == 'APPLICATIONID':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'COMMENTS':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'DEVAPPINSTALL':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'DEVAPPVER':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'DEVID':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'DEVLOCALE':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'DEVOSVER':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'DEV_MDL_VER':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'DVC_ID':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'DVC_MAK':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'DVC_MDL':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'DVC_NAME':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'DVC_OS':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'ENC_DVC_ID':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'ERR_CD':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'ERR_DESC':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'GEOLAT':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'GEOLON':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'GEOTS':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'INPT_DID':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'LANGUAGE':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'MLWR_SC':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'RT_SC':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'STS':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'TKN_TP':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'USR_AGNT_DVC_NM':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'SERVERID':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'CHANNELID':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'SLOTCODE':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'DEVICE_TRUST_LEVEL':
                        tempList.update({lineItem[0]:lineItem[1]})
                    if lineItem[0] == 'FAILED_DVC_TRUST_RULE':
                        tempList.update({lineItem[0]:lineItem[1]})
            
            # We're generating our list of processed "block data"
            # We then append this list to the running collection of "blocks" of data
            blockData = account.generateRefreshTokenList(tempList)
            account.stashRefreshTokenList(blockData)

            data_list.append(blockData)
  
        # Lets start processing the return
        if len(data_list) > 0:
            description = 'Refresh Token Login data from Chase Bank PDF returns.'
            report = ArtifactHtmlReport(f'Chase RTL - {filename}')
            report.start_artifact_report(report_folder, f'Chase RTL - {filename}', description)
            report.add_script()
            data_headers = ('Timestamp', 'Username', 'APPLICATIONID', 'COMMENTS', 'DEVAPPINSTALL', 'DEVAPPVER', 'DEVID', 
                            'DEVLOCALE', 'DEVOSVER', 'DEV_MDL_VER', 'DVC_ID', 'DVC_MAK', 'DVC_MDL', 'DVC_NAME', 'DVC_OS', 
                            'ENC_DVC_ID', 'ERR_CD', 'ERR_DESC', 'Latitude', 'Longitude', 'GEOTS', 'INPT_DID', 'LANGUAGE', 
                            'MLWR_SC', 'RT_SC', 'STS', 'TKN_TP', 'USR_AGNT_DVC_NM', 'SERVERID', 'CHANNELID', 'SLOTCODE', 
                            'DEVICE_TRUST_LEVEL', 'FAILED_DVC_TRUST_RULE')

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'Chase RTL - {filename}'
            tsv(report_folder, data_headers, data_list, tsvname)
            
            tlactivity = f'Chase RTL - {filename}'
            timeline(report_folder, tlactivity, data_list, data_headers)
            
            kmlactivity = f'Chase RTL - {filename}'
            kmlgen(report_folder, kmlactivity, data_list, data_headers)
            
        else:
            logfunc(f'No Chase RTL - {filename} data available')

__artifacts__ = {
        "chaseReturnsRTL": (
            "Chase Returns",
            ('*.pdf'),
            get_chaseReturnsRTL)
}
