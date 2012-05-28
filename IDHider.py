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

		

			