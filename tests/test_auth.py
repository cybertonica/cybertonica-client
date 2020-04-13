import os, sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())

from CybertonicaAPI.auth   import Auth
from CybertonicaAPI.client import Client

class TestInitAuthClass(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		mock = PropertyMock()
		cls.auth = Auth(mock)
	
	def test_client_object_creation(self):
		self.assertIsInstance(self.auth, Auth)

		self.assertTrue("login" in dir(self.auth))
		self.assertTrue("logout" in dir(self.auth))
		self.assertTrue("relogin_as" in dir(self.auth))
		self.assertTrue("recovery_password" in dir(self.auth))
		self.assertTrue("register" in dir(self.auth))
	
	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.auth, 'root'))
	
	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.auth.root, object)

class TestLoginMethod(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		client = PropertyMock(
			url = 'test_url',
			team = 'test_team',
			signature = 'test_signature',
			token = 'old_value',
			verify=True,
			r = Mock(return_value=(200,{'token':'123'}))
		)
		cls.auth = Auth(client)
	
	def test_login_sends_post_request(self):
		self.auth.login('test_login','test_password')

		self.assertTrue('POST' in self.auth.root.r.call_args[0])
	
	def test_login_builds_correct_url_and_endpoint(self):
		self.auth.login('test_login','test_password')

		expected_url = f'{self.auth.root.url}/api/v1/login'

		self.assertTrue(expected_url in self.auth.root.r.call_args[0])
	
	def test_login_builds_correct_data(self):
		self.auth.login('test_login','test_password')

		expected_json_string = json.dumps({
			"apiUser" : 'test_login',
			"team"    : self.auth.root.team,
			"apiUserKeyHash" : 'test_password'
		})
		self.assertTrue(expected_json_string in self.auth.root.r.call_args[0])
	
	def test_login_builds_correct_headers(self):
		self.auth.login('test_login','test_password')

		expected_headers = {"content-type" : "application/json"}

		self.assertTrue(expected_headers in self.auth.root.r.call_args[0])
	
	def test_login_sends_verify_flag_same_as_in_the_client(self):
		self.auth.login('test_login','test_password')

		expected_flag = self.auth.root.verify

		self.assertTrue(expected_flag == self.auth.root.r.call_args[-1:][0]['verify'])

	def test_login_method_changes_client_token_if_code_is_200(self):
		self.auth.login('test_login','test_password')
		
		self.assertEqual(self.auth.root.token,'123')
	
	def test_login_method_changes_client_token_if_code_is_201(self):
		client = PropertyMock(
			url = 'test_url',
			team = 'test_team',
			signature = 'test_signature',
			token = '',
			verify=True,
			r = Mock(return_value=(201,{'token':'123'}))
		)
		self.auth = Auth(client)
		self.auth.login('test_login','test_password')
		
		self.assertEqual(self.auth.root.token,'123')