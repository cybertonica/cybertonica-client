from CybertonicaAPI.af_auditor import AFCheckProtocol
import os
import sys
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestAuditor(unittest.TestCase):

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
		cls.auditor = AFCheckProtocol(cls.root) 
		
	def test_client_object_creation(self):
		self.assertIsInstance(self.auditor, AFCheckProtocol)
		self.assertFalse('__push_create_event' in dir(self.auditor))
		self.assertFalse('__test_v22' in dir(self.auditor))
		self.assertFalse('__test_v21' in dir(self.auditor))
		self.assertTrue('run' in dir(self.auditor))
	
	def test_attributes_inside_client_object(self):
		self.assertTrue(hasattr(self.auditor, 'root'))
		self.assertTrue(hasattr(self.auditor, 'channels'))
		self.assertTrue(hasattr(self.auditor, 'sub_channel'))
		self.assertTrue(hasattr(self.auditor, 'fields'))
		self.assertTrue(hasattr(self.auditor, 'expected_values'))
	
	def test_types_of_fields_inside_client_object(self):
		self.assertIsInstance(self.auditor.root, MagicMock)
		self.assertIsInstance(self.auditor.channels, tuple)
		self.assertIsInstance(self.auditor.sub_channel, str)
		self.assertIsInstance(self.auditor.fields, tuple)
		self.assertIsInstance(self.auditor.expected_values, dict)
	
	def test_values_of_fields_inside_client_object(self):
		self.assertEqual(self.auditor.root, self.root)
		self.assertEqual(self.auditor.channels,(
			'global',
			'session',
			'payment',
			'acquiring',
			'card2card',
			'invoice',
			'p2p_money_transfer',
			'login',
			'access_control_change',
			'email'
		))
		self.assertEqual(self.auditor.sub_channel, 'sys')
		self.assertEqual(self.auditor.fields, ('all','requiered'))
		self.assertEqual(self.auditor.expected_values,{
			'v2.2':{
				'id': '', 
				'channel': '',
				'action': 'ALLOW',
				'score': 0,
				'rules': ['Default'],
				'comments': ['from Default'],
				'tags': [],
				'queues': []
			},
			'v2.1':{
				"action":"ALLOW",
				"reason":"from Default",
				"risk_score":0,
				"rule_score":0,
				"tags":[],
				"tx_id":""
			}
		})