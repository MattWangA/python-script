# coding: utf-8

import sys
import intranet
import tools
import misc_report_data


def _update_rights(form_values):
    if intranet.get_platform() == 'QA':
        next_url = 'https://ops.intranet.test2.pro/rights_management.php'
    elif intranet.get_platform() == 'Production':
        next_url = 'https://intranet.thirdbridge.com/rights_management.php'
    else:
        sys.exit('Unknown Platform')

    intranet.submit_form_lite(next_url, form_values)


def _add_changed_id_when_modifying_a_right(rights_list, user_id):
    changed_id = 'changed-%s' % user_id
    rights_list.append([changed_id, '1'])


def _add_user_ids(rights_list, user_id, rights_str):
    rights = rights_str.split(',')
    user_header = 'user-%s[]' % user_id
    for right in rights:
        rights_list.append([user_header, right])


def _convert_users_groups_dict_to_list(users_groups_dict):
    rights_list = []
    for user_id, rights_str in users_groups_dict.items():
        _add_changed_id_when_modifying_a_right(rights_list, user_id)
        _add_user_ids(rights_list, user_id, rights_str)
    return rights_list


def get_form_rights_values(users_groups_dict):
    form_values = [
        ['pageaction', 'SUBMIT'],
        ['view', 'USERS'],
        ['filter', '']
    ]

    rights_list = _convert_users_groups_dict_to_list(users_groups_dict)

    form_values.extend(rights_list)
    # for new_right in rights_list:
    #   tools.log(str(new_right))
    return form_values


def change_rights(users_groups_dict):
    '''example: users_groups_dict = {'2088':'9,26,46', '1989':'9,26,46'}'''
    tools.log('Updating Rights for %s' % str(users_groups_dict))
    values = get_form_rights_values(users_groups_dict)
    _update_rights(values)


def get_dict_list():
    return misc_report_data.get_dict_list_from_sql(misc_report_data.EMPLOYEE_RIGHTS)


def change_rights_test():
    intranet.login_admin_qa()
    users_groups_dict = {'2235': '7,9,26,46', '2237': '9,26,46'}
    change_rights(users_groups_dict)
