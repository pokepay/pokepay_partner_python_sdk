# pokepay_partner_python_sdk

```python
import pokepay
from pokepay.client import Client
from pokepay.request.send_echo import SendEcho

c = Client('/home/wiz/.pokepay/config.ini')
req = SendEcho('Hello, world!')
res = c.send(req)
res.body
res.status_code
res.elapsed
```
