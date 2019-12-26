import json

class Channel:
    '''
    Channel class

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
        Get all available channels

        Method: GET
        Endpoint: /api/v1/subChannels/channels
        '''
        url =  f'{self.base_url}/api/v1/subChannels/channels'
        headers = self.headers
        data = None
        return self.do('GET',url,data,headers)