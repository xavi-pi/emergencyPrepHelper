from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import logging


# set up logger
fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def schedule_event(event_data: dict):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    event = service.events().insert(calendarId='primary', body=event_data).execute()
    logger.info('Event created: %s' % (event.get('htmlLink')))


def create_event(summary: str,
                 location: str,
                 description: str,
                 start: str,
                 end: str,
                 recurrence: str,
                 attendees: list) -> dict:
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            recurrence
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 60},
            {'method': 'popup', 'minutes': 60},
            ],
        },
    }
    event['attendees'] = [{'email': attendee} for attendee in attendees]
    return event
