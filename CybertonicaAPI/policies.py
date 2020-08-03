import json


class Policy:
	"""Policy class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root
		self._policy_keys = set([
			"aggregations", "channel", "comment",
			"const", "id", "name", "parent",
			"rules", "services", "updatedAt", "updatedBy","version",
			"lastUpdatedAt", "lastUpdatedBy"
		])

	def get_all(self):
		"""Get all policies.

		Method:
				`GET`
		Endpoint:
				`/api/v1/policies`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/policies'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def get_by_id(self, id):
		"""Get policy from system by ID.

		Args:
				id: Policy ID.
		Method:
				`GET`
		Endpoint:
				`/api/v1/policies/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/policies/{id}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def create(self, data):
		"""Create policy in the system.

		Args:
				data: Dictionary of user data.

						{
							"aggregations": "test",
							"channel": "test",
							"comment": "test",
							"const": {},
							"name": "test",
							"parent": "test",
							"rules": "test",
							"services": [],
							"version": 1
						}

		Method:
				`POST`
		Endpoint:
				`/api/v1/policies`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Policy data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/policies'
		data = json.dumps(data)
		return self.root.r('POST', url, data, headers=None, verify=self.root.verify)

	def update(self, id, data):
		"""Update list in the system.

		Args:
				id: Policy ID.
				data: Dictionary of user data.

						{
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

		Method:
				`PUT`
		Endpoint:
				`/api/v1/policies/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Policy data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/policies/{id}'
		data = json.dumps(data)
		return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)

	def delete(self, id):
		"""Delete policy from the system.

		Args:
				id: Policy ID.
		Method:
				`DELETE`
		Endpoint:
				`/api/v1/policies/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/policies/{id}'
		return self.root.r('DELETE', url, body=None, headers=None, verify=self.root.verify)
	
	def execute(self, channel, event_id, policy_id = None, policy_data = None):
		"""Execute a rule that is specified via the `policy ID`(implicitly)
			or through the body of the Policy entity(`policy_data`, explicitly) to the event `event_id` of the channel `channel`.

		Args:
				channel: Channel name.
				event_id: Event ID.
				policy_id: Policy ID.
				Policy_data: Policy data.
		Method:
				`POST`
		Endpoint:
				`/api/v1/luarepl/single`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(channel, str), 'The channel must be a string'
		assert channel, 'The channel must not be an empty string'
		assert isinstance(event_id, str), 'The event ID must be a string'
		assert event_id, 'The event ID must not be an empty string'

		data = {
			"channel": channel,
			"eventId": event_id
		}
		if policy_id:
			assert isinstance(policy_id, str), 'The policy ID must be a string'
			_, data["policy"] = self.get_by_id(policy_id)
		else:
			assert isinstance(policy_data, dict), 'The policy data must be a dict'
			assert self._policy_keys >= set(policy_data.keys()),  f'You are using unavailable policy structure. Keys: {self._policy_keys}'
			data["policy"] = policy_data


		url = f'{self.root.url}/api/v1/luarepl/single'
		data = json.dumps(data)
		return self.root.r('POST', url, data, headers=None, verify=self.root.verify)