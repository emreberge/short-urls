#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
from Crypto.Cipher import ARC4

class IDHider:

	secret_key = ''

	def __init__(self, secret_key):
		self.secret_key = secret_key
		
	def _num_to_char(self, number):
		chars = ''
		for i in range(4):
			chars += chr(number & 255)
			number = number >> 8
		return chars
		
	def _char_to_num(self, chars):
		number = 0
		for c in chars[::-1]:
			number = number << 8
			number = (ord(c)) | number
		return number
	
	# Since it's a stream chipper an we want to encrpyt regardless of order we have to create new ones each time.
	def _encode(self, value):
		return ARC4.new(self.secret_key).encrypt(value)
		
	def _decode(self, value):
		return ARC4.new(self.secret_key).decrypt(value)
		
	def hide_id(self, id):
		return self._char_to_num(self._encode(self._num_to_char(id)))
		
	def unhide_id(self, id):
		return self._char_to_num(self._decode(self._num_to_char(id)))

class Test_IDHider(unittest.TestCase):
	
	def setUp(self):
		self.id_hider = IDHider('My secret key')

	def test_convert__num_to_char(self):
		number = ((0x21 << 24) | (0x21 << 16) | (0x21 << 8) | 0x21)
		self.assertEquals(self.id_hider._num_to_char(number), '!!!!')
		
	def test_convert__char_to_num(self):
		number = ((0x21 << 24) | (0x21 << 16) | (0x21 << 8) | 0x21)
		self.assertEquals(self.id_hider._char_to_num('!!!!'), number)
	
	def test_convert_both_ways_32bit_number(self):
		number = 2**32-1
		self.assertEquals(self.id_hider._char_to_num(self.id_hider._num_to_char(number)), number)
		
	def test_encode(self):
		value = "There are 10 types of people in the world: those who understand binary, and those who don't."
		self.assertNotEqual(self.id_hider._encode(value),value)
		
	def test_decode(self):
		value = "I'm not anti-social; I'm just not user friendly"
		ecoded_value = self.id_hider._encode(value)
		self.assertEquals(self.id_hider._decode(ecoded_value), value)
		
	def test_only_decodable_by_same_secret_key(self):
		value = "I would love to change the world, but they won't give me the source code"
		ecoded_value = self.id_hider._encode(value)
		id_hider2 = IDHider('On other secret key')
		self.assertNotEquals(id_hider2._decode(ecoded_value), value)
		
	def test_hide_id1(self):
		id = 47548272628
		hidden_id = self.id_hider.hide_id(id)
		self.assertTrue(hidden_id < 2**32)
		self.assertNotEquals(hidden_id, id)
		
	def test_hide_id2(self):
		id = 45115123
		hidden_id = self.id_hider.hide_id(id)
		self.assertTrue(hidden_id < 2**32)
		self.assertNotEquals(hidden_id, id)
		
	def test_unhide_id_32_bit(self):
		id = 2**32-1
		hidden_id = self.id_hider.hide_id(id)
		self.assertTrue(hidden_id < 2**32)
		self.assertEquals(self.id_hider.unhide_id(hidden_id), id)
		
	def test_unhide_only_with_same_secret_key(self):
		id = 4161267685
		false_id_hider = IDHider('False secret key')
		hidden_id = self.id_hider.hide_id(id)
		self.assertEquals(self.id_hider.unhide_id(hidden_id), id)
		self.assertNotEquals(false_id_hider.unhide_id(hidden_id), id)
		self.assertNotEquals(self.id_hider.unhide_id(false_id_hider.hide_id(id)), id)
		self.assertTrue(hidden_id < 2**32)
		
if __name__ == '__main__':
    unittest.main()

		

			