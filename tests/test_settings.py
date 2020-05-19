from CybertonicaAPI.settings import Settings
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitSettingsClass(unittest.TestCase):

	def setUp(self):
		self.settings = Settings(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.settings, Settings)

		self.assertTrue("get_all" in dir(self.settings))
		self.assertTrue("update" in dir(self.settings))
		

	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.settings, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.settings.root, object)

class TestGetAllMethod(unittest.TestCase):

	def setUp(self):
		self.settings = Settings(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_all_request(self):
		self.settings.get_all()
		self.settings.root.r.assert_called_with(
			'GET',
			f'{self.settings.root.url}/api/v1/settings',
			body=None,
			headers=None,
			verify=self.settings.root.verify
		)

class TestUpdateMethod(unittest.TestCase):

	def setUp(self):
		self.settings = Settings(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.data = {'a': 1, 'b': 2}

	def test_update_request(self):
		self.settings.update(self.data)
		self.settings.root.r.assert_called_with(
			'PUT',
			f'{self.settings.root.url}/api/v1/settings',
			json.dumps(self.data),
			headers=None,
			verify=self.settings.root.verify
		)
	
	def test_update_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.settings.update(123)
		
	def test_update_with_empty_data_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Settings data must not be an empty dictionary'):
			self.settings.update({})