# pokepay_partner_python_sdk

```python
import pokepay
from pokepay.client import Client

c = Client('/home/wiz/.pokepay/config.ini')
req = pokepay.SendEcho('Hello, world!')
res = c.send(req)
res.body
res.status_code
res.elapsed
```
