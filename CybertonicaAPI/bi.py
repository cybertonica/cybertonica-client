import json


class BusinessIntelligence:
	"""BusinessIntelligence class.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root
		self._allow_channels = [
			'global', 'session', 'payment',
			'acquiring', 'card2card', 'p2p_money_transfer',
			'invoice', 'login', 'access_control_change',
			'email'                
		]
		self._allow_report_types = [
			'geoIp',
			'raw',
			'graph'
		]

	def get(self):
		"""Getting timeseries.

		Method:
				`GET`
		Endpoint:
				`/api/v1/bi`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		url = f'{self.root.url}/api/v1/bi'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def export(self, channel, start, end):
		"""Getting timeseries.

		Method:
				`GET`
		Endpoint:
				`/api/v1/bi`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(channel, str), 'The channel must be a string'
		assert channel, 'The channel must not be an empty string'
		assert channel in self._allow_channels, f'You are using unavailable channel. List of channels: {self._allow_channels}'
		assert isinstance(start, int), 'The start time must be an integer'
		assert start > 0, 'The start time must be greater than 0'
		assert isinstance(end, int), 'The end time must be an integer'
		assert end > 0, 'The end time must be greater than 0'

		url = f'{self.root.url}/api/v1/bi/export?channel={channel}&timeStart={start}&timeEnd={end}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

	def search(self, query, report_type, start, end):
		"""Export BusinessIntelligence from system.

		Method:
				`GET`
		Endpoint:
				`/api/v1/bi`
		Returns:
				See CybertonicaAPI.Client.r
		"""
		assert isinstance(query, str), 'The query must be a string'
		assert query, 'The query must not be an empty string'
		assert isinstance(report_type, str), 'The report_type must be a string'
		assert report_type, 'The report_type must not be an empty string'
		assert report_type in self._allow_report_types,  f'You are using unavailable report type. List of types: {self._allow_report_types}'
		assert isinstance(start, int), 'The start time must be an integer'
		assert start > 0, 'The start time must be greater than 0'
		assert isinstance(end, int), 'The end time must be an integer'
		assert end > 0, 'The end time must be greater than 0'

		url = f'{self.root.url}/api/v1/bi/search?channel={channel}&reportType={report_type}&timeStart={start}&timeEnd={end}'
		return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)