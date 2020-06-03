from CybertonicaAPI.abtests import ABTest
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitABTestClass(unittest.TestCase):

	def setUp(self):
		self.abtests = ABTest(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.abtests, ABTest)

		self.assertTrue("get_all" in dir(self.abtests))
		self.assertTrue("get_by_id" in dir(self.abtests))
		self.assertTrue("start" in dir(self.abtests))
		self.assertTrue("stop" in dir(self.abtests))
		self.assertTrue("create" in dir(self.abtests))
		self.assertTrue("update" in dir(self.abtests))
		self.assertTrue("delete" in dir(self.abtests))
		

	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.abtests, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.abtests.root, object)

class TestGetAllMethod(unittest.TestCase):

	def setUp(self):
		self.abtests = ABTest(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_all_request(self):
		self.abtests.get_all()
		self.abtests.root.r.assert_called_with(
			'GET',
			f'{self.abtests.root.url}/api/v1/tests',
			body=None,
			headers=None,
			verify=self.abtests.root.verify
		)

class TestGetByIdMethod(unittest.TestCase):

	def setUp(self):
		self.abtests = ABTest(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_get_by_id_request(self):
		self.abtests.get_by_id(self.id)
		self.abtests.root.r.assert_called_with(
			'GET',
			f'{self.abtests.root.url}/api/v1/tests/{self.id}',
			body=None,
			headers=None,
			verify=self.abtests.root.verify
		)

	def test_get_by_id_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.abtests.get_by_id(None)
	
	def test_get_by_id_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.abtests.get_by_id('')

class TestStartTestMethod(unittest.TestCase):

	def setUp(self):
		self.abtests = ABTest(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_start_request(self):
		self.abtests.start(self.id)
		self.abtests.root.r.assert_called_with(
			'GET',
			f'{self.abtests.root.url}/api/v1/tests/start/{self.id}',
			body=None,
			headers=None,
			verify=self.abtests.root.verify
		)

	def test_start_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.abtests.start(None)
	
	def test_start_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.abtests.start('')

class TestStopTestMethod(unittest.TestCase):

	def setUp(self):
		self.abtests = ABTest(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_stop_request(self):
		self.abtests.stop(self.id)
		self.abtests.root.r.assert_called_with(
			'GET',
			f'{self.abtests.root.url}/api/v1/tests/stop/{self.id}',
			body=None,
			headers=None,
			verify=self.abtests.root.verify
		)

	def test_stop_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.abtests.stop(None)
	
	def test_stop_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.abtests.stop('')

class TestCreateMethod(unittest.TestCase):

	def setUp(self):
		self.abtests = ABTest(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.data = {'a': 1, 'b': 2}

	def test_create_request(self):
		self.abtests.create(self.data)
		self.abtests.root.r.assert_called_with(
			'POST',
			f'{self.abtests.root.url}/api/v1/tests',
			json.dumps(self.data),
			headers=None,
			verify=self.abtests.root.verify
		)

	def test_create_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.abtests.create(123)
	
	def test_create_with_empty_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Test data must not be an empty dictionary'):
			self.abtests.create({})

class TestUpdateMethod(unittest.TestCase):

	def setUp(self):
		self.abtests = ABTest(PropertyMock(
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
		self.abtests.update(self.id, self.data)
		self.abtests.root.r.assert_called_with(
			'PUT',
			f'{self.abtests.root.url}/api/v1/tests/{self.id}',
			json.dumps(self.data),
			headers=None,
			verify=self.abtests.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.abtests.update(123,self.data)
	
	def test_update_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.abtests.update(self.id,123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.abtests.update('',self.data)
	
	def test_update_with_empty_data_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Test data must not be an empty dictionary'):
			self.abtests.update(self.id,{})

class TestDeleteMethod(unittest.TestCase):

	def setUp(self):
		self.abtests = ABTest(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_delete_request(self):
		self.abtests.delete(self.id)
		self.abtests.root.r.assert_called_with(
			'DELETE',
			f'{self.abtests.root.url}/api/v1/tests/{self.id}',
			body=None,
			headers=None,
			verify=self.abtests.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.abtests.delete(123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.abtests.delete('')