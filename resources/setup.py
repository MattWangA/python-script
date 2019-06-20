import os
import sys
sys.path.append(os.environ.get('PYTHON_RESOURCES_DIR'))
import resources.tools as tools

class Setup:
	def __init__(self, file_name):
		self.values = {}
		self.file_name = file_name
		if not os.path.isfile(file_name):
			sys.exit('File {%s} is not found.' % file_name)

		content = tools.read_file(file_name).split('\n')
		self.map_values(content)

	def map_values(self, content):
		for line in content:
			if line.find("=") == -1:
				continue

			field, value = map(str.strip, line.split("="))
			self.values[field] = value

	def validate_values(self, required_fields):
		for required_field in required_fields:
			if required_field not in self.values.keys():
				sys.exit('Field {%s} is required in file {%s}' % (required_field, self.file_name))

	def get(self, field):
		if field in self.values.keys():
			return self.values[field]
		else:
			raise Exception('File %s does not contain field %s' % (self.file_name, field))