import os
import datetime
import json
import shutil
from bs4 import BeautifulSoup
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigAccountInfo(files_found, report_folder, seeker, wrap_text, time_offset):
    data_list = []
    logfunc('Processing the request. This may take a few moments.')
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
    
        if filename.startswith('records.html') or filename.startswith('preservation'):
            rfilename = filename
            
            with open(file_found, encoding='utf-8') as fp:
                soup = BeautifulSoup(fp, 'lxml')
                
            data_list =[]
            uni = soup.find_all("div", {"id": "property-request_parameters"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                divinn = (div.find('div', class_='most_inner'))
                divtext = (divinn.get_text())
                if index == 0:
                    data_list.append(('Service',divtext))
                elif index == 1:
                    data_list.append(('Target',divtext))
                elif index == 2:
                    data_list.append(('Account Identifier',divtext))
                elif index == 3:
                    data_list.append(('Account Type',divtext))
                elif index == 4:
                    data_list.append(('Meta Business Records Report Generated',divtext))
                elif index == 5:
                    data_list.append(('Meta Business Records Report Date Range',divtext))
                else:
                    data_list.append(('',divtext))
                    
                    
                    
                    
            uni = soup.find_all("div", {"id": "property-name"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 1:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    data_list.append(('Name Provided by Account Holder',divtext))
                    
                    
                    
                    
            uni = soup.find_all("div", {"id": "property-emails"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 0:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    data_list.append(('Registered Email Address',divtext))
                    
                    
                    
            uni = soup.find_all("div", {"id": "property-vanity"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 0:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    data_list.append(('Vanity Name',divtext))
                    
                    
                    
                    
            uni = soup.find_all("div", {"id": "property-registration_date"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 0:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    data_list.append(('Account Registration/Creation Date',divtext))
                    
                    
            uni = soup.find_all("div", {"id": "property-registration_ip"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 0:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    data_list.append(('Registration IP',divtext))
                    
                    
                    
            uni = soup.find_all("div", {"id": "property-account_end_date"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 0:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    if index == 2:
                        data_list.append(('Account Still Active',divtext))
                    else:
                        data_list.append(('Account Data',divtext))
                        
                        
            uni = soup.find_all("div", {"id": "property-phone_numbers"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 0:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    data_list.append(('Phone Number', divtext))
            
            
            uni = soup.find_all("div", {"id": "property-privacy_settings"})
            pairs_list = []
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 1:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    pairs_list.append(divtext)
                    if len(pairs_list) == 2:
                        data_list.append((pairs_list[0],pairs_list[1]))
                        pairs_list = []
            
            uni = soup.find_all("div", {"id": "property-popular_block"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 1:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    data_list.append(('Blocked from showing media in Instagram explorer page', divtext))
                    
            uni = soup.find_all("div", {"id": "property-gender"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 0:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    data_list.append(('Gender', divtext))
            
            uni = soup.find_all("div", {"id": "property-date_of_birth"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 0:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    data_list.append(('Date of Birth', divtext))
                    
            uni = soup.find_all("div", {"id": "property-website"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 0:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    data_list.append(('Website', divtext))
            
            uni = soup.find_all("div", {"id": "property-profile_picture"})
            
            divs = uni[0].find_all('div', class_='div_table inner')
            for index, div in enumerate(divs):
                if index > 1:
                    divinn = (div.find('div', class_='most_inner'))
                    divtext = (divinn.get_text())
                    thumb = media_to_html(divtext, files_found, report_folder)
                    data_list.append(('Profile Picture',thumb))

        if data_list:
            report = ArtifactHtmlReport(f'Facebook & Instagram - Account and Report Information - {rfilename}')
            report.start_artifact_report(report_folder, f'Facebook Instagram - Account and Report Information - {rfilename}')
            report.add_script()
            data_headers = ('Key','Value')
            report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Value'])
            report.end_artifact_report()
            
            tsvname = f'Facebook Instagram - Account and Report  Information - {rfilename}'
            tsv(report_folder, data_headers, data_list, tsvname)
        
        else:
            logfunc(f'No Facebook Instagram - Account and Report  Information - {rfilename}')
                
__artifacts__ = {
        "fbigAccountInfo": (
            "Facebook - Instagram Returns",
            ('*/records.html', '*/preservation*.html', '*/linked_media/profile_picture_*.jpg'),
            get_fbigAccountInfo)
}