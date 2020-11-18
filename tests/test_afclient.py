from CybertonicaAPI.afclient import AFClient
from CybertonicaAPI.af_generator import GeneratorEvents
from CybertonicaAPI.af_auditor import AFCheckProtocol
import os
import sys
import unittest
from unittest.mock import patch, PropertyMock, MagicMock

sys.path.append(os.getcwd())


class TestInitAFClient(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.root = PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			af_version='v2.2'
			)
		cls.client = AFClient(cls.root)

	def test_client_object_creation(self):
		self.assertIsInstance(self.client, AFClient)
		self.assertTrue("create" in dir(self.client))
		self.assertTrue("update" in dir(self.client))
		self.assertFalse("__create_signature" in dir(self.client))
		self.assertFalse("__create_headers" in dir(self.client))
		self.assertFalse("__create_url" in dir(self.client))
		self.assertFalse("__create_url_for_update" in dir(self.client))


	def test_attributes_inside_client_object(self):
		self.assertTrue(hasattr(self.client, 'root'))
		self.assertTrue(hasattr(self.client, 'box'))
		self.assertTrue(hasattr(self.client, 'auditor'))

	def test_types_of_fields_inside_client_object(self):
		self.assertIsInstance(self.client.root, object)
		self.assertIsInstance(self.client.box, object)
		self.assertIsInstance(self.client.auditor, object)

	def test_values_of_fields_inside_client_object(self):
		self.assertEqual(self.client.root, self.root)

if __name__ == "__main__":
	unittest.main()