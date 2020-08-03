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
			url='test',
			team='test'
			)

	def test_client_object_creation(self):
		self.assertIsInstance(self.client, client.Client)
		self.assertTrue("r" in dir(self.client))
		self.assertFalse("__create_headers" in dir(self.client))
		self.assertFalse("__is_expired_session" in dir(self.client))

	def test_attributes_inside_client_object(self):
		self.assertTrue(hasattr(self.client, 'url'))
		self.assertTrue(hasattr(self.client, 'verify'))
		self.assertTrue(hasattr(self.client, 'token'))
		self.assertTrue(hasattr(self.client, 'team'))
		self.assertTrue(hasattr(self.client, 'login_time'))
		self.assertTrue(hasattr(self.client, 'ttl'))
		self.assertTrue(hasattr(self.client, 'auth'))
		self.assertTrue(hasattr(self.client, 'subchannels'))
		self.assertTrue(hasattr(self.client, 'lists'))
		self.assertTrue(hasattr(self.client, 'users'))
		self.assertTrue(hasattr(self.client, 'channels'))
		self.assertTrue(hasattr(self.client, 'policies'))
		self.assertTrue(hasattr(self.client, 'roles'))
		self.assertTrue(hasattr(self.client, 'abtests'))
		self.assertTrue(hasattr(self.client, 'af'))
		self.assertTrue(hasattr(self.client, 'cases'))
		self.assertTrue(hasattr(self.client, 'settings'))
		self.assertTrue(hasattr(self.client, 'queues'))
		self.assertTrue(hasattr(self.client, 'sessions'))
		self.assertTrue(hasattr(self.client, 'tech'))
		self.assertTrue(hasattr(self.client, 'bi'))
		self.assertTrue(hasattr(self.client, 'schema'))
		self.assertTrue(hasattr(self.client, 'currencies'))
		self.assertTrue(hasattr(self.client, 'geo'))

	def test_types_of_fields_inside_client_object(self):
		self.assertIsInstance(self.client.url, str)
		self.assertIsInstance(self.client.verify, bool)
		self.assertIsInstance(self.client.token, str)
		self.assertIsInstance(self.client.team, str)
		self.assertIsInstance(self.client.login_time, int)
		self.assertIsInstance(self.client.ttl, int)
		self.assertIsInstance(self.client.auth, object)
		self.assertIsInstance(self.client.subchannels, object)
		self.assertIsInstance(self.client.lists, object)
		self.assertIsInstance(self.client.users, object)
		self.assertIsInstance(self.client.policies, object)
		self.assertIsInstance(self.client.roles, object)
		self.assertIsInstance(self.client.channels, object)
		self.assertIsInstance(self.client.abtests, object)
		self.assertIsInstance(self.client.af, object)
		self.assertIsInstance(self.client.cases, object)
		self.assertIsInstance(self.client.settings, object)
		self.assertIsInstance(self.client.queues, object)
		self.assertIsInstance(self.client.sessions, object)
		self.assertIsInstance(self.client.tech, object)
		self.assertIsInstance(self.client.bi, object)
		self.assertIsInstance(self.client.schema, object)
		self.assertIsInstance(self.client.currencies, object)
		self.assertIsInstance(self.client.geo, object)

	def test_values_of_fields_inside_client_object(self):
		self.assertEqual(self.client.url, 'test')
		self.assertEqual(self.client.verify, True)
		self.assertEqual(self.client.token, '')
		self.assertEqual(self.client.team, 'test')
		self.assertEqual(self.client.api_user_id, '')
		self.assertEqual(self.client.api_signature, '')
		self.assertEqual(self.client.login_time, 0)
		self.assertEqual(self.client.ttl, 840)


class TestBadInitClient(unittest.TestCase):

	def test_init_client_without_required_params(self):
		with self.assertRaisesRegex(AssertionError, 'url is required parameter'):
			client.Client()

		with self.assertRaisesRegex(AssertionError, 'team is required parameter'):
			client.Client(url='')
		
	def test_init_client_with_incorrect_params(self):
		with self.assertRaisesRegex(AssertionError, 'url value must be a string'):
			t = client.Client(url=True, team={}, api_key=list)
		
		with self.assertRaisesRegex(AssertionError, 'team value must be a string'):
			t = client.Client(url='test', team={}, api_key=list)
		

		# self.assertIsInstance(t.url, str)
		# self.assertEqual(t.url, 'True')

		# self.assertIsInstance(t.team, str)
		# self.assertEqual(t.team, '{}')


class TestClientRequestWithToMock(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.client = client.Client(
			url='http://test',
			team='test',
		)

	@patch('requests.request', return_value=PropertyMock())
	@patch('CybertonicaAPI.client.BasicAuthToken')
	def test_client_must_use_default_url(self, auth_mock, mock):
		self.client.r('test_method', '', 'test_body',
					  {'test': 'test'}, None, True)

		mock.assert_called_with(method='test_method', url=self.client.url,
								data='test_body', headers={'test': 'test'},
								files=None, verify=True, auth=auth_mock(''))

	@patch('requests.request', return_value=PropertyMock())
	@patch('CybertonicaAPI.client.BasicAuthToken')
	def test_request_to_server_with_all_params(self, auth_mock, mock):
		self.client.r('test_method', 'test_url', 'test_body',
					  {'test_headers': 'test'}, 'test_files', True)

		mock.assert_called_with(method='test_method', url='test_url',
								data='test_body', headers=None,
								files='test_files', verify=True, auth=auth_mock(''))

	@patch('requests.request', return_value=PropertyMock())
	@patch('CybertonicaAPI.client.BasicAuthToken')
	def test_request_to_server_without_headers(self, auth_mock, mock):
		self.client.r(method='test_method', url='test_url', body='test_body',
					  headers=None, files='test_files', verify=True)

		expected_headers = {
			'Content-Type': 'application/json',
			'Connection': 'keep-alive',
			'Authorization': 'Bearer '
		}
		mock.assert_called_with(method='test_method', url='test_url',
								data='test_body', headers=None,
								files='test_files', verify=True, auth=auth_mock(''))

	@patch('requests.request', return_value=PropertyMock(
		status_code=200,
		headers={'Content-Type':'application/json'},
		json=lambda: {"data1": 1, "data2": 2}
	))
	def test_response_processing_from_server_if_json_exist(self, mock):
		status, json = self.client.r(method='test_method', url='test_url', body='test_body',
									 headers=None, files='test_files', verify=True)

		self.assertIsInstance(status, int)
		self.assertEqual(status, 200)

		self.assertIsInstance(json, dict)

	@patch('requests.request', return_value=PropertyMock(
		status_code=200,
		headers={'Content-Type': 'text/html'},
		json=lambda: "test"
	))
	def test_response_processing_from_server_if_json_not_exist(self, mock):
		status, data = self.client.r(method='test_method', url='test_url', body='test_body',
									 headers=None, files='test_files', verify=True)

		self.assertEqual(status, 200)

		self.assertIsInstance(data, unittest.mock.MagicMock)


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


if __name__ == "__main__":
	unittest.main()