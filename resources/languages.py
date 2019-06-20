# coding: utf-8
import misc_report_data
import intranet

languages = None

def get_dict_list():
	global languages
	if not languages:
		intranet.login()
		languages_data = misc_report_data.get_dict_list_from_sql(misc_report_data.LANGUAGES_LIST)
	return languages_data

def _get_name_impl(return_type, name):
	languages_dict_list = get_dict_list()

	for d in languages_dict_list:
		if name.lower().strip() in (d['ShortName'].lower(), d['LongName'].lower()):
			return d[return_type]
	raise Exception('Language {%s} not found.' % name)

def get_short_name(name):
	return _get_name_impl('ShortName', name)

def get_long_name(name):
	return _get_name_impl('LongName', name)

def test_get_dict():
	intranet.login_admin()
	print(get_dict_list())