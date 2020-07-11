import json


class Role:
	"""Role class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`

	Workflow with role updating:
		>>> status, data = cbt.roles.create('some_role', ['overview'], {'bi':[1,1,1,1]})
		>>> status, data
		>>> 201, {...}
		>>> # update only role name:
		>>> cbt.roles.update(data, 'new_name') 
		>>> # update only tabs:
		>>> cbt.roles.update(data, new_tabs=['overview', 'pfm']) 
		>>> # update only permissions:
		>>> cbt.roles.update(data, new_permissions={'bi':[1,1,1,1], 'cache':[0,0,1,1]}) 
		>>> # update tabs and permissions:
		>>> cbt.roles.update(data, new_tabs=['lists'], new_permissions={'roles':[1,1,1,1]}) 
		>>> # update name, tabs and permissions:
		>>> cbt.roles.update(data, new_name='new', new_tabs=['lists'], new_permissions={'roles':[1,1,1,1]}) 

	"""

	def __init__(self, root):
		self.root = root
		self._api = [
			"bi", "cache", "cases", "crmLink", "currency", "events",
			"filesAccess", "graphs", "hypothesis", "items", "kindList",
			"lists", "metrics", "opStatus", "paths", "permissions",
			"policies", "proxy", "queues", "reportTo", "roles",
			"schemas", "sessions", "settings", "subChannels", "superset",
			"tests", "timeseries", "users"]
		self._tabs = {"overview","pfm","channels","policy","cases","ab_test",
					"search","lists","users","roles","settings","jsonScheme"}

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
	
	def __permission_helper(self, tabs, api, permissions):
		"""Permission helper. Create permission structure.

		Args:
				api: API name
				tabs: List of tabs ( etc. ["overview","channels"])
				permissions: List of permissions (etc. [1,1,0,1]} ->
						create: True,
						read: True,
						update: False,
						delete: True)

		Returns:
				Dictionary
		"""
		assert isinstance(tabs, list), 'Tabs must be a list'
		assert isinstance(api, str), 'API name must be a string'
		assert isinstance(permissions, list), 'Permissions must be a list'
		assert api in self._api, f'{api} is not available api. List of all available API: {self._api}'
		assert self._tabs >= set(tabs), f'You are using unavailable tabs. List of tabs: {self._tabs}'
		return {
                "api":api,
                "name":"",
                "tabs": tabs,
                "create": bool(permissions[0]),
                "read": bool(permissions[1]),
                "update": bool(permissions[2]),
                "delete": bool(permissions[3])
		}
	
	def __role_helper(self, tabs, permissions):
		"""Create a partial role structure.

		Args:
				tabs: List of tabs ( etc. ["overview","channels"])
				permissions: See `CybertonicaAPI.Client.roles.create`

		Returns:
				Dictionary

		"""
		return {
            "tabs": tabs,
            "permissions":[self.__permission_helper(tabs, key, value) for key, value in permissions.items()]
        }

	def __permission_converter(self, permissions):
		"""Converts the permission format to a different format for sending.

		Args:
				permissions: List of dicts

		Returns:
				Dictionary. See __permission_helper() input data.
		"""
		return {p['api'] : [p['create'], p['read'], p['update'], p['delete']] for p in permissions}

	def create(self, name, tabs, permissions):
		"""Create role in the system. (wrapper on the raw_create)

		Args:
				name: Role name
				tabs: List of tabs ( etc. ["overview","channels"])
				permissions: Dict of lists, where key is permission name and value
					is permissions. (etc. {'bi':[1,1,0,1]} -> bi permission, with
						create: True,
						read: True,
						update: False,
						delete: True)

		Method:
				`POST`
		Endpoint:
				`/api/v1/roles`
		Returns:
				See CybertonicaAPI.Client.roles.raw_create
		"""
		assert isinstance(name, str), 'Role name must be a string'
		assert name, 'Role name must not be an empty string'
		assert isinstance(tabs, list), 'Tabs must be a list'
		assert isinstance(permissions, dict), 'Permissions must be a dict of list'
		role_data = self.__role_helper(tabs, permissions)
		role_data['name'] = name
		return self.raw_create(role_data)
	

	def raw_create(self, data):
		"""Create role in the system.

		`WARNING:` you will have to work with raw JSON data.

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
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Role data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/roles'
		data = json.dumps(data)
		return self.root.r('POST', url, data, headers=None, verify=self.root.verify)
	
	def update(self, raw_old_data, new_name='', new_tabs=[], new_permissions={}):
		"""Update role in the system. (wrapper on the raw_update)

		Args:
				new_name: New role name, empty string if you don't want to change it
				new_tabs: New list of tabs ( etc. ["overview","channels"]), empty list if you don't want to change it
				new_permissions: New permissions. Dict of lists, where key is permission
					name and value is permissions. Empty dict if you don't want to change it.
					(etc. {'bi':[1,1,0,1]} -> bi permission, with
						create: True,
						read: True,
						update: False,
						delete: True)

		Method:
				`POST`
		Endpoint:
				`/api/v1/roles`
		Returns:
				See CybertonicaAPI.Client.roles.raw_update
		"""
		assert isinstance(raw_old_data, dict), 'Raw old data must be a dict'
		assert raw_old_data, 'Raw old data must not be an empty dictionary'
		assert isinstance(new_name, str), 'Role name must be a string'
		assert isinstance(new_tabs, list), 'Tabs must be a list'
		assert isinstance(new_permissions, dict), 'Permissions must be a dict of list'
		role_data = {
			"createdAt" : raw_old_data['createdAt'],
			"createdBy" : raw_old_data['createdBy'],
			"updatedAt" : raw_old_data['updatedAt'],
			"updatedBy" : raw_old_data['updatedBy'],
			"version"   : raw_old_data['version'],
			"name"      : new_name if new_name else raw_old_data['name']
		}
		tabs = new_tabs if new_tabs else raw_old_data['tabs']
		permissions = new_permissions if new_permissions else self.__permission_converter(raw_old_data['permissions'])

		role_data = {**role_data, **self.__role_helper(tabs, permissions)}
		return self.raw_update(raw_old_data['id'], role_data)
	
	def raw_update(self, id, data):
		"""Update role in the system.
				
		`WARNING:` you will have to work with raw JSON data.

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