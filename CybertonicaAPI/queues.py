import json


class Queue:
	"""Queue class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def get_all(self):
		"""Get all queues.

		Method:
				`GET`
		Endpoint:
				`/api/v1/queues`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/queues'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def delete(self, id):
		"""Delete queue from the system.

		Args:
                id: Queue ID.
		Method:
				`DELETE`
		Endpoint:
				`/api/v1/queues/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/queues/{id}'
		return self.root.r('DELETE', url, body=None, headers=None, verify=self.root.verify)