from CybertonicaAPI.events import Event
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitEventClass(unittest.TestCase):

	def setUp(self):
		self.events = Event(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.events, Event)

		self.assertTrue("get_by_id" in dir(self.events))
		self.assertTrue("get_by_queue" in dir(self.events))


	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.events, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.events.root, object)


class TestGetByIdMethod(unittest.TestCase):

	def setUp(self):
		self.events = Event(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_get_by_id_request(self):
		self.events.get_by_id(self.id)
		self.events.root.r.assert_called_with(
			'GET',
			f'{self.events.root.url}/api/v1/events/{self.id}',
			body=None,
			headers=None,
			verify=self.events.root.verify
		)

	def test_get_by_id_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.events.get_by_id(None)
	
	def test_get_by_id_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.events.get_by_id('')

class TestGetByQueueMethod(unittest.TestCase):

	def setUp(self):
		self.events = Event(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.queue = 'test_queue'
		self.start = 0
		self.limit = 100

	def test_get_by_queue_request(self):
		self.events.get_by_queue(self.queue, self.start, self.limit)
		self.events.root.r.assert_called_with(
			'GET',
			f'{self.events.root.url}/api/v1.1/events/queue/{self.queue}?start={str(self.start)}&limit={str(self.limit)}',
			body=None,
			headers=None,
			verify=self.events.root.verify
		)

	def test_get_by_queue_without_start_and_limit_values(self):
		self.events.get_by_queue(self.queue)
		self.events.root.r.assert_called_with(
			'GET',
			f'{self.events.root.url}/api/v1.1/events/queue/{self.queue}?start={str(0)}&limit={str(100)}',
			body=None,
			headers=None,
			verify=self.events.root.verify
		)

	def test_get_by_queue_with_incorrect_queue_type(self):
		with self.assertRaisesRegex(AssertionError, 'Queue name must be a string'):
			self.events.get_by_queue(123, self.start, self.limit)
	
	def test_get_by_queue_with_empty_queue_string(self):
		with self.assertRaisesRegex(AssertionError, 'Queue name must not be an empty string'):
			self.events.get_by_queue('', self.start, self.limit)
	
	def test_get_by_queue_with_incorrect_start_value_type(self):
		with self.assertRaisesRegex(AssertionError, 'The start value must be an integer'):
			self.events.get_by_queue(self.queue, '12', self.limit)
	
	def test_get_by_queue_with_incorrect_start_value(self):
		with self.assertRaisesRegex(AssertionError, 'The start value must be greater than or equal to 0'):
			self.events.get_by_queue(self.queue, -2, self.limit)
	
	def test_get_by_queue_with_incorrect_limit_value_type(self):
		with self.assertRaisesRegex(AssertionError, 'The limit value must be an integer'):
			self.events.get_by_queue(self.queue, self.start, '200')
	
	def test_get_by_queue_with_incorrect_limit_value(self):
		with self.assertRaisesRegex(AssertionError, "The limit value must be in the range \\(0, 1000]"):
			self.events.get_by_queue(self.queue, self.start, 0)