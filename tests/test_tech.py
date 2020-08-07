from CybertonicaAPI.tech import Tech
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitTechClass(unittest.TestCase):

	def setUp(self):
		self.tech = Tech(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.tech, Tech)

		self.assertTrue("info" in dir(self.tech))
		self.assertTrue("ping" in dir(self.tech))
		
	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.tech, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.tech.root, object)

class TestInfoMethod(unittest.TestCase):

	def setUp(self):
		self.tech = Tech(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_info_request(self):
		self.tech.info()
		self.tech.root.r.assert_called_with(
			'GET',
			f'{self.tech.root.url}/api/v1/info',
			body=None,
			headers=None,
			verify=self.tech.root.verify
		)
class TestPingMethod(unittest.TestCase):

	def setUp(self):
		self.tech = Tech(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_ping_request(self):
		self.tech.ping()
		self.tech.root.r.assert_called_with(
			'GET',
			f'{self.tech.root.url}/api/v1/ping',
			body=None,
			headers=None,
			verify=self.tech.root.verify
		)

class TestPathsMethod(unittest.TestCase):

	def setUp(self):
		self.tech = Tech(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_paths_request(self):
		self.tech.paths()
		self.tech.root.r.assert_called_with(
			'GET',
			f'{self.tech.root.url}/api/v1/paths',
			body=None,
			headers=None,
			verify=self.tech.root.verify
		)