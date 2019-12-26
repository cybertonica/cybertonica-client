import json

class Event:
    '''
    Event class

    :param url: base url (see ../client.py)
    :type url: str
    :param do: function 'r', that sends requests (see ../client.py)
    :type do: function
    '''

    def __init__(self, url, do, headers):
        self.base_url = url
        self.do = do
        self.headers = headers

    def get_by_id_and_fk(self,id,fks):
        '''
        Get events by id and fks

        Method: GET
        Endpoint: /api/v1/events/?id={id}&fk={fk}
        '''
        url = f'{self.base_url}/api/v1/events/?id={id}&fk={fks}'
        headers = self.headers
        data = None
        return self.do('GET', url, data, headers)

    def get_by_id(self,id):
        '''
        Get event by id

        Method: GET
        Endpoint: /api/v1/events/{id}
        '''
        url = f'{self.base_url}/api/v1/events/{id}'
        headers = self.headers
        data = None
        return self.do('GET', url, data, headers)

    def get_by_queue(self,queue_name,start=0,limit=100):
        '''
        Get events by queue name, default values:
            start is 0
            limit is 100

        Method: GET
        Endpoint: /api/v1.1/events/queue/{queue_name}
        '''
        url = f'{self.base_url}/api/v1.1/events/queue/{queue_name}?start={str(start)}&limit={str(limit)}'
        headers = self.headers
        data = None
        return self.do('GET', url, data, headers)

    def get_by_ids_array(self,ids):
        '''
        Get events by ids array included by data

        Method: POST
        Endpoint: /api/v1/events/{queue}
        '''
        url = f'{self.base_url}/api/v1/events' #??? #TODO
        data = json.dumps(ids)
        headers = self.headers
        return self.do('POST',url,data,headers)
