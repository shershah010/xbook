import unittest
from main import *

class SimpleTest(unittest.TestCase):

    # Returns True or False.
    def test_get_response(self):
        response = get_response('hi')
        self.assertTrue(response[0] == 'success')
        self.assertTrue(response[1] == 200)

if __name__ == '__main__':
    unittest.main()
