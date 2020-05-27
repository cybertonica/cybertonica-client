import hashlib
import json
import base64
import requests
import hmac
import traceback


class AFClient:
	"""Sub-client for Cybertonica AF API.

	Attributes:
			root: Object of `CybertonicaAPI.Client`
	"""

	def __init__(self, root):
		self.root = root

	def __create_signature(self, key, raw):
		"""
		Creating signature

		Body data of post request is hashed by signature string, we got in initial parameters, into a hmac-sha1 format
		:param key: the same as initial api_signature
		:type key: str
		:param raw: json dumps of request body
		:type raw: str

		:return: signature string for headers
		:rtype: str
		"""
		hashed_data = hmac.new(key.encode(), raw.encode(), hashlib.sha1).digest()
		b = base64.encodebytes(hashed_data)
		b = b.rstrip()
		return b.decode("utf-8")

	def __create_headers(self, user_id, key, raw):
		"""
		Creating headers

		:param user_id: the same as initial api_user_id
		:type user_id: str
		:param key: the same as initial api_signature
		:type key: str
		:param raw: json dumps of request body
		:type raw: str

		:return: headers for post request
		:rtype: dict
		"""
		post_headers = {'Content-Type': 'application/json',
						'X-AF-Team': user_id,
						'Connection': 'keep-alive',
						'X-AF-Signature': self.__create_signature(key, raw)}
		return post_headers

	def __create_url(self,channel,sub_channel,update_status=None):
		"""
		Creating url

		Two initial parameters are used: protocol and hostname
		Also here is one more parameter: path.
		It gets value, depending on method where we use it.

		:param protocol: initial parameter
		:type protocol: str
		:param hostname: initial parameter
		:type hostname: str
		:param path: "createEvent" if method is post_create and "updateEvent" if method is post_update
		:type path: str

		:return: url for post request
		:rtype: str
		"""
		if update_status:
			return f"{self.root.af_url}/api/v2.2/events/{channel}?subChannel={sub_channel}&status={update_status}"
		else:
			return f"{self.root.af_url}/api/v2.2/events/{channel}?subChannel={sub_channel}"


	def __create_url_for_update(self, extid, channel, update_status):
		return f"{self.root.af_url}/api/v2.2/events/{channel}/{extid}?status={update_status}"

	def create(self, body,channel=None, sub_channel=None, update_status=None,sess=None, timeout=1):
		"""Doing a post request to createEvent.

		Combining all the previous methods we are creating a request to AF.
			In answer from AF there is `ext_id` that is used in `CybertonicaAPI.afclient.AFClient.update` method.

		Args:
				body: body of post request.

		Returns:
				See CybertonicaAPI.Client.r
		"""
		string_body = json.dumps(body)
		headers = self.__create_headers(self.root.api_user_id, self.root.api_signature, string_body)
		url = self.__create_url(body['channel'], body['sub_channel'], update_status)
		if sess:
			r = sess.post(url, headers=headers, data=string_body, timeout=timeout, verify=self.root.verify)
		else:
			return self.root.r(method='POST', url=url, headers=headers, body=string_body, verify=self.root.verify)
		return r.status_code, r.text

	def update(self,channel,extid,status,body,sess=None,timeout=1):
		"""Doing a post update with extid.

		Args:
				extid: value of extid.
				status: value of status

		Returns:
				See CybertonicaAPI.Client.r
		"""
		string_body = json.dumps(body)
		headers = self.__create_headers(self.root.api_user_id,self.root.api_signature,string_body)
		url = self.__create_url_for_update(extid,channel,status)
		if sess:
			r = sess.put(url,headers=headers,data = string_body,timeout=timeout, verify=self.root.verify)
		else:
			return self.root.r(method='PUT', url=url,headers=headers, body=string_body, verify=self.root.verify)
		return r.status_code,r.text
