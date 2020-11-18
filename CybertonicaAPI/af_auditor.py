from CybertonicaAPI.af_generator import GeneratorEvents
import hashlib
import json
import base64
import requests
import hmac
import traceback

class AFCheckProtocol:
	def __init__(self, root):
		self.root = root
		self.channels = (
			'global',
			'session',
			'payment',
			'acquiring',
			'card2card',
			'invoice',
			'p2p_money_transfer',
			'login',
			'access_control_change',
			'email'
		)
		self.sub_channel = 'sys'
		self.fields = ('all','requiered')
		
		self.expected_values = {
			'v2.2':{
				'id': '',  # filled in test
				'channel': '',  # filled in test
				'action': 'ALLOW',
				'score': 0,
				'rules': ['Default'],
				'comments': ['from Default'],
				'tags': [],
				'queues': []
			},
			'v2.1':{
				"action":"ALLOW",
				"reason":"from Default",
				"risk_score":0,
				"rule_score":0,
				"tags":[],
				"tx_id":"" # filled in test
				}
			}

	def run(self):
		'''
		Launches smoke testing of the anti-fraud system for V2.2 and v2.1 protocols.
		'''
		print('The test v2.2 protocol (%s) was launched ...' % self.root.af_url)
		self.__test_v22()
		print('v2.2 - DONE')
		print('The test v2.1 protocol (%s) was launched ...' % self.root.af_url)
		self.__test_v21()
		print('v2.1 - DONE')

	def __push_create_event(self, channel, sub_channel, field):
		event = self.root.af.box.pull_create_event(channel,self.sub_channel,field)
		status, data = self.root.af.create(event,channel,sub_channel)
		if self.root.af_version == 'v2.1':
			data = json.loads(data)
		return status, data
		
	def __test_v22(self):
		for channel in self.channels:
			for field in self.fields:
				prefix_error = '[CREATE] %s-%s with %s fields:' % (channel, self.sub_channel, field)
				event = self.root.af.box.pull_create_event(channel,self.sub_channel,field)
				status, data = self.__push_create_event(channel, self.sub_channel, field)

				assert status == 200, '%s BAD STATUS CODE' % prefix_error
				assert data, '%s DATA IS EMPTY' % prefix_error
				assert isinstance(data, dict), '%s DATA TYPE IS NOT CORRECT' % prefix_error
				assert data.keys() ==  self.expected_values[self.root.af_version].keys(), '%s DATA WITH BAD STRUCTURE' % prefix_error

				prefix_error = '[UPDATE] %s-%s with %s fields:' % (channel, self.sub_channel, field)

				update = self.root.af.box.pull_update_event()
				status, data = self.root.af.update('channel',data['id'],'SETTLED', update)

				assert status == 200, '%s BAD STATUS CODE' % prefix_error
				assert data is None, '%s BAD DATA' % prefix_error

	def __test_v21(self):
		self.root.af_version = 'v2.1'
		for channel in self.channels:
			for field in self.fields:
				prefix_error = '[CREATE] %s-%s with %s fields:' % (channel, self.sub_channel, field)
				event = self.root.af.box.pull_create_event(channel,self.sub_channel,field)
				status, data = self.__push_create_event(channel, self.sub_channel, field)

				assert status == 200, '%s BAD STATUS CODE' % prefix_error
				assert data, '%s DATA IS EMPTY' % prefix_error
				assert isinstance(data, dict), '%s DATA TYPE IS NOT CORRECT' % prefix_error
				assert data.keys() ==  self.expected_values[self.root.af_version].keys(), '%s DATA WITH BAD STRUCTURE' % prefix_error

				prefix_error = '[UPDATE] %s-%s with %s fields:' % (channel, self.sub_channel, field)

				update = self.root.af.box.pull_update_event(tx_id=data['tx_id'])
				status, data = self.root.af.update(channel,data['tx_id'],'FRAUD', update)

				assert status == 200, '%s BAD STATUS CODE' % prefix_error
				assert data  == 'OK', '%s BAD DATA' % prefix_error
