import html
import os
import pathlib
import shutil
import sqlite3
import sys

from collections import OrderedDict
from scripts.html_parts import *
from scripts.ilapfuncs import logfunc
from scripts.version_info import rleapp_version, rleapp_contributors

def get_icon_name(category, artifact):
    ''' Returns the icon name from the feathericons collection. To add an icon type for 
        an artifact, select one of the types from ones listed @ feathericons.com
        If no icon is available, the alert triangle is returned as default icon.
    '''
    category = category.upper()
    artifact = artifact.upper()
    icon = 'alert-triangle' # default (if not defined!)

    if category.find('ACCOUNT') >=0:
        if artifact.find('AUTH') >=0:      icon = 'key'
        else:                              icon = 'user'
    elif category == 'COINBASE ARCHIVE':
        if '3RD' in artifact:              icon = 'log-in'
        elif 'CARD' in artifact:           icon = 'credit-card'
        elif 'PERSONAL' in artifact:       icon = 'user'
        elif 'SITE' in artifact:           icon = 'activity'
        elif 'TRANS' in artifact:          icon = 'archive'
        else:                              icon = 'monitor'
    elif category == 'DEVICE HEALTH SERVICES':         
        if artifact.find('BLUETOOTH') >=0:  icon = 'bluetooth'
        elif artifact.find('BATTERY') >=0:  icon = 'battery-charging'
        else:                               icon = 'bar-chart-2'
    elif category == 'GOOGLE TAKEOUT ARCHIVE':
        if artifact.find('CHROME WEB HISTORY') >=0: icon = 'chrome'
        elif artifact.find('CHROME EXTENSIONS') >=0: icon = 'tool'
        elif artifact == 'GOOGLE ACCESS LOG ACTIVITIES': icon = 'activity'
        elif artifact == 'GOOGLE ACCESS LOG DEVICES': icon = 'smartphone'
        elif artifact == 'GOOGLE CHAT - MESSAGES': icon = 'message-square'
        elif artifact == 'GOOGLE FI - USER INFO RECORDS': icon = 'phone'
        elif artifact == 'GOOGLE FIT - DAILY ACTIVITY METRICS': icon = 'trending-up'
        elif artifact == 'GOOGLE LOCATION HISTORY': icon = 'map-pin'
        elif artifact == 'GOOGLE PAY TRANSACTIONS': icon = 'credit-card'
        elif artifact == 'GOOGLE PLAY STORE DEVICES': icon = 'smartphone'
        elif artifact == 'GOOGLE PLAY STORE INSTALLS': icon = 'box'
        elif artifact == 'GOOGLE PLAY STORE LIBRARY': icon = 'grid'
        elif artifact == 'GOOGLE PLAY STORE PROFILE': icon = 'user'
        elif artifact == 'GOOGLE PLAY STORE PURCHASE HISTORY': icon = 'shopping-cart'
        elif artifact == 'GOOGLE PLAY STORE REVIEWS': icon = 'edit-3'
        elif artifact == 'GOOGLE PLAY STORE SUBSCRIPTIONS': icon = 'refresh-cw'
        elif artifact == 'SAVED LINKS - DEFAULT LIST': icon = 'list'
        elif artifact == 'SAVED LINKS - FAVORITE IMAGES': icon = 'image'
        elif artifact == 'SAVED LINKS - FAVORITE PAGES': icon = 'link-2'
        elif artifact == 'SAVED LINKS - WANT TO GO': icon = 'navigation-2'
        elif artifact == 'YOUTUBE SUBSCRIPTIONS': icon = 'youtube'
        else:                               icon = 'user'
    elif category == 'KIK RETURNS':       
        if artifact == 'KIK - PROFILE PIC': icon = 'image'
        else:                               icon = 'file-text'
    elif category == 'NETFLIX ARCHIVE':
        if artifact == 'NETFLIX - BILLING HISTORY':    icon = 'credit-card'
        elif artifact == 'NETFLIX - PROFILES':         icon = 'users'
        elif artifact == 'NETFLIX - IP ADDRESS LOGIN': icon = 'log-in'
        elif artifact == 'NETFLIX - ACCOUNT DETAILS':  icon = 'users'
        elif artifact == 'NETFLIX - MESSAGES SENT BY NETFLIX':  icon = 'mail'
        elif artifact == 'NETFLIX - SEARCH HISTORY':   icon = 'search'
        else:                                          icon = 'tv'
    elif category == 'CONTACTS':            icon = 'user'
    elif category == 'GOOGLE RETURNS MBOXES':            icon = 'mail'
    elif category == 'MICROSOFT RETURNS':            icon = 'target'
    elif category == 'TWITTER RETURNS':            icon = 'twitter'
    elif category == 'DISCORD RETURNS':            icon = 'message-square'
    elif category == 'TIKTOK RETURNS':            icon = 'film'
    elif category == 'SNAPCHAT RETURNS':            icon = 'camera'
    elif category == 'FACEBOOK - INSTAGRAM RETURNS':            icon = 'facebook'
    elif category == 'INSTAGRAM ARCHIVE':  
        if artifact == 'INSTAGRAM ARCHIVE - ACCOUNT INFO': icon = 'user'
        elif artifact == 'INSTAGRAM ARCHIVE - PERSONAL INFO': icon = 'user'
        else:                               icon = 'instagram'
    elif category == 'ICLOUD RETURNS': 
        if artifact == 'ICLOUD - ACCOUNT FEATURES': icon = 'user'
        else:                                       icon = 'file-text'
    return icon
    
    '''
    '''
def generate_report(reportfolderbase, time_in_secs, time_HMS, extraction_type, image_input_path):

    control = None
    side_heading = \
    """<h6 class="sidebar-heading justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
        {0}
    </h6>
    """
    list_item = \
    """
    <li class="nav-item">
        <a class="nav-link {0}" href="{1}">
            <span data-feather="{2}"></span> {3}
        </a>
    </li>
    """
    # Populate the sidebar dynamic data (depends on data/files generated by parsers)
    # Start with the 'saved reports' (home) page link and then append elements
    nav_list_data = side_heading.format('Saved Reports') + list_item.format('', 'index.html', 'home', 'Report Home')
    # Get all files
    side_list = OrderedDict() # { Category1 : [path1, path2, ..], Cat2:[..] } Dictionary containing paths as values, key=category

    for root, dirs, files in sorted(os.walk(reportfolderbase)):
        files = sorted(files)
        for file in files:
            if file.endswith(".temphtml"):    
                fullpath = (os.path.join(root, file))
                head, tail = os.path.split(fullpath)
                p = pathlib.Path(fullpath)
                SectionHeader = (p.parts[-2])
                if SectionHeader == '_elements':
                    pass
                else:
                    if control == SectionHeader:
                        side_list[SectionHeader].append(fullpath)
                        icon = get_icon_name(SectionHeader, tail.replace(".temphtml", ""))
                        nav_list_data += list_item.format('', tail.replace(".temphtml", ".html"), icon, tail.replace(".temphtml", ""))
                    else:
                        control = SectionHeader
                        side_list[SectionHeader] = []
                        side_list[SectionHeader].append(fullpath)
                        nav_list_data += side_heading.format(SectionHeader)
                        icon = get_icon_name(SectionHeader, tail.replace(".temphtml", ""))
                        nav_list_data += list_item.format('', tail.replace(".temphtml", ".html"), icon, tail.replace(".temphtml", ""))

    # Now that we have all the file paths, start writing the files

    for category, path_list in side_list.items():
        for path in path_list:
            old_filename = os.path.basename(path)
            filename = old_filename.replace(".temphtml", ".html")
            # search for it in nav_list_data, then mark that one as 'active' tab
            active_nav_list_data = mark_item_active(nav_list_data, filename) + nav_bar_script
            artifact_data = get_file_content(path)

            # Now write out entire html page for artifact
            f = open(os.path.join(reportfolderbase, filename), 'w', encoding='utf8')
            artifact_data = insert_sidebar_code(artifact_data, active_nav_list_data, path)
            f.write(artifact_data)
            f.close()
            
            # Now delete .temphtml
            os.remove(path)
            # If dir is empty, delete it
            try:
                os.rmdir(os.path.dirname(path))
            except OSError:
                pass # Perhaps it was not empty!

    # Create index.html's page content
    create_index_html(reportfolderbase, time_in_secs, time_HMS, extraction_type, image_input_path, nav_list_data)
    elements_folder = os.path.join(reportfolderbase, '_elements')
    os.mkdir(elements_folder)
    __location__ = os.path.dirname(os.path.abspath(__file__))
    
    shutil.copy2(os.path.join(__location__,"logo.jpg"), elements_folder)
    shutil.copy2(os.path.join(__location__,"dashboard.css"), elements_folder)
    shutil.copy2(os.path.join(__location__,"feather.min.js"), elements_folder)
    shutil.copy2(os.path.join(__location__,"dark-mode.css"), elements_folder)
    shutil.copy2(os.path.join(__location__,"dark-mode-switch.js"), elements_folder)
    shutil.copytree(os.path.join(__location__,"MDB-Free_4.13.0"), os.path.join(elements_folder, 'MDB-Free_4.13.0'))

def get_file_content(path):
    f = open(path, 'r', encoding='utf8')
    data = f.read()
    f.close()
    return data

def create_index_html(reportfolderbase, time_in_secs, time_HMS, extraction_type, image_input_path, nav_list_data):
    '''Write out the index.html page to the report folder'''
    content = '<br />'
    content += """
    <div class="card bg-white" style="padding: 20px;">
        <h2 class="card-title">Case Information</h2>
    """ # CARD start
    
    case_list = [   ['Extraction location', image_input_path],
                    ['Extraction type', extraction_type],
                    ['Report directory', reportfolderbase],
                    ['Processing time', f'{time_HMS} (Total {time_in_secs} seconds)']  ]

    tab1_content = generate_key_val_table_without_headings('', case_list) + \
    """         <p class="note note-primary mb-4">
                    All dates and times are in UTC unless noted otherwise!
                </p>
    """

    # Get script run log (this will be tab2)
    devinfo_files_path = os.path.join(reportfolderbase, 'Script Logs', 'DeviceInfo.html')
    tab2_content = get_file_content(devinfo_files_path)
    
    # Get script run log (this will be tab3)
    script_log_path = os.path.join(reportfolderbase, 'Script Logs', 'Screen Output.html')
    tab3_content = get_file_content(script_log_path)
    
    # Get processed files list (this will be tab3)
    processed_files_path = os.path.join(reportfolderbase, 'Script Logs', 'ProcessedFilesLog.html')
    tab4_content = get_file_content(processed_files_path)
    
    content += tabs_code.format(tab1_content, tab2_content, tab3_content, tab4_content)
    
    content += '</div>' # CARD end

    authors_data = generate_authors_table_code(rleapp_contributors)
    credits_code = credits_block.format(authors_data)

    # WRITE INDEX.HTML LAST
    filename = 'index.html'
    page_title = 'RLEAPP Report'
    body_heading = 'Returns Logs Events And Properties Parser'
    body_description = 'RLEAPP is an open source project that aims to parse service provider returns for the purpose of triage analysis.'
    active_nav_list_data = mark_item_active(nav_list_data, filename) + nav_bar_script

    f = open(os.path.join(reportfolderbase, filename), 'w', encoding='utf8')
    f.write(page_header.format(page_title))
    f.write(body_start.format(f"RLEAPP {rleapp_version}"))
    f.write(body_sidebar_setup + active_nav_list_data + body_sidebar_trailer)
    f.write(body_main_header + body_main_data_title.format(body_heading, body_description))
    f.write(content)
    f.write(thank_you_note)
    f.write(credits_code)
    f.write(body_main_trailer + body_end + nav_bar_script_footer + page_footer)
    f.close()

def generate_authors_table_code(rleapp_contributors):
    authors_data = ''
    for author_name, blog, tweet_handle, git in rleapp_contributors:
        author_data = ''
        if blog:
            author_data += f'<a href="{blog}" target="_blank">{blog_icon}</a> &nbsp;\n'
        else:
            author_data += f'{blank_icon} &nbsp;\n'
        if tweet_handle:
            author_data += f'<a href="https://twitter.com/{tweet_handle}" target="_blank">{twitter_icon}</a> &nbsp;\n'
        else:
            author_data += f'{blank_icon} &nbsp;\n'
        if git:
            author_data += f'<a href="{git}" target="_blank">{github_icon}</a>\n'
        else:
            author_data += f'{blank_icon}'

        authors_data += individual_contributor.format(author_name, author_data)
    return authors_data

def generate_key_val_table_without_headings(title, data_list, html_escape=True, width="70%"):
    '''Returns the html code for a key-value table (2 cols) without col names'''
    code = ''
    if title:
        code += f'<h2>{title}</h2>'
    table_header_code = \
    """
        <div class="table-responsive">
            <table class="table table-bordered table-hover table-sm" width={}>
                <tbody>
    """
    table_footer_code = \
    """
                </tbody>
            </table>
        </div>
    """
    code += table_header_code.format(width)

    # Add the rows
    if html_escape:
        for row in data_list:
            code += '<tr>' + ''.join( ('<td>{}</td>'.format(html.escape(str(x))) for x in row) ) + '</tr>'
    else:
        for row in data_list:
            code += '<tr>' + ''.join( ('<td>{}</td>'.format(str(x)) for x in row) ) + '</tr>'

    # Add footer
    code += table_footer_code

    return code

def insert_sidebar_code(data, sidebar_code, filename):
    pos = data.find(body_sidebar_dynamic_data_placeholder)
    if pos < 0:
        logfunc(f'Error, could not find {body_sidebar_dynamic_data_placeholder} in file {filename}')
        return data
    else:
        ret = data[0 : pos] + sidebar_code + data[pos + len(body_sidebar_dynamic_data_placeholder):]
        return ret

def mark_item_active(data, itemname):
    '''Finds itemname in data, then marks that node as active. Return value is changed data'''
    pos = data.find(f'" href="{itemname}"')
    if pos < 0:
        logfunc(f'Error, could not find {itemname} in {data}')
        return data
    else:
        ret = data[0 : pos] + " active" + data[pos:]
        return ret
    
    