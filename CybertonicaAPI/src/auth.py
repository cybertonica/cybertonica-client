import json
from types import FunctionType, LambdaType

class Auth:
    '''
    Authorization and another actions class.

    :param url: base url (see ../client.py)
    :type url: str
    :param do: function 'r', that sends requests (see ../client.py)
    :type do: function

    '''
    def __init__(self,url,do):
        assert (isinstance(do, FunctionType) or isinstance(do, LambdaType))
        assert isinstance(url,str) and url
        self.do = do
        self.base_url = url

    def login(self, api_user, team, api_user_key_hash):
        '''
        Create web session

        Method: POST
        Endpoint: /api/v1/login

        :param api_user: user's login
        :type api_user: str
        :param team: user's team (test,dev, etc.)
        :type team: str
        :param api_user: user's password hash #TODO
        :type api_user: str

        '''
        url = f'{self.base_url}/api/v1/login'
        data = json.dumps({
            "apiUser" :api_user,
            "team" :team,
            "apiUserKeyHash" :api_user_key_hash
        })
        headers = {"content-type" : "application/json"}
        return self.do('POST',url,data,headers)

    def logout(self,token):
        '''
        Drop web session

        Method: POST
        Endpoint: /api/v1/logout

        :param token: user's token
        :type token: str
        '''
        url = f'{self.base_url}/api/v1/logout'
        headers = {
            "content-type" : "application/json",
            "Authorization": f"Bearer {token}"}
        data = None
        return self.do('POST',url,data,headers)

    def recovery(self,team,email):
        '''
        Recover password

        Method: GET
        Endpoint: /api/v1/recovery/{team}/{email adderss}

        :param team: user's team
        :type team: str
        :param email: user's email
        :type email: str
        '''
        url = f'{self.base_url}/api/v1/recovery/{team}/{email}'
        headers = {"content-type" : "application/json"}
        data = None
        return self.do('GET',url,data,headers)

    def register(self,data):
        '''
        Create new user with default role

        Method: POST
        Endpoint: /api/v1/registration

        :param data: new user data
        :type data: dict
        '''
        url = f'{self.base_url}/api/v1/registration'
        headers = {"content-type" : "application/json"}
        if "inivitedAt" not in data:
            data["inivitedAt"] = 0
        if "updatedAt" not in data:
            data["updatedAt"] = 0
        data = json.dumps(data)
        return self.do('POST',url,data,headers)

    def create_team(self,data,token):
        '''
        Create team

        Method: POST
        Endpoint: /api/v1/team

        :param data: new team data
        :type data: dict
        :param token: user's token from login()['token']
        :type token: str
        '''
        url = f'{self.base_url}/api/v1/team'
        headers = {
            "content-type" : "application/json",
            "Authorization": "Bearer " + token
        }
        data = json.dumps(data)
        return self.do('POST',url,data,headers)