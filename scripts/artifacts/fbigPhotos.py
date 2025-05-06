import os
import datetime
import json
import shutil
from bs4 import BeautifulSoup
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_fbigPhotos(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        if filename.startswith('records.html') or filename.startswith('preservation'):
            rfilename = filename
        
        
            with open(file_found, encoding='utf-8') as fp:
                soup = BeautifulSoup(fp, 'lxml')
                data_list = []
            
                uni = soup.find_all("div", {"id": "property-photos"})
                
                divs = uni[0].find_all('div', class_='div_table outer')
                
                current_group = 0
                for index, div in enumerate(divs):
                    if index > 1:
                        inner_div = div.find('div', class_='div_table inner')
                        if inner_div and 'Image' in inner_div.text:
                            if current_group == 1:
                                data_list.append((taken,thumb,lmf,url,source,filter,pub,sba,carid,caption,comments,location))
                                current_group = 0
                        elif inner_div and 'Linked Media File' in inner_div.text:
                            lmf = div.find('div', class_='most_inner')
                            lmf = (lmf.get_text())
                            #fnt = os.path.basename(lmf)
                            thumb = media_to_html(lmf, files_found, report_folder)
                        elif inner_div and 'Url' in inner_div.text:
                            url = div.find('div', class_='most_inner')
                            url = (url.get_text())
                        elif inner_div and 'Source' in inner_div.text:
                            source = div.find('div', class_='most_inner')
                            source = (source.get_text())
                        elif inner_div and 'Filter' in inner_div.text:
                            filter = div.find('div', class_='most_inner')
                            filter = (filter.get_text())
                        elif inner_div and 'Is Published' in inner_div.text:
                            pub = div.find('div', class_='most_inner')
                            pub = (pub.get_text())
                        elif inner_div and 'Shared By Author' in inner_div.text:
                            sba = div.find('div', class_='most_inner')
                            sba = (sba.get_text())
                        elif inner_div and 'Carousel Id' in inner_div.text:
                            carid = div.find('div', class_='most_inner')
                            carid = (carid.get_text())
                        elif inner_div and 'Caption' in inner_div.text:
                            caption = (str(div))  # Keep the entire div with tags
                        elif inner_div and 'Comments' in inner_div.text:
                            comments = (str(div))  # Keep the entire div with tags
                        elif inner_div and 'Taken' in inner_div.text:
                            taken = div.find('div', class_='most_inner')
                            taken = (taken.get_text())
                        elif inner_div and 'Location' in inner_div.text:
                            location = (str(div))  # Keep the entire div with tags
                            current_group = 1
                        else:
                            pass
                    
                data_list.append((taken,thumb,lmf,url,source,filter,pub,sba,carid,caption,comments,location))
            
            
                
        if data_list:
            report = ArtifactHtmlReport(f'Facebook & Instagram - Photos - {rfilename}')
            report.start_artifact_report(report_folder, f'Facebook Instagram - Photos - {rfilename}')
            report.add_script()
            data_headers = ('Timestamp','Thumb','Linked Media File','URL','Source','Filter','Is Published','Shared by Author','Carousel Id','Caption','Comments','Location')
            report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Thumb','Caption','Comments','Location'])
            report.end_artifact_report()
            
            #tsvname = f'Facebook Instagram - Videos - {rfilename}'
            #tsv(report_folder, data_headers, data_list, tsvname)
        
        else:
            logfunc(f'No Facebook Instagram - Photos - {rfilename}')
                
__artifacts__ = {
        "fbigPhotos": (
            "Facebook - Instagram Returns",
            ('*/records.html', '*/preservation*.html', '*/linked_media/*.*'),
            get_fbigPhotos)
}