import json


class User:
	"""User class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def get_all(self):
		"""Get all users.

		Method:
				`GET`
		Endpoint:
				`/api/v1/users`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/users'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def get_by_id(self, id):
		"""Get user from system by ID.

		Args:
				id: User ID.
		Method:
				`GET`
		Endpoint:
				`/api/v1/users/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/users/{id}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def create(self, data):
		"""Create user in the system.

		Args:
				data: Dictionary of user data. If the dictionary
								does not contain fields A and B, then they are
								automatically added with the values 0.

						{
							"login":"s",
							"firstName":"s",
							"lastName":"s",
							"email":"prettyandsimple@example.com",
							"roles":[],
							"active":True,
							"password":"ApogeeSystemPassword12345",
							"updatedAt":0,
							"invitedAt":0
						}

		Method:
				`POST`
		Endpoint:
				`/api/v1/users`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'User data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/users'
		data = json.dumps(data)
		return self.root.r('POST', url, data, headers=None, verify=self.root.verify)

	def update(self, id, data):
		"""Update user in the system.

		Args:
				id: User ID.
				data: Dictionary of user data.

						{
							"login":"test",
							"firstName":"test",
							"lastName":"test",
							"email":"test",
							"roles":[],
							"active":True,
							"updatedAt":1234567890,
							"invitedAt":1234567890,
							"id": "test",
							"experimental":None,
							"loginAt": 1234567890
						}

		Method:
				`PUT`
		Endpoint:
				`/api/v1/users/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'User data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/users/{id}'
		data = json.dumps(data)
		return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)

	def delete(self, id):
		"""Remove user from the system.

		Args:
				id: User ID.
		Method:
				`DELETE`
		Endpoint:
				`/api/v1/users/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/users/{str(id)}'
		return self.root.r('DELETE', url, body=None, headers=None, verify=self.root.verify)

	def add_role(self, id, role):
		"""Add role to the user.

		Gets the user data via the `CybertonicaAPI.users.User.get_by_id`.
				If the user does not have the `role`, then adds the value `role` to
				the array of user data and calls `CybertonicaAPI.users.User.update`.

		Args:
				id: User ID.
				role: Role name
		Returns:
				See CybertonicaAPI.users.User.update
		"""
		assert isinstance(role, str), 'Role name must be a string'
		assert isinstance(id, str), 'The ID must be a string'
		assert role, 'Role name must not be an empty string'
		assert id, 'The ID must not be an empty string'

		status, user = self.get_by_id(id)

		assert status == 200, 'The user data request was not successful'
		assert isinstance(
			user, dict), 'The user data type does not match the dictionary'
		assert "roles" in user, 'The data structure does not contain the roles key'
		assert role not in user["roles"], 'The user already has a role'

		user["roles"].append(role)  # ["FraudChiefOfficer"]
		return self.update(id, user)

	def remove_role(self, id, role):
		"""Removed role from the user.

		Gets the user data via the `CybertonicaAPI.users.User.get_by_id`.
				If the user has the `role`, then removes the value `role` from
				the array of user data and calls `CybertonicaAPI.users.User.update`.

		Args:
				id: User ID.
				role: Role name
		Returns:
				See CybertonicaAPI.users.User.update
		"""
		assert isinstance(role, str), 'Role name must be a string'
		assert isinstance(id, str), 'The ID must be a string'
		assert role, 'Role name must not be an empty string'
		assert id, 'The ID must not be an empty string'

		status, user = self.get_by_id(id)

		assert status == 200, 'The user data request was not successful'
		assert isinstance(
			user, dict), 'The user data type does not match the dictionary'
		assert "roles" in user, 'The data structure does not contain the roles key'
		assert role in user["roles"], 'The user already has not a role'

		user["roles"].remove(role)
		return self.update(id, user)
	
	def set_new_password(self, password):
		"""Set a new user password. If the new password matches
			the last 6 passwords that were used, it will not be overwritten.

		Args:
				password: A new password value.
		Method:
				`PUT`
		Endpoint:
				`/api/v1/users/attributes/password`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(password, str), 'Password value must be a string'
		assert password, 'Password value must not be an empty string'
		assert len(password) > 8, 'Length of password value must be greater  than 8'

		url = f'{self.root.url}/api/v1/users/attributes/password'
		data = json.dumps({"password":password})
		return self.root.r('PUT', url, body=data, headers=None, verify=self.root.verify)
