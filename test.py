import unittest
import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
from web import *
import manage
from flask import Response
from werkzeug.exceptions import NotFound
from b64 import *


class Test_integration_tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        manage.create_all()
        
    @classmethod
    def tearDownClass(cls):
        manage.drop_all()

    def test_adding_and_retriving(self):
        self.assertEqual(add_url_to_db('http://emreberge.com'), 'B')
        response = redirect_route('B')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://emreberge.com')
        
    def test_retrieving_non_existing_short_url_should_result_404(self):
        with self.assertRaises(NotFound):
            redirect_route('xDseF')
                
class Test_Url(unittest.TestCase):
    
    def check_redirect_response(self, response, expected_url):
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], expected_url)
    
    def test_craeting_with_valid_url_should_redirect_to_the_same_url(self):
        url = Url('http://emreberge.com');
        self.check_redirect_response(url.redirect(), 'http://emreberge.com')

    def test_creating_with_relative_url_should_recirect_to_full_url(self):
        url = Url('emreberge.com');
        self.check_redirect_response(url.redirect(), 'http://emreberge.com')
        
    def test_creating_with_id_1_returns_base64_encoded_short_url(self):
        url = Url('');
        url.id = 1;
        self.assertEqual(url.short_url(), 'B')
        
    def test_creating_with_id_23_returns_base64_encoded_short_url(self):
        url = Url('');
        url.id = 23;
        self.assertEqual(url.short_url(), 'X')
        
    def test_getting_id_for_short_url_B(self):
        self.assertEqual(Url.id_for_short_url('B'), 1)
    
    def test_getting_id_for_short_url_X(self):
        self.assertEqual(Url.id_for_short_url('X'), 23)
        
class Test_b64(unittest.TestCase):
    
    def test_1(self):
        self.assertEqual(num_decode(num_encode(1)),1)
        
    def test_encode_1234123(self):
        self.assertEqual(num_decode(num_encode(1234123)),1234123)
        
if __name__ == '__main__':
    unittest.main()
