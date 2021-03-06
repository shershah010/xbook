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
        response, status = login_helper_not_none('user', 'bad_password', database_manager)
        response, status = execute_helper_not_none('aboutme', response['token'], database_manager)
        self.assertTrue(response['response'] == 'user')
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
        self.assertTrue(name == 'acommand')
        self.assertTrue(args == ['-r', '-t', '-a'])

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
        response, status = login_helper_not_none('user', 'bad_password1', database_manager)
        self.assertTrue(response['response'] == 'FAILURE')
        self.assertTrue(status == 400)

    def test_login_helper_good(self):
        response, status = login_helper_not_none('user', 'bad_password', database_manager)
        self.assertTrue(response['response'] == 'SUCCESS')
        self.assertTrue(status == 200)
        self.assertTrue(len(response['token']) == 64)

    #
    #   REGISTER
    #

    def test_register_username_taken(self):
        response, status = register_helper_not_none('user', 'some_password', 'first', 'last', database_manager)
        self.assertTrue(status == 200)
        self.assertTrue(response['response'] == 'FAILURE')
        self.assertTrue(response['flag'] == 0)

    def test_register_username_taken(self):
        response, status = register_helper_not_none('user', 'some_password', 'first', 'last', database_manager)
        self.assertTrue(status == 200)
        self.assertTrue(response['response'] == 'FAILURE')
        self.assertTrue(response['flag'] == 0)

    #
    #   DB
    #

    def test_get_token(self):
        result = database_manager.get_token('user', 'bad_password')
        self.assertTrue(result is not None)

    def test_get_username(self):
        result = database_manager.get_username('some random token')
        self.assertTrue(result == 'Permission denied')

    def test_unique_user_registration(self):
        result = database_manager.unique_user('user', free=0)
        self.assertTrue(result == False)

    def test_unique_user_login(self):
        result = database_manager.unique_user('user', free=1)
        self.assertTrue(result)    

if __name__ == '__main__':
    unittest.main()
