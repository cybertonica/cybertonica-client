import json

class User:
	'''
	User class
	'''

	def __init__(self, root):
		self.root = root

	def get_all(self):
		'''
		Get all available users

		Method: GET
		Endpoint: /api/v1/users
		'''
		url = f'{self.root.url}/api/v1/users'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def get_by_id(self,id):
		'''
		Get user by ID

		Method: GET
		Endpoint: /api/v1/users/{id}

		:param id: user's ID
		:type id: str
		'''
		assert isinstance(id, str), 'The ID must be a string'
		assert id , 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/users/{str(id)}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)
	
	def create(self,data):
		'''
		Creating user by data

		Method: POST
		Endpoint: /api/v1/users

		:param data: data of new user
		:type data: dict
		'''
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'User data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/users'
		data = json.dumps(data)
		return self.root.r('POST', url, data, headers=None, verify=self.root.verify)

	def update(self,id,data):
		'''
		Updating user by ID

		Method: PUT
		Endpoint: /api/v1/users/{id}

		:param id: user's ID
		:type id: str
		:param data: new data for the user
		:type data: dict
		'''
		assert isinstance(id, str), 'The ID must be a string'
		assert id , 'The ID must not be an empty string'
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'User data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/users/{id}'
		data = json.dumps(data)
		return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)

	def delete(self,id):
		'''
		Removing user by ID

		Method: DELETE
		Endpoint: /api/v1/users/{id}

		:param id: user's ID
		:type id: str
		'''
		assert isinstance(id, str), 'The ID must be a string'
		assert id , 'The ID must not be an empty string'
		
		url = f'{self.root.url}/api/v1/users/{str(id)}'
		return self.root.r('DELETE', url, body=None, headers=None, verify=self.root.verify)
	
	def add_role(self,id,role):
		'''
		Add role to the user

		:param id: user's ID
		:type id: str
		:param role: target role (exist in the system), e.g. 'Fraud Support'
		:type role: str
		'''
		assert isinstance(role, str), 'Role name must be a string'
		assert isinstance(id, str), 'The ID must be a string'
		assert role, 'Role name must not be an empty string'
		assert id, 'The ID must not be an empty string'

		status, user = self.get_by_id(id)

		assert status == 200, 'The user data request was not successful'
		assert isinstance(user, dict), 'The user data type does not match the dictionary'
		assert "roles" in user, 'The data structure does not contain the roles key'
		assert role not in user["roles"], 'The user already has a role'
		
		user["roles"].append(role) #["FraudChiefOfficer"]
		return self.update(id, user)
	
	def remove_role(self,id,role):
		'''
		Remove role from the user

		:param id: user's ID
		:type id: str
		:param role: target role (exist in the system), e.g. 'Fraud Support'
		:type role: str
		'''
		assert isinstance(role, str), 'Role name must be a string'
		assert isinstance(id, str), 'The ID must be a string'
		assert role, 'Role name must not be an empty string'
		assert id, 'The ID must not be an empty string'

		status, user = self.get_by_id(id)

		assert status == 200, 'The user data request was not successful'
		assert isinstance(user, dict), 'The user data type does not match the dictionary'
		assert "roles" in user, 'The data structure does not contain the roles key'
		assert role in user["roles"], 'The user already has not a role'

		user["roles"].remove(role)
		return self.update(id, user)