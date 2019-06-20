# coding: utf-8
import intranet
import tools


def _get_edit_url():
    platform = intranet.get_platform()
    urls = {'QA': 'https://ops.intranet.test2.pro/offspring/stringsEditor/edit/save', 
            'Production': 'https://intranet.thirdbridge.com/offspring/stringsEditor/edit/save'}
    return urls[platform]


def _get_create_url():
    platform = intranet.get_platform()
    urls = {'QA': 'https://ops.intranet.test2.pro/offspring/offspring/stringsEditor/new/save', 
            'Production': 'https://intranet.thirdbridge.com/offspring/stringsEditor/new/save'}
    return urls[platform]


def _upload_string_impl(url, function, function_result, values=None):
    required_headers = ['eStatus', 'eLanguage', 'ePriority', 'eField', 'eSubfield', 'eHelp', 'highlightMode', 'eLabel']

    if not all(header in values.keys() for header in required_headers):
        tools.log('Could not upload string. %s function is missing a required header.' % function)
        return

    if function == 'edit_string' and not values['eId']:
        tools.log('Could not upload string. %s function is missing eId.' % function)
        return

    intranet.submit_form(url, values)
    tools.log('%s Field {%s} Subfield {%s} Language {%s}' % (function_result, values['eField'], values['eSubfield'], values['eLanguage']))


def edit_string(values):
    url = _get_edit_url()
    _upload_string_impl(url, 'edit_string', 'Modified', values)


def create_string(values):
    url = _get_create_url()
    _upload_string_impl(url, 'create_string', 'Created', values)
