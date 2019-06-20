# coding: utf-8

"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import os
import re
import sys

sys.path.append(os.environ.get('PYTHON_RESOURCES_DIR'))
import resources.intranet as intranet
import resources.tools as tools
import resources.misc_report_data as misc_report_data


def _setup_sheets_API():
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    store = file.Storage('bin/credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('bin/client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = discovery.build('sheets', 'v4', http=creds.authorize(Http()))
    return service


def _call_sheets_api(service, spreadsheet_id, sheet_tab, columns_range):
    RANGE_NAME = '%s!%s' % (sheet_tab, columns_range)
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=RANGE_NAME).execute()
    values = result.get('values', [])
    return values


def _get_data(spreadsheet_id, sheet_tab, columns_range):
    service = _setup_sheets_API()
    values = _call_sheets_api(service, spreadsheet_id, sheet_tab, columns_range)
    return values


def _parse_source(sheet_name):

    SPREADSHEET_ID = '1A5T6wnPTdovEUwm2CTFUx2is523n1DmaSOLe7-PXKVM'
    COLUMNS_RANGE = 'A:E'

    gs_data = _get_data(SPREADSHEET_ID, f'{sheet_name}', COLUMNS_RANGE)

    return gs_data
