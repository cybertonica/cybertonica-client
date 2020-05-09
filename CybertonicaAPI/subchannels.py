import json

class Subchannel:
	'''
	Sub-channel class
	'''

	def __init__(self, root):
		self.root = root

	def get_all(self):
		'''
		Get all available sub-channels

		Method: GET
		Endpoint: /api/v1/subChannels
		'''
		url = f'{self.root.url}/api/v1/subChannels'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def get_by_id(self,id):
		'''
		Get sub-channel by ID

		Method: GET
		Endpoint: /api/v1/subChannels/{id}

		:param id: sub-channel's ID
		:type id: str
		'''
		assert isinstance(id, str), 'The ID must be a string'
		assert id, 'The ID must not be an empty string'

		url = f'{self.root.url}/api/v1/subChannels/{id}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)
	
	def search_by(self, key, value):
		'''
		Search sub-channel by key with value

		:param key: 
		:type key: str
		:param value: 
		:type value: str or int
		'''
		status_code, subchannels = self.get_all()
		if status_code >= 400:
			return (status_code, subchannels)
	
		for channel in subchannels:
			if key in channel:
				if channel[key] == value:
					return (True, channel)
		return (False, None)
	
	def create(self,data):
		'''
		Creating sub-channel by data

		Method: GET
		Endpoint: /api/v1/subChannels

		:param data: data of new sub-channel
		:type data: dict
		'''
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Subchannel data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/subChannels'
		data = json.dumps(data)
		return self.root.r('POST', url, data, headers=None, verify=self.root.verify)

	def update(self,id,data):
		'''
		Updating sub-channel by ID

		Method: PUT
		Endpoint: /api/v1/subChannels/{id}

		:param id: sub-channel's ID
		:type id: str
		:param data: new data for the sub-channel
		:type data: dict
		'''
		assert isinstance(id, str), 'The ID must be a string'
		assert id , 'The ID must not be an empty string'
		assert isinstance(data, dict), 'The data type must be a dictionary'
		assert data, 'Subchannel data must not be an empty dictionary'

		url = f'{self.root.url}/api/v1/subChannels/{id}'
		data = json.dumps(data)
		return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)

	def delete(self,id):
		'''
		Removing sub-channel by ID

		Method: DELETE
		Endpoint: /api/v1/subChannels/{id}

		:param id: sub-channel's ID
		:type id: str
		'''
		assert isinstance(id, str), 'The ID must be a string'
		assert id , 'The ID must not be an empty string'
		
		url = f'{self.root.url}/api/v1/subChannels/{str(id)}'
		return self.root.r('DELETE', url, body=None, headers=None, verify=self.root.verify)
