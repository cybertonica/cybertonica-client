import json

class List:
	'''
	List class

	:param url: base url (see ../client.py)
	:type url: str
	:param do: function 'r', that sends requests (see ../client.py)
	:type do: function
	'''
	def __init__(self, root):
		self.root = root
		self.items = Item(root)

	def get_all(self):
		'''
		Get all Policies

		Method: GET
		Endpoint: /api/v1/lists
		'''
		url = f'{self.root.url}/api/v1/lists'
		return self.root.r('GET',url,body=None,headers=None,verify=self.root.verify)

	def get_by_id(self, id):
		'''
		Get list by ID

		Method: GET
		Endpoint: /api/v1/lists/{id}

		:param id: list id
		:type id: str
		'''
		assert isinstance(id, str), 'The ID must be a string'
		assert id , 'The ID must not be an empty string'
		
		url = f'{self.root.url}/api/v1/lists/{id}'
		return self.root.r('GET',url,body=None,headers=None,verify=self.root.verify)

	def create(self, data):
		'''
		Create list by data

		Method: POST
		Endpoint: /api/v1/lists

		:param data: new list data
		:type data: dict
		'''
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'List data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/lists'
		data = json.dumps(data)
		return self.root.r('POST',url,data,headers=None,verify=self.root.verify)

	def update(self, id, data):
		'''
		Update list by ID

		Method: PUT
		Endpoint:  /api/v1/lists/{id}

		:param id: list id
		:type id: str
		:param data: new list data
		:type data: dict
		'''
		assert isinstance(id, str), 'The ID must be a string'
		assert id , 'The ID must not be an empty string'
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'List data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/lists/{id}'
		data = json.dumps(data)
		return self.root.r('PUT',url,data,headers=None,verify=self.root.verify)

	def delete(self, id):
		'''
		Remove list by ID

		Method: DELETE
		Endpoint: /api/v1/lists/{id}

		:param id: list id
		:type id: str
		'''
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
		'''
		Get all items by list

		Method: GET
		Endpoint: /api/v1/items/{id}

		:param lid: list id
		:type lid: str
		'''
		assert isinstance(list_id, str), 'List ID must be a string'
		assert list_id , 'List ID must not be an empty string'

		url = f'{self.root.url}/api/v1/items/{list_id}'
		return self.root.r('GET',url,body=None,headers=None,verify=self.root.verify)

	def get_by_id(self, list_id, id):
		'''
		Get item by ID from list

		Method: GET
		Endpoint: /api/v1/items/{list_id}/item/{id}

		:param lid: list id
		:type lid: str
		:param id: item id
		:type id: str
		'''
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
		'''
		Create item by data

		Method: POST
		Endpoint: /api/v1/items

		:param data: new item data
		:type data: dict
		'''
		assert isinstance(list_id, str), "List ID type must be a string"
		assert list_id, "List ID must not be an empty string"
		assert isinstance(data, dict), "The data type must be a dictionary"
		assert data, "Item data must not be an empty dictionary"

		url = f'{self.root.url}/api/v1/items/{list_id}'
		data = json.dumps(data)
		return self.root.r('POST',url,data,headers=None,verify=self.root.verify)
		

	def update(self, list_id, id, data):
		'''
		Update item by id

		Method: PUT
		Endpoint: /api/v1/items/{id}

		:param id: item id
		:type id: str
		:param data: new item data
		:type data: str
		'''
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
		'''
		Remove item by id

		Method: DELETE
		Endpoint: /api/v1/items/{id}

		:param id: item id
		:type id: str
		'''
		assert isinstance(list_id, str), "List ID must be a string"
		assert list_id, "List ID must not be an empty string"
		assert isinstance(id, str), "The ID must be a string"
		assert id, "The ID must not be an empty string"
		
		url = f'{self.root.url}/api/v1/items/{list_id}/{id}'
		return self.root.r('DELETE',url,body=None,headers=None,verify=self.root.verify)