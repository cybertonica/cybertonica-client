import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from CybertonicaAPI.src.auth         import Auth
from CybertonicaAPI.src.events       import Event
from CybertonicaAPI.src.channels     import Channel
from CybertonicaAPI.src.sub_channels import SubChannel
from CybertonicaAPI.src.policies     import Policy
from CybertonicaAPI.src.lists        import List #include Item

def r(method=None,url=None,body=None,headers=None,files=None):
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
    r = requests.request(method=method,url=url,data=body,headers=headers,files=files)
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
    def __init__(self, scheme, host, key, team, login, password):
        self.url  = f'{scheme}://{host}'

        self.auth = Auth(self.url,r)

        self.token    = self.auth.login(login,team,password)[1]['token']
        self.headers  = {
            'content-type'  : 'application/json;charset=utf-8',
            'apiUserId'     : team,
            'apiSignature'  : key,
            'Connection'    :  'keep-alive',
            "Authorization" : f'Bearer {self.token}'
        }

        self.events = Event(self.url,r,self.headers)
        self.channels = Channel(self.url,r,self.headers)
        self.sub_channels = SubChannel(self.url,r,self.headers)
        self.policies = Policy(self.url,r,self.headers)
        self.lists = List(self.url,r,self.headers)