import json

class Policy:
    '''
    Policy class

    :param url: base url (see ../client.py)
    :type url: str
    :param do: function 'r', that sends requests (see ../client.py)
    :type do: function
    '''

    def __init__(self, url, do, headers, verify):
        self.base_url = url
        self.do = do
        self.headers = headers
        self.verify = verify

    def get_all(self):
        '''
        Get all Policies

        Method: GET
        Endpoint: /api/v1/policies

        '''
        url = f'{self.base_url}/api/v1/policies'
        headers = self.headers
        data = None
        return self.do('GET',url,data,headers,verify=self.verify)

    def get(self,id):
        '''
        Get policy by ID

        Method: GET
        Endpoint: /api/v1/policies/{id}
        '''
        url = f'{self.base_url}/api/v1/policies/{id}'
        headers = self.headers
        data = None
        return self.do('GET',url,data,headers,verify=self.verify)

    def get_by_name(self,name):
        policies = json.loads(self.get_all())
        target = None
        for i in policies:
            if i['name'] == name:
                target = i
                break
        return target

    def create(self,data):
        '''
        Create policy

        Method: POST
        Endpoint: /api/v1/policies
        '''
        url = f'{self.base_url}/api/v1/policies'
        headers = self.headers
        data = json.dumps(data)
        return self.do('POST',url,data,headers,verify=self.verify)

    def update(self,id,data):
        '''
        Update policy by ID

        Method: PUT
        Endpoint: /api/v1/policies/{id}
        '''
        url = f'{self.base_url}/api/v1/policies/{id}'
        headers = self.headers
        data = json.dumps(data)
        return self.do('PUT',url,data,headers,verify=self.verify)

    def remove(self,id):
        '''
        Remove policy by ID

        Method: DELETE
        Endpoint: /api/v1/policies/{id}
        '''
        url = f'{self.base_url}/api/v1/policies/{id}'
        headers = self.headers
        data = None
        return self.do('DELETE',url,data,headers,verify=self.verify)