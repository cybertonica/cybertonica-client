from CybertonicaAPI.bins import Bin
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitBinClass(unittest.TestCase):

	def setUp(self):
		self.bin = Bin(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.bin, Bin)
		self.assertTrue("get" in dir(self.bin))


	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.bin, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.bin.root, object)


class TestGetMethod(unittest.TestCase):

	def setUp(self):
		self.bin = Bin(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.b = '8.8.8.8'

	def test_get_request(self):
		self.bin.get(self.b)
		self.bin.root.r.assert_called_with(
			'GET',
			f'{self.bin.root.url}/api/v1.2/bins/{self.b}',
			body=None,
			headers=None,
			verify=self.bin.root.verify
		)

	def test_get_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The BIN must be a string'):
			self.bin.get(None)
	
	def test_get_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The BIN must not be an empty string'):
			self.bin.get('')