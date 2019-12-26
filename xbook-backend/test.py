import unittest
from main import *

class SimpleTest(unittest.TestCase):

    def test_get_response_bad_input(self):
        response = get_response('bad response')
        self.assertTrue(response[0] == 'BAD INPUT')
        self.assertTrue(response[1] == 400)

    def test_get_response_login(self):
        pass

if __name__ == '__main__':
    unittest.main()
