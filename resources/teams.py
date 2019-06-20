# coding: utf-8
import misc_report_data
import intranet

teams = None

def _get_teams_from_intranet():
	return misc_report_data.get_dict_list_from_sql(misc_report_data.TEAMS_LIST)

def _get_id_names_list(team_data):
	fields = ['ID','Name']
	id_names = []
	for team in team_data:
		new_dict = {'ID': team['ID'], 'Name': team['Name']}
		id_names.append(new_dict)
	return id_names

def _get_team_shortnames(id_names):
	short_names = []
	for team in id_names:
		name = team['Name']
		dash_index = name.rfind('- ')
		if dash_index > -1:
			short_name = name[name.rfind('- ')+2:]
			new_dict = {'ID': team['ID'], 'Name': short_name}
			short_names.append(new_dict)
	return short_names

def _get_all_team_names(team_data):
	id_names = _get_id_names_list(team_data)
	team_shortnames = _get_team_shortnames(id_names)
	id_names.extend(team_shortnames)
	return id_names

def add_forum_team(team_data):
	new_team_data = []
	for team in team_data:
		new_team_data.append(team)
		if team['ID'] == '19':
			forum_team = team.copy()
			forum_team['Name'] = 'Forum'
			new_team_data.append(forum_team)
	return new_team_data

def get_list():
	global teams
	if not teams:
		intranet.login()
		team_data = _get_teams_from_intranet()
		team_data = add_forum_team(team_data)
		teams = _get_all_team_names(team_data)
	return teams

def test_get_list():
	intranet.login_admin()
	print(get_list())