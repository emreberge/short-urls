import unittest
import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
from web import *
import manage
from flask import Response


class Test_integration_tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        manage.create_all()
        
    @classmethod
    def tearDownClass(cls):
        manage.drop_all()

    def test_adding_and_retriving(self):
        self.assertEqual(add_url_to_db('http://emreberge.com'), 1)
        response = redirect_route(1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://emreberge.com')
        
class Test_Url(unittest.TestCase):
    
    def check_redirect_response(self, response, expected_url):
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], expected_url)
    
    def test_craeting_with_valid_url_should_redirect_to_the_same_url(self):
        url = Url('http://emreberge.com');
        self.check_redirect_response(url.redirect(), 'http://emreberge.com')

        
        
if __name__ == '__main__':
    unittest.main()
