# coding: utf-8
import sys
import os
sys.path.append(os.environ.get('PYTHON_RESOURCES_DIR'))
import re
import urllib.request, urllib.error, urllib.parse
import tools
from getpass import getpass
from poster.streaminghttp import register_openers
from poster.encode import multipart_encode
import base64

class EnvironmentSelector:
	_saved_platform_users = {}
	_saved_platform_passwords = {}
	_platform_values = {'0':'Exit', '1':'Production', '2':'QA', '3':'Training'}
	_environment = None
	use_saved_login = False

	def __init__(self):
		pass

	def _print_extra_options(self):
		if login_file_exists():
			login_text = tools.read_file(login_fname)
			qa_match = re.search("\[QA\]\nUser=(.*)\nPassword=(.*)", login_text)
			training_match = re.search("\[Training\]\nUser=(.*)", login_text)
			production_match = re.search("\[Production\]\nUser=(.*)", login_text)

			if qa_match:
				self._saved_platform_users['QA'] = qa_match.group(1)
				self._saved_platform_passwords['QA'] = qa_match.group(2)
				print(("\t%s: QA login as %s" % ('4', self._saved_platform_users['QA'])))
			if training_match:
				self._saved_platform_users['Training'] = training_match.group(1)
				print(("\t%s: Training login as %s" % ('5', self._saved_platform_users['Training'])))
			if production_match:
				self._saved_platform_users['Production'] = production_match.group(1)
				print(("\t%s: Production login as %s" % ('6', self._saved_platform_users['Production'])))

	def _print_default_options(self):
		display_string = "\nEnvironments:"
		for key, value in sorted(self._platform_values.items()):
			line_string = "\n\t%s: %s" % (key, value)
			if key == '0':
				continue
			display_string += line_string
		print(display_string)

	def _print_exit_option(self):
		print(("\t0: %s" % (self._platform_values['0'])))

	def _print_line_separator(self):
		line_separator = '-'*40
		print(("%s\n" % (line_separator)))

	def save_env(self, choice, save_login = False):
		env_mapping = {
			'1': {'Env':'Production', 'SaveLogin':False},
			'2': {'Env':'QA', 'SaveLogin':False},
			'3': {'Env':'Training', 'SaveLogin':False},
			'4': {'Env':'QA', 'SaveLogin':True},
			'5': {'Env':'Training', 'SaveLogin':True},
			'6': {'Env':'Production', 'SaveLogin':True}
		}

		self.set_environment(env_mapping[choice]['Env'], env_mapping[choice]['SaveLogin'])

	def get_environment(self):
		if not self._environment:
			raise Exception('Environment has not been set')
		return self._environment

	def set_environment(self, env, save_login = False):
		self._environment = env
		self.use_saved_login = save_login

	def select_environment(self):
		choice = None
		while choice not in ('0','1','2','3','4','5','6'):
			self._print_default_options()
			self._print_extra_options()
			self._print_exit_option()
			self._print_line_separator()
			choice = eval(input('Select Environment: '))	
		print('\n')

		if choice == '0':
			sys.exit('Exiting Program.')

		self.save_env(choice)

	def is_login_previously_saved(self):
		return self.use_saved_login

class Platform(EnvironmentSelector):
	def get_saved_user(self):
		return self._saved_platform_users[self._environment]

	def get_saved_password(self):
		if self._environment == "QA":
			decoded_password = base64.b64decode(self._saved_platform_passwords[self._environment])
			return decoded_password

def function_requires_login(decorated_function):
	def new_func(*args, **kwargs):
		if requires_login:
			login()
		return decorated_function(*args)
	return new_func

def login_file_exists():
	if os.path.isfile(login_fname):
		return True
	return False

def _request_login():
	user = eval(input("\tUsername? "))
	password = getpass("\tPassword? ")
	return [user, password]

def create_login_file(env, user, password):
	tools.create_directory('bin')
	encoded_password = base64.b64encode(password)
	text = "[%s]\nUser=%s\nPassword=%s\n" % (env, user, encoded_password)
	tools.write_to_file_silently(login_fname, text)

def modify_existing_login(login_text, env, user, password):
	pattern_s = '\[%s\]\nUser=.*\nPassword=.*' % env
	encoded_password = base64.b64encode(password)
	replace_s = '[%s]\nUser=%s\nPassword=%s' % (env, user, encoded_password)
	login_text = re.sub(pattern_s, replace_s, login_text)
	tools.write_to_file_silently(login_fname, login_text)

def add_new_platform_login(login_text, env, user, password):
	encoded_password = base64.b64encode(password)
	login_text += "[%s]\nUser=%s\nPassword=%s\n" % (env, user, encoded_password)
	tools.write_to_file_silently(login_fname, login_text)

def save_login(user, password):
	env = platform.get_environment()
	if login_file_exists():
		login_text = tools.read_file(login_fname)
		pattern = '\[%s\]\nUser=.*\nPassword=.*' % env
		match = re.search(pattern, login_text)
		if match:
			modify_existing_login(login_text, env, user, password)
		else:
			add_new_platform_login(login_text, env, user, password)
	else:
		create_login_file(env, user, password)

def use_existing_login():
	user = platform.get_saved_user()
	print(("\tUsername? %s" % user))

	password = platform.get_saved_password()
	if not password:
		password = getpass("\tPassword? ")	
	return [user, password]

def get_authentication_url():
	urls = {
		'Production':'https://intranet.thirdbridge.com/offspring/login',
		'QA':'https://intranet.qa.thirdbridge.com/offspring/login',
		'Training':'https://intranet-training.thirdbridge.com/offspring/login',
		'DEV': 'https://intranet.dev.thirdbridge.com/offspring/login'
	}
	return urls[platform.get_environment()]

def get_user_and_password():
	env = platform.get_environment()
	if env in ('Production', 'QA', 'Training'):
		print(('Logging into %s' % env))
		if platform.is_login_previously_saved():
			return use_existing_login()
		return _request_login()
	sys.exit('Unknown Environment: %s' % env)

def _validate_login(response):
	content = response.read()
	if content.find('Wrong email address or password') != -1:
		sys.exit('Failed to Log In: Wrong email address or password')
	else:
		print('Successfully Logged In\n')

def _process_login(user, password):
	print('Processing Login')
	params = {'useUrl':'', 'email_address': user, 'password': password}
	authentication_url = get_authentication_url()

	return submit_form_lite(authentication_url, params)

def _add_authorization_for_external_login(request):
	global external_password
	username='cognoweb'
	if not external_password:
		external_password = eval(input('Enter External Password: '))
	base64string = base64.encodestring('%s:%s' % (username, external_password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)
	try:
		response = urllib.request.urlopen(request)
	except urllib.error.HTTPError:
		sys.exit('Could not login externally')
	return response

@function_requires_login
def submit_form_lite(url, values={}):
	data, headers = multipart_encode(values)
	request = urllib.request.Request(url, data, headers)

	try:
		response = urllib.request.urlopen(request)
	except urllib.error.HTTPError:
		response = _add_authorization_for_external_login(request)
	return response

@function_requires_login
def submit_form(url, values={}):
	response = submit_form_lite(url, values)
	text = response.read()

	# Should look into refactoring this.
	if text.find('Login - Third Bridge') != -1:
		msg = 'Failed to submit form to %s. See debug.txt for details.' % (url)
		tools.log(msg)
		tools.log(text, 1)
		sys.exit(msg)
	return text

@function_requires_login
def read_url_lite(url):
	return submit_form_lite(url)

@function_requires_login
def read_url(url):
	return submit_form_lite(url).read()

def _login_with_user_and_pass(user=None, password=None):
	global login_username
	response = _process_login(user, password)
	_validate_login(response)
	login_username = user
	save_login(user, password)

def _setup_ssl():
	''' Magic to bypass SSL '''
	import ssl
	ssl._create_default_https_context = ssl._create_unverified_context

def _setup_opener():
	import http.cookiejar
	opener = register_openers()
	cj = http.cookiejar.CookieJar()
	cookie_handler = urllib.request.HTTPCookieProcessor(cj)
	opener.add_handler(cookie_handler)

def login(env=None):
	global requires_login
	if requires_login:
		requires_login = False

		_setup_ssl()
		_setup_opener()

		if env:
			platform.set_environment(env)
			file_path = os.path.join(os.environ.get('PYTHON_RESOURCES_DIR'), '.login.cfg')
			file = tools.read_file(file_path).split('\n')
			for line in file:
				if line.find('user=') != -1:
					admin_user = line.split('=', 1)[1]
					user = admin_user.decode('base64')
				elif line.find('password=') != -1:
					admin_password = line.split('=', 1)[1]
					password = admin_password.decode('base64')
		else:
			platform.select_environment()
			user, password = get_user_and_password()
		_login_with_user_and_pass(user, password)

def login_admin():
	print("=== Logging as Admin Prod. REMOVE ME BEFORE BUILDING EXECUTABLE! ===")
	login('Production')

def login_admin_qa():
	print("=== Logging as Admin QA. REMOVE ME BEFORE BUILDING EXECUTABLE! ===")
	login('QA')

def login_admin_dev():
	print("=== Logging as Admin DEV. REMOVE ME BEFORE BUILDING EXECUTABLE! ===")
	login('DEV')

@function_requires_login
def get_platform():
	return platform.get_environment()

@function_requires_login
def get_login_username():
	return login_username

requires_login = True
platform = Platform()
login_fname = 'bin/login.cfg'
external_password = None
login_username = None

def main():
	pass

if __name__ == '__main__':
	main()
