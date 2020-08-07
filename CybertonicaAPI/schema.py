import json

class Schema:
	"""Schema class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def get_all(self):
		"""Get all schema.

		Method:
				`GET`
		Endpoint:
				`/api/v1.2/schemas`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1.2/schemas'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)
	
	def get_by_id(self, id):
		"""Get schema by ID.

		Method:
				`GET`
		Endpoint:
				`/api/v1.2/schemas/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'
		
		url = f'{self.root.url}/api/v1.2/schemas/{id}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def create(self, data):
		"""Create Schema in the system.

		Args:
				data: Dictionary of Schema data.

		Method:
				`POST`
		Endpoint:
				`/api/v1.2/schemas`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Schema data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1.2/schemas'
		data = json.dumps(data)
		return self.root.r('POST', url, data, headers=None, verify=self.root.verify)

	def update(self, id, data):
		"""Update Schema in the system.

		Args:
				id: Schema ID.
				data: Dictionary of Schema data.

		Method:
				`PUT`
		Endpoint:
				`/api/v1.2/schemas/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Schema data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1.2/schemas/{id}'
		data = json.dumps(data)
		return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)

	def delete(self, id):
		"""Remove Schema from the system.

		Args:
				id: Schema ID.
		Method:
				`DELETE`
		Endpoint:
				`/api/v1.2/Schemas/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1.2/schemas/{id}'
		return self.root.r('DELETE', url, body=None, headers=None, verify=self.root.verify)