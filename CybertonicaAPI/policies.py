import json

class Policy:
    '''
    Policy class

    :param url: base url (see ../client.py)
    :type url: str
    :param do: function 'r', that sends requests (see ../client.py)
    :type do: function
    '''

    def __init__(self, root):
        self.root = root

    def get_all(self):
        '''
        Get all Policies

        Method: GET
        Endpoint: /api/v1/policies

        '''
        url = f'{self.root.url}/api/v1/policies'
        return self.root.r('GET',url,body=None,headers=None,verify=self.root.verify)

    def get_by_id(self,id):
        '''
        Get policy by ID

        Method: GET
        Endpoint: /api/v1/policies/{id}
        '''
        url = f'{self.root.url}/api/v1/policies/{id}'
        return self.root.r('GET',url,body=None,headers=None,verify=self.root.verify)

    def create(self,data):
        '''
        Create policy

        Method: POST
        Endpoint: /api/v1/policies
        '''
        url = f'{self.root.url}/api/v1/policies'
        data = json.dumps(data)
        return self.root.r('POST',url,data,headers=None,verify=self.root.verify)

    def update(self,id,data):
        '''
        Update policy by ID

        Method: PUT
        Endpoint: /api/v1/policies/{id}
        '''
        url = f'{self.root.url}/api/v1/policies/{id}'
        data = json.dumps(data)
        return self.root.r('PUT',url,data,headers=None,verify=self.root.verify)

    def delete(self,id):
        '''
        Remove policy by ID

        Method: DELETE
        Endpoint: /api/v1/policies/{id}
        '''
        url = f'{self.root.url}/api/v1/policies/{id}'
        return self.root.r('DELETE',url,body=None,headers=None,verify=self.root.verify)