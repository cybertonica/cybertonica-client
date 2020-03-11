import json

class User:
    '''
    User class
    '''

    def __init__(self, root):
        self.root = root

    def get_all(self):
        '''
        Get all available users

        Method: GET
        Endpoint: /api/v1/users
        '''
        url = f'{self.root.url}/api/v1/users'
        return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)

    def get_by_id(self,id):
        '''
        Get user by ID

        Method: GET
        Endpoint: /api/v1/users/{id}

        :param id: user's ID
        :type id: str
        '''
        url = f'{self.root.url}/api/v1/subChannels/{str(id)}'
        return self.root.r('GET', url, body=None, headers=None, verify=self.root.verify)
    
    def create(self,data):
        '''
        Creating user by data

        Method: POST
        Endpoint: /api/v1/users

        :param data: data of new user
        :type data: dict
        '''
        url = f'{self.root.url}/api/v1/users'
        data = json.dumps(data)
        return self.root.r('POST', url, data, headers=None, verify=self.root.verify)

    def update(self,id,data):
        '''
        Updating user by ID

        Method: PUT
        Endpoint: /api/v1/users/{id}

        :param id: user's ID
        :type id: str
        :param data: new data for the user
        :type data: dict
        '''
        url = f'{self.root.url}/api/v1/users/{id}'
        data = json.dumps(data)
        return self.root.r('PUT', url, data, headers=None, verify=self.root.verify)

    def delete(self,id):
        '''
        Removing user by ID

        Method: DELETE
        Endpoint: /api/v1/users/{id}

        :param id: user's ID
        :type id: str
        '''
        url = f'{self.root.url}/api/v1/subChannels/{str(id)}'
        return self.root.r('DELETE', url, body=None, headers=None, verify=self.root.verify)
