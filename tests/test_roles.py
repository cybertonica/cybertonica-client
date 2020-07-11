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
		self.assertTrue("raw_create" in dir(self.roles))
		self.assertTrue("create" in dir(self.roles))
		self.assertTrue("update" in dir(self.roles))
		self.assertTrue("raw_update" in dir(self.roles))
		self.assertTrue("delete" in dir(self.roles))

		self.assertFalse("__permission_helper" in dir(self.roles))
		self.assertFalse("__role_helper" in dir(self.roles))
		self.assertFalse("__permission_converter" in dir(self.roles))

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

class TestRawUpdateMethod(unittest.TestCase):

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
	def test_raw_update_should_work_if_dev_mode_eq_True(self):
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

class TestCreateMethod(unittest.TestCase):

	def setUp(self):
		self.roles = Role(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.name = 'test'
		self.tabs = ['overview']
		self.permissions = {'bi':[1,1,0,1]}

	def test_create_request(self):
		self.roles.create(self.name, self.tabs, self.permissions)
		self.roles.root.r.assert_called_with(
			'POST',
			f'{self.roles.root.url}/api/v1/roles',
			json.dumps({
				"tabs": ["overview"],
				"permissions": [{
					"api": "bi",
					"name": "",
					"tabs": ["overview"],
					"create": True,
					"read": True,
					"update": False,
					"delete": True
				}],
				"name": "test"
			}),
			headers=None,
			verify=self.roles.root.verify
		)

	def test_create_with_incorrect_name_type(self):
		with self.assertRaisesRegex(AssertionError, 'Role name must be a string'):
			self.roles.create(123, self.tabs, self.permissions)

	def test_create_with_empty_name_string(self):
		with self.assertRaisesRegex(AssertionError, 'Role name must not be an empty string'):
			self.roles.create('', self.tabs, self.permissions)
	
	def test_create_with_incorrect_tabs_type(self):
		with self.assertRaisesRegex(AssertionError, 'Tabs must be a list'):
			self.roles.create(self.name, 123, self.permissions)
	
	def test_create_with_unavailable_tab(self):
		with self.assertRaisesRegex(AssertionError, r"You are using unavailable tabs. List of tabs: "):
			self.roles.create(self.name, ['unavailable'], self.permissions)
	
	def test_create_with_incorrect_permissions_type(self):
		with self.assertRaisesRegex(AssertionError, "Permissions must be a dict of list"):
			self.roles.create(self.name, self.tabs, 123)
	
	def test_create_with_unavailable_permissions(self):
		with self.assertRaisesRegex(AssertionError, r"la is not available api. List of all available API: "):
			self.roles.create(self.name, self.tabs, {'la':[1,2,3,4]})

class TestUpdateMethod(unittest.TestCase):

	def setUp(self):
		self.roles = Role(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.old_data = {
			'createdAt': 1234567890,
			'createdBy': 'test',
			'id': 'role_id',
			'name': 'old_name',
			'permissions': [{
				'api': 'roles',
				'create': True,
				'delete': True,
				'id': 'permission_id',
				'read': True,
				'update': True,
				'version': 1}
			],
			'tabs': ['overview'],
			'updatedAt': 1234567890,
			'updatedBy': 'test',
			'version': 1
		}
		self.new_name = 'test'
		self.new_tabs = ['overview']
		self.new_permissions = {'bi':[1,1,0,1]}

	def test_update_request(self):
		self.roles.update(self.old_data, self.new_name, self.new_tabs, self.new_permissions)
		self.roles.root.r.assert_called_with(
			'PUT',
			f'{self.roles.root.url}/api/v1/roles/{self.old_data["id"]}',
			json.dumps({
				"createdAt": 1234567890,
				"createdBy": "test",
				"updatedAt": 1234567890,
				"updatedBy": "test",
				"version": 1,
				"name": "test",
				"tabs": ["overview"],
				"permissions": [{
					"api": "bi",
					"name": "",
					"tabs": ["overview"],
					"create": True,
					"read": True,
					"update": False,
					"delete": True
				}]
			}),
			headers=None,
			verify=self.roles.root.verify
		)

	def test_update_with_incorrect_raw_old_type(self):
		with self.assertRaisesRegex(AssertionError, 'Raw old data must be a dict'):
			self.roles.update(123,self.new_name, self.new_tabs, self.new_permissions)

	def test_update_with_empty_raw_old_data(self):
		with self.assertRaisesRegex(AssertionError, 'Raw old data must not be an empty dictionary'):
			self.roles.update({},self.new_name, self.new_tabs, self.new_permissions)
	
	def test_update_with_incorrect_new_name_type(self):
		with self.assertRaisesRegex(AssertionError, 'Role name must be a string'):
			self.roles.update(self.old_data,123, self.new_tabs, self.new_permissions)
	
	def test_update_with_incorrect_new_tabs_type(self):
		with self.assertRaisesRegex(AssertionError, 'Tabs must be a list'):
			self.roles.update(self.old_data, self.new_name, 123, self.new_permissions)
	
	def test_update_with_incorrect_new_permissions_type(self):
		with self.assertRaisesRegex(AssertionError, 'Permissions must be a dict of list'):
			self.roles.update(self.old_data, self.new_name, self.new_tabs, 123)
	
	def test_update_with_unavailable_tab(self):
		with self.assertRaisesRegex(AssertionError, r"You are using unavailable tabs. List of tabs: "):
			self.roles.update(self.old_data, self.new_name, ['unavailable'], self.new_permissions)
	
	def test_update_with_unavailable_permissions(self):
		with self.assertRaisesRegex(AssertionError, r"la is not available api. List of all available API: "):
			self.roles.update(self.old_data, self.new_name, ['unavailable'], {'la':[1,2,3,4]})