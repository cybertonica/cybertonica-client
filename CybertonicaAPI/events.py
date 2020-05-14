import json


class Event:
	"""Event class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

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

	def get_by_id(self, id):
		"""Get event from system by ID.

		Args:
				id: Event ID.
		Method:
				`GET`
		Endpoint:
				`/api/v1/events/{id}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(id, str), "The ID must be a string"
		assert id, "The ID must not be an empty string"

		url = f'{self.root.url}/api/v1/events/{id}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def get_by_queue(self, queue_name, start=0, limit=100):
		"""Get events from system by queue.

		Endpoint has a simple pagination analog.
				The `start` variable is shifted to the required offset.
				The `limit` value is a constant in the range from 0 to 1000.

		Args:
				queue_name: Queue name in the system.
				start: Offset value. Default value is 0.
				limit: Maximum sample size from the system.
		Method:
				`GET`
		Endpoint:
				`/api/v1.1/events/queue/{queue_name}?start={start}&limit={limit}`
		Returns:
				See CybertonicaAPI.Client.r
		"""
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

	def bulk_review(self, ids, comment, status):
		"""Setting an operation status to the events.

		Args:
				ids: List of event IDs
				comment: A string that contains comments for the operation
				status: Status to be assigned to events. The status can only
						be `Ok`, `Challenge`, `Fraud`.
		Method:
				`PUT`
		Endpoint:
				`/api/v1.2/opStatus/review`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(ids, list), "ID list must be a list of string"
		assert ids, "ID List must not be an empty list"

		assert isinstance(comment, str), "Comment value must be a string"
		assert isinstance(status, str), "Status value must be a string"

		assert status in [
			'Ok', 'Challenge', 'Fraud'], "Status value must be either 'Ok', 'Challenge' or 'Fraud'"

		url = f'{self.root.url}/api/v1.2/opStatus/review'
		data = json.dumps({
			"ids": ids,
			"comment": comment,
			"status": status
		})
		return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)

	def review(self, id, comment, status):
		"""Setting an operation status to the single event.

		It is a special case of the `CybertonicaAPI.events.Event.bulk_review` function.

		Args:
				id: Event ID
				comment: A string that contains comments for the operation
				status: Status to be assigned to events. The status can only
						be Ok, Challenge, Fraud.
		Method:
				`PUT`
		Endpoint:
				`/api/v1.2/opStatus/review`
		Returns:
				See CybertonicaAPI.events.Event.bulk_review
		"""
		return self.bulk_review([id], comment, status)
