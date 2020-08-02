import json


class Currency:
	"""Currency class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def get_by_code(self, code):
		"""Get currency by code.

		Method:
				`GET`
		Endpoint:
				`/api/v1/currency/int/{code}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(code, str), 'The code must be a string'
		assert code, 'The code must not be an empty string'

		url = f'{self.root.url}/api/v1/currency/int/{code}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def get_union_base(self):
		"""Get all available base of currencies.

		Method:
				`GET`
		Endpoint:
				`/api/v1/currency/unionBase`
		Returns:
				See CybertonicaAPI.Client.r
		"""

		url = f'{self.root.url}/api/v1/currency/unionBase'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)
