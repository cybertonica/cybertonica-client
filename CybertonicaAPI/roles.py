import json


class Role:
	"""Role class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def get_all(self):
		"""Get all role.

		Method:
				`GET`
		Endpoint:
				`/api/v1/roles`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/roles'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def search_by_id(self, id):
		"""Search role  by ID.

		Calls `CybertonicaAPI.roles.Role.get_all` function
			and searches for the specified `id` values.

		Args:
				id: Role ID.
		Returns:
				- `CybertonicaAPI.Client.r` If the response from the server is not equal `200`.
				- `(True, role)` if successful.
				- `(False, None)` in case of failure.
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		status_code, roles = self.get_all()
		if status_code >= 400:
			return (status_code, roles)
		
		for role in roles:
			if role['id'] == id:
				return (True, role)
		return (False, None)

	def raw_create(self, data):
		"""Create role in the system.

		This functionality `only for developers`!
		
		You can enable this by setting the variable `dev_mode = True` in the client
				and calling the function again.
				
		`WARNING:` you will have to work with JSON data.

		Args:
				data: Dictionary of user data.

					{
						"permissions":[
							{
								"api":"bi",
								"name":"",
								"read":true,
								"create":false,
								"update":false,
								"delete":false,
								"tabs":[
									"overview",
									"pfm"
								]
							},
							...
						],
						"name":"test",
						"tabs":[
							"overview",
							"pfm"
							...
						]
					}

		Method:
				`POST`
		Endpoint:
				`/api/v1/roles`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert self.root.dev_mode == True, 'This functionality only for developers'
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Role data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/roles'
		data = json.dumps(
			data)
		return self.root.r('POST', url, data, headers=None, verify=self.root.verify)

	def raw_update(self, id, data):
		"""Update role in the system.

		This functionality `only for developers`!
		
		You can enable this by setting the variable `dev_mode = True` in the client
				and calling the function again.
				
		`WARNING:` you will have to work with JSON data.

		Args:
				id: Role ID.
				data: Dictionary of user data.

		Method:
				`PUT`
		Endpoint:
				`/api/v1/roles/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert self.root.dev_mode == True, 'This functionality only for developers'
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Role data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/roles/{id}'
		data = json.dumps(data)
		return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)

	def delete(self, id):
		"""Delete role from the system.

		Args:
				id: Role ID.
		Method:
				`DELETE`
		Endpoint:
				`/api/v1/roles/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/roles/{id}'
		return self.root.r('DELETE', url, body=None, headers=None, verify=self.root.verify)