from __future__ import print_function
import datetime, time
import json
import os.path
from sys import maxsize
from google.oauth2 import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from oauth2client.client import OAuth2WebServerFlow
from events import Events

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Google_Calendar:
    def __init__(self):
        self.events = []

    def google_auth_token_refresh(self):
        token_exists = os.path.exists('token.json')
        if token_exists:
          creds = Credentials.from_authorized_user_file('token.json', SCOPES)
          print(creds)
          with open('token.json', 'r+') as jsonFile:
            originalToken = json.loads(creds.to_json())
            if originalToken != creds:
              jsonFile.seek(0) # go to first char pos
              json.dump(json.loads(creds.to_json()), jsonFile, indent=6)
              jsonFile.truncate
            else:
              print('creds matches that in token')
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        return creds
     

gcal = Google_Calendar()
response = gcal.google_auth_token_refresh()
print(response.to_json())
