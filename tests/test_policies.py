from CybertonicaAPI.policies import Policy
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitPolicyClass(unittest.TestCase):

	def setUp(self):
		self.policies = Policy(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.policies, Policy)

		self.assertTrue("get_all" in dir(self.policies))
		self.assertTrue("get_by_id" in dir(self.policies))
		self.assertTrue("create" in dir(self.policies))
		self.assertTrue("update" in dir(self.policies))
		self.assertTrue("delete" in dir(self.policies))

	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.policies, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.policies.root, object)

class TestGetAllMethod(unittest.TestCase):

	def setUp(self):
		self.policies = Policy(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_all_request(self):
		self.policies.get_all()
		self.policies.root.r.assert_called_with(
			'GET',
			f'{self.policies.root.url}/api/v1/policies',
			body=None,
			headers=None,
			verify=self.policies.root.verify
		)

class TestGetByIdMethod(unittest.TestCase):

	def setUp(self):
		self.policies = Policy(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_get_by_id_request(self):
		self.policies.get_by_id(self.id)
		self.policies.root.r.assert_called_with(
			'GET',
			f'{self.policies.root.url}/api/v1/policies/{self.id}',
			body=None,
			headers=None,
			verify=self.policies.root.verify
		)

	def test_get_by_id_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.policies.get_by_id(None)
	
	def test_get_by_id_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.policies.get_by_id('')

class TestCreateMethod(unittest.TestCase):

	def setUp(self):
		self.policies = Policy(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.data = {'a': 1, 'b': 2}

	def test_create_request(self):
		self.policies.create(self.data)
		self.policies.root.r.assert_called_with(
			'POST',
			f'{self.policies.root.url}/api/v1/policies',
			json.dumps(self.data),
			headers=None,
			verify=self.policies.root.verify
		)

	def test_create_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.policies.create(123)
	
	def test_create_with_empty_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Policy data must not be an empty dictionary'):
			self.policies.create({})

class TestUpdateMethod(unittest.TestCase):

	def setUp(self):
		self.policies = Policy(PropertyMock(
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
		self.policies.update(self.id, self.data)
		self.policies.root.r.assert_called_with(
			'PUT',
			f'{self.policies.root.url}/api/v1/policies/{self.id}',
			json.dumps(self.data),
			headers=None,
			verify=self.policies.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.policies.update(123,self.data)
	
	def test_update_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.policies.update(self.id,123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.policies.update('',self.data)
	
	def test_update_with_empty_data_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Policy data must not be an empty dictionary'):
			self.policies.update(self.id,{})

class TestDeleteMethod(unittest.TestCase):

	def setUp(self):
		self.policies = Policy(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_delete_request(self):
		self.policies.delete(self.id)
		self.policies.root.r.assert_called_with(
			'DELETE',
			f'{self.policies.root.url}/api/v1/policies/{self.id}',
			body=None,
			headers=None,
			verify=self.policies.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.policies.delete(123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.policies.delete('')


# class TestLogoutMethod(unittest.TestCase):

#     def setUp(self):
#         self.auth = Auth(PropertyMock(
#             url='test_url',
#             team='test_team',
#             signature='test_signature',
#             token='old_value',
#             verify=True,
#             r=Mock(return_value=(200, {'token': '123'}))
#         ))

#     def test_logout_sends_post_request(self):
#         self.auth.logout()
#         self.assertTrue('POST' in self.auth.root.r.call_args[0])

#     def test_logout_builds_correct_url_and_endpoint(self):
#         expected_url = f'{self.auth.root.url}/api/v1/logout'
#         self.auth.logout()
#         self.assertTrue(expected_url in self.auth.root.r.call_args[0])

#     def test_logout_builds_correct_data(self):
#         self.auth.logout()
#         self.assertTrue(None in self.auth.root.r.call_args[0])

#     def test_logout_builds_correct_headers(self):
#         expected_headers = {
#             "content-type": "application/json",
#             "Authorization": f"Bearer {self.auth.root.token}"}
#         self.auth.logout()
#         self.assertTrue(expected_headers in self.auth.root.r.call_args[0])

#     def test_logout_sends_verify_flag_same_as_in_the_client(self):
#         expected_flag = self.auth.root.verify
#         self.auth.logout()
#         self.assertTrue(expected_flag ==
#                         self.auth.root.r.call_args[-1:][0]['verify'])

#     def test_logout_clears_client_token_if_status_less_400(self):
#         expected_token = ''
#         self.auth.logout()
#         self.assertEqual(self.auth.root.token, expected_token)

#     def test_logout_does_not_clear_client_token_if_status_400_and_more(self):
#         self.auth.root.r = Mock(return_value=(401, {'token': '123'}))
#         expected_token = self.auth.root.token
#         self.auth.logout()
#         self.assertEqual(self.auth.root.token, expected_token)


# class TestRecoveryPasswordMethod(unittest.TestCase):

#     def setUp(self):
#         self.auth = Auth(PropertyMock(
#             url='test_url',
#             team='test_team',
#             signature='test_signature',
#             token='old_value',
#             verify=True,
#             r=Mock(return_value=(200, {'token': '123'}))
#         ))
#         self.test_email = 'test@email.com'

#     def test_recovery_sends_get_request(self):
#         self.auth.recovery_password(self.test_email)
#         self.assertTrue('GET' in self.auth.root.r.call_args[0])

#     def test_recovery_builds_correct_url_and_endpoint(self):
#         expected_url = f'{self.auth.root.url}/api/v1/recovery/request?team={self.auth.root.team}&email={self.test_email}'
#         self.auth.recovery_password(self.test_email)
#         self.assertTrue(expected_url in self.auth.root.r.call_args[0])

#     def test_recovery_builds_correct_data(self):
#         self.auth.recovery_password(self.test_email)
#         self.assertTrue(None in self.auth.root.r.call_args[0])

#     def test_recovery_builds_correct_headers(self):
#         self.auth.recovery_password(self.test_email)
#         expected_headers = {
#             "content-type": "application/json",
#         }
#         self.assertTrue(expected_headers in self.auth.root.r.call_args[0])

#     def test_recovery_sends_verify_flag_same_as_in_the_client(self):
#         self.auth.logout()
#         expected_flag = self.auth.root.verify
#         self.assertTrue(expected_flag ==
#                         self.auth.root.r.call_args[-1:][0]['verify'])


# class TestRegisterMethod(unittest.TestCase):

#     def setUp(self):
#         self.auth = Auth(PropertyMock(
#             url='test_url',
#             team='test_team',
#             signature='test_signature',
#             token='old_value',
#             verify=True,
#             r=Mock(return_value=(200, {'token': '123'}))
#         ))
#         self.user_data = {
#             "email": "test@email.com",
#             "password": "test_password",
#             "team": "test_team",
#             "firstName": "John",
#             "lastName": "Smith",
#             "login": "jsmith"
#         }

#     def test_register_sends_post_request(self):
#         self.auth.register(self.user_data)
#         self.assertTrue('POST' in self.auth.root.r.call_args[0])

#     def test_register_builds_correct_url_and_endpoint(self):
#         expected_url = f'{self.auth.root.url}/api/v1/registration'
#         self.auth.register(self.user_data)
#         self.assertTrue(expected_url in self.auth.root.r.call_args[0])

#     def test_register_builds_correct_data_without_dates(self):
#         self.auth.register(self.user_data)
#         self.user_data['invitedAt'] = 0
#         self.user_data['updatedAt'] = 0
#         expected_data = json.dumps(self.user_data)
#         self.assertTrue(expected_data in self.auth.root.r.call_args[0])

#     def test_register_builds_correct_data_with_invitedAt_field(self):
#         self.user_data['invitedAt'] = 100
#         self.auth.register(self.user_data)
#         self.user_data['updatedAt'] = 0
#         expected_data = json.dumps(self.user_data)
#         self.assertTrue(expected_data in self.auth.root.r.call_args[0])

#     def test_register_builds_correct_data_with_updatedAt_field(self):
#         self.user_data['updatedAt'] = 100
#         self.auth.register(self.user_data)
#         self.user_data['invitedAt'] = 0
#         expected_data = json.dumps(self.user_data)
#         self.assertTrue(expected_data in self.auth.root.r.call_args[0])

#     def test_register_builds_correct_headers(self):
#         expected_headers = {
#             "content-type": "application/json",
#         }
#         self.auth.register(self.user_data)
#         self.assertTrue(expected_headers in self.auth.root.r.call_args[0])

#     def test_register_sends_verify_flag_same_as_in_the_client(self):
#         expected_flag = self.auth.root.verify
#         self.auth.logout()
#         self.assertTrue(expected_flag ==
#                         self.auth.root.r.call_args[-1:][0]['verify'])


# class TestReloginMethod(unittest.TestCase):

#     def setUp(self):
#         self.auth = Auth(PropertyMock(
#             url='test_url',
#             team='test_team',
#             signature='test_signature',
#             token='old_value',
#             verify=True,
#             r=Mock(return_value=(200, {'token': '123'}))
#         ))
#         self.login = 'test_login'
#         self.password = 'test_password'

#     @patch('CybertonicaAPI.auth.Auth.login', return_value=(200, {'token': '123'}))
#     @patch('CybertonicaAPI.auth.Auth.logout', return_value=(200, {'token': '123'}))
#     def test_relogin_called_logout_and_login_once(self, mock_login, mock_logout):
#         self.auth.relogin_as(self.login, self.password)
#         mock_login.assert_called_once()
#         mock_logout.assert_called_once()

#     @patch('CybertonicaAPI.auth.Auth.logout', return_value=(200, {'token': '123'}))
#     @patch('CybertonicaAPI.auth.Auth.login', return_value=(200, {'token': '123'}))
#     def test_relogin_called_login_with_correct_params(self, mock_login, mock_logout):
#         self.auth.relogin_as(self.login, self.password)
#         self.assertTrue(self.login in mock_login.call_args[0])
#         self.assertTrue(self.password in mock_login.call_args[0])
