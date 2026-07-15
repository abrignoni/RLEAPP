__artifacts_v2__ = {
    "playstore_purchase_history": {
        "name": "Google Play Store - Purchase History",
        "description": "List of Google Play store account purchases",
        "author": "@stark4n6",
        "creation_date": "2021-08-20",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Google Play Store/Purchase History.json",
        "output_types": "standard",
        "artifact_icon": "shopping-cart",
    },
    "playstore_devices": {
        "name": "Google Play Store - Devices",
        "description": "Metadata about devices that have accessed the Google Play Store.",
        "author": "@stark4n6",
        "creation_date": "2021-08-22",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Google Play Store/Devices.json",
        "output_types": "standard",
        "artifact_icon": "device-mobile",
    },
    "playstore_library": {
        "name": "Google Play Store - Library",
        "description": "List of Google Play downloads including music, movies and apps",
        "author": "@stark4n6",
        "creation_date": "2021-08-22",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Google Play Store/Library.json",
        "output_types": "standard",
        "artifact_icon": "shopping-bag",
    },
    "playstore_reviews": {
        "name": "Google Play Store - Reviews",
        "description": "Details about Google Play reviews",
        "author": "@stark4n6",
        "creation_date": "2021-08-23",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Google Play Store/Reviews.json",
        "output_types": "standard",
        "artifact_icon": "pencil-minus",
    },
    "playstore_subscriptions": {
        "name": "Google Play Store - Subscriptions",
        "description": "List of Google Play subscriptions",
        "author": "@stark4n6",
        "creation_date": "2021-08-22",
        "last_update_date": "2026-06-19",
        "requirements": "none",
        "category": "Google Takeout Archive",
        "notes": "",
        "paths": "*/Google Play Store/Subscriptions.json",
        "output_types": "standard",
        "artifact_icon": "bell",
    },
}

import json
from scripts.ilapfuncs import artifact_processor, get_file_path

@artifact_processor
def playstore_purchase_history(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'Purchase History.json')

    with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        data = json.loads(f.read())

    for x in data:
        invoicePrice = x['purchaseHistory'].get('invoicePrice','')
        paymentMethod = x['purchaseHistory'].get('paymentMethodTitle','')
        userCountry = x['purchaseHistory'].get('userCountry','')
        documentType = x['purchaseHistory']['doc'].get('documentType','')

        itemTitle = x['purchaseHistory']['doc'].get('title','')
        purchaseTime = x['purchaseHistory'].get('purchaseTime','')
        purchaseTime = purchaseTime.replace('T', ' ').replace('Z', '')
       
        data_list.append((purchaseTime, itemTitle, documentType, invoicePrice, paymentMethod, userCountry))

    data_headers = (('Purchase Timestamp','datetime'),'Item Title','Document Type','Price','Payment Method','User Country') 
    return data_headers, data_list, file_found
    
@artifact_processor    
def playstore_devices(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'Devices.json')
    
    with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        data = json.loads(f.read())

    for x in range(0, len(data)):
        carrierName = data[x]['device']['mostRecentData']['carrierName']
        manufacturer = data[x]['device']['mostRecentData']['manufacturer']
        modelName = data[x]['device']['mostRecentData']['modelName']
        deviceName = data[x]['device']['mostRecentData']['deviceName']
        totalMemoryBytes = str(round(int(data[x]['device']['mostRecentData']['totalMemoryBytes'])/1000000000,2))
        deviceIpCountry = data[x]['device']['mostRecentData']['deviceIpCountry']
        androidSdkVersion = data[x]['device']['mostRecentData']['androidSdkVersion']
        deviceRegistrationTime = data[x]['device']['deviceRegistrationTime']
        deviceRegistrationTime = deviceRegistrationTime.replace('T', ' ').replace('Z', '')
        userAddedOnDeviceTime = data[x]['device']['userAddedOnDeviceTime']
        userAddedOnDeviceTime = userAddedOnDeviceTime.replace('T', ' ').replace('Z', '')
        lastTimeDeviceActive = data[x]['device']['lastTimeDeviceActive']
        lastTimeDeviceActive = lastTimeDeviceActive.replace('T', ' ').replace('Z', '')
               
        data_list.append((deviceRegistrationTime, userAddedOnDeviceTime, lastTimeDeviceActive, manufacturer, modelName, totalMemoryBytes, carrierName, deviceIpCountry, deviceName, androidSdkVersion))
    
    
    data_headers = (('Device Registration Timestamp','datetime'),('User Added Timestamp','datetime'),('Last Device Active Timestamp','datetime'),'Device Manufacturer','Device Model','Device RAM (GBs)','Carrier','Device IP Country','Device Code Name','SDK Version')
    return data_headers, data_list, file_found
    
@artifact_processor
def playstore_library(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'Library.json')
    
    with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        data = json.loads(f.read())

    for x in data:
        docType = x['libraryDoc']['doc'].get('documentType','')
        title = x['libraryDoc']['doc'].get('title','')
        acquisitionTime = x['libraryDoc'].get('acquisitionTime','')
        acquisitionTime = acquisitionTime.replace('T', ' ').replace('Z', '')

        data_list.append((acquisitionTime, title, docType))
    
    data_headers = (('Acquisition Timestamp','datetime'),'Title','Type')
    return data_headers, data_list, file_found
    
@artifact_processor
def playstore_reviews(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'Reviews.json')

    with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        data = json.loads(f.read())

    for x in data:
        creationTime = x['review'].get('creationTime','')
        creationTime = creationTime.replace('T', ' ').replace('Z', '')
        title = x['review']['document'].get('title','')
        comment = x['review'].get('comment','')
        reviewTitle = x['review'].get('title','')
        starRating = x['review'].get('starRating','')
        docType = x['review']['document'].get('documentType','')

        data_list.append((creationTime, title, comment, reviewTitle, starRating, docType))

    data_headers = (('Creation Timestamp','datetime'),'Title','Comment','Review Title','Star Rating','Type')
    return data_headers, data_list, file_found
    
@artifact_processor
def playstore_subscriptions(context):
    files_found = context.get_files_found()
    data_list = []
    file_found = get_file_path(files_found, 'Subscriptions.json')    

    with open(file_found, encoding = 'utf-8', mode = 'r') as f:
        data = json.loads(f.read())

    for x in data:
        title = x['subscription']['doc'].get('title','')
        renewalDate = x['subscription'].get('renewalDate','')
        renewalDate = renewalDate.replace('T', ' ').replace('Z', '')
        renewalPrice = x['subscription']['pricing'][0].get('price','')
        renewalUnit = x['subscription']['pricing'][0]['period'].get('unit','')
        renewalCount = x['subscription']['pricing'][0]['period'].get('count','')
        renewalPeriod = str(renewalCount) + ' / ' + renewalUnit
        state = x['subscription'].get('state','')
        
        data_list.append((renewalDate, title, renewalPrice, renewalPeriod, state))

    data_headers = (('Renewal Timestamp','datetime'),'Subscription','Renewal Price','Renewal Period','Status')
    return data_headers, data_list, file_found
