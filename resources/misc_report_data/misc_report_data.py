# coding: utf-8
import sys
import os
sys.path.append(os.environ.get('PYTHON_RESOURCES_DIR'))
import re
import resources.intranet as intranet
import resources.tools  as tools
from . import custom_misc_report
import json
import urllib


class MiscReportData:
    custom_report_id = None
    custom_report_name = None
    user_id = None

    def update_script(self, sql):
        if self.custom_report_id == None:
            self.custom_report_id, self.custom_report_name = custom_misc_report.get_report_id_and_name()

            if not self.custom_report_id:
                self.custom_report_id = custom_misc_report.create_custom_report(self.custom_report_name, self.get_user_id())

        if intranet.get_platform() == 'Production':
            url = f"https://intranet.thirdbridge.com/offspring/miscreports/update"
        else:
            url = f"https://ops.intranet.test2.pro/offspring/miscreports/update"

        values = [
            ['saveReport', 'Save'],
            ['reportId', self.custom_report_id],
            ['category', '26'],
            ['status', 'OK'],
            ['owner', self.get_user_id()],
            ['restrictionFlag', 'on'],
            ['label', self.custom_report_name],
            ['query', sql],
            ['comment', ' ']
        ]

        source = intranet.submit_form(url, values)
        if 'response' not in json.loads(source).keys():
            message = 'No Access Rights to Modify Misc Report.'
            tools.log(message, 1)
            sys.exit(message)

        return self.custom_report_id

    def get_user_id(self):
        if not self.user_id:
            employee_list = self.get_dict_list(1113)  # Employee List Query
            expected_email = '{}@thirdbridge.com'.format(intranet.get_login_username())
            for employee in employee_list:
                if employee['Email'] == expected_email:
                    self.user_id = employee['EmployeeID']

        return self.user_id

    def _get_table_source(self, misc_report_id_and_parameters):
        url = self._get_url(misc_report_id_and_parameters)
        html_source = intranet.read_url(url)
        match = re.search('<table class="report">.*</table>', html_source, re.MULTILINE | re.DOTALL)
        if match:
            return match.group()
        elif re.search('An error has occurred in report', html_source, re.MULTILINE | re.DOTALL):
            sys.exit(f"Error when running misc report. Make sure 'id' parameter is provided: {param_dict}")

    def _get_url(self, misc_report_id_and_parameters):
        params = f'id={misc_report_id_and_parameters}'
        if type(misc_report_id_and_parameters) == dict:
            params = urllib.parse.urlencode(misc_report_id_and_parameters)

        if intranet.get_platform() == 'Production':
            return f"https://intranet.thirdbridge.com/offspring/miscreports/results?{params}"
        else:
            return f"https://ops.intranet.test2.pro/offspring/miscreports/results?{params}"

    def _get_results_list_from_source(self, source):
        headers = re.findall('<th>(.*)</th>', source)

        values_list = re.findall('<td>(.*?)</td>', source, re.S)
        max_columns = len(headers)
        if max_columns == 0:
            return []
        list_of_lists = [values_list[i:i + max_columns] for i in range(0, len(values_list), max_columns)]
        return list_of_lists

    def _convert_lists_to_dicts(self, headers, list_of_lists):
        final_results = []
        for data_list in list_of_lists:
            d = {}
            for i in range(len(headers)):
                d[headers[i]] = data_list[i]
            final_results.append(d)
        return final_results

    def get_dict_list(self, misc_report_id_and_parameters):
        source = self._get_table_source(misc_report_id_and_parameters)
        if not source:
            tools.log('No Misc Report data found.')
            return
        headers = re.findall('<th>(.*)</th>', source)

        list_of_lists = self._get_results_list_from_source(source)
        dict_list = self._convert_lists_to_dicts(headers, list_of_lists)
        return dict_list

    def get_list(self, misc_report_id_and_parameters):
        source = self._get_table_source(misc_report_id_and_parameters)
        results_list = self._get_results_list_from_source(source)
        return results_list


def get_list(misc_report_id_and_parameters):
    return mrd.get_list(misc_report_id_and_parameters)


def get_dict_list(misc_report_id_and_parameters):
    return mrd.get_dict_list(misc_report_id_and_parameters)


def get_dict_list_with_params(misc_report_id, param_dict={}):
    return mrd.get_dict_list_with_params(misc_report_id, param_dict)


def get_list_from_sql(sql):
    report_id = mrd.update_script(sql)
    return mrd.get_list(report_id)


def get_dict_list_from_sql(sql):
    report_id = mrd.update_script(sql)
    return mrd.get_dict_list(report_id)


def get_data(misc_report_id_and_parameters, max_columns):
    ''' Deprecate when possible'''
    return get_list(misc_report_id_and_parameters)


mrd = MiscReportData()

# Tests


def test_get_dict_list_from_sql():
    import queries
    intranet.login_admin_qa()
    sql = queries.EMPLOYEE_RIGHTS
    dict_list = get_dict_list_from_sql(sql)
    print(dict_list)


def test_list():
    intranet.login_admin_qa()
    results_list = get_list(1012)
    print(results_list)


def test_get_report_as_dictionary():
    intranet.login_admin_qa()
    results_list = get_dict_list(1012)
    print(results_list)


def test_get_dict_list_with_params():
    intranet.login_admin()
    results_list = get_dict_list({'id': '1108', 'ExpertID': '10000'})
    print(results_list)
