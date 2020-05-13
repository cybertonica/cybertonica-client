import json

class Channel:
	"""Channel class.

	Attributes:
		root: Object of Client class.
	"""
	def __init__(self, root):
		self.root = root

	def get_all(self):
		"""Get all available channels.

		Method:
			GET
		Endpoint:
			/api/v1/subChannels/channels
		Returns:
			A tuple that contains status code and response's JSON.
				If headers does not contain 'json' in the Content-Type,
				then data is None.
		"""
		url =  f'{self.root.url}/api/v1/subChannels/channels'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)