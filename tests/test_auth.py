from CybertonicaAPI.auth import Auth
import os
import sys
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock

sys.path.append(os.getcwd())


class TestInitAuthClass(unittest.TestCase):

    def setUp(self):
        self.auth = Auth(PropertyMock(
            url='test_url',
            team='test_team',
            signature='test_signature',
            token='old_value',
            verify=True,
            r=Mock(return_value=(200, {'token': '123'}))
        ))

    def test_client_object_creation(self):
        self.assertIsInstance(self.auth, Auth)

        self.assertTrue("login" in dir(self.auth))
        self.assertTrue("logout" in dir(self.auth))
        self.assertTrue("relogin_as" in dir(self.auth))
        self.assertTrue("recovery_password" in dir(self.auth))
        self.assertTrue("register" in dir(self.auth))

    def test_attributes_inside_auth_object(self):
        self.assertTrue(hasattr(self.auth, 'root'))

    def test_types_of_fields_inside_auth_object(self):
        self.assertIsInstance(self.auth.root, object)


class TestLoginMethod(unittest.TestCase):

    def setUp(self):
        self.auth = Auth(PropertyMock(
            url='test_url',
            team='test_team',
            signature='test_signature',
            token='old_value',
            verify=True,
            r=Mock(return_value=(200, {'token': '123'}))
        ))
        self.login = 'test_login'
        self.password = 'test_password'

    def test_login_sends_post_request(self):
        self.auth.login(self.login, self.password)
        self.assertTrue('POST' in self.auth.root.r.call_args[0])

    def test_login_builds_correct_url_and_endpoint(self):
        expected_url = f'{self.auth.root.url}/api/v1/login'
        self.auth.login(self.login, self.password)
        self.assertTrue(expected_url in self.auth.root.r.call_args[0])

    def test_login_builds_correct_data(self):
        expected_json_string = json.dumps({
            "apiUser": self.login,
            "team": self.auth.root.team,
            "apiUserKeyHash": self.password
        })
        self.auth.login(self.login, self.password)
        self.assertTrue(expected_json_string in self.auth.root.r.call_args[0])

    def test_login_builds_correct_headers(self):
        expected_headers = {"content-type": "application/json"}
        self.auth.login(self.login, self.password)
        self.assertTrue(expected_headers in self.auth.root.r.call_args[0])

    def test_login_sends_verify_flag_same_as_in_the_client(self):
        expected_flag = self.auth.root.verify
        self.auth.login(self.login, self.password)
        self.assertTrue(expected_flag ==
                        self.auth.root.r.call_args[-1:][0]['verify'])

    def test_login_method_changes_client_token_if_code_is_200(self):
        self.auth.login(self.login, self.password)
        self.assertEqual(self.auth.root.token, '123')

    def test_login_method_changes_client_token_if_code_is_201(self):
        self.auth.root.r = Mock(return_value=(201, {'token': '123'}))
        self.auth.login(self.login, self.password)
        self.assertEqual(self.auth.root.token, '123')

    def test_login_method_does_not_change_client_token_if_code_is_not_200_201(self):
        self.auth.root.r = Mock(return_value=(401, {'token': '123'}))
        expected_token = self.auth.root.token
        self.auth.login(self.login, self.password)
        self.assertEqual(self.auth.root.token, expected_token)


class TestLogoutMethod(unittest.TestCase):

    def setUp(self):
        self.auth = Auth(PropertyMock(
            url='test_url',
            team='test_team',
            signature='test_signature',
            token='old_value',
            verify=True,
            r=Mock(return_value=(200, {'token': '123'}))
        ))

    def test_logout_sends_post_request(self):
        self.auth.logout()
        self.assertTrue('POST' in self.auth.root.r.call_args[0])

    def test_logout_builds_correct_url_and_endpoint(self):
        expected_url = f'{self.auth.root.url}/api/v1/logout'
        self.auth.logout()
        self.assertTrue(expected_url in self.auth.root.r.call_args[0])

    def test_logout_builds_correct_data(self):
        self.auth.logout()
        self.assertTrue(None in self.auth.root.r.call_args[0])

    def test_logout_builds_correct_headers(self):
        expected_headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.auth.root.token}"}
        self.auth.logout()
        self.assertTrue(expected_headers in self.auth.root.r.call_args[0])

    def test_logout_sends_verify_flag_same_as_in_the_client(self):
        expected_flag = self.auth.root.verify
        self.auth.logout()
        self.assertTrue(expected_flag ==
                        self.auth.root.r.call_args[-1:][0]['verify'])

    def test_logout_clears_client_token_if_status_less_400(self):
        expected_token = ''
        self.auth.logout()
        self.assertEqual(self.auth.root.token, expected_token)

    def test_logout_does_not_clear_client_token_if_status_400_and_more(self):
        self.auth.root.r = Mock(return_value=(401, {'token': '123'}))
        expected_token = self.auth.root.token
        self.auth.logout()
        self.assertEqual(self.auth.root.token, expected_token)


class TestRecoveryPasswordMethod(unittest.TestCase):

    def setUp(self):
        self.auth = Auth(PropertyMock(
            url='test_url',
            team='test_team',
            signature='test_signature',
            token='old_value',
            verify=True,
            r=Mock(return_value=(200, {'token': '123'}))
        ))
        self.test_email = 'test@email.com'

    def test_recovery_sends_get_request(self):
        self.auth.recovery_password(self.test_email)
        self.assertTrue('GET' in self.auth.root.r.call_args[0])

    def test_recovery_builds_correct_url_and_endpoint(self):
        expected_url = f'{self.auth.root.url}/api/v1/recovery/request?team={self.auth.root.team}&email={self.test_email}'
        self.auth.recovery_password(self.test_email)
        self.assertTrue(expected_url in self.auth.root.r.call_args[0])

    def test_recovery_builds_correct_data(self):
        self.auth.recovery_password(self.test_email)
        self.assertTrue(None in self.auth.root.r.call_args[0])

    def test_recovery_builds_correct_headers(self):
        self.auth.recovery_password(self.test_email)
        expected_headers = {
            "content-type": "application/json",
        }
        self.assertTrue(expected_headers in self.auth.root.r.call_args[0])

    def test_recovery_sends_verify_flag_same_as_in_the_client(self):
        self.auth.logout()
        expected_flag = self.auth.root.verify
        self.assertTrue(expected_flag ==
                        self.auth.root.r.call_args[-1:][0]['verify'])


class TestRegisterMethod(unittest.TestCase):

    def setUp(self):
        self.auth = Auth(PropertyMock(
            url='test_url',
            team='test_team',
            signature='test_signature',
            token='old_value',
            verify=True,
            r=Mock(return_value=(200, {'token': '123'}))
        ))
        self.user_data = {
            "email": "test@email.com",
            "password": "test_password",
            "team": "test_team",
            "firstName": "John",
            "lastName": "Smith",
            "login": "jsmith"
        }

    def test_register_sends_post_request(self):
        self.auth.register(self.user_data)
        self.assertTrue('POST' in self.auth.root.r.call_args[0])

    def test_register_builds_correct_url_and_endpoint(self):
        expected_url = f'{self.auth.root.url}/api/v1/registration'
        self.auth.register(self.user_data)
        self.assertTrue(expected_url in self.auth.root.r.call_args[0])

    def test_register_builds_correct_data_without_dates(self):
        self.auth.register(self.user_data)
        self.user_data['invitedAt'] = 0
        self.user_data['updatedAt'] = 0
        expected_data = json.dumps(self.user_data)
        self.assertTrue(expected_data in self.auth.root.r.call_args[0])

    def test_register_builds_correct_data_with_invitedAt_field(self):
        self.user_data['invitedAt'] = 100
        self.auth.register(self.user_data)
        self.user_data['updatedAt'] = 0
        expected_data = json.dumps(self.user_data)
        self.assertTrue(expected_data in self.auth.root.r.call_args[0])

    def test_register_builds_correct_data_with_updatedAt_field(self):
        self.user_data['updatedAt'] = 100
        self.auth.register(self.user_data)
        self.user_data['invitedAt'] = 0
        expected_data = json.dumps(self.user_data)
        self.assertTrue(expected_data in self.auth.root.r.call_args[0])

    def test_register_builds_correct_headers(self):
        expected_headers = {
            "content-type": "application/json",
        }
        self.auth.register(self.user_data)
        self.assertTrue(expected_headers in self.auth.root.r.call_args[0])

    def test_register_sends_verify_flag_same_as_in_the_client(self):
        expected_flag = self.auth.root.verify
        self.auth.logout()
        self.assertTrue(expected_flag ==
                        self.auth.root.r.call_args[-1:][0]['verify'])


class TestReloginMethod(unittest.TestCase):

    def setUp(self):
        self.auth = Auth(PropertyMock(
            url='test_url',
            team='test_team',
            signature='test_signature',
            token='old_value',
            verify=True,
            r=Mock(return_value=(200, {'token': '123'}))
        ))
        self.login = 'test_login'
        self.password = 'test_password'

    @patch('CybertonicaAPI.auth.Auth.login', return_value=(200, {'token': '123'}))
    @patch('CybertonicaAPI.auth.Auth.logout', return_value=(200, {'token': '123'}))
    def test_relogin_called_logout_and_login_once(self, mock_login, mock_logout):
        self.auth.relogin_as(self.login, self.password)
        mock_login.assert_called_once()
        mock_logout.assert_called_once()

    @patch('CybertonicaAPI.auth.Auth.logout', return_value=(200, {'token': '123'}))
    @patch('CybertonicaAPI.auth.Auth.login', return_value=(200, {'token': '123'}))
    def test_relogin_called_login_with_correct_params(self, mock_login, mock_logout):
        self.auth.relogin_as(self.login, self.password)
        self.assertTrue(self.login in mock_login.call_args[0])
        self.assertTrue(self.password in mock_login.call_args[0])
