import json

class List:
	"""List class.

	Attributes:
		root: Object of Client class.
	"""
	def __init__(self, root):
		self.root = root
		self.items = Item(root)

	def get_all(self):
		"""Get all lists.

		Method:
			GET
		Endpoint:
			/api/v1/lists
		Returns:
			A tuple that contains status code and response's JSON.
				If headers does not contain 'json' in the Content-Type,
				then data is None.
		"""
		url = f'{self.root.url}/api/v1/lists'
		return self.root.r('GET',url,body=None,headers=None,verify=self.root.verify)

	def get_by_id(self, id):
		"""Get list from system by ID.
		
		Args:
			id: List ID.
		Method:
			GET
		Endpoint:
			/api/v1/lists/{id}
		Returns:
			A tuple that contains status code and response's JSON.
				If headers does not contain 'json' in the Content-Type,
				then data is None.
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id , 'The ID must not be an empty string'
		
		url = f'{self.root.url}/api/v1/lists/{id}'
		return self.root.r('GET',url,body=None,headers=None,verify=self.root.verify)

	def create(self, data):
		"""Create list in the system by data.
		
		Args:
			data: Dictionary of user data.

				{
					'name': "name",
					'kind': "WHITE"
				}

		Method:
			POST
		Endpoint:
			/api/v1/lists
		Returns:
			A tuple that contains status code and response's JSON.
				If headers does not contain 'json' in the Content-Type,
				then data is None.
		"""
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'List data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/lists'
		data = json.dumps(data)
		return self.root.r('POST',url,data,headers=None,verify=self.root.verify)

	def update(self, id, data):
		"""Update list in the system by data.
		
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
			PUT
		Endpoint:
			/api/v1/lists/{id}
		Returns:
			A tuple that contains status code and response's JSON.
				If headers does not contain 'json' in the Content-Type,
				then data is None.
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id , 'The ID must not be an empty string'
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'List data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/lists/{id}'
		data = json.dumps(data)
		return self.root.r('PUT',url,data,headers=None,verify=self.root.verify)

	def delete(self, id):
		"""Delete list from the system by ID.
		
		Args:
			id: List ID.
		Method:
			DELETE
		Endpoint:
			/api/v1/lists/{id}
		Returns:
			A tuple that contains status code and response's JSON.
				If headers does not contain 'json' in the Content-Type,
				then data is None.
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id , 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/lists/{id}'
		return self.root.r('DELETE',url,body=None,headers=None,verify=self.root.verify)

	# def import_csv(self, id, csv_filename):
	# 	'''
	# 	Import CSV file to the list

	# 	Method: POST
	# 	Endpoint: /api/v1/lists/import/{id}/csv

	# 	:param id: list id
	# 	:type id: str
	# 	:param csv_file: filename(or path) for the uploading
	# 	:type csv_file: str
	# 	'''
	# 	pass

	# def export_csv(self, id, output):
	# 	'''
	# 	Export CSV file from the list

	# 	Method: GET
	# 	Endpoint: /api/v1/lists/export/{id}/csv

	# 	:param id: list id
	# 	:type id: str
	# 	:param output: filename(or path) for the download
	# 	:type output: str
	# 	'''
	# 	pass

class Item:
	#  #TODO:
	# /api/v1/items/search/{pattern}/?limit={limit}   GET Search Items by pattern with limit default by 100
	# /api/v1/items/{list}/search/{pattern}/?limit={limit}    GET Search Items by pattern and list with limit default by 100
	# /api/v1/items/export/{id}/csv   GET Export current Items by id to csv
	'''
	Item class

	:param url: base url (see ../client.py)
	:type url: str
	:param do: function 'r', that sends requests (see ../client.py)
	:type do: function
	'''
	def __init__(self, root):
		self.root = root

	def get_all(self, list_id):
		"""Get all items from list.

		Method:
			GET
		Endpoint:
			/api/v1/items/{list_id}
		Returns:
			A tuple that contains status code and response's JSON.
				If headers does not contain 'json' in the Content-Type,
				then data is None.
		"""
		assert isinstance(list_id, str), 'List ID must be a string'
		assert list_id , 'List ID must not be an empty string'

		url = f'{self.root.url}/api/v1/items/{list_id}'
		return self.root.r('GET',url,body=None,headers=None,verify=self.root.verify)

	def get_by_id(self, list_id, id):
		"""Get item from list by ID.
		
		Args:
			list_id: List ID.
			id: Item ID.
		Method:
			GET
		Endpoint:
			/api/v1/items/{list_id}/item/{id}
		Returns:
			A tuple that contains status code and response's JSON.
				If headers does not contain 'json' in the Content-Type,
				then data is None.
		"""
		assert isinstance(list_id, str), 'List ID must be a string'
		assert list_id , 'List ID must not be an empty string'
		assert isinstance(id, str), 'The ID must be a string'
		assert id , 'The ID must not be an empty string'
		
		url = f'{self.root.url}/api/v1/items/{list_id}/item/{id}'
		return self.root.r('GET',url,body=None,headers=None,verify=self.root.verify)
		

	# def get_all_alive(self, list_id):
	# 	'''
	# 	Get all alive Items by list

	# 	Method: GET
	# 	Endpoint: /api/v1/items/{list_id}/alive

	# 	:param lid: list id
	# 	:type id: str
	# 	'''
	# 	assert isinstance(list_id, str), "List ID must be a string"
	# 	assert list_id, "List ID must not be an empty string"

	# 	url = f'{self.root.url}/api/v1/items/{list_id}/alive'
	# 	return self.root.r('GET',url,body=None,headers=None,verify=self.root.verify)
		

	def create(self, list_id, data):
		"""Create list in the system by data.
		
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
			POST
		Endpoint:
			/api/v1/items/{list_id}
		Returns:
			A tuple that contains status code and response's JSON.
				If headers does not contain 'json' in the Content-Type,
				then data is None.
		"""
		assert isinstance(list_id, str), "List ID type must be a string"
		assert list_id, "List ID must not be an empty string"
		assert isinstance(data, dict), "The data type must be a dictionary"
		assert data, "Item data must not be an empty dictionary"

		url = f'{self.root.url}/api/v1/items/{list_id}'
		data = json.dumps(data)
		return self.root.r('POST',url,data,headers=None,verify=self.root.verify)
		

	def update(self, list_id, id, data):
		"""Update item in the list by ID.
		
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
			PUT
		Endpoint:
			/api/v1/items/{list_id}/{id}
		Returns:
			A tuple that contains status code and response's JSON.
				If headers does not contain 'json' in the Content-Type,
				then data is None.
		"""
		assert isinstance(list_id, str), "List ID must be a string"
		assert list_id, "List ID must not be an empty string"

		assert isinstance(id, str), "The ID must be a string"
		assert id, "The ID must not be an empty string"

		assert isinstance(data, dict), "The data type must be a dictionary"
		assert data, "Item data must not be an empty dictionary"

		url = f'{self.root.url}/api/v1/items/{list_id}/{id}'
		data = json.dumps(data)
		return self.root.r('PUT',url,data,headers=None,verify=self.root.verify)

	def delete(self,list_id, id):
		"""Delete item from the list by ID.
		
		Args:
			list_id: The ID of the list to which the item will belong to.
			id: Item ID.
		Method:
			DELETE
		Endpoint:
			/api/v1/items/{list_id}/{id}
		Returns:
			A tuple that contains status code and response's JSON.
				If headers does not contain 'json' in the Content-Type,
				then data is None.
		"""
		assert isinstance(list_id, str), "List ID must be a string"
		assert list_id, "List ID must not be an empty string"
		assert isinstance(id, str), "The ID must be a string"
		assert id, "The ID must not be an empty string"
		
		url = f'{self.root.url}/api/v1/items/{list_id}/{id}'
		return self.root.r('DELETE',url,body=None,headers=None,verify=self.root.verify)