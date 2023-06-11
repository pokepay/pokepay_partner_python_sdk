# pokepay_partner_python_sdk

## Usage

```python
import pokepay
from pokepay.client import Client

c = Client('/path/to/config.ini')
req = pokepay.SendEcho('Hello, world!')
res = c.send(req)
res.body
res.status_code
res.elapsed
```

## Run test

```
python tests/request_validation_test.py
```
