import json
from types import FunctionType, LambdaType

class Auth:
    '''
    Authorization and another actions class
    '''
    def __init__(self, root):
        self.root = root

    def login(self, api_user, api_user_key_hash):
        '''
        Create web session

        Method: POST
        Endpoint: /api/v1/login

        :param api_user: user's login
        :type api_user: str
        :param api_user: user's password hash #TODO
        :type api_user: str
        '''
        url = f'{self.root.url}/api/v1/login'
        data = json.dumps({
            "apiUser" : api_user,
            "team"    : self.root.team,
            "apiUserKeyHash" : api_user_key_hash
        })
        headers = {"content-type" : "application/json"}
        status_code, data = self.root.r('POST',url,data,headers,verify=self.root.verify)
        if status_code == 200 or status_code == 201:
            self.root.token = data['token']
        return (status_code, data)

    def logout(self):
        '''
        Drop web session

        Method: POST
        Endpoint: /api/v1/logout
        '''
        url = f'{self.root.url}/api/v1/logout'
        headers = {
            "content-type" : "application/json",
            "Authorization": f"Bearer {self.root.token}"}
        data = None
        status_code, data = self.root.r('POST',url,data,headers,verify=self.root.verify)
        if status_code < 400:
            self.root.token = ''
        return (status_code, data)
    
    def relogin_as(self, api_user, api_user_key_hash):
        self.logout()
        status, data = self.login(api_user,api_user_key_hash)
        return (status, data)
   
    def recovery_password(self,email):
        '''
        Recover password

        Method: GET
        Endpoint: /api/v1/recovery/{team}/{email adderss}

        :param email: user's email
        :type email: str
        '''
        url = f'{self.root.url}/api/v1/recovery/request?team={self.root.team}&email={email}'
        headers = {"content-type" : "application/json"}
        data = None
        return self.root.r('GET',url,data,headers,verify=self.root.verify)

    # def register(self,data):
    #     '''
    #     Create new user with default role

    #     Method: POST
    #     Endpoint: /api/v1/registration

    #     :param data: new user data
    #     :type data: dict
    #     '''
    #     url = f'{self.base_url}/api/v1/registration'
    #     headers = {"content-type" : "application/json"}
    #     if "inivitedAt" not in data:
    #         data["inivitedAt"] = 0
    #     if "updatedAt" not in data:
    #         data["updatedAt"] = 0
    #     data = json.dumps(data)
    #     return self.do('POST',url,data,headers,verify=self.verify)

    # def create_team(self,data,token):
    #     '''
    #     Create team

    #     Method: POST
    #     Endpoint: /api/v1/team

    #     :param data: new team data
    #     :type data: dict
    #     :param token: user's token from login()['token']
    #     :type token: str
    #     '''
    #     url = f'{self.base_url}/api/v1/team'
    #     headers = {
    #         "content-type" : "application/json",
    #         "Authorization": "Bearer " + token
    #     }
    #     data = json.dumps(data)
    #     return self.do('POST',url,data,headers,verify=self.verify)