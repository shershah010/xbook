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
        self.assertTrue(response['token'] == '0000000000')


if __name__ == '__main__':
    unittest.main()
