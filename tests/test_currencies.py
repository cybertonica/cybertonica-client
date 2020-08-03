from CybertonicaAPI.currencies import Currency
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitCurrenciesClass(unittest.TestCase):

	def setUp(self):
		self.currencies = Currency(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.currencies, Currency)

		self.assertTrue("get_by_code" in dir(self.currencies))
		self.assertTrue("get_union_base" in dir(self.currencies))
		

	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.currencies, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.currencies.root, object)

class TestGetByCodeMethod(unittest.TestCase):

	def setUp(self):
		self.currencies = Currency(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.code = "704"

	def test_get_by_code_request(self):
		self.currencies.get_by_code(self.code)
		self.currencies.root.r.assert_called_with(
			'GET',
			f'{self.currencies.root.url}/api/v1/currency/int/{self.code}',
			body=None,
			headers=None,
			verify=self.currencies.root.verify
		)
	def test_get_by_code_with_incorrect_code(self):
		with self.assertRaisesRegex(AssertionError, 'The code must be a string'):
			self.currencies.get_by_code(123)
		
	def test_get_by_code_with_empty_code(self):
		with self.assertRaisesRegex(AssertionError, 'The code must not be an empty string'):
			self.currencies.get_by_code("")

class TestGetUnionBaseMethod(unittest.TestCase):

	def setUp(self):
		self.currencies = Currency(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_union_base_request(self):
		self.currencies.get_union_base()
		self.currencies.root.r.assert_called_with(
			'GET',
			f'{self.currencies.root.url}/api/v1/currency/unionBase',
			body=None,
			headers=None,
			verify=self.currencies.root.verify
		)