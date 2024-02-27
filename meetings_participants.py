#Script to fetch participants of the last meeting, print their email, display name, joined time, and left time in CSV file.

import requests
import os
import json
import csv

#Fetch the access token from the OS.
access_token = os.getenv("Access_Token")
headers = {'Authorization': f'Bearer {access_token}', "Content-Type": "application/json"}

def find_last_meeting_id():
    url = "https://webexapis.com/v1/meetings?meetingType=meeting&state=ended"    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if len(data["items"]) > 0:
            last_meeting_id = data["items"][0]['id']
            return last_meeting_id
        else:
            return "No meetings found."
    else:
        return f"Failed to fetch meeting details. Status code: {response.status_code}"

def find_meeting_participants(meeting_id):
    base_url = "https://webexapis.com/v1/meetingParticipants?meetingId={}"
    url = base_url.format(meeting_id)
    participant_list = requests.get(url, headers=headers)
    return participant_list.text

# Find the meeting ID of the last meeting I hosted.
meeting_id = find_last_meeting_id()

# Retrieve the list of participants from my most recent meeting using the meeting ID.
participants = find_meeting_participants(meeting_id)

# Convert the string data into a dictionary.
participant_list = participants.replace("'", '"')
participant_list_dict = json.loads(participant_list)

# Define the file name where the CSV data will be saved
output_csv_file = 'participants.csv'

# Initialize a flag to determine if headers have been printed.
headers_printed = False

with open(output_csv_file, mode='w', newline='') as file:
    # Define the field names.
    fieldnames = ['email', 'displayName', 'joinedTime', 'leftTime']
    
    # Create a CSV DictWriter object
    writer = csv.DictWriter(file, fieldnames=fieldnames)
        
    for participant in participant_list_dict['items']:
        if participant.get('host') == False:
            # Extract the desired keys
            selected_data = {key: participant.get(key, '') for key in fieldnames}

            # Check if headers have been printed (written); if not, write them
            if not headers_printed:
                writer.writeheader()
                headers_printed = True

            # Write the corresponding values as a CSV row
            writer.writerow(selected_data)

print(f"CSV file '{output_csv_file}' has been created with participant details.")
