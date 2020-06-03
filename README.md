<span align="center">

<pre>
    <img src="https://gitlab.cybertonica.com/AF/vega/-/blob/develop/ext/logo.png" align="center"/></a>
    
    <div align="left">
    <p></p>
    <code> Python 3.6.9 (default, Nov  7 2019, 10:44:02)</code>
    <code> >>> <strong>from CybertonicaAPI import Client</strong></code>
    <code> >>> cbt = Client(url='https://test.cybertonica.com',team='test')</code>
    <code> >>> status, data = cbt.auth.login('login', 'password')</code>
    <code> >>> f'{status} | {cbt.token}'</code>
    <code> '200 | 37d9c47b-4837-44db-9dbe-b5427eb70b43'</code>
    <code> >>> cbt.api_user_id = 'api_user_id'</code>
    <code> >>> cbt.api_signature = 'api_signature'</code>
    <code> >>> cbt.af.create({"channel":"global","sub_channel":"sys"})</code>
    <code> (200, {'action': 'ALLOW', 'channel': 'global', 'comments': ['from Default'], 'id': 'eve_global:8dd5fc24-3fc2-4e7c-a909-94afbe44931a', 'queues': [], 'rules': ['Default'], 'score': 0, 'tags': []})</code>
    </div>
</pre>
</span>

<p>&nbsp;</p><p>&nbsp;</p>

<p align="center">Cybertonica API Python Client</p>

<p>&nbsp;</p>

```pycon
>>> from CybertonicaAPI import Client
>>> cbt = Client(url='https://test.cybertonica.com',team='test')
>>> status, data = cbt.auth.login('login', 'password')
>>> cbt.events.get_by_id('eve_global:8dd5fc24-3fc2-4e7c-a909-94afbe44931a')
>>> (200, {'_cls': 'eve_global', 'channel': 'global', 'source': {'sub_channel': 'sys', 'channel': 'global'}, '_t': 1591179224097, '_id': 'eve_global:8dd5fc24-3fc2-4e7c-a909-94afbe44931a', .... })
>>> cbt.lists.create({"name":"simple_list","kind":"WHITE"})
(201, {'createdAt': 1591179867918, 'createdBy': 'user', 'id': 'e166502a-8332-4317-9421-edd9dcca7694', 'kind': 'WHITE', 'name': 'simple_list', 'size': 0})
>>> cbt.lists.get_by_id('e166502a-8332-4317-9421-edd9dcca7694')
(200, {'createdAt': 1591179867918, 'createdBy': 'user', 'id': 'e166502a-8332-4317-9421-edd9dcca7694', 'kind': 'WHITE', 'name': 'simple_list', 'size': 0})
>>> cbt.lists.create("bad_structure")
AssertionError: The data type must be a dictionary
```