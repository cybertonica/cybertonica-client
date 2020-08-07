from CybertonicaAPI.geo import Geo
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitGeoClass(unittest.TestCase):

	def setUp(self):
		self.geo = Geo(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.geo, Geo)
		self.assertTrue("get" in dir(self.geo))


	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.geo, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.geo.root, object)


class TestGetIpMethod(unittest.TestCase):

	def setUp(self):
		self.geo = Geo(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.ip = '8.8.8.8'

	def test_get_request(self):
		self.geo.get(self.ip)
		self.geo.root.r.assert_called_with(
			'GET',
			f'{self.geo.root.url}/api/v1.2/geo/ip/{self.ip}',
			body=None,
			headers=None,
			verify=self.geo.root.verify
		)

	def test_get_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The IP must be a string'):
			self.geo.get(None)
	
	def test_get_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The IP must not be an empty string'):
			self.geo.get('')