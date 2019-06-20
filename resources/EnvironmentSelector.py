# coding: utf-8
import sys
import os
sys.path.append(os.environ.get('PYTHON_RESOURCES_DIR'))
import re
import resources.tools as tools


class EnvironmentSelector:
    _saved_platform_users = {}
    _saved_platform_passwords = {}
    _platform_values = {'0': 'Exit', '1': 'Production', '2': 'QA', '3': 'Training'}
    _environment = None
    use_saved_login = False

    def __init__(self):
        pass

    def _print_extra_options(self, login_fname):
        if tools.login_file_exists(login_fname):
            login_text = tools.read_file(login_fname)
            qa_match = re.search("\[QA\]\nUser=(.*)\nPassword=(.*)", login_text)
            training_match = re.search("\[Training\]\nUser=(.*)", login_text)
            production_match = re.search("\[Production\]\nUser=(.*)", login_text)

            if qa_match:
                self._saved_platform_users['QA'] = qa_match.group(1)
                self._saved_platform_passwords['QA'] = qa_match.group(2)
                print("\t%s: QA login as %s" % ('4', self._saved_platform_users['QA']))
            if training_match:
                self._saved_platform_users['Training'] = training_match.group(1)
                print("\t%s: Training login as %s" % ('5', self._saved_platform_users['Training']))
            if production_match:
                self._saved_platform_users['Production'] = production_match.group(1)
                print("\t%s: Production login as %s" % ('6', self._saved_platform_users['Production']))

    def _print_default_options(self):
        display_string = "\nEnvironments:"
        for key, value in sorted(self._platform_values.items()):
            line_string = "\n\t%s: %s" % (key, value)
            if key == '0':
                continue
            display_string += line_string
        print(display_string)

    def _print_exit_option(self):
        print("\t0: %s" % (self._platform_values['0']))

    def _print_line_separator(self):
        line_separator = '-' * 40
        print("%s\n" % (line_separator))

    def save_env(self, choice, save_login=False):
        env_mapping = {
            '1': {'Env': 'Production', 'SaveLogin': False},
            '2': {'Env': 'QA', 'SaveLogin': False},
            '3': {'Env': 'Training', 'SaveLogin': False},
            '4': {'Env': 'QA', 'SaveLogin': True},
            '5': {'Env': 'Training', 'SaveLogin': True},
            '6': {'Env': 'Production', 'SaveLogin': True}
        }

        self.set_environment(env_mapping[choice]['Env'], env_mapping[choice]['SaveLogin'])

    def get_environment(self):
        if not self._environment:
            raise Exception('Environment has not been set')
        return self._environment

    def get_env_prefix(self):
        if not self._environment:
            raise Exception('Environment has not been set')
        elif self._environment == 'QA':
            return 'qa.'
        return ''

    def set_environment(self, env, save_login=False):
        self._environment = env
        self.use_saved_login = save_login

    def select_environment(self, login_fname):
        choice = None
        while choice not in ('0', '1', '2', '3', '4', '5', '6'):
            self._print_default_options()
            self._print_extra_options(login_fname)
            self._print_exit_option()
            self._print_line_separator()
            choice = input('Select Environment: ')
        print('\n')

        if choice == '0':
            sys.exit('Exiting Program.')

        self.save_env(choice)

    def is_login_previously_saved(self):
        return self.use_saved_login
