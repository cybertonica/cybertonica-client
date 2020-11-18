from CybertonicaAPI.af_generator import GeneratorEvents as Box
import os
import sys
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitGenerator(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.root = PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			af_version='v2.2'
			)
		cls.box = Box(cls.root)
		
	def test_client_object_creation(self):
		self.assertIsInstance(self.box, Box)

		self.assertFalse('__generate' in dir(self.box))
		self.assertTrue('pull_create_event' in dir(self.box))
		self.assertTrue('pull_update_event' in dir(self.box))
		self.assertFalse('__get_random_cart' in dir(self.box))
		self.assertTrue('get_random_cart' not in dir(self.box))
		
		channels = self.box._GeneratorEvents__generate().keys()
		for channel in channels:
			if channel == 'p2p_money_transfer':
				channel = 'p2p'
			if channel == 'access_control_change':
				channel = 'access'
			self.assertTrue('create_%s' % channel in dir(self.box))
	
	def test_attributes_inside_client_object(self):
		self.assertTrue(hasattr(self.box, 'fields'))
		self.assertTrue(hasattr(self.box, 'allowed_channels'))
		self.assertTrue(hasattr(self.box, 'root'))
	
	def test_types_of_fields_inside_client_object(self):
		self.assertIsInstance(self.box.fields, str)
		self.assertIsInstance(self.box.root, MagicMock)
	
	def test_values_of_fields_inside_client_object(self):
		self.assertTrue(self.box.fields, 'all')
		self.assertTrue(
			self.box.allowed_channels,
			self.box._GeneratorEvents__generate().keys()
		)
		self.assertTrue(self.box.root, self.root)


class TestStructure(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.root = PropertyMock(
			url='test_url',
			team='test_team',
			signature='test_signature',
			token='old_value',
			verify=True,
			af_version='v2.2'
			)
		cls.box = Box(cls.root)

	def create_structure_mock(self, af_version):
		default = set([])
		update  = set(['comment','code', 'status', 't'])
		if af_version == 'v2.1':
			default = set(['channel','sub_channel'])
			update = set([
				'comment',
				'code',
				'status',
				'is_authed',
				'extid',
				'tx_id'
			])

		global_requiered = set([])
		global_all = set([
						't','timezone','extid','tid',
						'ip', 'ext_fraud_score','query'])

		session_requiered = set(['tid'])
		session_all = set(['tid'])

		payment_requiered = set([
						'src_id','src_parent','dst_id',
						'dst_parent','amount','exp','currency'])
		payment_all = payment_requiered | set([
						'src_partner','src_client_id',
						'dst_partner','dst_client_id'])

		acquiring_requiered = set(['exp_date'])
		acquiring_all = acquiring_requiered | set([
						'mcc','shipping_address','zipcode',
						'is_3ds_enabled','is_recurrent','cart',
						'email','phonenumber'])

		card2card_requiered = set([])
		card2card_all = card2card_requiered | set([
						'is_3ds_enabled','src_exp_date','src_email',
						'src_billing_address','src_zipcode',
						'src_phonenumber','src_fullname',
						'src_birthdate','dst_exp_date',
						'dst_billing_address','dst_zipcode',
						'dst_email','dst_phonenumber','dst_fullname',
						'dst_birthdate'])

		p2p_requiered = set(['src_partner','dst_partner','operation_type'])
		p2p_all = p2p_requiered | set([
					'system_name','sender_phonenumber','src_pos_city',
					'src_pos_id','src_pos_country','receiver_phonenumber',
					'dst_pos_city','dst_pos_id','dst_pos_country'])
					#not implemented
					# 'receiver_info_hash',
					# 'receiver_info',
					# 'sender_info_hash',
					# 'sender_info'

		invoice_requiered = set([]) # new fields does not exist
		invoice_all = invoice_requiered| set(['shipping_address','zipcode','cart'])

		login_requiered = set(['login'])
		login_all = login_requiered |  set([
					'email','phonenumber','imsi_number',
					'oauth_system','2FAused'])

		access_requiered = set(['dst_id','dst_parent'])
		access_all = access_requiered | set([
						'email','phonenumber','imsi_number',
						'2FA_used'])

		email_requiered = set(['src_id','dst_id','subject'])
		email_all = email_requiered | set(['contentType','body','is_encrypted'])
					#not implemented
					#'attachments_size',
					#'attachments'
		
		return {
			'global':{
				'requiered': default | global_requiered,
				'all':  default | global_requiered | global_all
			},
			'session':{
				'requiered':  default  | global_requiered | session_requiered,
				'all': default | global_all | session_all
			},
			'payment':{
				'requiered': default | global_requiered | payment_requiered,
				'all':  default | global_all | payment_all
			},
			'acquiring':{
				'requiered': default | global_requiered | payment_requiered | acquiring_requiered,
				'all': default | global_all | payment_all | acquiring_all
			},
			'card2card':{
				'requiered': default | global_requiered | payment_requiered | card2card_requiered,
				'all': default | global_all | payment_all | card2card_all
			},
			'p2p_money_transfer':{
				'requiered': default | global_requiered | payment_requiered | p2p_requiered,
				'all': default | global_all | payment_all | p2p_all
			},
			'invoice':{
				'requiered': default | global_requiered | payment_requiered | invoice_requiered,
				'all': default | global_all | payment_all | invoice_all
			},
			'login':{
				'requiered': default | global_requiered | login_requiered,
				'all': default | global_all | login_all
			},
			'access_control_change':{
				'requiered': default | global_requiered | access_requiered,
				'all':  default | global_all | access_all
			},
			'email':{
				'requiered': default | global_requiered | email_requiered,
				'all':  default | global_all | email_all
			},
			'update': update
		}

	def test_event_structure_v22(self):
		expected = self.create_structure_mock(af_version='v2.2')
		channels = self.box._GeneratorEvents__generate().keys()
		self.box.root.af_version = 'v2.2' # # manual change af version to v2.2
		for channel in channels:
			for field in ('all','requiered'):
				actual = set(self.box.pull_create_event(channel,'sys',field).keys())
				self.assertTrue(actual == expected[channel][field])
		
	def test_event_structure_v21(self):
		expected = self.create_structure_mock(af_version='v2.1')
		channels = self.box._GeneratorEvents__generate().keys()
		self.box.root.af_version = 'v2.1' # manual change af version to v2.1
		for channel in channels:
			for field in ('all','requiered'):
				actual = set(self.box.pull_create_event(channel,'sys',field).keys())
				self.assertTrue(actual == expected[channel][field])
	
	def test_update_structure_v22(self):
		expected = self.create_structure_mock(af_version='v2.2')['update']
		self.box.root.af_version = 'v2.2' # # manual change af version to v2.2
		actual = set(self.box.pull_update_event().keys())
		self.assertTrue(actual == expected)
	
	def test_update_structure_v21(self):
		expected = self.create_structure_mock(af_version='v2.1')['update']
		self.box.root.af_version = 'v2.1' # # manual change af version to v2.1
		actual = set(self.box.pull_update_event(extid='test').keys())
		self.assertTrue(actual == expected)
	
	def test_get_update_for_v21_without_extid(self):
		self.box.root.af_version = 'v2.1' # # manual change af version to v2.1
		with self.assertRaisesRegex(AssertionError, 'extid or tx_id must be present for v2.1'):
			self.box.pull_update_event()