from CybertonicaAPI.reports import Report
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitReportClass(unittest.TestCase):

	def setUp(self):
		self.reports = Report(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.reports, Report)
		self.assertTrue("send" in dir(self.reports))


	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.reports, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.reports.root, object)


class TestSendMethod(unittest.TestCase):

	def setUp(self):
		self.reports = Report(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_send_request(self):
		self.reports.send('test')
		self.reports.root.r.assert_called_with(
			'POST',
			f'{self.reports.root.url}/api/v1/report/test',
			body=None,
			headers=None,
			verify=self.reports.root.verify
		)

	def test_send_with_report_type(self):
		with self.assertRaisesRegex(AssertionError, 'The kind must be a string'):
			self.reports.send(None)
	
	def test_send_with_empty_kind_string(self):
		with self.assertRaisesRegex(AssertionError, 'The kind must not be an empty string'):
			self.reports.send('')
	
	def test_send_with_unavailable_kind(self):
		with self.assertRaisesRegex(AssertionError, r"q report is not available. List of kinds: "):
			self.reports.send('q')