import json


class Case:
	"""Case class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def get_all(self):
		"""Get all cases.

		Method:
				`GET`
		Endpoint:
				`/api/v1.2/cases`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1.2/cases'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def create(self, data):
		"""Create case in the system.

		Args:
				data: Dictionary of Case data.

		Method:
				`POST`
		Endpoint:
				`/api/v1.2/cases`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Case data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1.2/cases'
		data = json.dumps(data)
		return self.root.r('POST', url, data, headers=None, verify=self.root.verify)

	def update(self, id, data):
		"""Update case in the system.

		Args:
				id: Case ID.
				data: Dictionary of Case data.

		Method:
				`PUT`
		Endpoint:
				`/api/v1.2/cases/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Case data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1.2/cases/{id}'
		data = json.dumps(data)
		return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)

	def delete(self, id):
		"""Remove case from the system.

		Args:
				id: Case ID.
		Method:
				`DELETE`
		Endpoint:
				`/api/v1.2/cases/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1.2/cases/{str(id)}'
		return self.root.r('DELETE', url, body=None, headers=None, verify=self.root.verify)