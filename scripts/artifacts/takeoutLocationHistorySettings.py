# Module Description: Parses Device Information from Google Takeout Location History Exports. Device Information is also parsed through free to use Google Location History Data Parser available at https://github.com/MetadataForensics/Google-Location-History-Data-Parser
# Author: @MetadataForensics by @SQL_McGee
# Date: 2024-03-21
# Date Updated: 2024-04-09
# Artifact version: 0.0.1
# Requirements: none

import datetime
import json
import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, is_platform_windows, kmlgen

# Lookup table for Android OS versions, values from https://apilevels.com/
android_versions = {
	34: 'Android 14',
	33: 'Android 13',
	32: 'Android 12',
	31: 'Android 12',
	30: 'Android 11',
	29: 'Android 10',
	28: 'Android 9.0',
	27: 'Android 8.1',
	26: 'Android 8.0',
	25: 'Android 7.1',
	24: 'Android 7.0',
	23: 'Android 6',
	22: 'Android 5.1',
	21: 'Android 5.0',
	20: 'Android 4.4W',
	19: 'Android 4.4',
	18: 'Android 4.3',
	17: 'Android 4.2',
	16: 'Android 4.1',
	15: 'Android 4.0.3 - 4.0.4',
	14: 'Android 4.0.1 - 4.0.2',
	13: 'Android 3.2',
	12: 'Android 3.1',
	11: 'Android 3.0',
	10: 'Android 2.3.3 - 2.3.7',
	9: 'Android 2.3.0 - 2.3.2',
	8: 'Android 2.2',
	7: 'Android 2.1',
	6: 'Android 2.0.1',
	5: 'Android 2.0',
	4: 'Android 1.6',
	3: 'Android 1.5',
	2: 'Android 1.1',
	1: 'Android 1.0',
	# Add more API levels and their corresponding Android versions here
}

iphone_models = {
	'iPhone1,1': 'Original iPhone (1st generation)',
	'iPhone1,2': 'iPhone 3G',
	'iPhone2,1': 'iPhone 3GS',
	'iPhone3,1': 'iPhone 4',
	'iPhone3,2': 'iPhone 4',
	'iPhone3,3': 'iPhone 4',
	'iPhone4,1': 'iPhone 4s',
	'iPhone5,1': 'iPhone 5',
	'iPhone5,2': 'iPhone 5',
	'iPhone5,3': 'iPhone 5c',
	'iPhone5,4': 'iPhone 5c',
	'iPhone6,1': 'iPhone 5s',
	'iPhone6,2': 'iPhone 5s',
	'iPhone7,1': 'iPhone 6 Plus',
	'iPhone7,2': 'iPhone 6',
	'iPhone8,1': 'iPhone 6s',
	'iPhone8,2': 'iPhone 6s Plus',
	'iPhone8,4': 'iPhone SE (1st generation)',
	'iPhone9,1': 'iPhone 7',
	'iPhone9,2': 'iPhone 7 Plus',
	'iPhone9,3': 'iPhone 7 (Global)',
	'iPhone9,4': 'iPhone 7 Plus (Global)',
	'iPhone10,1': 'iPhone 8',
	'iPhone10,2': 'iPhone 8 Plus',
	'iPhone10,3': 'iPhone X',
	'iPhone10,4': 'iPhone 8 (Global)',
	'iPhone10,5': 'iPhone 8 Plus (Global)',
	'iPhone10,6': 'iPhone X (Global)',
	'iPhone11,2': 'iPhone Xs',
	'iPhone11,4': 'iPhone Xs Max (China)',
	'iPhone11,6': 'iPhone Xs Max',
	'iPhone11,8': 'iPhone XR',
	'iPhone12,1': 'iPhone 11',
	'iPhone12,3': 'iPhone 11 Pro',
	'iPhone12,5': 'iPhone 11 Pro Max',
	'iPhone12,8': 'iPhone SE (2nd generation)',
	'iPhone13,1': 'iPhone 12 Mini',
	'iPhone13,2': 'iPhone 12',
	'iPhone13,3': 'iPhone 12 Pro',
	'iPhone13,4': 'iPhone 12 Pro Max',
	'iPhone14,4': 'iPhone 13 mini',
	'iPhone14,5': 'iPhone 13',
	'iPhone14,2': 'iPhone 13 Pro',
	'iPhone14,3': 'iPhone 13 Pro Max',
	'iPhone14,6': 'iPhone SE',
	'iPhone14,7': 'iPhone 14',
	'iPhone14,8': 'iPhone 14 Plus',
	'iPhone15,2': 'iPhone 14 Pro',
	'iPhone15,3': 'iPhone 14 Pro Max',
	'iPhone15,4': 'iPhone 15',
	'iPhone15,5': 'iPhone 15 Plus',
	'iPhone16,1': 'iPhone 15 Pro',
	'iPhone16,2': 'iPhone 15 Pro Max',
}

def get_takeoutLocationHistorySettings(files_found, report_folder, seeker, wrap_text, time_offset):
	
	for file_found in files_found:
		file_found = str(file_found)
		if not os.path.basename(file_found) == 'Settings.json': # skip -journal and other files
			continue
	
		with open(file_found, encoding = 'utf-8', mode = 'r') as f:
			data = json.loads(f.read())
		data_list = []
	
		# Extract the pertinent data from the JSON data
		createdTime = data['createdTime'].replace('T', ' ').replace('Z', '') # Displays the time the Google account associated with the Location History data was created
		modifiedTime = data['modifiedTime'].replace('T', ' ').replace('Z', '') # Displays the time the Google account associated with the Location History data was last modified to capture, or cease capturing, data collection
		try:
			if 'historyEnabled' in data:
				enabled_key = 'historyEnabled' # Reflects whether Location History was enabled or not enabled for the Google account, True for Enabled
			elif 'timelineEnable' in data:
				enabled_key = 'timelineEnabled' # Renamed in newer exports
			else:
				enabled_key = None
			
			if enabled_key:
				enabled = data[enabled_key]
			else:
				enabled = None
		except KeyError:
			enabled = None

		try:
			if 'historyDeletionTime' in data:
				deletion_time_key = 'historyDeletionTime'
			elif 'timelineDeletionTime' in data:
				deletion_time_key = 'timelineDeletionTime'
			else:
				deletion_time_key = None
			
			if deletion_time_key:
				deletion_time = data[deletion_time_key].replace('T', ' ').replace('Z', '')
			else:
				deletion_time = None
		except KeyError:
			deletion_time = None
		devices = data.get('deviceSettings', []) # One or more devices can be associated with the Google account, this will capture data for all devices associated when more than one devices are present
		if len(data['deviceSettings']) > 1:
			# Loop through each device and print its details
			for device in data['deviceSettings']:
				deviceTag = device['deviceTag'] # Displays the globally unique identifier for the device, as created by Google
				reportingEnabled = device['reportingEnabled'] # Reflects whether Location History was enabled or not enabled for the Device itself, True for Enabled
				try:
					legalCountryCode = device['legalCountryCode'].upper() # Displays the device Country Code
				except KeyError:
					legalCountryCode = None
				devicePrettyName = device['devicePrettyName'] # Displays the device pretty name
				platformType = device['platformType'] # Displays the device platform type - "IOS" for Apple iOS
				deviceCreationTime = device['deviceCreationTime'].replace('T', ' ').replace('Z', '') # Displays the time the device was first associated with the Google account
				reportingEnabledModificationTime = device['latestLocationReportingSettingChange']['reportingEnabledModificationTime'].replace('T', ' ').replace('Z', '') # Displays the time Location History permissions were last modified for the device
				try:
					OSVersion = device['iosVersion'] # Displays the iOS version for Apple devices
				except KeyError:
					iosVersion = None
				try:
					osLevel = device['androidOsLevel'] # Displays the OS version for Android devices
					OSVersion = android_versions[osLevel]
				except KeyError:
					androidOsLevel = None
				deviceSpec = device['deviceSpec']['device'] # Displays the model type for the device
				if deviceSpec in iphone_models:
					deviceSpec = iphone_models[deviceSpec]
				try:
					hasSavedTimelineData = device['deviceActiveness']['hasSavedTimelineData']
				except KeyError:
					hasSavedTimelineData = "New Data Supported in Recent Export Versions"
				try:
					observedPlaceVisitsFor30PercentOfTheLast7d = device['deviceActiveness']['observedPlaceVisitsFor30PercentOfTheLast7d']
				except KeyError:
					observedPlaceVisitsFor30PercentOfTheLast7d = "New Data Supported in Recent Export Versions"
				historyEnabledModificationTime = None
				try:
					historyEnabledModificationTime = data['latestLocationHistorySettingChange']['historyEnabledModificationTime'].replace('T', ' ').replace('Z', '') # Displays the time Location History permissions were last modified for the Google account
				except KeyError:
					try:
						historyEnabledModificationTime = data['latestTimelineSettingChange']['timelineEnabledModificationTime'].replace('T', ' ').replace('Z', '') # Key-pair name change
					except KeyError:
						historyEnabledModificationTime = None
				try:
					retentionWindowDays = data['retentionWindowDays'] # Displays the Location History data retention period for the Google account: "540" for the default value, 18 months; "90" for 3 months; "1080" for 36 months; and "2147483647" if no retention period was set
				except KeyError:
					try:
						retentionWindowDays = data['retentionControl']['retentionWindowDays']
					except KeyError:
						retentionWindowDays = None 
				try:
					encrypted_backups_info = []
					for device_key, device_data in data['encryptedBackupsControls'].items():
						enabled = device_data['enabled']
						encrypted_backups_info.append(f"Device Tag: {device_key}, Enabled: {enabled}")
					encrypted_backups_info = '\n'.join(encrypted_backups_info)
				except KeyError:
					encrypted_backups_info = "New Data Supported in Recent Export Versions"
				hasReportedLocations = data['hasReportedLocations'] # Reflects whether Location History data is present for the Google account, True for data present
				hasSetRetention = data['hasSetRetention'] # Reflects if a rentention period was applied to the Google account, True for "Auto-delete activity older than XX months" or False for "Don't auto-delete activity"
				data_list.append((createdTime, modifiedTime, enabled, deletion_time, deviceTag, reportingEnabled, legalCountryCode, devicePrettyName, platformType, deviceCreationTime, reportingEnabledModificationTime, OSVersion, deviceSpec, hasSavedTimelineData, observedPlaceVisitsFor30PercentOfTheLast7d, historyEnabledModificationTime, retentionWindowDays, encrypted_backups_info, hasReportedLocations, hasSetRetention))
		else:
			for device in data['deviceSettings']:
				deviceTag = device['deviceTag'] # Displays the globally unique identifier for the device, as created by Google
				reportingEnabled = device['reportingEnabled'] # Reflects whether Location History was enabled or not enabled for the Device itself, True for Enabled
				try:
					legalCountryCode = device['legalCountryCode'].upper() # Displays the device Country Code
				except KeyError:
					legalCountryCode = None
				devicePrettyName = device['devicePrettyName'] # Displays the device pretty name
				platformType = device['platformType'] # Displays the device platform type - "IOS" for Apple iOS
				deviceCreationTime = device['deviceCreationTime'].replace('T', ' ').replace('Z', '') # Displays the time the device was first associated with the Google account
				reportingEnabledModificationTime = device['latestLocationReportingSettingChange']['reportingEnabledModificationTime'].replace('T', ' ').replace('Z', '') # Displays the time Location History permissions were last modified for the device
				try:
					OSVersion = device['iosVersion'] # Displays the iOS version for Apple devices
				except KeyError:
					iosVersion = None
				try:
					osLevel = device['androidOsLevel'] # Displays the OS version for Android devices
					OSVersion = android_versions[osLevel]
				except KeyError:
					androidOsLevel = None
				deviceSpec = device['deviceSpec']['device'] # Displays the model type for the device
				if deviceSpec in iphone_models:
					deviceSpec = iphone_models[deviceSpec]
				try:
					historyEnabledModificationTime = data['latestLocationHistorySettingChange']['historyEnabledModificationTime'].replace('T', ' ').replace('Z', '') # Displays the time Location History permissions were last modified for the Google account
				except KeyError:
					historyEnabledModificationTime = None
				deviceSpec = device['deviceSpec']['device'] # Displays the model type for the device
				if deviceSpec in iphone_models:
					deviceSpec = iphone_models[deviceSpec]
				try:
					hasSavedTimelineData = device['deviceActiveness']['hasSavedTimelineData']
				except KeyError:
					hasSavedTimelineData = "New Data Supported in Recent Export Versions"
				try:
					observedPlaceVisitsFor30PercentOfTheLast7d = device['deviceActiveness']['observedPlaceVisitsFor30PercentOfTheLast7d']
				except KeyError:
					observedPlaceVisitsFor30PercentOfTheLast7d = "New Data Supported in Recent Export Versions"
				historyEnabledModificationTime = None  # Initialize historyEnabledModificationTime
				try:
					historyEnabledModificationTime = data['latestLocationHistorySettingChange']['historyEnabledModificationTime'].replace('T', ' ').replace('Z', '') # Displays the time Location History permissions were last modified for the Google account
				except KeyError:
					try:
						historyEnabledModificationTime = data['latestTimelineSettingChange']['timelineEnabledModificationTime'].replace('T', ' ').replace('Z', '') # Key-pair name change
					except KeyError:
						historyEnabledModificationTime = None
				try:
					retentionWindowDays = data['retentionWindowDays'] # Displays the Location History data retention period for the Google account: "540" for the default value, 18 months; "90" for 3 months; "1080" for 36 months; and "2147483647" if no retention period was set
				except KeyError:
					try:
						retentionWindowDays = data['retentionControl']['retentionWindowDays']
					except KeyError:
						retentionWindowDays = None
				encrypted_backups_info = ""  # Initialize encrypted_backups_info
				try:
					encrypted_backups_info = []
					for device_key, device_data in data['encryptedBackupsControls'].items():
						enabled = device_data['enabled']
						encrypted_backups_info.append(f"Device Tag: {device_key}, Enabled: {enabled}")
					encrypted_backups_info = '\n'.join(encrypted_backups_info)
				except KeyError:
					encrypted_backups_info = "New Data Supported in Recent Export Versions"
				hasReportedLocations = data['hasReportedLocations'] # Reflects whether Location History data is present for the Google account, True for data present
				hasSetRetention = data['hasSetRetention'] # Reflects if a rentention period was applied to the Google account, True for "Auto-delete activity older than XX months" or False for "Don't auto-delete activity"
				data_list.append((createdTime, modifiedTime, enabled, deletion_time, deviceTag, reportingEnabled, legalCountryCode, devicePrettyName, platformType, deviceCreationTime, reportingEnabledModificationTime, OSVersion, deviceSpec, hasSavedTimelineData, observedPlaceVisitsFor30PercentOfTheLast7d, historyEnabledModificationTime, retentionWindowDays, encrypted_backups_info, hasReportedLocations, hasSetRetention))
	
	num_entries = len(data_list)
	if num_entries > 0:
		description = 'Account and Device Data for Google Location History.'
		report = ArtifactHtmlReport('Google Location History - Settings')
		report.start_artifact_report(report_folder, 'Google Location History - Settings', description)
		report.add_script()
		data_headers = ('Google Account Creation Time','Location History Modified Time', 'History Enabled', 'History/Timeline Deletion Time', 'Device Tag', 'Device Reporting Enabled', 'Device Country Code', 'Device Pretty Name', 'Device Platform Type', 'Device Creation Time', 'Device Latest Location History Setting Change', 'Device OS Version', 'Device Model', 'Has Saved Timeline Data', 'ObservedPlace Visits for 30% of the last 7 Days', 'Google Account Latest Location History Setting Change', 'Google Account Retention Window (in Days)', 'Encrypted Backups Controls', 'Has Reported Locations', 'Has Set Retention')
		
		report.write_artifact_data_table(data_headers, data_list, file_found)
		report.end_artifact_report()
		
		tsvname = 'Google Location History - Settings'
		tsv(report_folder, data_headers, data_list, tsvname)
		
		tlactivity = 'Google Location History - Settings'
		timeline(report_folder, tlactivity, data_list, data_headers)
	
	else:
		logfunc('No Google Location History - Settings data available')
	
__artifacts__ = {
		"takeoutLocationHistorySettings": (
			"Google Takeout Archive",
			('*/Location History*/Settings.json'),
			get_takeoutLocationHistorySettings)
}
