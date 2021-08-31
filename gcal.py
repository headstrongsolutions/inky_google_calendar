from __future__ import print_function
import datetime, time
import os.path
from sys import maxsize
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from events import Events

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Google_Calendar:
    def __init__(self):
        self.events = []
        self.get_calendar()

    def get_calendar(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
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

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        # set the timeMin-timeMax appropriate to capture 4 full weeks of display, from the first monday before or on this day
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday())
        timestamp2 = time.mktime(last_monday.timetuple())
        min_time = datetime.datetime.fromtimestamp(timestamp2)
        max_time = min_time + datetime.timedelta(days=30)
        events_result = service.events().list(calendarId='primary', timeMin=min_time.isoformat() + 'Z',
                                            maxResults=250, singleEvents=True,
                                            timeMax=max_time.isoformat() + 'Z',
                                            orderBy='startTime').execute()
        gcal_events = events_result.get('items', [])

        # order events into dates
        events = Events(min_time, max_time)   
        for event in gcal_events:
            raw_start = event['start'].get('dateTime', event['start'].get('date'))
            if validate_long_dt(raw_start):
                start_dt = datetime.datetime.strptime(raw_start, '%Y-%m-%dT%H:%M:%S%z')
            elif validate_short_dt(raw_start):
                start_dt = datetime.datetime.strptime(raw_start, '%Y-%m-%d')
            
            raw_end = event['end'].get('dateTime', event['end'].get('date'))
            if validate_long_dt(raw_end):    
                end_dt = datetime.datetime.strptime(raw_end, '%Y-%m-%dT%H:%M:%S%z')
            elif validate_short_dt(raw_end):
                end_dt = datetime.datetime.strptime(raw_end, '%Y-%m-%d')
            
            if start_dt and end_dt:
                summary=event['summary']
                description = ""
                if 'description' in event:
                    description=event['description']
                events.add_event(start=start_dt, end=end_dt, title=summary, description=description)

        self.events = events

def validate_long_dt(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S%z')
        return True
    except ValueError:
        return False

def validate_short_dt(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

