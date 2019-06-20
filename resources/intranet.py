# coding: utf-8
import sys
import os
sys.path.append(os.environ.get('PYTHON_RESOURCES_DIR'))
import re
import resources.tools as tools
from getpass import getpass
import base64
import requests
import yaml

from resources.EnvironmentSelector import EnvironmentSelector


class Platform(EnvironmentSelector):
    def get_saved_user(self):
        return self._saved_platform_users[self._environment]

    def get_saved_password(self):
        if self._environment == "QA":
            encoded_password = self._saved_platform_passwords[self._environment]
            decoded_password = convert_base64_to_utf8(encoded_password)
            return decoded_password


def function_requires_login(decorated_function):
    def new_func(*args, **kwargs):
        if requires_login:
            login()
        return decorated_function(*args)
    return new_func


def _request_login():
    user = input("\tUsername? ")
    password = getpass("\tPassword? ")
    return [user, password]


def convert_utf8_to_base64(password):
    password_bytes = password.encode('utf-8')
    encoded_password_bytes = base64.b64encode(password_bytes)
    return encoded_password_bytes.decode('utf-8')


def convert_base64_to_utf8(s):
    s_bytes = s.encode('utf-8')
    decoded_s = base64.b64decode(s_bytes)
    return decoded_s.decode('utf-8')


def create_login_file(env, user, password):
    tools.create_directory('bin')
    password = decode_bytes_to_string(password)
    encoded_password_str = convert_utf8_to_base64(password)
    text = "[%s]\nUser=%s\nPassword=%s\n" % (env, user, encoded_password_str)
    tools.write_to_file_silently(login_fname, text)


def decode_bytes_to_string(s):
    if type(s) == bytes:
        return s.decode('utf-8')
    return s


def modify_existing_login(login_text, env, user, new_password):
    encoded_new_password_str = convert_utf8_to_base64(new_password)

    pattern_s = '\[%s\]\nUser=.*\nPassword=.*' % env
    replace_s = '[%s]\nUser=%s\nPassword=%s' % (env, user, encoded_new_password_str)
    login_text = re.sub(pattern_s, replace_s, login_text)
    tools.write_to_file_silently(login_fname, login_text)


def add_new_platform_login(login_text, env, user, password):
    encoded_password_str = convert_utf8_to_base64(password)
    login_text += "[%s]\nUser=%s\nPassword=%s\n" % (env, user, encoded_password_str)
    tools.write_to_file_silently(login_fname, login_text)


def save_login(user, password):
    user = decode_bytes_to_string(user)
    password = decode_bytes_to_string(password)

    env = platform.get_environment()
    if tools.login_file_exists(login_fname):
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
    print("\tUsername? %s" % user)

    password = platform.get_saved_password()
    if not password:
        password = getpass("\tPassword? ")
    return [user, password]


def get_authentication_url():
    urls = {
        'Production': 'https://intranet.thirdbridge.com/offspring/login',
        'QA': 'https://ops.intranet.test2.pro/offspring/login',
        'Training': 'https://intranet-training.thirdbridge.com/offspring/login',
        'DEV': 'https://intranet.dev.thirdbridge.com/offspring/login'
    }
    return urls[platform.get_environment()]


def get_user_and_password():
    env = platform.get_environment()
    if env in ('Production', 'QA', 'Training'):
        print('Logging into %s' % env)
        if platform.is_login_previously_saved():
            return use_existing_login()
        return _request_login()
    sys.exit('Unknown Environment: %s' % env)


def _validate_login(response):
    content = response.text
    if content.find('Wrong email address or password') != -1:
        sys.exit('Failed to Log In: Wrong email address or password')
    else:
        print('Successfully Logged In\n')


def _process_login(user, password):
    print('Processing Login')
    params = {'useUrl': '', 'email_address': user, 'password': password}
    authentication_url = get_authentication_url()
    response = submit_form_lite(authentication_url, params)
    if re.search('401 Authorization Required', response.text):
        _add_authorization_for_external_login(authentication_url, params)
    return response


def _add_authorization_for_external_login(url, values):
    global auth_login
    username = 'cognoweb'
    external_password = input('Enter External Password: ')
    auth_login = (username, external_password)
    session.post(url, data=values, auth=auth_login)


@function_requires_login
def submit_form_lite(url, values={}):
    if values:
        response = session.post(url, data=values, auth=auth_login)
    else:
        response = session.get(url, auth=auth_login)

    response.encoding = 'utf-8'
    return response


@function_requires_login
def submit_form(url, values={}):
    response = submit_form_lite(url, values)
    text = response.text

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
    return submit_form_lite(url).text


def _login_with_user_and_pass(user=None, password=None):
    global login_username
    response = _process_login(user, password)
    _validate_login(response)
    login_username = user
    save_login(user, password)


def _setup_session():
    global session
    session = requests.Session()


def login(env=None):
    global requires_login
    if requires_login:
        requires_login = False

        _setup_session()

        if env:
            platform.set_environment(env)
            file_path = os.path.join(os.environ.get('PYTHON_RESOURCES_DIR'), '.login.cfg')
            file = tools.read_file(file_path).split('\n')
            for line in file:
                if line.find('user=') != -1:
                    admin_user = line.split('=', 1)[1]
                    user = base64.b64decode(admin_user)
                elif line.find('password=') != -1:
                    admin_password = line.split('=', 1)[1]
                    password = base64.b64decode(admin_password)
        else:
            platform.select_environment(login_fname)
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
def get_platform_prefix():
    return platform.get_env_prefix()


@function_requires_login
def get_login_username():
    return decode_bytes_to_string(login_username)


requires_login = True
platform = Platform()
login_fname = 'bin/login.cfg'
auth_login = {}
login_username = None
