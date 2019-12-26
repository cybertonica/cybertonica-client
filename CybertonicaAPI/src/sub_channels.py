import json

class SubChannel:
    '''
    Sub-channel class

    :param url: base url (see ../client.py)
    :type url: str
    :param do: function 'r', that sends requests (see ../client.py)
    :type do: function
    '''

    def __init__(self,url,do,headers):
        self.do = do
        self.base_url = url
        self.headers = headers

    def get_all(self):
        '''
        Get all available sub-channels

        Method: GET
        Endpoint: /api/v1/subChannels
        '''
        url = f'{self.base_url}/api/v1/subChannels'
        headers = self.headers
        data = None
        return self.do('GET', url, data, headers)

    def get(self,id):
        '''
        Get sub-channel by ID

        Method: GET
        Endpoint: /api/v1/subChannels/{id}

        :param id: sub-channel's ID
        :type id: str
        '''
        url = f'{self.base_url}/api/v1/subChannels/{id}'
        headers = self.headers
        data = None
        return self.do('GET', url, data, headers)

    def create(self,data):
        '''
        Creating sub-channel by data

        Method: GET
        Endpoint: /api/v1/subChannels

        :param data: data of new sub-channel
        :type data: dict
        '''
        url = f'{self.base_url}/api/v1/subChannels'
        headers = self.headers
        data = json.dumps(data)
        return self.do('POST', url, data, headers)

    def update(self,id,data):
        '''
        Updating sub-channel by ID

        Method: PUT
        Endpoint: /api/v1/subChannels/{id}

        :param id: sub-channel's ID
        :type id: str
        :param data: new data for the sub-channel
        :type data: dict
        '''
        url = f'{self.base_url}/api/v1/subChannels/{id}'
        headers = self.headers
        data = json.dumps(data)
        return self.do('PUT', url, data, headers)


    def remove(self,id):
        '''
        Removing sub-channel by ID

        Method: DELETE
        Endpoint: /api/v1/subChannels/{id}

        :param id: sub-channel's ID
        :type id: str
        '''
        url = f'{self.base_url}/api/v1/subChannels/{id}'
        headers = self.headers
        data = None
        return self.do('DELETE', url, data, headers)
