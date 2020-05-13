import json

class Event:
	'''
	Event class

	:param url: base url (see ../client.py)
	:type url: str
	:param do: function 'r', that sends requests (see ../client.py)
	:type do: function
	'''
	def __init__(self, root):
		self.root = root

	# def get_by_id_and_fk(self,id,fks):
	#     '''
	#     Get events by id and fks

	#     Method: GET
	#     Endpoint: /api/v1/events/?id={id}&fk={fk}
	#     '''
	#     url = f'{self.root.url}/api/v1/events/?id={id}&fk={fks}'
	#     return self.root.r('GET', url, body=None, headers=None,verify=self.root.verify)

	def get_by_id(self,id):
		'''
		Get event by id

		Method: GET
		Endpoint: /api/v1/events/{id}
		'''
		assert isinstance(id, str), "The ID must be a string"
		assert id, "The ID must not be an empty string"

		url = f'{self.root.url}/api/v1/events/{id}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def get_by_queue(self,queue_name,start=0,limit=100):
		'''
		Get events by queue name, default values:
			start is 0
			limit is 100

		Method: GET
		Endpoint: /api/v1.1/events/queue/{queue_name}
		'''
		assert isinstance(queue_name, str), "Queue name must be a string"
		assert queue_name, "Queue name must not be an empty string"
		
		assert isinstance(start, int), "The start value must be an integer"
		assert start >= 0, "The start value must be greater than or equal to 0"

		assert isinstance(limit, int), "The limit value must be an integer"
		assert limit > 0 and limit <= 1000, "The limit value must be in the range (0, 1000]"

		url = f'{self.root.url}/api/v1.1/events/queue/{queue_name}?start={str(start)}&limit={str(limit)}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	# def get_by_ids_array(self,ids):
	#     '''
	#     Get events by ids array included by data

	#     Method: POST
	#     Endpoint: /api/v1/events/{queue}
	#     '''
	#     url = f'{self.root.url}/api/v1/events' #??? #TODO
	#     data = json.dumps(ids)
	#     return self.root.r('POST',url,data,headers=None, verify=self.root.verify)
