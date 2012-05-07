import unittest
import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
from web import *
import manage
from flask import Response


class Test_integration_tests(unittest.TestCase):

    def setUp(self):
        manage.create_all()

    def test_adding_and_retriving(self):
        self.assertEqual(add_url_to_db('http://emreberge.com'), 1)
        response = redirect_route(1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://emreberge.com')
        
if __name__ == '__main__':
    unittest.main()
