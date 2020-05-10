from CybertonicaAPI.channels import Channel
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())

class TestInitChannelClass(unittest.TestCase):

	def setUp(self):
		self.channels = Channel(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.channels, Channel)

		self.assertTrue("get_all" in dir(self.channels))

	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.channels, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.channels.root, object)

class TestGetAllMethod(unittest.TestCase):

	def setUp(self):
		self.channels = Channel(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_all_request(self):
		self.channels.get_all()
		self.channels.root.r.assert_called_with(
			'GET',
			f'{self.channels.root.url}/api/v1/subChannels/channels',
			body=None,
			headers=None,
			verify=self.channels.root.verify
		)