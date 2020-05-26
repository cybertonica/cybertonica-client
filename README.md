# Open API python client
### Requirements
- Python 3( ver. 3.6.9+)
- Request lib (pip install requests)
### Installation

```sh
$ pip install git+https://gitlab.cybertonica.com/AF/vega.git@develop
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
### How to run and test it locally
1. git clone https://gitlab.cybertonica.com/AF/vega.git .
2. touch ./internal_tests.py # add your test logic here
Select command:
3. pip install . && python3 internal_tests.py && yes | pip uninstall CybertonicaAPI # run your internal tests
4. python3 -m unittest discover -s tests -p "*.py" && pip install . && python3 -c "from CybertonicaAPI import Client; c = Client(url='https://test.com',team='test',api_key='test')" && yes |pip uninstall CybertonicaAPI # run full cycle: tests, install, simple import, uninstall
5. python3 -m unittest discover -s tests -p "*.py" #just tests
6. pip install . #just install (after, you can use it as from CybertonicaAPI import Client)
7. pdoc --html --config show_source_code=False --force CybertonicaAPI #generate docs. see html folder
