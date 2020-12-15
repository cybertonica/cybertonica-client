from CybertonicaAPI.lists import List
import os
import sys
import json
import unittest
import tempfile
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitListClass(unittest.TestCase):

	def setUp(self):
		self.lists = List(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.lists, List)

		self.assertTrue("get_all" in dir(self.lists))
		self.assertTrue("get_by_id" in dir(self.lists))
		self.assertTrue("create" in dir(self.lists))
		self.assertTrue("update" in dir(self.lists))
		self.assertTrue("delete" in dir(self.lists))
		self.assertTrue("import_csv" in dir(self.lists))
		self.assertTrue("export_csv" in dir(self.lists))

	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.lists, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.lists.root, object)

class TestGetAllMethod(unittest.TestCase):

	def setUp(self):
		self.lists = List(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_all_request(self):
		self.lists.get_all()
		self.lists.root.r.assert_called_with(
			'GET',
			f'{self.lists.root.url}/api/v1/lists',
			body=None,
			headers=None,
			verify=self.lists.root.verify
		)

class TestGetByIdMethod(unittest.TestCase):

	def setUp(self):
		self.lists = List(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_get_by_id_request(self):
		self.lists.get_by_id(self.id)
		self.lists.root.r.assert_called_with(
			'GET',
			f'{self.lists.root.url}/api/v1/lists/{self.id}',
			body=None,
			headers=None,
			verify=self.lists.root.verify
		)

	def test_get_by_id_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.lists.get_by_id(None)
	
	def test_get_by_id_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.lists.get_by_id('')

class TestGetKindListsMethod(unittest.TestCase):

	def setUp(self):
		self.lists = List(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_kinds_request(self):
		self.lists.kinds()
		self.lists.root.r.assert_called_with(
			'GET',
			f'{self.lists.root.url}/api/v1/kindList',
			body=None,
			headers=None,
			verify=self.lists.root.verify
		)

class TestCreateMethod(unittest.TestCase):

	def setUp(self):
		self.lists = List(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.data = {'a': 1, 'b': 2}

	def test_create_request(self):
		self.lists.create(self.data)
		self.lists.root.r.assert_called_with(
			'POST',
			f'{self.lists.root.url}/api/v1/lists',
			json.dumps(self.data),
			headers=None,
			verify=self.lists.root.verify
		)

	def test_create_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.lists.create(123)
	
	def test_create_with_empty_dict(self):
		with self.assertRaisesRegex(AssertionError, 'List data must not be an empty dictionary'):
			self.lists.create({})

class TestUpdateMethod(unittest.TestCase):

	def setUp(self):
		self.lists = List(PropertyMock(
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
		self.lists.update(self.id, self.data)
		self.lists.root.r.assert_called_with(
			'PUT',
			f'{self.lists.root.url}/api/v1/lists/{self.id}',
			json.dumps(self.data),
			headers=None,
			verify=self.lists.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.lists.update(123,self.data)
	
	def test_update_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.lists.update(self.id,123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.lists.update('',self.data)
	
	def test_update_with_empty_data_dict(self):
		with self.assertRaisesRegex(AssertionError, 'List data must not be an empty dictionary'):
			self.lists.update(self.id,{})

class TestDeleteMethod(unittest.TestCase):

	def setUp(self):
		self.lists = List(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_delete_request(self):
		self.lists.delete(self.id)
		self.lists.root.r.assert_called_with(
			'DELETE',
			f'{self.lists.root.url}/api/v1/lists/{self.id}',
			body=None,
			headers=None,
			verify=self.lists.root.verify
		)

	def test_delete_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.lists.delete(123)
	
	def test_delete_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.lists.delete('')

class TestImportMethod(unittest.TestCase):

	def setUp(self):
		self.lists = List(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='test_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'
		self.filename = tempfile.mktemp(suffix='.csv', prefix='tmp', dir=None)
		self.delimiter = ';'


	
	def test_import_csv_with_incorrect_filename_type(self):
		with self.assertRaisesRegex(AssertionError, 'File name must be a string'):
			self.lists.import_csv(123,'self.id', self.delimiter)

	def test_import_csv_with_incorrect_list_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'List ID must be a string'):
			self.lists.import_csv(filename=self.filename, list_id=123, delimiter= self.delimiter)
	
	def test_import_csv_with_empty_list_id(self):
		with self.assertRaisesRegex(AssertionError, 'List ID must not be an empty string'):
			self.lists.import_csv(filename=self.filename,list_id='', delimiter= self.delimiter)
	
	def test_import_csv_with_incorrect_filename_extension(self):
		with self.assertRaisesRegex(AssertionError, 'The file must have the CSV extension'):
			self.lists.import_csv(filename='./tempfile.txt',list_id=self.id, delimiter= self.delimiter)

	def test_import_csv_with_empty_filename(self):
		with self.assertRaisesRegex(AssertionError, 'The file name must not be an empty string'):
			self.lists.import_csv(filename='',list_id=self.id, delimiter=self.delimiter)

	def test_import_csv_with_incorrect_delimiter_type(self):
		with self.assertRaisesRegex(AssertionError, "Delimiter value must be an string"):
			self.lists.import_csv(filename=self.filename, list_id=self.id, delimiter=1)

	def test_import_csv_with_wrong_delimiter(self):
		with self.assertRaisesRegex(AssertionError, "Wrong delimiter"):
			self.lists.import_csv(filename='./tempfile.csv', list_id=self.id, delimiter=',')

class TestExportMethod(unittest.TestCase):

	def setUp(self):
		self.lists = List(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='test_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'
		self.filename = tempfile.mktemp(suffix='.csv', prefix='tmp', dir=None)
	
	def test_export_csv_with_incorrect_filename_type(self):
		with self.assertRaisesRegex(AssertionError, 'File name must be a string'):
			self.lists.export_csv(123,'self.id')

	def test_export_csv_with_incorrect_list_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'List ID must be a string'):
			self.lists.export_csv(self.filename,123)
	
	def test_export_csv_with_empty_list_id(self):
		with self.assertRaisesRegex(AssertionError, 'List ID must not be an empty string'):
			self.lists.export_csv(self.filename,'')
	
	def test_export_csv_with_incorrect_filename_extension(self):
		with self.assertRaisesRegex(AssertionError, 'The file must have the CSV extension'):
			self.lists.export_csv('./tempfile.txt',self.id)

	def test_export_csv_with_empty_filename(self):
		with self.assertRaisesRegex(AssertionError, 'The file name must not be an empty string'):
			self.lists.export_csv('',self.id)
