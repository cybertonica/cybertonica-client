import json


class Subchannel:
	"""Subchannel class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def get_all(self):
		"""Get all subchannels.

		Method:
				`GET`
		Endpoint:
				`/api/v1/subChannels`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/subChannels'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def get_by_id(self, id):
		"""Get subchannel from system by ID.

		Args:
				id: Subchannel ID.
		Method:
				`GET`
		Endpoint:
				`/api/v1/subChannels/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/subChannels/{id}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def search_by(self, key, value):
		"""Search subchannel in the system by `key:value`.

		Calls `CybertonicaAPI.subchannels.Subchannel.get_all` function
				and searches for the specified `key:value`.

		Args:
				key: The key that will be used for searching.
				value: The value that will be used for searching.

		Returns:
				- `CybertonicaAPI.Client.r` If the response from the server is not equal `200`.
				- `(True, channel)` if successful.
				- `(False, None)` in case of failure.
		"""
		status_code, subchannels = self.get_all()
		if status_code >= 400:
			return (status_code, subchannels)

		for channel in subchannels:
			if key in channel:
				if channel[key] == value:
					return (True, channel)
		return (False, None)

	def create(self, data):
		"""Create subchannel in the system.

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
				`/api/v1/subChannels`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Subchannel data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/subChannels'
		data = json.dumps(data)
		return self.root.r('POST', url, data, headers=None, verify=self.root.verify)

	def update(self, id, data):
		"""Update subchannel in the system.

		Args:
				id: Subchannel ID.
				data: Dictionary of user data.

						{
							"channel":"test",
							"comment":"test",
							"createdAt":1234567890,
							"createdBy":"test",
							"id":"test",
							"name":"test",
							"policy":"test",
							"updatedAt":1234567890,
							"updatedBy":"test",
							"version":1
						}

		Method:
				`PUT`
		Endpoint:
				`/api/v1/subChannels/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Subchannel data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/subChannels/{id}'
		data = json.dumps(data)
		return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)

	def delete(self, id):
		"""Remove subchannel from the system.

		Args:
				id: Subchannel ID.
		Method:
				`DELETE`
		Endpoint:
				`/api/v1/subChannels/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/subChannels/{id}'
		return self.root.r('DELETE', url, body=None, headers=None, verify=self.root.verify)
