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
from CybertonicaAPI.cases import Case
from CybertonicaAPI.settings import Settings
from CybertonicaAPI.queues import Queue
from CybertonicaAPI.sessions import Session
from CybertonicaAPI.tech import Tech
from CybertonicaAPI.bi import BusinessIntelligence
from CybertonicaAPI.schema import Schema
from CybertonicaAPI.currencies import Currency
from CybertonicaAPI.geo import Geo
from CybertonicaAPI.bins import Bin
from CybertonicaAPI.reports import Report

import logging
import json
import requests
import urllib3
import time

# ignore SSL certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BasicAuthToken(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r

class Client:
	"""Main Facade class. Contains all methods.

	Attributes:
			**settings: Set of settings for the class. It must contains a
					required parameters: `url`, `team`. If you want to use
					`CybertonicaAPI.afclient.AFClient` you should include
					`api_user_id` and `api_signature` to settings.

				url: target url of environment.
				team: value of team.
				custom_af_url: AFClient will use the specified address.
					By default, the address is equal to a url with a port 7499.
				api_user_id: user id for AF.
				api_signature: value of signature for AF.
				verify: True, if you need to ignore SSL certificates.
				dev_mode: True, if you need enable hidden functions.
	"""

	def __init__(self, **settings):
		self.log = logging.getLogger(__name__)
		self.log.debug('Client has been init with %s',settings)

		assert 'url' in settings, 'url is required parameter'
		assert isinstance(settings['url'], str), 'url value must be a string'
		assert 'team' in settings, 'team is required parameter'
		assert isinstance(settings['team'], str), 'team value must be a string'

		self.url = str(settings['url'])
		self.af_url = str(settings['custom_af_url']) if 'custom_af_url' in settings else self.url+':7499'
		self.team = str(settings['team'])
		self.api_user_id = str(settings['api_user_id']) if 'api_user_id' in settings else ''
		self.api_signature = str(settings['api_signature']) if 'api_signature' in settings else ''
		self.af_version = str(settings['af_version']) if 'af_version' in settings else 'v2.2'
		self.verify = bool(settings['verify']) if 'verify' in settings else True

		self.token = ''
		self.login_time = 0
		self.ttl = 840 # Session TTL == 14 mins
		
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
		self.cases = Case(self)
		self.settings = Settings(self)
		self.queues = Queue(self)
		self.sessions = Session(self)
		self.tech = Tech(self)
		self.bi = BusinessIntelligence(self)
		self.schema = Schema(self)
		self.currencies = Currency(self)
		self.geo = Geo(self)
		self.bins = Bin(self)
		self.reports = Report(self)


	def __create_headers(self):
		return {
			'Content-Type': 'application/json',
			'Connection':  'keep-alive'
		}
	def __is_expired_session(self):
		if self.login_time:
			if int(time.monotonic() - self.login_time) >= self.ttl:
				self.log.debug('Refresh token')
				self.sessions.refresh()

	def r(self, method, url=None, body=None, headers=None, files=None, verify=True):
		"""Main function for the sending requests.

		Args:
				method: request's method.
				url: target URL.
				body: request's data after applying json.dumps().
				headers: request's headers. if the headers is None
						(and you don't upload the file) then standard
						headers are created:

					{
						'content-type': 'application/json',
						'Connection':  'keep-alive'
					}
		Returns:
				A tuple that contains status code and response's JSON.
						If headers does not contain `'application/json'`,
						`'text/html'`, `'text/csv` in the Content-Type, then data is `None`.
		"""
		self.log.debug(
			"Trying %s request to %s with body=%s headers=%s files=%s verify=%s",
			method,
			url,
			body,
			headers,
			files,
			verify
		) 
		assert method, 'method is required parameter'
		self.__is_expired_session()

		headers = headers if headers else self.__create_headers()
		headers = None if files else headers 
		url = url if url else self.url
		try:
			r = requests.request(method=method, url=url, data=
					body, headers=headers, files=files, verify=verify, auth=BasicAuthToken(self.token))

			data = None
			headers = r.headers.get('Content-Type', '')
			if 'json' in headers:
				data = r.json()
			if 'csv' in headers:
				data = r.content
			if 'plain' in headers or 'html' in headers:
				data = r.text
	
			return (r.status_code, data)
		except Exception as e:
			self.log.debug('%s', repr(e))
			return (500, None)

if __name__ == "__main__":
	pass