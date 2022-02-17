from __future__ import print_function

import os.path
import json
import datetime
import shutil
import glob
import time
from pprint import pprint

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_ID = 'c_oek5apckj3l4c7t3qdsf95auls@group.calendar.google.com'
DEST = '/Volumes/GoogleDrive/Shared drives/fin_fs9_2022-01/Recordings'
ZOOM = '/Users/duynguyen/Documents/Zoom'


def getDate(str):
    return time.strptime(str.split(' ')[1], '%H.%M.%S')


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.now()

        start = now.replace(hour=7, minute=0, second=0,
                            microsecond=0).isoformat() + 'Z'

        end = now.replace(hour=18, minute=0, second=0,
                          microsecond=0).isoformat() + 'Z'

        calendar = service.events().list(calendarId=CALENDAR_ID,
                                         timeMin=start,
                                         timeMax=end,
                                         maxResults=2,
                                         singleEvents=True,
                                         orderBy='startTime'
                                         ).execute()
        events = calendar.get('items')
        event_names = [item.get('summary') for item in events]

        # get zoom videos
        zoom_dirs_today = glob.glob(
            '%s/%s*' % (ZOOM, now.date()))
        zoom_dirs_today.sort(key=getDate)

        for index, dir in enumerate(zoom_dirs_today):
            video = glob.glob('%s/*.mp4' % dir)
            abs_path = os.path.join(dir)
            new_name = '%s/%s.mp4' % (abs_path, event_names[index])
            os.rename(video[0], new_name)
            shutil.copyfile(new_name, DEST)

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
