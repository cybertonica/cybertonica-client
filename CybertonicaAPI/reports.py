import json


class Report:
	"""Report class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root
		self._allow_kinds = [
		   'test', 'daily', 'listExpired' 
		]

	def send(self,  kind):
		"""Sends a `kind` report to all emails specified in settings.

		Args:
				kind: Kind of report (test, daily or listExpired)
		Method:
				`GET`
		Endpoint:
				`/api/v1.2/report`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(kind, str), 'The kind must be a string'
		assert kind, 'The kind must not be an empty string'
		assert kind in self._allow_kinds, f'{kind} report is not available. List of kinds: {self._allow_kinds}'

		url = f'{self.root.url}/api/v1/report/{kind}'
		return self.root.r('POST', url, body=None, headers=None, verify=self.root.verify)
