from CybertonicaAPI.lists import List  # include Item
from CybertonicaAPI.users import User
from CybertonicaAPI.policies import Policy
from CybertonicaAPI.subchannels import Subchannel
from CybertonicaAPI.channels import Channel
from CybertonicaAPI.events import Event
from CybertonicaAPI.auth import Auth
import json

import requests
import urllib3
# ignore SSL certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Client:
	'''
	Facade class. Contains all methods from /src classes

	:param scheme: request's scheme (http/https)
	:type scheme: str
	:param host: host (test.cybertonica.com)
	:type host: str
	:param team: user team (test,dev)
	:type team: str
	:param key: apiUserKey (see Settings tab)
	:type key: str
	:param login: user login
	:type login: str
	:param password: user password
	:type password: str
	'''

	def __init__(self, **settings):
		assert 'url' in settings, 'url is required parameter'
		assert 'team' in settings, 'team is required parameter'
		assert 'api_key' in settings, 'api_key is required parameter'

		self.url = str(settings['url'])
		self.team = str(settings['team'])
		self.signature = str(settings['api_key'])

		self.verify = bool(settings['verify']
						   ) if 'verify' in settings else False
		self.token = ''

		self.auth = Auth(self)
		self.subchannels = Subchannel(self)
		self.lists = List(self)
		self.users = User(self)
		self.channels = Channel(self)
		self.policies = Policy(self)
		self.events = Event(self)

	def __create_headers(self):
		return {
			'content-type': 'application/json;charset=utf-8',
			'apiUserId': self.team,
			'apiSignature': self.signature,
			'Connection':  'keep-alive',
			'Authorization': f'Bearer {self.token}'
		}

	def r(self, method, url=None, body=None, headers=None, files=None, verify=True):
		'''
		Main function for the sending requests

		:param method: request's method (GET,POST,PUT, etc)
		:type methpd: str
		:param url: URL (<scheme>://<host>/<endpoint>..)
		:type url: str
		:param body: request's data (result after json.dumps())
		:type body: str
		:return: status code and JSON(if there is it else json=None)
		:rtype: couple
		'''
		assert method, 'method is required parameter'
		
		if not headers:
			headers = self.__create_headers()

		assert isinstance(headers, dict), 'headers must be a dict'

		url = url if url else self.url

		r = requests.request(method=str(method), url=str(url), data=str(
			body), headers=headers, files=files, verify=verify)

		json = r.json() if 'json' in r.headers['Content-Type'] else None
		return (r.status_code, json)

if __name__ == "__main__":
	pass
