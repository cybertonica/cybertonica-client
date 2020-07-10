import json
import requests


class List:
	"""List class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root
		self.items = Item(root)

	def get_all(self):
		"""Get all lists.

		Method:
				`GET`
		Endpoint:
				`/api/v1/lists`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/lists'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def get_by_id(self, id):
		"""Get list from system by ID.

		Args:
				id: List ID.
		Method:
				`GET`
		Endpoint:
				`/api/v1/lists/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/lists/{id}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)
	
	def kinds(self):
		"""Get kinds of list from system.

		Method:
				`GET`
		Endpoint:
				`/api/v1/kindList`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/kindList'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def create(self, data):
		"""Create list in the system.

		Args:
				data: Dictionary of user data.

						{
							'name': "name",
							'kind': "WHITE"
						}

		Method:
				`POST`
		Endpoint:
				`/api/v1/lists`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'List data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/lists'
		data = json.dumps(data)
		return self.root.r('POST', url, data, headers=None, verify=self.root.verify)

	def update(self, id, data):
		"""Update list in the system.

		Args:
				data: Dictionary of user data.

						{
							'createdAt': '<time>',
							'createdBy': "test",
							'id': '<id>',
							'name': "test",
							'kind': "WHITE",
							'size': 0
						}

		Method:
				`PUT`
		Endpoint:
				`/api/v1/lists/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'List data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/lists/{id}'
		data = json.dumps(data)
		return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)

	def delete(self, id):
		"""Delete list from the system.

		Args:
				id: List ID.
		Method:
				`DELETE`
		Endpoint:
				`/api/v1/lists/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/lists/{id}'
		return self.root.r('DELETE', url, body=None, headers=None, verify=self.root.verify)

	def import_csv(self, filename, list_id):
		"""Import CSV file to the list.

		Args:
				filename: CSV file name or full path (use pwd)
				list_id: The ID of the list.
		Method:
				`POST`
		Endpoint:
				`/api/v1/items/{list_id}/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(filename, str), "File name must be a string"
		assert filename, "The file name must not be an empty string"
		assert '.csv' in filename, "The file must have the CSV extension"
		assert isinstance(list_id, str), "List ID must be a string"
		assert list_id, "List ID must not be an empty string"

		files = {
			'files': open(filename, 'rb')
		}
		url = f'{self.root.url}/api/v1/lists/import/{list_id}/csv'
		return self.root.r('POST', url, body=None, headers=None, verify=self.root.verify, files=files)
	
	def export_csv(self, filename, list_id):
		"""Export CSV file to the list.

		Args:
				filename: CSV file name or full path (use pwd)
				list_id: The ID of the list.
		Method:
				`GET`
		Endpoint:
				`/api/v1/lists/export/{list_id}/csv`
		Returns:
				Tuple (status, info), where status is the response state;
					info is information about the exception error,
					or `0` if the process was successful.
		"""
		assert isinstance(filename, str), "File name must be a string"
		assert filename, "The file name must not be an empty string"
		assert '.csv' in filename, "The file must have the CSV extension"
		assert isinstance(list_id, str), "List ID must be a string"
		assert list_id, "List ID must not be an empty string"
		
		try:
			url = f'{self.root.url}/api/v1/lists/export/{list_id}/csv'
			with open(filename, "wb") as file:
				status, data  = self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)
				file.write(data)
			file.close()
		except requests.exceptions.HTTPError as err:
			return status, err
		
		return status, 0
		
class Item:
	"""Item class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def get_all(self, list_id):
		"""Get all items from list.

		Method:
				`GET`
		Endpoint:
				`/api/v1/items/{list_id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(list_id, str), 'List ID must be a string'
		assert list_id, 'List ID must not be an empty string'

		url = f'{self.root.url}/api/v1/items/{list_id}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def get_by_id(self, list_id, id):
		"""Get item from list by ID.

		Args:
				list_id: List ID.
				id: Item ID.
		Method:
				`GET`
		Endpoint:
				`/api/v1/items/{list_id}/item/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(list_id, str), 'List ID must be a string'
		assert list_id, 'List ID must not be an empty string'
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/items/{list_id}/item/{id}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def get_by_pattern(self, pattern, list_id, start=0, limit=100):
		"""Get items from list by pattern.

		Args:
				pattern: search template
				list_id: List ID
				start: offset for working with pagination
				limit: limit on the number of elements in a response ( <= 100)
		Method:
				`GET`
		Endpoint:
				`/api/v1/items/{list_id}/search/{pattern}?start={start}&limit={limit}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(pattern, str), 'Pattern must be a string'
		assert pattern, 'Pattern must not be an empty string'
		assert isinstance(list_id, str), 'List ID must be a string'
		assert list_id, 'List ID must not be an empty string'
		assert isinstance(start, int), 'Start value must be an integer'
		assert isinstance(limit, int), 'Limit value must be an integer'
		assert start >= 0, 'Start value must be greater than 0'
		assert ((limit > 0) and (limit <= 100)), 'Limit value must be greater than 0 and less than 100'

		url = f'{self.root.url}/api/v1/items/{list_id}/search/{pattern}?start={start}&limit={limit}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def create(self, list_id, data):
		"""Create item in the list.

		Args:
				list_id: The ID of the list to which the item will belong to.
				data: Dictionary of user data.

						{
							"listId": <list_id>,
							"value":"test",
							"comment":"test",
							"expireAt":1234567890,
							"status":"test"
						}

		Method:
				`POST`
		Endpoint:
				`/api/v1/items/{list_id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(list_id, str), "List ID type must be a string"
		assert list_id, "List ID must not be an empty string"
		assert isinstance(data, dict), "The data type must be a dictionary"
		assert data, "Item data must not be an empty dictionary"

		url = f'{self.root.url}/api/v1/items/{list_id}'
		data = json.dumps(data)
		return self.root.r('POST', url, data, headers=None, verify=self.root.verify)

	def update(self, list_id, id, data):
		"""Update item in the list.

		Args:
				list_id: The ID of the list to which the item will belong to.
				id: Item ID
				data: Dictionary of user data.

						{
							'comment': 'test',
							'createdAt': 1234567890,
							'createdBy': 'test',
							'expireAt': 1234567890,
							'expired': True,
							'id': '<id>',
							'listId': '<list_id>',
							'status': 'test',
							'updatedBy': 'test',
							'value': 'test'
						}

		Method:
				`PUT`
		Endpoint:
				`/api/v1/items/{list_id}/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(list_id, str), "List ID must be a string"
		assert list_id, "List ID must not be an empty string"

		assert isinstance(id, str), "The ID must be a string"
		assert id, "The ID must not be an empty string"

		assert isinstance(data, dict), "The data type must be a dictionary"
		assert data, "Item data must not be an empty dictionary"

		url = f'{self.root.url}/api/v1/items/{list_id}/{id}'
		data = json.dumps(data)
		return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)

	def delete(self, list_id, id):
		"""Delete item from the list.

		Args:
				list_id: The ID of the list to which the item will belong to.
				id: Item ID.
		Method:
				`DELETE`
		Endpoint:
				`/api/v1/items/{list_id}/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(list_id, str), "List ID must be a string"
		assert list_id, "List ID must not be an empty string"
		assert isinstance(id, str), "The ID must be a string"
		assert id, "The ID must not be an empty string"

		url = f'{self.root.url}/api/v1/items/{list_id}/{id}'
		return self.root.r('DELETE', url, body=None, headers=None, verify=self.root.verify)
