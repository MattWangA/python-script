# coding: utf-8

import intranet
import misc_report_data
from poster.encode import multipart_encode

class EmployeeData():
	employee_data = None

	def __init__(self):
		self.get_list()

	def get_team(self, name):
		for e in self.employee_data:
			if e['Name'] == name:
				return e['Team']

	def get_employee_id(self, name):
		for e in self.employee_data:
			if e['Name'] == name:
				return e['EmployeeID']

	def get_role(self, name):
		for e in self.employee_data:
			if e['Name'] == name:
				return e['Role']

	def get_list(self):
		self.employee_data = misc_report_data.get_dict_list_from_sql(misc_report_data.EMPLOYEE_LIST)
				
def get():
	global employee_data
	if not employee_data:
		employee_data = EmployeeData()
	return employee_data

employee_data = None