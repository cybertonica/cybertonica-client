from CybertonicaAPI.lists import List  # include Item
from CybertonicaAPI.users import User
from CybertonicaAPI.policies import Policy
from CybertonicaAPI.subchannels import Subchannel
from CybertonicaAPI.channels import Channel
from CybertonicaAPI.events import Event
from CybertonicaAPI.auth import Auth
from CybertonicaAPI.roles import Role
from CybertonicaAPI.abtests import ABTest
from CybertonicaAPI.afclient import AFClient

import json

import requests
import urllib3
import logging
# ignore SSL certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Client:
	"""Main Facade class. Contains all methods.

	Attributes:
			**settings: Set of settings for the class.It must contains a
					required parameters: `url`, `team`, `api_key`.
	"""

	def __init__(self, **settings):
		assert 'url' in settings, 'url is required parameter'
		assert 'team' in settings, 'team is required parameter'
		
		self.url = str(settings['url'])
		self.team = str(settings['team'])
		self.api_user_id = str(settings['api_user_id']) if 'api_user_id' in settings else ''
		self.api_signature = str(settings['api_signature']) if 'api_signature' in settings else ''
		self.verify = bool(settings['verify']
						   ) if 'verify' in settings else True
		self.token = ''
		self.dev_mode = bool(settings['dev_mode']
						   ) if 'dev_mode' in settings else False
		self.auth = Auth(self)
		self.subchannels = Subchannel(self)
		self.lists = List(self)
		self.users = User(self)
		self.channels = Channel(self)
		self.policies = Policy(self)
		self.events = Event(self)
		self.roles = Role(self)
		self.abtests = ABTest(self)
		self.af = AFClient(self)

	def __create_headers(self):
		return {
			'content-type': 'application/json;charset=utf-8',
			'Connection':  'keep-alive',
			'Authorization': f'Bearer {self.token}'
		}

	def r(self, method, url=None, body=None, headers=None, files=None, verify=True):
		"""Main function for the sending requests.

		Args:
				method: request's method.
				url: target URL.
				body: request's data after applying json.dumps().
				headers: request's headers. if the header is None
						then standard headers are created:

						{
							'content-type': 'application/json;charset=utf-8',
							'Connection':  'keep-alive',
							'Authorization': 'Bearer <user_token>'
						}
		Returns:
				A tuple that contains status code and response's JSON.
						If headers does not contain 'json' or 'text' in the Content-Type,
						then data is None.
		"""
		assert method, 'method is required parameter'

		if not headers:
			headers = self.__create_headers()

		assert isinstance(headers, dict), 'headers must be a dict'

		url = url if url else self.url

		r = requests.request(method=str(method), url=str(url), data=str(
			body), headers=headers, files=files, verify=verify)

		data = None
		if r.headers.get('content-type'):
			data = r.json() if 'json' in r.headers.get('content-type') else r.text
		
		return (r.status_code, data)

if __name__ == "__main__":
	pass
