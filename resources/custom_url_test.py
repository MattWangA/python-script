import unittest
import sys
import os
sys.path.append(os.environ.get('PYTHON_RESOURCES_DIR'))
import tools
import intranet
import misc_report_data


class MyTest(unittest.TestCase):

    def setUp(self):
        text = "custom_intranet_prefix = 'intranet.qa.thirdbridge.com'"
        tools.write_to_file('settings.py', text)
        print(text)

    def test1(self):
        self.assertEqual(intranet.get_custom_url('intranet.thirdbridge.com'), 'intranet.qa.thirdbridge.com')

    def test2(self):
        self.assertEqual(intranet.get_custom_url('intranet-v2.thirdbridge.com'), 'intranet-v2.qa.thirdbridge.com')


class MyTest2(unittest.TestCase):

    def setUp(self):
        text = "custom_intranet_prefix = 'ruk.intranet.thirdbridge.com'"
        tools.write_to_file('settings.py', text)
        print(text)

    def test3(self):
        self.assertEqual(intranet.get_custom_url('intranet-v2.thirdbridge.com'), 'ruk.intranet-v2.thirdbridge.com')

    def test4(self):
        self.assertEqual(intranet.get_custom_url('intranet.thirdbridge.com'), 'ruk.intranet.thirdbridge.com')

    def test5(self):
        self.assertEqual(intranet.get_custom_url('https://intranet.thirdbridge.com'), 'https://ruk.intranet.thirdbridge.com')


class MyTest3(unittest.TestCase):

    def test6(self):
        intranet.login_admin_qa()
        id_and_params = {'id': 1116}
        results = misc_report_data.get_dict_list(id_and_params)
        print(results)


unittest.main(MyTest3())
