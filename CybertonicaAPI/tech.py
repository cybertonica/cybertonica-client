import json


class Tech:
	"""Tech class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def info(self):
		"""Get service info.

		Method:
				`GET`
		Endpoint:
				`/api/v1/info`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/info'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def ping(self):
		"""Ping to the system

		Method:
				`GET`
		Endpoint:
				`/api/v1/ping`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/ping'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)
	
	def paths(self):
		"""Get all paths

		Method:
				`GET`
		Endpoint:
				`/api/v1/paths`
		Returns:
				See CybertonicaAPI.Client.r
		""" 
		url = f'{self.root.url}/api/v1/paths'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)
		