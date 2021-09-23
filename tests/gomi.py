import client
from requests.send_echo import SendEcho

c = client.Client('/home/wiz/.pokepay/config.ini')
req = SendEcho('hello')
