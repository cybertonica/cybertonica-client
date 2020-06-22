from CybertonicaAPI.cases import Case
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitCaseClass(unittest.TestCase):

	def setUp(self):
		self.cases = Case(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.cases, Case)

		self.assertTrue("get_all" in dir(self.cases))
		self.assertTrue("create" in dir(self.cases))
		self.assertTrue("update" in dir(self.cases))
		self.assertTrue("delete" in dir(self.cases))

	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.cases, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.cases.root, object)

class TestGetAllMethod(unittest.TestCase):

	def setUp(self):
		self.cases = Case(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_all_request(self):
		self.cases.get_all()
		self.cases.root.r.assert_called_with(
			'GET',
			f'{self.cases.root.url}/api/v1.2/cases',
			body=None,
			headers=None,
			verify=self.cases.root.verify
		)

class TestCreateMethod(unittest.TestCase):

	def setUp(self):
		self.cases = Case(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.data = {'a': 1, 'b': 2}

	def test_create_request(self):
		self.cases.create(self.data)
		self.cases.root.r.assert_called_with(
			'POST',
			f'{self.cases.root.url}/api/v1.2/cases',
			json.dumps(self.data),
			headers=None,
			verify=self.cases.root.verify
		)

	def test_create_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.cases.create(123)
	
	def test_create_with_empty_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Case data must not be an empty dictionary'):
			self.cases.create({})

class TestUpdateMethod(unittest.TestCase):

	def setUp(self):
		self.cases = Case(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'
		self.data = {'a': 1, 'b': 2}

	def test_update_request(self):
		self.cases.update(self.id, self.data)
		self.cases.root.r.assert_called_with(
			'PUT',
			f'{self.cases.root.url}/api/v1.2/cases/{self.id}',
			json.dumps(self.data),
			headers=None,
			verify=self.cases.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.cases.update(123,self.data)
	
	def test_update_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.cases.update(self.id,123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.cases.update('',self.data)
	
	def test_update_with_empty_data_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Case data must not be an empty dictionary'):
			self.cases.update(self.id,{})

class TestDeleteMethod(unittest.TestCase):

	def setUp(self):
		self.cases = Case(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_delete_request(self):
		self.cases.delete(self.id)
		self.cases.root.r.assert_called_with(
			'DELETE',
			f'{self.cases.root.url}/api/v1.2/cases/{self.id}',
			body=None,
			headers=None,
			verify=self.cases.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.cases.delete(123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.cases.delete('')