import unittest
import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['SECRET_KEY'] = 'Secret Key'
import web
from web import *
import manage
from flask import Response
from werkzeug.exceptions import NotFound
from b64 import *
from skip32 import skip32

SKIP_32_CODED_SHORT_URL_FOR_DB_FIRST_INDEX = 'bT6bSa'

class Test_Web_App(unittest.TestCase):
        
    def setUp(self):
        manage.create_all()
        web.app.config['TESTING'] = True
        self.app = web.app.test_client()
        
    def tearDown(self):
        manage.drop_all()


# Positive adding/redirecting tests
    
    def test_valid_url(self):
        self.url_redirects_to('http://emreberge.com', 'http://emreberge.com')
        
    def url_redirects_to(self, test_url, redirect_url, db_index=SKIP_32_CODED_SHORT_URL_FOR_DB_FIRST_INDEX):
        request_data = self.request_data_with_url(test_url)
        response_data = self.app.post('/', data=request_data).data
        self.response_data_is_json(response_data, db_index)
        self.response_redirects_to(self.app.get(db_index), redirect_url)
                
    def request_data_with_url(self, url_address):
        request_data=dict()
        request_data[REQUEST_URL_PARAMETER_NAME] = url_address
        return request_data
        
    def response_data_is_json(self, data, short_url):
        self.assertEqual(data, '{"short_url": "%s"}' % short_url)
    
    def response_redirects_to(self, response, redirect_url):
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], redirect_url)
    
    def test_https_url(self):
        self.url_redirects_to('https://google.com', 'https://google.com')

    def test_ip_address(self):
        self.url_redirects_to('72.26.203.99/939/', 'http://72.26.203.99/939/')

    def test_relative_url(self):
        self.url_redirects_to('emreberge.com', 'http://emreberge.com')
        
    def test_urls_with_parameters(self):
        self.url_redirects_to('http://www.youtube.com/watch?v=oHg5SJYRHA0', 'http://www.youtube.com/watch?v=oHg5SJYRHA0');
        

# Negative adding tests
        
    def test_mailto_should_fail_with_400(self):
        self.adding_should_fail_with_error('mailto:spam@spamer.com', 400)
        
    def adding_should_fail_with_error(self, url_to_add, error_code):
        request_data = self.request_data_with_url(url_to_add)
        response = self.app.post('/', data=request_data)
        self.assertEqual(response.status_code, error_code)

    def test_javascript_should_fail_with_400(self):
        self.adding_should_fail_with_error('javascript:alert(\'BAM!\')', 400)
        
    def test_non_valid_url_should_fail_with_400(self):
        self.adding_should_fail_with_error('this/url/is/not/valid', 400)
        
    def test_empty_url_should_fail_with_400(self):
        self.adding_should_fail_with_error('', 400)
        
    def test_no_parameters_should_fail_with_400(self):
        response = self.app.post('/')
        self.assertEqual(response.status_code, 400)


# Negative redirect tests

    def test_non_existing_short_url_should_fail_with_404(self):        
        self.redirect_fails_with_error('/xDseF', 404)
        
    def redirect_fails_with_error(self, test_url, error_code):
        response = self.app.get(test_url)
        self.assertEqual(response.status_code, error_code)
            
    def test_malformated_short_url_char_should_faile_with_404(self):
        self.redirect_fails_with_error('*', 404)
            
    def test_malformated_short_url_string_should_fail_with_404(self):
        self.redirect_fails_with_error('/*#%', 404)


# Feature tests

    def test_urls_allready_in_the_db_should_return_same_short_url(self):
        self.url_redirects_to('www.emreberge.com', 'http://www.emreberge.com', SKIP_32_CODED_SHORT_URL_FOR_DB_FIRST_INDEX);
        self.url_redirects_to('www.emreberge.com', 'http://www.emreberge.com', SKIP_32_CODED_SHORT_URL_FOR_DB_FIRST_INDEX);
        
class Test_Url(unittest.TestCase):
                
    def test_url_with_id_1(self):
        url = Url('http://emreberge.com');
        url.id = 1;
        self.assertEqual(url.short_url(), 'bT6bSa')
        
    def test_url_with_id_23(self):
        url = Url('http://emreberge.com');
        url.id = 23;
        self.assertEqual(url.short_url(), 'L2kam')
        
    def test_short_url_B(self):
		skip32_encoded_short_url_for_b = 'bT6bSa'
		self.assertEqual(Url.id_for_short_url(skip32_encoded_short_url_for_b), 1)

    def test_short_url_X(self):
		skip32_encoded_short_url_for_x = 'L2kam'
		self.assertEqual(Url.id_for_short_url(skip32_encoded_short_url_for_x), 23)

class Test_b64(unittest.TestCase):
    
    def test_encode_decode_1(self):
        self.assertEqual(num_decode(num_encode(1)),1)
        
    def test_encode_decode_1234123(self):
        self.assertEqual(num_decode(num_encode(1234123)),1234123)
        
    def test_decode_ilegal_char_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            num_decode('*')

class IDHiding_Tests(unittest.TestCase):
	
	def setUp(self):
		self.id_hider = skip32('\x00\x99\x88\x77\x66\x55\x44\x33\x22\x11')
	
	def test_both(self):
		self.assertEquals(self.id_hider.hide_id(self.id_hider.unhide_id(0x33221100)), 0x33221100)
	
	def test_hiding(self):
		hidden = self.id_hider.hide_id(0x33221100);
		self.assertEquals(hidden, 0x819d5f1f)
		
	def test_unhiding(self):
		unhidden = self.id_hider.unhide_id(0x819d5f1f);
		self.assertEquals(unhidden, 0x33221100)

if __name__ == '__main__':
	unittest.main()