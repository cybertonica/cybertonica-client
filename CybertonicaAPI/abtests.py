import json


class ABTest:
	"""ABTest class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def get_all(self):
		"""Get all tests.

		Method:
				`GET`
		Endpoint:
				`/api/v1/tests`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/tests'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def get_by_id(self, id):
		"""Get ABTest from system by ID.

		Args:
				id: ABTest ID.
		Method:
				`GET`
		Endpoint:
				`/api/v1/tests/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/tests/{id}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def start(self, id):
		"""Start ABTest  by ID.

		Args:
				id: ABTest ID.
		Method:
				`GET`
		Endpoint:
				`/api/v1/tests/start/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/tests/start/{id}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def stop(self, id):
		"""Stop ABTest  by ID.

		Args:
				id: ABTest ID.
		Method:
				`GET`
		Endpoint:
				`/api/v1/tests/start/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/tests/stop/{id}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def create(self, data):
		"""Create ABTest in the system.

		Args:
				data: Dictionary of user data.

		Method:
				`POST`
		Endpoint:
				`/api/v1/tests`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Test data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/tests'
		data = json.dumps(data)
		return self.root.r('POST', url, data, headers=None, verify=self.root.verify)

	def update(self, id, data):
		"""Update ABTest in the system.

		Args:
				id: ABTest ID.
				data: Dictionary of user data.


		Method:
				`PUT`
		Endpoint:
				`/api/v1/tests/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Test data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/tests/{id}'
		data = json.dumps(data)
		return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)

	def delete(self, id):
		"""Delete ABTest from the system.

		Args:
				id: ABTest ID.
		Method:
				`DELETE`
		Endpoint:
				`/api/v1/tests/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/tests/{id}'
		return self.root.r('DELETE', url, body=None, headers=None, verify=self.root.verify)
