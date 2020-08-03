import json


class Geo:
	"""Geo class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def get_ip(self, ip):
		"""Checks for ip in the geoip data.

		Args:
				ip: IP
		Method:
				`GET`
		Endpoint:
				`/api/v1.2/geo`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(ip, str), 'The IP must be a string'
		assert ip, 'The IP must not be an empty string'

		url = f'{self.root.url}/api/v1.2/geo/ip/{ip}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)
