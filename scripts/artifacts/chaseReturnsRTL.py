# Module Description: Parses Refresh Token Login data from a Chase Bank PDF return
# Author: infosec.exchange/@abrignoni
# Date: 2022-12-29
# Artifact version: 0.0.1
# Requirements: none

import PyPDF2
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, kmlgen

def pairs(keya,keyb,subtext):
    keya = subtext.find(keya)
    keyb = subtext.find(keyb)
    try:
        value = (subtext[keya:keyb]).split(' - ')[1]
    except:
        value = ' '
    return value

def get_chaseReturnsRTL(files_found, report_folder, seeker, wrap_text, time_offset):
    
    data_list = []
    
    refreshtokendict = {
        'APPLICATIONID':'COMMENTS',
        'COMMENTS':'ENC_DVC_ID',
        'TKN_TP':'STS',
        'DVC_OS':'DVC_MDL',
        'DVC_MDL':'DVC_MAK',
        'DVC_MAK':'DVC_NAME',
        'DVC_NAME':'DEVAPPINSTALL',
        'DEVAPPINSTALL':'DEVAPPVER',
        'DEVAPPVER':'DEVID',
        'DEVID':'DEVLOCALE',
        'DEVLOCALE':'DEV_MDL_VER',
        'DEV_MDL_VER':'DEVOSVER',
        'DEVOSVER':'GEOLAT',
        'GEOLAT':'GEOLON',
        'GEOLON':'GEOTS',
        'GEOTS':'LANGUAGE',
        'LANGUAGE':'RT_SC',
        'RT_SC':'USR_AGNT_DVC_NM',
        'USR_AGNT_DVC_NM':'DEVICE_TRUST_LEVEL',
        'DEVICE_TRUST_LEVEL':'SERVERID',
        'SERVERID':'CHANNELID',
        'CHANNELID':'SLOTCODE'
    }
    
    for file_found in files_found:
        file_found = str(file_found)
        filename = os.path.basename(file_found)
        
        pdffileobj = open(file_found,'rb')
        pdfmagic = pdffileobj.read(4)
        if (pdfmagic!='%PDF'):
            return
        pdfreader=PyPDF2.PdfFileReader(pdffileobj)
        x=pdfreader.numPages
        
        text = ''
        index = 0
        
        for page in range(x):
            pageobj=pdfreader.getPage(page)
            text = text.replace('\n', '' ) + pageobj.extractText()
            
        while index < len(text):
            index = text.find('Refresh Token Login', index)
            if index == -1:
                break
            #print('Term found at', index)
            startpoint = index
            endpoint = text.find('************',index)
            #print('End point found at', endpoint)
            index += 19
            
            subtext = text[startpoint:endpoint]
            templist = []
            
            timestampstart = subtext.find('Comments:')
            timestartend = subtext.find(',')
            timestamp = subtext[timestampstart:timestartend].split('Comments:')[1]
            templist.append(timestamp)
            
            usernamestart = subtext.find('Refresh Token Login ')
            usernameend = subtext.find(' Comments:')
            username = (subtext[usernamestart:usernameend].split(' ')[3])
            templist.append(username)
            
            for key, value in refreshtokendict.items():
                hk, hv = (key, pairs(key,value,subtext))
                templist.append(hv)
            
            data_list.append(templist)
        
        if len(data_list) > 0:
            description = 'Refresh Token Login data from Chase Bank PDF returns.'
            report = ArtifactHtmlReport(f'Chase RTL - {filename}')
            report.start_artifact_report(report_folder, f'Chase RTL - {filename}', description)
            report.add_script()
            data_headers = ('Timestamp', 'Username', 'APPLICATIONID', 'COMMENTS', 'TKN_TP', 'DVC_OS', 'DVC_MDL', 'DVC_MAK', 'DVC_NAME', 'DEVAPPINSTALL', 'DEVAPPVER', 'DEVID', 'DEVLOCALE', 'DEV_MDL_VER', 'DEVOSVER', 'Latitude', 'Longitude', 'GEOTS', 'LANGUAGE', 'RT_SC', 'USR_AGNT_DVC_NM', 'DEVICE_TRUST_LEVEL', 'SERVERID', 'CHANNELID')

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
            ('*.pdf','*.PDF'),
            get_chaseReturnsRTL)
}
