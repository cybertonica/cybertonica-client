import json

class List:
    '''
    List class

    :param url: base url (see ../client.py)
    :type url: str
    :param do: function 'r', that sends requests (see ../client.py)
    :type do: function
    '''
    def __init__(self, root):
        self.root = root
        # self.items = Item(root)

    def get_all(self):
        '''
        Get all Policies

        Method: GET
        Endpoint: /api/v1/lists
        '''
        url = f'{self.root.url}/api/v1/lists'
        return self.root.r('GET',url,body=None,headers=None,verify=self.root.verify)

    def get_by_id(self, id):
        '''
        Get list by ID

        Method: GET
        Endpoint: /api/v1/lists/{id}

        :param id: list id
        :type id: str
        '''
        url = f'{self.root.url}/api/v1/lists/{id}'
        return self.root.r('GET',url,body=None,headers=None,verify=self.root.verify)

    def create(self, data):
        '''
        Create list by data

        Method: POST
        Endpoint: /api/v1/lists

        :param data: new list data
        :type data: dict
        '''
        url = f'{self.root.url}/api/v1/lists'
        data = json.dumps(data)
        return self.root.r('POST',url,data,headers=None,verify=self.root.verify)

    def update(self, id, data):
        '''
        Update list by ID

        Method: PUT
        Endpoint:  /api/v1/lists/{id}

        :param id: list id
        :type id: str
        :param data: new list data
        :type data: dict
        '''
        url = f'{self.root.url}/api/v1/lists/{id}'
        data = json.dumps(data)
        return self.root.r('PUT',url,data,headers=None,verify=self.root.verify)

    def delete(self, id):
        '''
        Remove list by ID

        Method: DELETE
        Endpoint: /api/v1/lists/{id}

        :param id: list id
        :type id: str
        '''
        url = f'{self.root.url}/api/v1/lists/{id}'
        return self.root.r('DELETE',url,body=None,headers=None,verify=self.root.verify)

    def import_csv(self, id, csv_filename):
        '''
        Import CSV file to the list

        Method: POST
        Endpoint: /api/v1/lists/import/{id}/csv

        :param id: list id
        :type id: str
        :param csv_file: filename(or path) for the uploading
        :type csv_file: str
        '''
        url = f'{self.root.url}/api/v1/lists/import/{id}/csv'
        files = {'file': open(csv_filename,'rb')}
        return self.root.r('POST',url,body=None,headers=None,files=files,verify=self.root.verify)

    def export_csv(self, id, output):
        '''
        Export CSV file from the list

        Method: GET
        Endpoint: /api/v1/lists/export/{id}/csv

        :param id: list id
        :type id: str
        :param output: filename(or path) for the download
        :type output: str
        '''
        # status = False
        # try:
        #     url = f'{self.base_url}/api/v1/lists/export/{id}/csv'
        #     headers = self.headers
        #     files = None
        #     data = None
        #     r = self.do('GET',url,data,headers,files)
        #     open(output, 'wb').write(r[1].content)
        #     status = True
        # except Exception as err:
        #     print(f'{err}')
        # return status
        pass

# class Item:
#     '''
#     #TODO:
#     /api/v1/items/search/{pattern}/?limit={limit}   GET Search Items by pattern with limit default by 100
#     /api/v1/items/{list}/search/{pattern}/?limit={limit}    GET Search Items by pattern and list with limit default by 100
#     /api/v1/items/export/{id}/csv   GET Export current Items by id to csv
#     '''
#     '''
#     Item class

#     :param url: base url (see ../client.py)
#     :type url: str
#     :param do: function 'r', that sends requests (see ../client.py)
#     :type do: function
#     '''
#     def __init__(self, url, do, headers, verify):
#         self.base_url = url
#         self.do = do
#         self.headers = headers
#         self.verify = verify

#     def get_all(self, lid):
#         '''
#         Get all items by list

#         Method: GET
#         Endpoint: /api/v1/items/{id}

#         :param lid: list id
#         :type lid: str
#         '''
#         url = f'{self.base_url}/api/v1/items/{lid}'
#         headers = self.headers
#         data = None
#         return self.do('GET',url,data,headers,verify=self.verify)

#     def get_by_id(self, lid, id):
#         '''
#         Get item by ID from list

#         Method: GET
#         Endpoint: /api/v1/items/{list_id}/item/{id}

#         :param lid: list id
#         :type lid: str
#         :param id: item id
#         :type id: str
#         '''
#         url = f'{self.base_url}/api/v1/items/{lid}/item/{id}'
#         headers = self.headers
#         data = None
#         return self.do('GET',url,data,headers,verify=self.verify)

#     def get_all_alive(self, lid):
#         '''
#         Get all alive Items by list

#         Method: GET
#         Endpoint: /api/v1/items/{list_id}/alive

#         :param lid: list id
#         :type id: str
#         '''
#         url = f'{self.base_url}/api/v1/items/{lid}/alive'
#         headers = self.headers
#         data = None
#         return self.do('GET',url,data,headers,verify=self.verify)

#     def create(self, data):
#         '''
#         Create item by data

#         Method: POST
#         Endpoint: /api/v1/items

#         :param data: new item data
#         :type data: dict
#         '''
#         url = f'{self.base_url}/api/v1/items'
#         headers = self.headers
#         data = json.dumps(data)
#         return self.do('POST',url,data,headers,verify=self.verify)

#     def update(self, id, data):
#         '''
#         Update item by id

#         Method: PUT
#         Endpoint: /api/v1/items/{id}

#         :param id: item id
#         :type id: str
#         :param data: new item data
#         :type data: str
#         '''
#         url = f'{self.base_url}/api/v1/items/{id}'
#         headers = self.headers
#         data = json.dumps(data)
#         return self.do('PUT',url,data,headers,verify=self.verify)

#     def delete(self,id):
#         '''
#         Remove item by id

#         Method: DELETE
#         Endpoint: /api/v1/items/{id}

#         :param id: item id
#         :type id: str
#         '''
#         url = f'{self.base_url}/api/v1/items/{id}'
#         headers = self.headers
#         data = None
#         return self.do('DELETE',url,data,headers,verify=self.verify)