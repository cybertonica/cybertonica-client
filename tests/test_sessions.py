from CybertonicaAPI.sessions import Session
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())

class TestInitSessionClass(unittest.TestCase):

	def setUp(self):
		self.session = Session(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.session, Session)

		self.assertTrue("get_all" in dir(self.session))
		self.assertTrue("get_all_permissions" in dir(self.session))
		self.assertTrue("refresh" in dir(self.session))

	def test_attributes_inside_queue_object(self):
		self.assertTrue(hasattr(self.session, 'root'))

	def test_types_of_fields_inside_queue_object(self):
		self.assertIsInstance(self.session.root, object)

class TestGetAllMethod(unittest.TestCase):

	def setUp(self):
		self.session = Session(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_all_request(self):
		self.session.get_all()
		self.session.root.r.assert_called_with(
			'GET',
			f'{self.session.root.url}/api/v1/sessions',
			body=None,
			headers=None,
			verify=self.session.root.verify
		)

class TestGetAllPermissionsMethod(unittest.TestCase):

	def setUp(self):
		self.session = Session(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_all_permissions_request(self):
		self.session.get_all_permissions()
		self.session.root.r.assert_called_with(
			'GET',
			f'{self.session.root.url}/api/v1/sessions/permissions',
			body=None,
			headers=None,
			verify=self.session.root.verify
		)

class TestRefreshSessionMethod(unittest.TestCase):

	def setUp(self):
		self.session = Session(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_refresh_request(self):
		self.session.refresh()
		self.session.root.r.assert_called_with(
			'GET',
			f'{self.session.root.url}/api/v1/sessions/refresh',
			body=None,
			headers=None,
			verify=self.session.root.verify
		)
	
	def test_refresh_response_tuple(self):
		self.session.root.r = Mock(return_value=(200, {'token': 'new_value'}))
		status, flag = self.session.refresh()
		self.assertEqual(status, 200)
		self.assertTrue(flag)

	def test_refresh_write_token_if_all_ok(self):
		self.session.root.r = Mock(return_value=(200, {'token': 'new_value'}))
		self.session.refresh()
		self.assertEqual(self.session.root.token, 'new_value')

	def test_refresh_should_not_write_token_if_error(self):
		self.session.root.r = Mock(return_value=(400, {'token': 'new_value'}))
		self.session.refresh()
		self.assertEqual(self.session.root.token, 'old_value')
	
	def test_refresh_should_not_write_token_if_token_not_exist(self):
		self.session.root.r = Mock(return_value=(200, {'abc': 'value'}))
		self.session.refresh()
		self.assertEqual(self.session.root.token, 'old_value')
	
	def test_refresh_should_not_write_token_if_bad_response_type(self):
		self.session.root.r = Mock(return_value=(200, 123))
		self.session.refresh()
		self.assertEqual(self.session.root.token, 'old_value')

