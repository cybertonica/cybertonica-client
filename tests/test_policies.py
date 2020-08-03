from CybertonicaAPI.policies import Policy
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitPolicyClass(unittest.TestCase):

	def setUp(self):
		self.policies = Policy(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_client_object_creation(self):
		self.assertIsInstance(self.policies, Policy)

		self.assertTrue("get_all" in dir(self.policies))
		self.assertTrue("get_by_id" in dir(self.policies))
		self.assertTrue("create" in dir(self.policies))
		self.assertTrue("update" in dir(self.policies))
		self.assertTrue("delete" in dir(self.policies))

	def test_attributes_inside_auth_object(self):
		self.assertTrue(hasattr(self.policies, 'root'))

	def test_types_of_fields_inside_auth_object(self):
		self.assertIsInstance(self.policies.root, object)

class TestGetAllMethod(unittest.TestCase):

	def setUp(self):
		self.policies = Policy(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))

	def test_get_all_request(self):
		self.policies.get_all()
		self.policies.root.r.assert_called_with(
			'GET',
			f'{self.policies.root.url}/api/v1/policies',
			body=None,
			headers=None,
			verify=self.policies.root.verify
		)

class TestGetByIdMethod(unittest.TestCase):

	def setUp(self):
		self.policies = Policy(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_get_by_id_request(self):
		self.policies.get_by_id(self.id)
		self.policies.root.r.assert_called_with(
			'GET',
			f'{self.policies.root.url}/api/v1/policies/{self.id}',
			body=None,
			headers=None,
			verify=self.policies.root.verify
		)

	def test_get_by_id_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.policies.get_by_id(None)
	
	def test_get_by_id_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.policies.get_by_id('')

class TestCreateMethod(unittest.TestCase):

	def setUp(self):
		self.policies = Policy(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.data = {'a': 1, 'b': 2}

	def test_create_request(self):
		self.policies.create(self.data)
		self.policies.root.r.assert_called_with(
			'POST',
			f'{self.policies.root.url}/api/v1/policies',
			json.dumps(self.data),
			headers=None,
			verify=self.policies.root.verify
		)

	def test_create_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.policies.create(123)
	
	def test_create_with_empty_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Policy data must not be an empty dictionary'):
			self.policies.create({})

class TestUpdateMethod(unittest.TestCase):

	def setUp(self):
		self.policies = Policy(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'
		self.data = {'a': 1, 'b': 2}

	def test_update_request(self):
		self.policies.update(self.id, self.data)
		self.policies.root.r.assert_called_with(
			'PUT',
			f'{self.policies.root.url}/api/v1/policies/{self.id}',
			json.dumps(self.data),
			headers=None,
			verify=self.policies.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.policies.update(123,self.data)
	
	def test_update_with_incorrect_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The data type must be a dictionary'):
			self.policies.update(self.id,123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.policies.update('',self.data)
	
	def test_update_with_empty_data_dict(self):
		with self.assertRaisesRegex(AssertionError, 'Policy data must not be an empty dictionary'):
			self.policies.update(self.id,{})

class TestDeleteMethod(unittest.TestCase):

	def setUp(self):
		self.policies = Policy(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'token': '123'}))
		))
		self.id = 'test_id'

	def test_delete_request(self):
		self.policies.delete(self.id)
		self.policies.root.r.assert_called_with(
			'DELETE',
			f'{self.policies.root.url}/api/v1/policies/{self.id}',
			body=None,
			headers=None,
			verify=self.policies.root.verify
		)

	def test_update_with_incorrect_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must be a string'):
			self.policies.delete(123)
	
	def test_update_with_empty_id_string(self):
		with self.assertRaisesRegex(AssertionError, 'The ID must not be an empty string'):
			self.policies.delete('')

class TestExecuteMethod(unittest.TestCase):

	def setUp(self):
		self.policies = Policy(PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			r=Mock(return_value=(200, {'policy': '123'}))
		))
		self.channel = "test_channel"
		self.event_id = "event_id"
		self.policy_id = "policy_id"
		self.policy_data = {
			"aggregations": "test",
			"channel": "test",
			"comment": "test",
			"const": {},
			"id": 'test',
			"lastUpdatedAt": 1234567890,
			"lastUpdatedBy": "test",
			"name": "test",
			"parent": "test",
			"rules": "test",
			"services": [],
			"version": 1
		}

	def test_execute_request_with_policy_id(self):
		self.policies.execute(self.channel, self.event_id, policy_id=self.policy_id)
		self.policies.root.r.assert_called_with(
			'POST',
			f'{self.policies.root.url}/api/v1/luarepl/single',
			json.dumps({
				"channel": self.channel,
				"eventId": self.event_id,
				"policy" : {'policy': '123'}

			}),
			headers=None,
			verify=self.policies.root.verify
		)

	def test_execute_request_with_policy_data(self):
		self.policies.execute(self.channel, self.event_id, policy_data=self.policy_data)
		self.policies.root.r.assert_called_with(
			'POST',
			f'{self.policies.root.url}/api/v1/luarepl/single',
			json.dumps({
				"channel": self.channel,
				"eventId": self.event_id,
				"policy" : self.policy_data
			}),
			headers=None,
			verify=self.policies.root.verify
		)
	
	def test_execute_with_incorrect_channel_type(self):
		with self.assertRaisesRegex(AssertionError, 'The channel must be a string'):
			self.policies.execute(123, self.event_id, policy_id=self.policy_id)
	
	def test_execute_with_empty_channel_value(self):
		with self.assertRaisesRegex(AssertionError, 'The channel must not be an empty string'):
			self.policies.execute("", self.event_id, policy_id=self.policy_id)
	
	def test_execute_with_incorrect_event_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The event ID must be a string'):
			self.policies.execute(self.channel, 123, policy_id=self.policy_id)
	
	def test_execute_with_empty_event_id_value(self):
		with self.assertRaisesRegex(AssertionError, 'The event ID must not be an empty string'):
			self.policies.execute(self.channel, "", policy_id=self.policy_id)
	
	def test_execute_with_incorrect_policy_id_type(self):
		with self.assertRaisesRegex(AssertionError, 'The policy ID must be a string'):
			self.policies.execute(self.channel, self.event_id, policy_id=123)
	
	def test_execute_with_incorrect_policy_data_type(self):
		with self.assertRaisesRegex(AssertionError, 'The policy data must be a dict'):
			self.policies.execute(self.channel, self.event_id, policy_data=123)
	
	def test_execute_logic_with_policy_id(self):
		self.policies.get_by_id = Mock(return_value=(200, {'policy': '123'}))
		self.policies.execute(self.channel, self.event_id, policy_id=self.policy_id)
		self.policies.get_by_id.assert_called_with('policy_id')
		self.policies.root.r.assert_called_with(
			'POST',
			f'{self.policies.root.url}/api/v1/luarepl/single', 
			json.dumps({
				"channel": "test_channel",
				"eventId": "event_id",
				"policy": {"policy": "123"}
			}),
			headers=None,
			verify=self.policies.root.verify
		)