import unittest
from main import *

class SimpleTest(unittest.TestCase):

    def test_execute_helper_none(self):
        response, status = execute_helper(None)
        self.assertTrue(response['response'] == 'BAD COMMAND')
        self.assertTrue(status == 400)

if __name__ == '__main__':
    unittest.main()
