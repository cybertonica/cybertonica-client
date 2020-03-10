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

#local imports:
# from auth         import Auth
# from events       import Event
# from channels     import Channel
# from subchannels import SubChannel
# from policies     import Policy
# from lists        import List #include Item

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
    def __init__(self, scheme, host, team, key, verify=True):
        self.url  = f'{scheme}://{host}'
        self.verify = verify
        self.token = ''
        self.team = team
        self.signature = key
        
        self.auth = Auth(self)
        self.subchannels = SubChannel(self)
        self.lists = List(self)
        
        # self.events = Event(self.url, r, self.verify)
        # self.channels = Channel(self.url, r, self.verify)
        # self.sub_channels = SubChannel(self.url, r, self.verify)
        # self.policies = Policy(self.url, r, self.verify)
        

    def __create_headers(self):
        return {
            'content-type'  : 'application/json;charset=utf-8',
            'apiUserId'     : self.team,
            'apiSignature'  : self.signature,
            'Connection'    :  'keep-alive',
            'Authorization' : f'Bearer {self.token}'
        }
    
    def r(self, method=None, url=None, body=None, headers=None, files=None, verify=True):
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
        if not headers:
            headers = self.__create_headers()

        r = requests.request(method=method,url=url,data=body,headers=headers,files=files, verify=verify)
        json = None
        try:
            json = r.json()
        except: ##TODO: implemented raising Exceptions
            pass
        return (r.status_code,json)
    
    def set_role_for_apogee_user(self, user_data):
        '''
        '''
        url = f'{self.url}/api/v1/users'

        status, data = self.r(method='GET', url=url, verify=self.verify)

        target_user = data[0]
        url += f'/{target_user["id"]}'

        target_user["roles"] = ["FraudChiefOfficer"]

        status, data = self.r(method='PUT', url=url, body=json.dumps(target_user), verify=self.verify)

if __name__ == "__main__":
    pass






        

        

        





