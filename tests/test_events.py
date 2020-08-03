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
		self.assertTrue("bulk_review" in dir(self.events))
		self.assertTrue("review" in dir(self.events))
		self.assertTrue("search")


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

class TestBulkReviewMethod(unittest.TestCase):

	def setUp(self):
		self.events = Event(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.ids = ['test_1', 'test_2']
		self.comment = "test_comment"
		self.status = "Challenge"

	def test_bulk_review_request(self):
		self.events.bulk_review(self.ids, self.comment, self.status)
		self.events.root.r.assert_called_with(
			'PUT',
			f'{self.events.root.url}/api/v1.2/opStatus/review',
			json.dumps({"ids":self.ids,"comment":self.comment,"status":self.status}),
			headers=None,
			verify=self.events.root.verify
		)
	
	def test_bulk_review_with_incorrect_ids_type(self):
		with self.assertRaisesRegex(AssertionError, "ID list must be a list of string"):
			self.events.bulk_review(('a','b','c'), self.comment, self.status)
	
	def test_bulk_review_with_incorrect_comment_type(self):
		with self.assertRaisesRegex(AssertionError, "Comment value must be a string"):
			self.events.bulk_review(self.ids, 123, self.status)
	
	def test_bulk_review_with_incorrect_status_type(self):
		with self.assertRaisesRegex(AssertionError, "Status value must be a string"):
			self.events.bulk_review(self.ids, self.comment, 123)
	
	def test_bulk_review_with_incorrect_status_value(self):
		with self.assertRaisesRegex(AssertionError, "Status value must be either 'Ok', 'Challenge' or 'Fraud'"):
			self.events.bulk_review(self.ids, self.comment, 'lalala')

class TestSingleReviewMethod(unittest.TestCase):

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
		self.comment = "test_comment"
		self.status = "Challenge"

	def test_single_review_request(self):
		self.events.review(self.id, self.comment, self.status)
		self.events.root.r.assert_called_with(
			'PUT',
			f'{self.events.root.url}/api/v1.2/opStatus/review',
			json.dumps({"ids":[self.id],"comment":self.comment,"status":self.status}),
			headers=None,
			verify=self.events.root.verify
		)

class TestSearchMethod(unittest.TestCase):

	def setUp(self):
		self.events = Event(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.channel = "payment"
		self.sub_channel = "test"
		self.query = "amount > 0"
		self.start = 1595241235974
		self.end = 1596450835974
		self.limit = 10

	def test_search_request(self):
		self.events.search(self.channel, self.sub_channel, self.query, self.start, self.end, self.limit)
		self.events.root.r.assert_called_with(
			'GET',
			f'{self.events.root.url}/api/v1.1/events/search?channel={self.channel}&subChannel={self.sub_channel}&query={self.query}&limit={self.limit}&from={self.start}&to={self.end}',
			body=None,
			headers=None,
			verify=self.events.root.verify
		)
	
	def test_search_request_without_limit_value(self):
		self.events.search(self.channel, self.sub_channel, self.query, self.start, self.end)
		self.events.root.r.assert_called_with(
			'GET',
			f'{self.events.root.url}/api/v1.1/events/search?channel={self.channel}&subChannel={self.sub_channel}&query={self.query}&limit=10&from={self.start}&to={self.end}',
			body=None,
			headers=None,
			verify=self.events.root.verify
		)

	def test_search_with_incorrect_channel_type(self):
		with self.assertRaisesRegex(AssertionError, 'Channel name must be a string'):
			self.events.search(123, self.sub_channel, self.query, self.start, self.end, self.limit)

	def test_search_with_empty_channel(self):
		with self.assertRaisesRegex(AssertionError, 'Channel name must not be an empty string'):
			self.events.search("", self.sub_channel, self.query, self.start, self.end, self.limit)
	
	def test_search_with_incorrect_subchannel_type(self):
		with self.assertRaisesRegex(AssertionError, 'Sub-channel name must be a string'):
			self.events.search(self.channel, 123, self.query, self.start, self.end, self.limit)
	
	def test_search_with_incorrect_query_type(self):
		with self.assertRaisesRegex(AssertionError, 'Query must be a string'):
			self.events.search(self.channel, self.sub_channel, 123, self.start, self.end, self.limit)
	
	def test_search_with_empty_query(self):
		with self.assertRaisesRegex(AssertionError, 'Query must not be an empty string'):
			self.events.search(self.channel, self.sub_channel, "", self.start, self.end, self.limit)
	
	def test_search_with_incorrect_start_type(self):
		with self.assertRaisesRegex(AssertionError, 'Start time must be an integer'):
			self.events.search(self.channel, self.sub_channel, self.query, "123", self.end, self.limit)
		
	def test_search_with_incorrect_end_type(self):
		with self.assertRaisesRegex(AssertionError, 'End time must be an integer'):
			self.events.search(self.channel, self.sub_channel, self.query, self.start, "123", self.limit)
	
	def test_search_with_start_gt_end(self):
		with self.assertRaisesRegex(AssertionError, 'End time must be greater than start time'):
			self.events.search(self.channel, self.sub_channel, self.query, self.end, self.start, self.limit)
	
	def test_search_with_incorrect_limit(self):
		with self.assertRaisesRegex(AssertionError, 'Limit must be an integer'):
			self.events.search(self.channel, self.sub_channel, self.query, self.start, self.end, "123")
	
	def test_search_with_limit_gt_1000(self):
		with self.assertRaisesRegex(AssertionError, 'The range of the limit value is from 1 to 1000'):
			self.events.search(self.channel, self.sub_channel, self.query, self.start, self.end, 1001)
	
	def test_search_with_limit_lt_1(self):
		with self.assertRaisesRegex(AssertionError, 'The range of the limit value is from 1 to 1000'):
			self.events.search(self.channel, self.sub_channel, self.query, self.start, self.end, 0)