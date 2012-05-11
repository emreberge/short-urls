import unittest
import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
import web
from web import *
import manage
from flask import Response
from werkzeug.exceptions import NotFound
from b64 import *


class Test_integration_tests(unittest.TestCase):
        
    def setUp(self):
        manage.create_all()
        web.app.config['TESTING'] = True
        self.app = web.app.test_client()
        
    def tearDown(self):
        manage.drop_all()
        
    def test_adding(self):
        short_url = self.app.post('/', data=dict(url='http://emreberge.com')).data
        #db index starts at 1 = B
        self.assertEqual(short_url, 'B')
    
    def test_craeting_with_valid_url_should_redirect_to_the_same_url(self):
        self.redirect_works_for('http://emreberge.com', 'http://emreberge.com')
        
    def redirect_works_for(self, test_url, redirect_url):
        self.assertEqual(add_url_to_db(test_url), 'B')
        response = self.app.get('/B')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], redirect_url)
    
    def test_should_work_with_https(self):
        self.redirect_works_for('https://google.com', 'https://google.com')

    def test_should_work_with_url(self):
        self.redirect_works_for('72.26.203.99/939/', 'http://72.26.203.99/939/')

    def test_shoudl_work_with_relative_url(self):
        self.redirect_works_for('emreberge.com', 'http://emreberge.com')
        
    def test_mail_links_should_return_400(self):
        response = self.app.post('/', data=dict(url='mailto:spam@spamer.com'))
        self.assertEqual(response.status_code, 400)
        
    def test_javascript_should_return_400(self):
        response = self.app.post('/', data=dict(url='javascript:alert(\'BAM!\')'))
        self.assertEqual(response.status_code, 400)
        
    def test_non_valid_url_should_return_400(self):
        response = self.app.post('/', data=dict(url='this/url/is/not/valid'))
        self.assertEqual(response.status_code, 400)

    def test_retrieving_non_existing_short_url_should_result_404(self):
        response = self.app.get('/xDseF')
        self.assertEqual(response.status_code, 404)
            
    def test_retrieving_malformated_short_url_char_should_result_404(self):
        response = self.app.get('/*')
        self.assertEqual(response.status_code, 404)
            
    def test_retrieving_malformated_short_url_string_should_result_404(self):
        response = self.app.get('/*#%')
        self.assertEqual(response.status_code, 404)
                
class Test_Url(unittest.TestCase):
    
    def check_redirect_response(self, response, expected_url):
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], expected_url)
            
    def test_creating_with_id_1_returns_base64_encoded_short_url(self):
        url = Url('http://emreberge.com');
        url.id = 1;
        self.assertEqual(url.short_url(), 'B')
        
    def test_creating_with_id_23_returns_base64_encoded_short_url(self):
        url = Url('http://emreberge.com');
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
        
    def test_decode_ilegal_char_should_reise_illegal_argument_exeption(self):
        with self.assertRaises(ValueError):
            num_decode('*')
        
if __name__ == '__main__':
    unittest.main()
