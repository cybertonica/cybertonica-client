import json

class Session:
	"""Session class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def get_all(self):
		"""Get all sessions.

		Method:
				`GET`
		Endpoint:
				`/api/v1/sessions`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/sessions'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)
	
	def get_all_permissions(self):
		"""Get all permissions for current session.

		Method:
				`GET`
		Endpoint:
				`/api/v1/sessions/permission`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/sessions/permissions'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def refresh(self):
		"""Refresh current session. Overwrites the token value
			in the client if the request is successful.

		Method:
				`GET`
		Endpoint:
				`/api/v1/sessions/refresh`
		Returns:
				Tuple (status, flag), where status is status of response and
					flag is an operation success indicator
		"""
		url = f'{self.root.url}/api/v1/sessions/refresh'
		status, data = self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)
		try:
			if status < 400:
				if 'token' in data:
					self.root.token = data['token']
					return status, True
		except:
			return status, False