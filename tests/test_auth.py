from CybertonicaAPI.auth import Auth
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitAuthClass(unittest.TestCase):

	def setUp(self):
		self.auth = Auth(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.auth, Auth)

		self.assertTrue("login" in dir(self.auth))
		self.assertTrue("logout" in dir(self.auth))
		self.assertTrue("recovery_password" in dir(self.auth))
		self.assertTrue("register" in dir(self.auth))

	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.auth, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.auth.root, object)


class TestLoginMethod(unittest.TestCase):

	def setUp(self):
		self.auth = Auth(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.login = 'test_login'
		self.password = 'test_password'

		self.data = {
			"apiUser": self.login,
			"team": self.auth.root.team,
			"apiUserKeyHash": self.password
		}
		self.headers = {"content-type": "application/json"}

	def test_login_request(self):

		self.auth.login(self.login, self.password)
		self.auth.root.r.assert_called_with(
			'POST',
			f'{self.auth.root.url}/api/v1/login',
			json.dumps(self.data),
			self.headers,
			verify=self.auth.root.verify
		)

	def test_login_method_changes_client_token_if_code_is_200(self):
		self.auth.login(self.login, self.password)
		self.assertEqual(self.auth.root.token, '123')

	def test_login_method_changes_client_token_if_code_is_201(self):
		self.auth.root.r = Mock(return_value=(201, {'token': '123'}))
		self.auth.login(self.login, self.password)
		self.assertEqual(self.auth.root.token, '123')

	def test_login_method_does_not_change_client_token_if_code_is_not_200_201(self):
		self.auth.root.r = Mock(return_value=(401, {'token': '123'}))
		expected_token = self.auth.root.token
		self.auth.login(self.login, self.password)
		self.assertEqual(self.auth.root.token, expected_token)
	
	def test_login_with_incorrect_apiuser_type(self):
		with self.assertRaisesRegex(AssertionError, 'The api user must be a string'):
			self.auth.login(123, self.password)
	
	def test_login_with_incorrect_apiuserhash_type(self):
		with self.assertRaisesRegex(AssertionError, 'The api user key hash must be a string'):
			self.auth.login(self.login, 123)
	
	def test_login_with_empty_apiuser_string(self):
		with self.assertRaisesRegex(AssertionError, 'The api user must not be an empty string'):
			self.auth.login('', self.password)
	
	def test_login_with_empty_apiuserhash_string(self):
		with self.assertRaisesRegex(AssertionError, 'The api user key hash must not be an empty string'):
			self.auth.login(self.login, '')


class TestLogoutMethod(unittest.TestCase):

	def setUp(self):
		self.auth = Auth(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.auth.root.token}"
			}

	def test_logout_request(self):
		self.auth.logout()
		self.auth.root.r.assert_called_with(
			'POST',
			f'{self.auth.root.url}/api/v1/logout',
			self.headers,
			body=None,
			verify=self.auth.root.verify
		)

	def test_logout_clears_client_token_if_status_less_400(self):
		self.auth.logout()
		self.assertEqual(self.auth.root.token, '')

	def test_logout_does_not_clear_client_token_if_status_400_and_more(self):
		self.auth.root.r = Mock(return_value=(401, {'token': '123'}))
		expected_token = self.auth.root.token
		self.auth.logout()
		self.assertEqual(self.auth.root.token, expected_token)


class TestRecoveryPasswordMethod(unittest.TestCase):

	def setUp(self):
		self.auth = Auth(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.team = 'test'
		self.email = 'test@email.com'
		self.headers = {"content-type": "application/json"}
	
	def test_recovery_request(self):
		self.auth.recovery_password(self.team, self.email)
		self.auth.root.r.assert_called_with(
			'GET',
			f'{self.auth.root.url}/api/v1/recovery/request?team={self.team}&email={self.email}',
			self.headers,
			body=None,
			verify=self.auth.root.verify
		)
	
	def test_recovery_with_incorrect_team_type(self):
		with self.assertRaisesRegex(AssertionError, 'Team must be a string'):
			self.auth.recovery_password(123, self.email)
	
	def test_recovery_with_incorrect_email_type(self):
		with self.assertRaisesRegex(AssertionError, 'Email must be a string'):
			self.auth.recovery_password(self.team, 123)
	
	def test_recovery_with_empty_team_string(self):
		with self.assertRaisesRegex(AssertionError, 'Team must not be an empty string'):
			self.auth.recovery_password('', self.email)
	
	def test_recovery_with_empty_email_string(self):
		with self.assertRaisesRegex(AssertionError, 'Email must not be an empty string'):
			self.auth.recovery_password(self.team, '')
	
	def test_recovery_with_invalid_email_address(self):
		with self.assertRaisesRegex(AssertionError, 'Email must be valid'):
			self.auth.recovery_password(self.team, 'invalid-email')

class TestRegisterMethod(unittest.TestCase):

	def setUp(self):
		self.auth = Auth(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.user_data_without_times = {
			"email": "test@email.com",
			"password": "test_password",
			"team": "test_team",
			"firstName": "John",
			"lastName": "Smith",
			"login": "jsmith"
		}
		self.user_data_with_times = {
			**self.user_data_without_times,
			**{
				"invitedAt": 0,
				"updatedAt": 0
			}
		}
		self.headers = {"content-type": "application/json"}
	
	def test_register_request_without_times(self):
		self.auth.register(self.user_data_without_times)
		self.auth.root.r.assert_called_with(
			'POST',
			f'{self.auth.root.url}/api/v1/registration',
			json.dumps(self.user_data_with_times),
			self.headers,
			verify=self.auth.root.verify
		)
	
	def test_register_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.auth.register(123)
	
	def test_register_with_empty_dict(self):
		with self.assertRaisesRegex(AssertionError, 'User data must not be an empty dictionary'):
			self.auth.register({})