class TeamLeader():
	def get_right_id(self, location):
		if location in ('HKG','DEL','SHG'):
			return '63, 49'
		return '63'

	def get_name(self):
		return 'TL'

	def get_position(self):
		return 'TEAM_LEADER'

	def get_title(self):
		return 'Team Leader'

class SeniorResearchAssociate:
	def get_right_id(self, location):
		if location in ('HKG','DEL','SHG'):
			return '62, 49'
		return '62'

	def get_name(self):
		return 'SRA'

	def get_position(self):
		return 'SENIOR_RESEARCH_ASSOCIATE'

	def get_title(self):
		return 'Senior Associate'

class ResearchAssociate:
	def get_right_id(self, location):
		if location in ('LDN','NYC'):
			return '60'
		elif location in ('HKG','DEL','SHG'):
			return '61, 49'
		return '61'
		
	def get_name(self):
		return 'RA'

	def get_position(self):
		return 'RESEARCH_ASSOCIATE'

	def get_title(self):
		return 'Research Associate'

class ResearchAnalyst2:
	def get_right_id(self, location):
		if location in ('LDN','NYC'):
			return '58'
		elif location in ('HKG','DEL','SHG'):
			return '59, 49'
		return '59'
		
	def get_name(self):
		return 'RA2'

	def get_position(self):
		return 'RESEARCH_ANALYST_LVL2'

	def get_title(self):
		return 'Analyst'

class ResearchAnalyst1:
	def get_right_id(self, location):
		if location in ('HKG','DEL','SHG'):
			return '57, 49'
		return '57'
		
	def get_name(self):
		return 'RA1'

	def get_position(self):
		return 'RESEARCH_ANALYST_LVL1'

	def get_title(self):
		return 'Analyst'

class SeniorResearchCoordinator:
	def get_right_id(self, location):
		return '20,62'
		
	def get_name(self):
		return 'RC, SRA'

	def get_position(self):
		return ''

	def get_title(self):
		return 'Senior Research Coordinator'

class ForumAnalyst:
	def get_right_id(self, location):
		return '13,22,26'
		
	def get_name(self):
		return ''

	def get_position(self):
		return ''

	def get_title(self):
		return 'Analyst'

class SalesAssociate:
	def get_right_id(self, location):
		return '11'
		
	def get_name(self):
		return ''

	def get_position(self):
		return ''

	def get_title(self):
		return 'Sales Associate'

class Intern:
	def get_right_id(self, location):
		return '13'
		
	def get_name(self):
		return ''

	def get_position(self):
		return 'Intern'

	def get_title(self):
		return 'Intern'

class OperationsCoordinator:
	def get_right_id(self, location):
		return '13,20'
		
	def get_name(self):
		return ''

	def get_position(self):
		return ''

	def get_title(self):
		return 'Research Coordinator'

mapping = {
		'TL': TeamLeader,
		'TEAM_LEADER': TeamLeader,
		'SRA': SeniorResearchAssociate,
		'SENIOR_RESEARCH_ASSOCIATE': SeniorResearchAssociate,
		'RA': ResearchAssociate,
		'Associate': ResearchAssociate,
		'Research Associate': ResearchAssociate,
		'RESEARCH_ASSOCIATE': ResearchAssociate,
		'A2': ResearchAnalyst2,
		'RA2': ResearchAnalyst2,
		'RESEARCH_ANALYST_LVL2': ResearchAnalyst2,
		'A1': ResearchAnalyst1,
		'RA1': ResearchAnalyst1,
		'RESEARCH_ANALYST_LVL1': ResearchAnalyst1,
		'Senior Research Coordinator': SeniorResearchCoordinator,
		'Forum Analyst': ForumAnalyst,
		'Sales Associate': SalesAssociate,
		'Ops Intern': Intern,
		'Intern': Intern,
		'INTERN': Intern,
		'Operations Coordinator': OperationsCoordinator
	}

def get(role, location):
	if not role:
		return
	role = role.strip()
	return mapping[role]().get_right_id(location)

def get_name(role):
	role = role.strip()
	return mapping[role]().get_name()

def get_position(role):
	role = role.strip()
	return mapping[role]().get_position()

def get_title(role):
	role = role.strip()
	return mapping[role]().get_title()