# coding: utf-8
TEAMS_LIST = '''
select 
	t.ID,
	t.Name,
	t.Category,
	t.TeamManagerID,
	t.ParentTeamID,
	t.CreationDate,
	t.Location
from 
	cognolink.teams t
where
	t.deprecationDate = 0
'''