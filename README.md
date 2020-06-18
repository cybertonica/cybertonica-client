<a href="https://cybertonica.com/">
    <img src="https://github.com/cybertonica/cybertonica-client/blob/master/ext/logo.png" alt="Cybertonica Ltd." title="Cybertonica" align="right" height="60" />
</a>

Cybertonica API client
======================
[![Python 3.6.9](https://img.shields.io/badge/python-3.6.9-blue.svg)](https://www.python.org/downloads/release/python-369/) ![version](https://img.shields.io/badge/version-0.1-blue) ![Stage: Alpha](https://img.shields.io/badge/stage-alpha-blueviolet)

## Table of content

- [Getting Started](#Getting-Started)
    - [Installing](#Installing)
    - [Usage](#Usage)
- [Code statuses description](#Code-statuses-description)
- [Client structure](#Client-structure)
- [For developers](#For-developers)
    
## Getting Started

The client is implemented via the Facade pattern, so the necessary function is called as follows:

```python
client.<module>.<sub_module>.function()
```
See client structure [below](#Client-structure)

### Installing

CybertonicaAPI client can be installed using [pip](https://pypi.org/project/pip/):

```sh
pip install git+https://github.com/cybertonica/cybertonica-client.git
```

To test that installation was successful, try:
```python
>>> from CybertonicaAPI import Client
>>> cbt = Client(url='https://test.cybertonica.com',team='test')
>>> status, data = cbt.auth.login('login', 'password')
>>> f'{status} | {cbt.token}'
'200 | 37d9c47b-4837-44db-9dbe-b5427eb70b43'
```

## Usage

```python
>>> from CybertonicaAPI import Client
>>> cbt = Client(url='https://test.cybertonica.com',team='test')
>>> status, data = cbt.auth.login('login', 'password')
>>> cbt.events.get_by_id('eve_global:8dd5fc24-3fc2-4e7c-a909-94afbe44931a')
(200, {'_cls': 'eve_global', 'channel': 'global', ... })
>>> cbt.lists.create({"name":"simple_list","kind":"WHITE"})
(201, {'createdAt': 1591179867918, 'createdBy': ... })
>>> cbt.lists.get_by_id('e166502a-8332-4317-9421-edd9dcca7694')
(200, {'createdAt': 1591179867918, 'createdBy': ... })
>>> cbt.lists.create("bad_structure")
AssertionError: The data type must be a dictionary
```
If you need to use Anti-Fraud subsystem API, add two parameters and send the event to the system:

```python
>>> from CybertonicaAPI import Client
>>> cbt = Client(url='https://test.cybertonica.com',team='test')
>>> cbt.api_user_id = 'api_user_id'
>>> cbt.api_signature = 'api_signature'
>>> cbt.af.create({"channel":"global","sub_channel":"sys"})
(200, {'action': 'ALLOW', 'channel': 'global', ...})
```
The client has logging. To see more detailed information about the client's work, do this:

```python
from CybertonicaAPI import Client
import logging

logging.basicConfig(level=logging.DEBUG)

cbt = Client(url='https://test.cybertonica.com',team='test')
# DEBUG:CybertonicaAPI.client:Client has been init with {'url': 'https://test.cybertonica.com', 'team': 'test'}

cbt.auth.login('login','password')
# DEBUG:CybertonicaAPI.client:Trying POST request to https://test.cybertonica.com/api/v1/login with body={"apiUser": "login", "team": "test", "apiUserKeyHash": "password_hash"} headers={'content-type': 'application/json'} files=None verify=False
```


Each class or method contains a docstring

```python
>>> print(cbt.__doc__)
Main Facade class. Contains all methods.
    Attributes:
        **settings: Set of settings for the class. It must contains a
            required parameters: `url`, `team`. If you want to use
            `CybertonicaAPI.afclient.AFClient` you should include
            `api_user_id` and `api_signature` to settings.

            url: target url of environment.
            team: value of team.
            custom_af_url: AFClient will use the specified address.
                          By default, the address is equal to a url with a port 7499.
            api_user_id: user id for AF.
            api_signature: value of signature for AF.
            verify: True, if you need to ignore SSL certificates.
            dev_mode: True, if you need enable hidden functions.
```
## Code statuses description
| Code  | Description |
| ------------- | ------------- |
| 201  | The request has been fulfilled, resulting in the creation of a new resource.  |
| 204  | The server successfully processed the request and is not returning any content.  |
| 400  | The server cannot or will not process the request due to an apparent client error.  |
| 401  | The authentication is required and has failed or has not yet been provided.  |
| 403  | The request was valid, but the server is refusing action. The user might not have the necessary permissions for a resource.  |
| 404  | The requested resource could not be found but may be available in the future.  |
| 409  | The request could not be processed because of conflict in the request, such as an edit conflict between multiple simultaneous updates.  |
| 423  | The resource that is being accessed is locked.  |
| 500  | There was an internal server error.  |
| 502  | The server was acting as a gateway or proxy and received an invalid response from the upstream server.  |
## Client structure

```python
client.abtests
    create
    delete
    get_all
    get_by_id
    start
    stop
    update
client.af
    create
    update
client.auth
    login
    logout
    recovery_password
    register
client.cases
    create
    delete
    get_all
    update
client.channels
    get_all
client.events
    bulk_review
    get_by_id
    get_by_queue
    review
client.lists
    client.lists.items
        create
        delete
        get_all
        get_by_id
        get_by_pattern
        update
    create
    delete
    get_all
    get_by_id
    update
    import_csv
    export_csv
client.policies
    create
    delete
    get_all
    get_by_id
    update
client.queues
    delete
    get_all
client.roles
    delete
    get_all
    raw_create
    raw_update
    search_by_id
client.settings
    get_all
    update
client.subchannels
    create
    delete
    get_all
    get_by_id
    search_by
    update
client.users
    add_role
    create
    delete
    get_all
    get_by_id
    remove_role
    update
```
## For developers
#### How to run and test it locally
```sh
git clone https://github.com/cybertonica/cybertonica-client.git .
```
##### Unittests
```sh
python -m unittest discover -s tests -p "*.py"
```
##### Install, test import and uninstall
```sh
pip install .
&& python3 -c "from CybertonicaAPI import Client; c = Client(url='https://test.com',team='test')"
&& yes | pip uninstall CybertonicaAPI
```
##### Work with pdoc module
```sh
pip install pdoc
pdoc --html --config show_source_code=False --force CybertonicaAPI
ls ./html/CybertonicaAPI
abtests.html   auth.html   channels.html  events.html  lists.html     queues.html  settings.html     users.html
afclient.html  cases.html  client.html    index.html   policies.html  roles.html   subchannels.html
```
