import json

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #ignore SSL certificates

from CybertonicaAPI.auth         import Auth
from CybertonicaAPI.events       import Event
from CybertonicaAPI.channels     import Channel
from CybertonicaAPI.sub_channels import SubChannel
from CybertonicaAPI.policies     import Policy
from CybertonicaAPI.lists        import List #include Item


def r(method=None,url=None,body=None,headers=None,files=None, verify=True):
    '''
    Main function for the sending requests

    :param method: request's method (GET,POST,PUT, etc)
    :type methpd: str
    :param url: URL (<scheme>://<host>/<endpoint>..)
    :type url: str
    :param body: request's data (result after json.dumps())
    :type body: str
    :return: status code and JSON(if there is else None)
    :rtype: couple
    '''
    r = requests.request(method=method,url=url,data=body,headers=headers,files=files, verify=verify)
    json = None
    try:
        json = r.json()
    except: ##TODO: implemented raising Exceptions
        pass
    return (r.status_code,json)

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
    def __init__(self, scheme, host, key, team, login, password, auto_auth=True, verify=True):
        self.url  = f'{scheme}://{host}'
        self.verify = verify

        self.auth = Auth(self.url,r,verify)
        self.token = None
        self.headers = {
            'content-type'  : 'application/json;charset=utf-8',
            'apiUserId'     : team,
            'apiSignature'  : key,
            'Connection'    :  'keep-alive',
            'Authorization' : f'Bearer {str(self.token)}'
        }
        if auto_auth:
            self.token =  self.auth.login(login,team,password)[1]['token']
            self.headers['Authorization'] =f'Bearer {self.token}'
        

        self.events = Event(self.url,r,self.headers)
        self.channels = Channel(self.url,r,self.headers)
        self.sub_channels = SubChannel(self.url,r,self.headers, verify)
        self.policies = Policy(self.url,r,self.headers)
        self.lists = List(self.url,r,self.headers, verify)

    def create_new_team(self,team, login, password, custom_body={}):

        body = {
            "team": team,
            "password": password,
            "firstName": "Apogee",
            "lastName": "System",
            "email": "ochaplashkin@cybertonica.com",
            "login": "user"
        }
        if custom_body:
            body = custom_body

        headers = {
            'Authorization': 'Bearer 123',
            'Content-type': 'application/json'
        }
        url = f'{self.url}/api/v1/team'

        return r(method='POST',url=self.url,body=json.dumps(body),headers=headers,verify=self.verify)
    
    def set_role_for_apogee_user(self, user_data):
        '''
        '''
        url = f'{self.url}/api/v1/users'
        headers = self.headers

        status, data = r(method='GET', url=url, headers=headers, verify=self.verify)

        target_user_id = data[0]['id']
        url += f'/{target_user_id}'
        target_user_id["roles"] = ["FraudChiefOfficer"]

        status, data = r(method='PUT', url=url, body=json.dumps(user_data), headers=headers, verify=self.verify)

        self.auth.logout(self.token)
        self.auth.login(user_data['login'],user_data['team'],user_data['password'])

        

        





