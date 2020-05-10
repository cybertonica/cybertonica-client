import json

class Channel:
	'''
	Channel class
	'''
	def __init__(self, root):
		self.root = root

	def get_all(self):
		'''
		Get all available channels

		Method: GET
		Endpoint: /api/v1/subChannels/channels
		'''
		url =  f'{self.root.url}/api/v1/subChannels/channels'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)