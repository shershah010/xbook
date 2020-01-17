import unittest
from main import *

class Test(unittest.TestCase):

    #
    #   SETUP
    #

    database_manager = Database_Manager()

    #
    #   EXECUTE
    #

    def test_execute_helper_none(self):
        response, status = execute_helper(None, database_manager)
        self.assertTrue(response['response'] == 'NO COMMAND')
        self.assertTrue(status == 400)

    def test_execute_helper_bad_input(self):
        response, status = execute_helper_not_none('dfhdoid', None, database_manager)
        self.assertTrue(response['response'] == 'BAD COMMAND')
        self.assertTrue(status == 200)

    def test_execute_helper_aboutme(self):
        response, status = login_helper_not_none('user_temp', 'bad_password', database_manager)
        response, status = execute_helper_not_none('aboutme', response['token'], database_manager)
        self.assertTrue(response['response'] == 'user_temp')
        self.assertTrue(status == 200)

    def test_clean_command_empty(self):
        result = clean_command('')
        self.assertTrue(result is None)

    def test_clean_command_spaces_only(self):
        result = clean_command('     ')
        self.assertTrue(result is None)

    def test_clean_command_name_only(self):
        name, _, _ = clean_command('  HereIsACommand   ')
        self.assertTrue(name == 'hereisacommand')

    def test_clean_command_with_args_only(self):
        name, args, _ = clean_command('aCommand -r -t     -a')
        self.assetTrue(name == 'acommand')
        self.assetTrue(args == ['-r', '-t', '-a'])

    #
    #   LOGIN
    #

    def test_login_helper_none(self):
        response, status = login_helper(None, database_manager)
        self.assertTrue(response['response'] == 'FAILURE')
        self.assertTrue(status == 400)

    def test_login_helper_bad_username(self):
        response, status = login_helper_not_none('user_temp1', 'bad_password', database_manager)
        self.assertTrue(response['response'] == 'FAILURE')
        self.assertTrue(status == 400)

    def test_login_helper_bad_password(self):
        response, status = login_helper_not_none('user_temp', 'bad_password1', database_manager)
        self.assertTrue(response['response'] == 'FAILURE')
        self.assertTrue(status == 400)

    def test_login_helper_good(self):
        response, status = login_helper_not_none('user_temp', 'bad_password', database_manager)
        self.assertTrue(response['response'] == 'SUCCESS')
        self.assertTrue(status == 200)
        self.assertTrue(len(response['token']) == 64)


if __name__ == '__main__':
    unittest.main()
