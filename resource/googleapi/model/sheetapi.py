from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from app.config import setting
class googleSheet:

    def __init__(self,sheetID, range):
        # If modifying these scopes, delete the file token.pickle.
        self.SCOPES  = setting.SCOPES
        self.sheetID = sheetID
        self.range = range
        self.service = self.service(SAMPLE_SPREADSHEET_ID =self.sheetID,SAMPLE_RANGE_NAME = self.range)

    def service(self, SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
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
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)
        return service

    def read_excel(self):

        # Call the Sheets API
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.sheetID,range=self.range).execute()
        values = result.get('values', [])
        if not values:
            return False
        else:
            return values




