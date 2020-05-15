from CybertonicaAPI.roles import Role
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitRoleClass(unittest.TestCase):

	def setUp(self):
		self.roles = Role(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.roles, Role)

		self.assertTrue("get_all" in dir(self.roles))
		self.assertTrue("search_by_id" in dir(self.roles))
		self.assertTrue("raw_create" in dir(self.roles)) #TODO: implement user-friendly ui
		self.assertTrue("raw_update" in dir(self.roles)) #TODO: implement user-friendly ui
		self.assertTrue("delete" in dir(self.roles))

	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.roles, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.roles.root, object)

class TestGetAllMethod(unittest.TestCase):

	def setUp(self):
		self.roles = Role(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_all_request(self):
		self.roles.get_all()
		self.roles.root.r.assert_called_with(
			'GET',
			f'{self.roles.root.url}/api/v1/roles',
			body=None,
			headers=None,
			verify=self.roles.root.verify
		)

class TestSearchByIdMethod(unittest.TestCase):

	def setUp(self):
		self.roles = Role(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, [{'id': 'test_id'}]))
		))
		self.id = 'test_id'

	def test_search_by_id_request(self):
		flag, response = self.roles.search_by_id(self.id)
		self.roles.root.r.assert_called_with(
			'GET',
			f'{self.roles.root.url}/api/v1/roles',
			body=None,
			headers=None,
			verify=self.roles.root.verify
		)
		self.assertTrue(flag)
		self.assertEqual(response, {'id': 'test_id'})

	def test_search_by_id_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.roles.search_by_id(None)
	
	def test_search_by_id_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.roles.search_by_id('')

class TestRawCreateMethod(unittest.TestCase):

	def setUp(self):
		self.roles = Role(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			dev_mode=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.data = {'a': 1, 'b': 2}

	def test_raw_create_request(self):
		self.roles.raw_create(self.data)
		self.roles.root.r.assert_called_with(
			'POST',
			f'{self.roles.root.url}/api/v1/roles',
			json.dumps(self.data),
			headers=None,
			verify=self.roles.root.verify
		)

	def test_raw_create_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.roles.raw_create(123)
	
	def test_raw_create_with_empty_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Role data must not be an empty dictionary'):
			self.roles.raw_create({})

class Testraw_updateMethod(unittest.TestCase):

	def setUp(self):
		self.roles = Role(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			dev_mode=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'
		self.data = {'a': 1, 'b': 2}

	def test_raw_update_request(self):
		self.roles.raw_update(self.id, self.data)
		self.roles.root.r.assert_called_with(
			'PUT',
			f'{self.roles.root.url}/api/v1/roles/{self.id}',
			json.dumps(self.data),
			headers=None,
			verify=self.roles.root.verify
		)
	def test_raw_update_should_work_if_dev_mode_eq_true(self):
		self.roles.root.dev_mode = True
		self.roles.raw_update(self.id,self.data)

	def test_raw_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.roles.raw_update(123,self.data)
	
	def test_raw_update_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.roles.raw_update(self.id,123)
	
	def test_raw_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.roles.raw_update('',self.data)
	
	def test_raw_update_with_empty_data_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Role data must not be an empty dictionary'):
			self.roles.raw_update(self.id,{})

class TestDeleteMethod(unittest.TestCase):

	def setUp(self):
		self.roles = Role(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_delete_request(self):
		self.roles.delete(self.id)
		self.roles.root.r.assert_called_with(
			'DELETE',
			f'{self.roles.root.url}/api/v1/roles/{self.id}',
			body=None,
			headers=None,
			verify=self.roles.root.verify
		)

	def test_delete_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.roles.delete(123)
	
	def test_delete_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.roles.delete('')