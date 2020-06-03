from CybertonicaAPI.lists import Item
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitItemClass(unittest.TestCase):

	def setUp(self):
		self.items = Item(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.items, Item)

		self.assertTrue("get_all" in dir(self.items))
		# self.assertTrue("get_all_alive" in dir(self.items))
		self.assertTrue("get_by_id" in dir(self.items))
		self.assertTrue("create" in dir(self.items))
		self.assertTrue("update" in dir(self.items))
		self.assertTrue("delete" in dir(self.items))

	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.items, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.items.root, object)

class TestGetAllMethod(unittest.TestCase):

	def setUp(self):
		self.items = Item(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.list_id = 'test_id'

	def test_get_all_request(self):
		self.items.get_all(self.list_id)
		self.items.root.r.assert_called_with(
			'GET',
			f'{self.items.root.url}/api/v1/items/{self.list_id}',
			body=None,
			headers=None,
			verify=self.items.root.verify
		)

	def test_get_all_with_incorrect_list_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'List ID must be a string'):
			self.items.get_all(123)
	
	def test_get_all_with_empty_list_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'List ID must not be an empty string'):
			self.items.get_all('')

class TestGetByIDMethod(unittest.TestCase):

	def setUp(self):
		self.items = Item(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.list_id, self.id = 'list_id', 'test_id'

	def test_get_by_id_request(self):
		self.items.get_by_id(self.list_id, self.id)
		self.items.root.r.assert_called_with(
			'GET',
			f'{self.items.root.url}/api/v1/items/{self.list_id}/item/{self.id}',
			body=None,
			headers=None,
			verify=self.items.root.verify
		)

	def test_get_by_id_with_incorrect_list_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'List ID must be a string'):
			self.items.get_by_id(123, self.id)
	
	def test_get_by_id_with_empty_list_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'List ID must not be an empty string'):
			self.items.get_by_id('', self.id)
	
	def test_get_by_id_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.items.get_by_id(self.list_id, 123)
	
	def test_get_by_id_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.items.get_by_id(self.list_id, '')

# class TestGetAllAliveMethod(unittest.TestCase):

# 	def setUp(self):
# 		self.items = Item(PropertyMock(
# 			url='test_url',
# 			team='test_team',
# 			signature='test_signature',
# 			token='old_value',
# 			verify=True,
# 			r=Mock(return_value=(200, {'token': '123'}))
# 		))
# 		self.list_id = 'list_id'

# 	def test_get_all_alive_request(self):
# 		self.items.get_all_alive(self.list_id)
# 		self.items.root.r.assert_called_with(
# 			'GET',
# 			f'{self.items.root.url}/api/v1/items/{self.list_id}/alive',
# 			body=None,
# 			headers=None,
# 			verify=self.items.root.verify
# 		)

# 	def test_get_all_alive_with_incorrect_list_id_type(self):
# 		with self.assertRaisesRegex(AssertionError, 'List ID must be a string'):
# 			self.items.get_all_alive(123)
	
# 	def test_get_all_alive_with_empty_list_id_string(self):
# 		with self.assertRaisesRegex(AssertionError, 'List ID must not be an empty string'):
# 			self.items.get_all_alive('')

class TestCreateMethod(unittest.TestCase):

	def setUp(self):
		self.items = Item(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.list_id = 'test_id'
		self.data = {'a': 1, 'b': 2}

	def test_create_request(self):
		self.items.create(self.list_id, self.data)
		self.items.root.r.assert_called_with(
			'POST',
			f'{self.items.root.url}/api/v1/items/{self.list_id}',
			json.dumps(self.data),
			headers=None,
			verify=self.items.root.verify
		)

	def test_create_with_incorrect_list_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'List ID type must be a string'):
			self.items.create(123, self.data)
	
	def test_create_with_empty_list_id(self):
		with self.assertRaisesRegex(AssertionError, 'List ID must not be an empty'):
			self.items.create('',self.data)

	def test_create_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.items.create(self.list_id, 123)
	
	def test_create_with_empty_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Item data must not be an empty dictionary'):
			self.items.create(self.list_id,{})

class TestUpdateMethod(unittest.TestCase):

	def setUp(self):
		self.items = Item(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.list_id = 'test_id'
		self.id = 'test_id'
		self.data = {'a': 1, 'b': 2}

	def test_update_request(self):
		self.items.update(self.list_id, self.id, self.data)
		self.items.root.r.assert_called_with(
			'PUT',
			f'{self.items.root.url}/api/v1/items/{self.list_id}/{self.id}',
			json.dumps(self.data),
			headers=None,
			verify=self.items.root.verify
		)

	def test_update_with_incorrect_list_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'List ID must be a string'):
			self.items.update(123, self.id, self.data)

	def test_update_with_empty_list_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'List ID must not be an empty string'):
			self.items.update('',self.id, self.data)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.items.update(self.list_id, 123,self.data)

	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.items.update(self.list_id, '',self.data)
	
	def test_update_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.items.update(self.list_id, self.id,123)
	
	def test_update_with_empty_data_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Item data must not be an empty dictionary'):
			self.items.update(self.list_id, self.id,{})

class TestDeleteMethod(unittest.TestCase):

	def setUp(self):
		self.items = Item(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.list_id = 'test_id'
		self.id = 'test_id'

	def test_delete_request(self):
		self.items.delete(self.list_id, self.id)
		self.items.root.r.assert_called_with(
			'DELETE',
			f'{self.items.root.url}/api/v1/items/{self.list_id}/{self.id}',
			body=None,
			headers=None,
			verify=self.items.root.verify
		)

	def test_update_with_incorrect_list_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'List ID must be a string'):
			self.items.delete(123, self.id)
	
	def test_update_with_empty_list_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'List ID must not be an empty string'):
			self.items.delete('', self.id)
	
	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.items.delete(self.list_id, 123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.items.delete(self.list_id, '')