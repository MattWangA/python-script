# coding: utf-8
import sys
import os
import re
import resources.intranet as intranet
import resources.tools as tools


def _get_edit_url(template_id):
    platform = intranet.get_platform()
    url = {'QA': "https://ops.intranet.test2.pro/offspring/emailTemplate/edit?templateId=%s" % (template_id), 
            'Production': "https://intranet.thirdbridge.com/offspring/emailTemplate/edit?templateId=%s" % (template_id)
           }
    return url[platform]


def _parse_for_body(source):
    final_results = []
    pattern = '<textarea rows="10" cols="40" name="body" class="mandatory scroll">(.*)</textarea>'
    match = re.search(pattern, source, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1)


def _get_long_url():
    platform = intranet.get_platform()
    url = {'QA': "https://ops.intranet.test2.pro/offspring/emailTemplate/",
           'Production': "https://intranet.thirdbridge.com/offspring/emailTemplate/"}
    return url[platform]


def _submit_form(url, values):
    return intranet.submit_form_lite(url, values)


def get_body(template_id):
    url = _get_edit_url(template_id)
    response = intranet.submit_form_lite(url)
    source = response.read()
    return _parse_for_body(source)


def create(title, values):
    platform = intranet.get_platform()
    url = _get_long_url() + 'saveNew'

    response = _submit_form(url, values)
    tools.log('Created Template {%s}' % (title))
    return response


def modify(title, values):
    platform = intranet.get_platform()
    url = _get_long_url() + 'saveEdit'

    response = _submit_form(url, values)
    tools.log('Modified Template {%s}' % (title))
    return response


def copy(title, values):
    platform = intranet.get_platform()
    url = _get_long_url() + 'saveCopy'

    response = _submit_form(url, values)
    tools.log('Copied Template {%s}' % (title))
    return response
