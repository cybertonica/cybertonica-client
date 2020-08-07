import json


class Bin:
	"""Bin class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root
	def get(self, bin):
		"""Checks for bin in the system hashes

		Args:
				bin: BIN value
		Method:
				`GET`
		Endpoint:
				`/api/v1.2/bins/{bin}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(bin, str), 'The BIN must be a string'
		assert bin, 'The BIN must not be an empty string'

		url = f'{self.root.url}/api/v1.2/bins/{bin}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)
