from CybertonicaAPI.users import User
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitUserClass(unittest.TestCase):

	def setUp(self):
		self.users = User(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.users, User)

		self.assertTrue("get_all" in dir(self.users))
		self.assertTrue("get_by_id" in dir(self.users))
		self.assertTrue("create" in dir(self.users))
		self.assertTrue("update" in dir(self.users))
		self.assertTrue("delete" in dir(self.users))
		self.assertTrue("remove_role" in dir(self.users))
		self.assertTrue("remove_role" in dir(self.users))

	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.users, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.users.root, object)

class TestGetAllMethod(unittest.TestCase):

	def setUp(self):
		self.users = User(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_all_request(self):
		self.users.get_all()
		self.users.root.r.assert_called_with(
			'GET',
			f'{self.users.root.url}/api/v1/users',
			body=None,
			headers=None,
			verify=self.users.root.verify
		)

class TestGetByIdMethod(unittest.TestCase):

	def setUp(self):
		self.users = User(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_get_by_id_request(self):
		self.users.get_by_id(self.id)
		self.users.root.r.assert_called_with(
			'GET',
			f'{self.users.root.url}/api/v1/users/{self.id}',
			body=None,
			headers=None,
			verify=self.users.root.verify
		)

	def test_get_by_id_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.users.get_by_id(None)
	
	def test_get_by_id_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.users.get_by_id('')

class TestCreateMethod(unittest.TestCase):

	def setUp(self):
		self.users = User(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.data = {'a': 1, 'b': 2}

	def test_create_request(self):
		self.users.create(self.data)
		self.users.root.r.assert_called_with(
			'POST',
			f'{self.users.root.url}/api/v1/users',
			json.dumps(self.data),
			headers=None,
			verify=self.users.root.verify
		)

	def test_create_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.users.create(123)
	
	def test_create_with_empty_dict(self):
		with self.assertRaisesRegex(AssertionError, 'User data must not be an empty dictionary'):
			self.users.create({})

class TestUpdateMethod(unittest.TestCase):

	def setUp(self):
		self.users = User(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'
		self.data = {'a': 1, 'b': 2}

	def test_update_request(self):
		self.users.update(self.id, self.data)
		self.users.root.r.assert_called_with(
			'PUT',
			f'{self.users.root.url}/api/v1/users/{self.id}',
			json.dumps(self.data),
			headers=None,
			verify=self.users.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.users.update(123,self.data)
	
	def test_update_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.users.update(self.id,123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.users.update('',self.data)
	
	def test_update_with_empty_data_dict(self):
		with self.assertRaisesRegex(AssertionError, 'User data must not be an empty dictionary'):
			self.users.update(self.id,{})

class TestDeleteMethod(unittest.TestCase):

	def setUp(self):
		self.users = User(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_delete_request(self):
		self.users.delete(self.id)
		self.users.root.r.assert_called_with(
			'DELETE',
			f'{self.users.root.url}/api/v1/users/{self.id}',
			body=None,
			headers=None,
			verify=self.users.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.users.delete(123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.users.delete('')

class TestAddRoleMethod(unittest.TestCase):

	def setUp(self):
		self.users = User(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'
		self.role = 'my_role'

	@patch('CybertonicaAPI.users.User.get_by_id',
		return_value=(200, {'roles':['a','b']})
	)
	@patch('CybertonicaAPI.users.User.update', return_value=PropertyMock())
	def test_add_role_logic(self, update_mock, get_mock):
		self.users.add_role(self.id, self.role)
		get_mock.assert_called_once()
		update_mock.assert_called_once()

		get_mock.assert_called_with(self.id)
		update_mock.assert_called_with(self.id, {'roles':['a','b','my_role']})

	def test_add_role_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.users.add_role(123, self.role)
	
	def test_add_role_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.users.add_role('', self.role)
	
	def test_add_role_with_incorrect_role_type(self):
		with self.assertRaisesRegex(AssertionError, 'Role name must be a string'):
			self.users.add_role(self.id, 123)
	
	def test_add_role_with_empty_role_string(self):
		with self.assertRaisesRegex(AssertionError, 'Role name must not be an empty string'):
			self.users.add_role(self.id, '')
	
	@patch('CybertonicaAPI.users.User.get_by_id',
		return_value=(1, None)
	)
	def test_add_role_get_by_id_return_not_200_status(self, get_mock):
		with self.assertRaisesRegex(AssertionError, 'The user data request was not successful'):
			self.users.add_role(self.id,self.role)
	
	@patch('CybertonicaAPI.users.User.get_by_id',
		return_value=(200, None)
	)
	def test_add_role_get_by_id_return_none_data(self, get_mock):
		with self.assertRaisesRegex(AssertionError, 'The user data type does not match the dictionary'):
			self.users.add_role(self.id,self.role)
	
	@patch('CybertonicaAPI.users.User.get_by_id',
		return_value=(200, {'a':1})
	)
	def test_add_role_get_by_id_return_dict_without_roles_key(self, get_mock):
		with self.assertRaisesRegex(AssertionError, 'The data structure does not contain the roles key'):
			self.users.add_role(self.id,self.role)
	
	@patch('CybertonicaAPI.users.User.get_by_id',
		return_value=(200, {'a':1, "roles":['my_role']})
	)
	def test_add_role_already_has_target_role(self, get_mock):
		with self.assertRaisesRegex(AssertionError, 'The user already has a role'):
			self.users.add_role(self.id,self.role)


class TestRemoveRoleMethod(unittest.TestCase):

	def setUp(self):
		self.users = User(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'
		self.role = 'my_role'

	@patch('CybertonicaAPI.users.User.get_by_id',
		return_value=(200, {'roles':['a','b','my_role']})
	)
	@patch('CybertonicaAPI.users.User.update', return_value=PropertyMock())
	def test_remove_role_logic(self, update_mock, get_mock):
		self.users.remove_role(self.id, self.role)
		get_mock.assert_called_once()
		update_mock.assert_called_once()

		get_mock.assert_called_with(self.id)
		update_mock.assert_called_with(self.id, {'roles':['a','b']})

	def test_remove_role_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.users.remove_role(123, self.role)
	
	def test_remove_role_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.users.remove_role('', self.role)
	
	def test_remove_role_with_incorrect_role_type(self):
		with self.assertRaisesRegex(AssertionError, 'Role name must be a string'):
			self.users.remove_role(self.id, 123)
	
	def test_remove_role_with_empty_role_string(self):
		with self.assertRaisesRegex(AssertionError, 'Role name must not be an empty string'):
			self.users.remove_role(self.id, '')
	
	@patch('CybertonicaAPI.users.User.get_by_id',
		return_value=(1, None)
	)
	def test_remove_role_get_by_id_return_not_200_status(self, get_mock):
		with self.assertRaisesRegex(AssertionError, 'The user data request was not successful'):
			self.users.remove_role(self.id,self.role)
	
	@patch('CybertonicaAPI.users.User.get_by_id',
		return_value=(200, None)
	)
	def test_remove_role_get_by_id_return_none_data(self, get_mock):
		with self.assertRaisesRegex(AssertionError, 'The user data type does not match the dictionary'):
			self.users.remove_role(self.id,self.role)
	
	@patch('CybertonicaAPI.users.User.get_by_id',
		return_value=(200, {'a':1})
	)
	def test_remove_role_get_by_id_return_dict_without_roles_key(self, get_mock):
		with self.assertRaisesRegex(AssertionError, 'The data structure does not contain the roles key'):
			self.users.remove_role(self.id,self.role)
	
	@patch('CybertonicaAPI.users.User.get_by_id',
		return_value=(200, {'a':1, "roles":['a']})
	)
	def test_remove_role_already_has_not_target_role(self, get_mock):
		with self.assertRaisesRegex(AssertionError, 'The user already has not a role'):
			self.users.remove_role(self.id,self.role)