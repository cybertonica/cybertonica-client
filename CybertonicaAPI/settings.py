import json


class Settings:
	"""Settings class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def get_all(self):
		"""Get all settings.

		Method:
				`GET`
		Endpoint:
				`/api/v1/settings`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/settings'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def update(self, data):
		"""Update settings in the system.

		Args:
				data: Dictionary of settings data.
		Method:
				`PUT`
		Endpoint:
				`/api/v1/settings`
		Returns:
				See CybertonicaAPI.Client.r
		"""

		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Settings data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/settings'
		data = json.dumps(data)
		return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)