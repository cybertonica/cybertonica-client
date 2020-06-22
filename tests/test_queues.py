from CybertonicaAPI.queues import Queue
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())

class TestInitQueueClass(unittest.TestCase):

	def setUp(self):
		self.queue = Queue(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.queue, Queue)

		self.assertTrue("get_all" in dir(self.queue))
		self.assertTrue("delete" in dir(self.queue))

	def test_attributes_inside_queue_object(self):
		self.assertTrue(hasattr(self.queue, 'root'))

	def test_types_of_fields_inside_queue_object(self):
		self.assertIsInstance(self.queue.root, object)


class TestGetAllMethod(unittest.TestCase):

	def setUp(self):
		self.queue = Queue(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_all_request(self):
		self.queue.get_all()
		self.queue.root.r.assert_called_with(
			'GET',
			f'{self.queue.root.url}/api/v1/queues',
			body=None,
			headers=None,
			verify=self.queue.root.verify
		)

class TestDeleteMethod(unittest.TestCase):

	def setUp(self):
		self.queue = Queue(PropertyMock(
			url='test_url',
			team='test_team',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_delete_request(self):
		self.queue.delete(self.id)
		self.queue.root.r.assert_called_with(
			'DELETE',
			f'{self.queue.root.url}/api/v1/queues/{self.id}',
			body=None,
			headers=None,
			verify=self.queue.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.queue.delete(123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.queue.delete('')