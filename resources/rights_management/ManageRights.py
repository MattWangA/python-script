# coding: utf-8

import os
import sys
sys.path.append(os.environ.get('PYTHON_RESOURCES_DIR'))
import intranet
import tools


def _update_rights_groups(form_values):
    if intranet.get_platform() == 'QA':
        url = 'https://ops.intranet.test2.pro/rights_management.php'
    else:
        url = 'https://intranet.thirdbridge.com/rights_management.php'
    intranet.submit_form_lite(url, form_values)


def _add_changed_id(rights_list, identifier_id):
    changed_id = 'changed-%s' % identifier_id
    rights_list.append([changed_id, '1'])


def _add_group_id_values(rights_list, identifier, groups_str):
    groups = groups_str.split(',')
    for group in groups:
        right_key = 'right-%s-%s' % (identifier, group)
        rights_list.append([right_key, group])


def _convert_rights_groups_dict_to_list(rights_groups_dict):
    rights_list = []
    for identifier, groups_str in rights_groups_dict.iteritems():
        _add_changed_id(rights_list, identifier)
        _add_group_id_values(rights_list, identifier, groups_str)

    return rights_list


def _get_form_rights_values(rights_groups_dict):
    form_values = [
        ['pageaction', 'SUBMIT'],
        ['view', 'RIGHTS'],
        ['filter', '']
    ]

    changed_values = _convert_rights_groups_dict_to_list(rights_groups_dict)
    form_values.extend(changed_values)
    return form_values


def change_rights_groups(rights_groups_dict):
    tools.log('Updating Rights Groups for {%s}' % str(rights_groups_dict))
    values = _get_form_rights_values(rights_groups_dict)
    _update_rights_groups(values)


def test_change_rights():
    intranet.login_admin_qa()
    rights_groups_dict = {'739': '7,8'}
    change_rights_groups(rights_groups_dict)
