import os
import xlrd

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows

def get_icloudQueryLogs(files_found, report_folder, seeker, wrap_text):
    
    for file_found in files_found:
        file_found = str(file_found)
        filename = os.path.basename(file_found)
        
        if filename.startswith('~'):
            continue
        if filename.startswith('.'):
            continue
        
        loc = file_found
        
        
        dth = []
        list = []
        data_headers = []
        data_list =[]
        
        #First worksheet
        
        wb = xlrd.open_workbook(loc)
        sheetnames = wb.sheet_names() 
        sheet = wb.sheet_by_index(0)
        dsid = sheet.cell_value(2, 0)
        
        for i in range(sheet.nrows):
            
            if i == 8:
                #Row is headers
                idsh = sheet.cell_value(8,0)
                timestamph = sheet.cell_value(8,1)
                ciph = sheet.cell_value(8,2)
                sourceHandleh = sheet.cell_value(8,3)
                lookupHandleh = sheet.cell_value(8,4)
                lookupDevicesh = sheet.cell_value(8,5)
                usrh = sheet.cell_value(8,6)
                hwvh = sheet.cell_value(8,7)
                osvh = sheet.cell_value(8,8)
                
                data_headers = (timestamph,idsh,ciph,sourceHandleh,lookupHandleh,lookupDevicesh,usrh,hwvh,osvh)
                                
            elif i >= 9:
                #Row data
                ids = sheet.cell_value(i,0)
                timestamp = sheet.cell_value(i,1)
                split_timestamp = timestamp.split(' ')
                clean_timestamp = f'{split_timestamp[0]}-{split_timestamp[1]}'
                cip = sheet.cell_value(i,2)
                sourceHandle = sheet.cell_value(i,3)
                lookupHandle = sheet.cell_value(i,4)
                lookupDevices = sheet.cell_value(i,5)
                usr = sheet.cell_value(i,6)
                hwv = sheet.cell_value(i,7)
                osv = sheet.cell_value(i,8)
                
                data_list.append((clean_timestamp, ids, cip, sourceHandle, lookupHandle, lookupDevices, usr, hwv, osv))
                
            else:
                continue
            

        if data_list:
            description = f'Sheet name: {sheetnames[0]} - {dsid}'
            report = ArtifactHtmlReport('iCloud - Query Logs')
            report.start_artifact_report(report_folder, 'iCloud - Query Logs', description)
            report.add_script()
            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
        else:
            logfunc('No iCloud - No Query Log data available')
            
__artifacts__ = {
        "icloudQueryLogs": (
            "iCloud Returns",
            ('*/LOG/*_IDS_QueryLogs.xlsx'),
            get_icloudQueryLogs)
}