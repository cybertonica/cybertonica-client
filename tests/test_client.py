from CybertonicaAPI import client
import os
import sys
import unittest
from unittest.mock import patch, PropertyMock

sys.path.append(os.getcwd())


class TestInitClient(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.client = client.Client(
			url='https://test.com',
			team='test',
			api_key='test')

	def test_client_object_creation(self):
		self.assertIsInstance(self.client, client.Client)
		self.assertTrue("r" in dir(self.client))
		self.assertFalse("__create_headers" in dir(self.client))

	def test_attributes_inside_client_object(self):
		self.assertTrue(hasattr(self.client, 'url'))
		self.assertTrue(hasattr(self.client, 'verify'))
		self.assertTrue(hasattr(self.client, 'token'))
		self.assertTrue(hasattr(self.client, 'team'))
		self.assertTrue(hasattr(self.client, 'signature'))
		self.assertTrue(hasattr(self.client, 'dev_mode'))
		self.assertTrue(hasattr(self.client, 'auth'))
		self.assertTrue(hasattr(self.client, 'subchannels'))
		self.assertTrue(hasattr(self.client, 'lists'))
		self.assertTrue(hasattr(self.client, 'users'))
		self.assertTrue(hasattr(self.client, 'channels'))
		self.assertTrue(hasattr(self.client, 'policies'))
		self.assertTrue(hasattr(self.client, 'roles'))
		self.assertTrue(hasattr(self.client, 'abtests'))

	def test_types_of_fields_inside_client_object(self):
		self.assertIsInstance(self.client.url, str)
		self.assertIsInstance(self.client.verify, bool)
		self.assertIsInstance(self.client.token, str)
		self.assertIsInstance(self.client.team, str)
		self.assertIsInstance(self.client.signature, str)
		self.assertIsInstance(self.client.auth, object)
		self.assertIsInstance(self.client.subchannels, object)
		self.assertIsInstance(self.client.lists, object)
		self.assertIsInstance(self.client.users, object)
		self.assertIsInstance(self.client.policies, object)
		self.assertIsInstance(self.client.roles, object)
		self.assertIsInstance(self.client.channels, object)
		self.assertIsInstance(self.client.abtests, object)

	def test_values_of_fields_inside_client_object(self):
		self.assertEqual(self.client.url, 'https://test.com')
		self.assertEqual(self.client.verify, False)
		self.assertEqual(self.client.token, '')
		self.assertEqual(self.client.team, 'test')
		self.assertEqual(self.client.signature, 'test')
		self.assertFalse(self.client.dev_mode)


class TestBadInitClient(unittest.TestCase):

	def test_init_client_without_required_params(self):
		with self.assertRaisesRegex(AssertionError, 'url is required parameter'):
			client.Client()

		with self.assertRaisesRegex(AssertionError, 'team is required parameter'):
			client.Client(url='')

		with self.assertRaisesRegex(AssertionError, 'api_key is required parameter'):
			client.Client(url='', team='')

	def test_init_client_with_incorrect_params(self):
		t = client.Client(url=True, team={}, api_key=list)

		self.assertIsInstance(t.url, str)
		self.assertEqual(t.url, 'True')

		self.assertIsInstance(t.team, str)
		self.assertEqual(t.team, '{}')

		self.assertIsInstance(t.signature, str)
		self.assertEqual(t.signature, "<class 'list'>")


class TestClientRequestWithToMock(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.client = client.Client(
			url='test',
			team='test',
			api_key='test')

	@patch('requests.request', return_value=PropertyMock())
	def test_client_must_use_default_url(self, mock):
		self.client.r('test_method', '', 'test_body',
					  {'test': 'test'}, 'test_files', True)

		mock.assert_called_with(method='test_method', url=self.client.url,
								data='test_body', headers={'test': 'test'},
								files='test_files', verify=True)

	@patch('requests.request', return_value=PropertyMock())
	def test_request_to_server_with_all_params(self, mock):
		self.client.r('test_method', 'test_url', 'test_body',
					  {'test_headers': 'test'}, 'test_files', True)

		mock.assert_called_with(method='test_method', url='test_url',
								data='test_body', headers={'test_headers': 'test'},
								files='test_files', verify=True)

	@patch('requests.request', return_value=PropertyMock())
	def test_request_to_server_without_headers(self, mock):
		self.client.r(method='test_method', url='test_url', body='test_body',
					  headers=None, files='test_files', verify=True)

		expected_headers = {
			'content-type': 'application/json;charset=utf-8',
			'apiUserId': 'test',
			'apiSignature': 'test',
			'Connection': 'keep-alive',
			'Authorization': 'Bearer '
		}
		mock.assert_called_with(method='test_method', url='test_url',
								data='test_body', headers=expected_headers,
								files='test_files', verify=True)

	@patch('requests.request', return_value=PropertyMock(
		status_code=200,
		headers={'Content-Type': 'application/json'},
		json=lambda: {"data1": 1, "data2": 2}
	))
	def test_response_processing_from_server_if_json_exist(self, mock):
		status, json = self.client.r(method='test_method', url='test_url', body='test_body',
									 headers=None, files='test_files', verify=True)

		self.assertIsInstance(status, int)
		self.assertEqual(status, 200)

		self.assertIsInstance(json, dict)
		self.assertEqual(json, {"data1": 1, "data2": 2})

	@patch('requests.request', return_value=PropertyMock(
		status_code=200,
		headers={'Content-Type': 'text/html'},
		json=lambda: "test"
	))
	def test_response_processing_from_server_if_json_not_exist(self, mock):
		status, json = self.client.r(method='test_method', url='test_url', body='test_body',
									 headers=None, files='test_files', verify=True)

		self.assertIsInstance(status, int)
		self.assertEqual(status, 200)

		self.assertEqual(json, None)


class TestClientIncorrectRequestToMock(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.client = client.Client(
			url='test',
			team='test',
			api_key='test')

	def test_request_without_method(self):
		with self.assertRaises(TypeError):
			self.client.r()
		with self.assertRaisesRegex(AssertionError, 'method is required parameter'):
			self.client.r('')
		with self.assertRaisesRegex(AssertionError, 'method is required parameter'):
			self.client.r(None)

	@patch('requests.request', return_value=PropertyMock())
	def test_client_must_check_headers_by_type(self, mock):
		with self.assertRaisesRegex(AssertionError, 'headers must be a dict'):
			self.client.r('test_method', headers='test')

	@patch('requests.request', return_value=PropertyMock())
	def test_client_must_convert_params_to_string_if_necessary(self, mock):
		self.client.r(method=123, url=123, body=123,
					  headers={'test': 'test'}, files='test_files', verify=True)

		mock.assert_called_with(method='123', url='123',
								data='123', headers={'test': 'test'},
								files='test_files', verify=True)


if __name__ == "__main__":
	unittest.main()
