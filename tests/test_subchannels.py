from CybertonicaAPI.subchannels import Subchannel
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitSubchannelClass(unittest.TestCase):

	def setUp(self):
		self.subchannels = Subchannel(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.subchannels, Subchannel)

		self.assertTrue("get_all" in dir(self.subchannels))
		self.assertTrue("get_by_id" in dir(self.subchannels))
		self.assertTrue("create" in dir(self.subchannels))
		self.assertTrue("update" in dir(self.subchannels))
		self.assertTrue("delete" in dir(self.subchannels))
		self.assertTrue("search_by" in dir(self.subchannels))

	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.subchannels, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.subchannels.root, object)

class TestGetAllMethod(unittest.TestCase):

	def setUp(self):
		self.subchannels = Subchannel(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_all_request(self):
		self.subchannels.get_all()
		self.subchannels.root.r.assert_called_with(
			'GET',
			f'{self.subchannels.root.url}/api/v1/subChannels',
			body=None,
			headers=None,
			verify=self.subchannels.root.verify
		)

class TestGetByIdMethod(unittest.TestCase):

	def setUp(self):
		self.subchannels = Subchannel(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_get_by_id_request(self):
		self.subchannels.get_by_id(self.id)
		self.subchannels.root.r.assert_called_with(
			'GET',
			f'{self.subchannels.root.url}/api/v1/subChannels/{self.id}',
			body=None,
			headers=None,
			verify=self.subchannels.root.verify
		)

	def test_get_by_id_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.subchannels.get_by_id(None)
	
	def test_get_by_id_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.subchannels.get_by_id('')

class TestCreateMethod(unittest.TestCase):

	def setUp(self):
		self.subchannels = Subchannel(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.data = {'a': 1, 'b': 2}

	def test_create_request(self):
		self.subchannels.create(self.data)
		self.subchannels.root.r.assert_called_with(
			'POST',
			f'{self.subchannels.root.url}/api/v1/subChannels',
			json.dumps(self.data),
			headers=None,
			verify=self.subchannels.root.verify
		)

	def test_create_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.subchannels.create(123)
	
	def test_create_with_empty_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Subchannel data must not be an empty dictionary'):
			self.subchannels.create({})

class TestUpdateMethod(unittest.TestCase):

	def setUp(self):
		self.subchannels = Subchannel(PropertyMock(
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
		self.subchannels.update(self.id, self.data)
		self.subchannels.root.r.assert_called_with(
			'PUT',
			f'{self.subchannels.root.url}/api/v1/subChannels/{self.id}',
			json.dumps(self.data),
			headers=None,
			verify=self.subchannels.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.subchannels.update(123,self.data)
	
	def test_update_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.subchannels.update(self.id,123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.subchannels.update('',self.data)
	
	def test_update_with_empty_data_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Subchannel data must not be an empty dictionary'):
			self.subchannels.update(self.id,{})

class TestDeleteMethod(unittest.TestCase):

	def setUp(self):
		self.subchannels = Subchannel(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_delete_request(self):
		self.subchannels.delete(self.id)
		self.subchannels.root.r.assert_called_with(
			'DELETE',
			f'{self.subchannels.root.url}/api/v1/subChannels/{self.id}',
			body=None,
			headers=None,
			verify=self.subchannels.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.subchannels.delete(123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.subchannels.delete('')