# coding: utf-8
import sys
import os
sys.path.append(os.environ.get('PYTHON_RESOURCES_DIR'))
import re
import resources.intranet as intranet
import resources.tools as tools
import json


def _get_existing_IT_reports():
    if intranet.get_platform() == 'Production':
        url = 'https://intranet.thirdbridge.com/offspring/miscreports/getreportslist'
    else:
        url = 'https://ops.intranet.test2.pro/offspring/miscreports/getreportslist'

    payload = {'id': '26', 'type': 'category'}
    source = intranet.submit_form(url, payload)
    existing_reports = json.loads(source)['response']
    return existing_reports


def create_custom_report(custom_report_name, user_id):
    tools.log(f'Creating new report {custom_report_name}')
    if intranet.get_platform() == 'Production':
        url = 'https://intranet.thirdbridge.com/offspring/miscreports/new/add'
    else:
        url = 'https://ops.intranet.test2.pro/offspring/miscreports/new/add'

    payload = [
        ['category', '26'],
        ['status', 'OK'],
        ['owner', user_id],
        ['restrictionFlag', 'on'],
        ['label', custom_report_name],
        ['query', ' '],
        ['comment', ''],
        ['saveNewReport', 'Save']
    ]

    source = intranet.submit_form(url, payload)
    m = re.search('"response":([0-9]*)}', source)
    if m:
        return m.group(1)

    message = 'No Access Rights to Create Misc Report.'
    tools.log(message, 1)
    sys.exit(message)


def _get_custom_report_name():
    username = intranet.get_login_username()
    return f'Query - {username}'


def get_report_id_and_name():
    existing_reports = _get_existing_IT_reports()
    custom_report_name = _get_custom_report_name()
    report_id = None

    for existing_report in existing_reports:
        if existing_report['label'] == custom_report_name:
            report_id = existing_report['id']

    return [report_id, custom_report_name]
