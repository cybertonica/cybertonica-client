# Open API python client
### Requirements
- Python 3 ( ver. 3.6.9+)
- Request lib (pip install requests)
### Installation

```sh
$ pip install git+https://gitlab+deploy-token-11:RRtP8-9wBU8Rmv92QZJU@gitlab.cybertonica.com/ochaplashkin/openapi_python_client.git@future-structure
```

### Usage
```python3
>>> from CybertonicaAPI import Client
>>> c = Client(url='https://<env>.cybertonica.com',team='<team>',api_key='<team_apikey>')
>>> c.auth.login('your_login','your_pass')
```
You can check out your success log in the following way:

```python3
>>> c.auth.login('your_login','your_pass')
>>> print(c.token)
your_token here
```
### Client methods
* Client
  * auth
    * auth.login
    * auth.logout
    * auth.recovery_password
    * auth.register
  * subchannels
    * subchannels.get_all
    * subchannels.get_by_id
    * subchannels.search_by
    * subchannels.create
    * subchannels.update
    * subchannels.delete
  * lists
    * lists.get_all
    * lists.get_by_id
    * lists.create
    * lists.update
    * lists.delete
    * items
        * lists.items.get_all
        * lists.items.get_by_id
        * lists.items.create
        * lists.items.update
        * lists.items.delete
  * users
    * users.get_all
    * users.get_by_id
    * users.create
    * users.update
    * users.delete
    * users.add_role
    * users.remove_role
  * channels
    * channels.get_all
  * policies
    * policies.get_all
    * policies.get_by_id
    * policies.create
    * policies.update
    * policies.delete
  * events
    * events.get_by_id
    * events.get_by_queue
    * events.bulk_review
    * events.review