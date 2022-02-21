from __future__ import print_function

import os.path
import json
import datetime
import shutil
import glob
import time
import sys
from pprint import pprint

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_ID = None
DEST = '/Volumes/GoogleDrive/Shared drives/fin_fs9_2022-01/Recordings'
ZOOM = '/Users/duynguyen/Documents/Zoom'

if os.environ.get('CALENDAR_ID'):
    CALENDAR_ID = os.environ.get('CALENDAR_ID')
else:
    print('Please input your calendar id')
    sys.exit(1)


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

        if not event_names:
            print('No events today, exiting')
            sys.exit()

        # get zoom videos
        zoom_dirs_today = glob.glob(
            '%s/%s*' % (ZOOM, now.date()))
        zoom_dirs_today.sort(key=getDate)

        if not zoom_dirs_today:
            print('No zoom videos')
            sys.exit()

        for index, dir in enumerate(zoom_dirs_today):
            try:
                current_event = event_names[index]
            except IndexError:
                print('Current video does not have corresponding event name')
                break
                sys.exit()

            video = glob.glob('%s/*.mp4' % dir)
            abs_path = os.path.join(dir)
            new_video_name = '%s.mp4' % (event_names[index])
            new_full_name = '%s/%s' % (abs_path, new_video_name)
            os.rename(video[0], new_full_name)

            final_name = '%s/%s' % (DEST, new_video_name)
            if os.path.exists(final_name):
                print('Video already uploaded')
                continue
            else:
                shutil.copy(new_full_name, DEST)

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
