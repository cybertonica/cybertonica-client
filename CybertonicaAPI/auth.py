import json
from types import FunctionType, LambdaType
from email.utils import parseaddr


class Auth:
	"""Auth class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def login(self, api_user, api_user_key_hash):
		"""Create web session.

		Args:
				api_user: User login.
				api_user_key_hash: User password.
		Method:
				`POST`
		Endpoint:
				`/api/v1/login`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(api_user, str), 'The api user must be a string'
		assert api_user, 'The api user must not be an empty string'
		assert isinstance(api_user_key_hash,
						  str), 'The api user key hash must be a string'
		assert api_user_key_hash, 'The api user key hash must not be an empty string'

		url = f'{self.root.url}/api/v1/login'
		data = json.dumps({
			"apiUser": api_user,
			"team": self.root.team,
			"apiUserKeyHash": api_user_key_hash
		})
		headers = {"content-type": "application/json"}
		status_code, data = self.root.r(
			'POST', url, data, headers, verify=self.root.verify)
		if status_code == 200 or status_code == 201:
			self.root.token = data['token']
		return (status_code, data)

	def logout(self):
		"""Drop web session.

		Method:
				`POST`
		Endpoint:
				`/api/v1/logout`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/logout'
		headers = {
			"content-type": "application/json",
			"Authorization": f"Bearer {self.root.token}"}
		status_code, data = self.root.r(
			'POST', url, headers, body=None, verify=self.root.verify)
		if status_code < 400:
			self.root.token = ''
		return (status_code, data)

	def recovery_password(self, team, email):
		"""Recovery password.

		Args:
				team: user team.
				email: user email.
		Method:
				`GET`
		Endpoint:
				`/api/v1/recovery/request?team={team}&email={email}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(team, str), 'Team must be a string'
		assert team, 'Team must not be an empty string'
		assert isinstance(email, str), 'Email must be a string'
		assert email, 'Email must not be an empty string'
		assert '@' in parseaddr(email)[1], 'Email must be valid'

		url = f'{self.root.url}/api/v1/recovery/request?team={team}&email={email}'
		headers = {"content-type": "application/json"}
		return self.root.r('GET', url, headers, body=None, verify=self.root.verify)

	def register(self, data):
		"""Create a new user in the system.

		Args:
				data: Dictionary of user data. If the dictionary
								does not contain fields `invitedAt` or `updatedAt`,
								then they are automatically added with the values `0`.

						{
							"email":"example@test.com",
							"password":"Password12345",
							"team":"test",
							"firstName":"Test",
							"lastName":"Test",
							"login":"test",
							"invitedAt":0,
							"updatedAt":0
						}
		Method:
				`POST`
		Endpoint:
				`/api/v1/registration`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'User data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/registration'
		headers = {"content-type": "application/json"}
		if "invitedAt" not in data:
			data["invitedAt"] = 0
		if "updatedAt" not in data:
			data["updatedAt"] = 0
			
		data = json.dumps(data)
		return self.root.r('POST', url, data, headers, verify=self.root.verify)
