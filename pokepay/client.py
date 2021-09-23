import requests
import configparser
import json
import uuid
import pytz
from datetime import datetime
from urllib.parse import urlparse
from pokepay.crypto import AESCipher


def _current_timestamp(tz='Asia/Tokyo'):
    timezone_obj = pytz.timezone(tz)
    now = datetime.now(tz=timezone_obj)
    return now.isoformat()


class Client(object):
    def __init__(self, path_to_inifile, profile_name='global'):
        self.conf = configparser.ConfigParser()
        self.conf.read(path_to_inifile, encoding='utf-8')
        profile = self.conf[profile_name]
        self.client_id = profile.get('CLIENT_ID')
        self.client_secret = profile.get('CLIENT_SECRET')
        self.api_base_url = profile.get('API_BASE_URL')
        self.timezone = profile.get('TIMEZONE')
        self.timeout = profile.get('TIMEOUT')
        self.session = requests.Session()
        self.cipher = AESCipher(self.client_secret)
        self.use_ssl = False
        if urlparse(self.api_base_url).scheme == 'https':
            self.use_ssl = True
            self.ssl_key_file = profile.get('SSL_KEY_FILE')
            self.ssl_cert_file = profile.get('SSL_CERT_FILE')
            self.session.cert = (self.ssl_cert_file, self.ssl_key_file)

    def send(self, request_object):
        encrypt_data = {
            'request_data': request_object.body_params,
            'timestamp': _current_timestamp(self.timezone),
            'partner_call_id': str(uuid.uuid4())
        }
        params = {
            'partner_client_id': self.client_id,
            'data': self.cipher.encrypt(json.dumps(encrypt_data)),
            'request_method': request_object.method
        }
        response = self.session.post(url=self.api_base_url +
                                     request_object.path,
                                     data=params)
        if response.ok:
            res_dict = json.loads(response.content)
            decrypt_data_str = self.cipher.decrypt(res_dict['response_data'])
            decrypt_data = json.loads(decrypt_data_str)
            return request_object.response_class(response, decrypt_data)
        else:
            # return self.cipher.decrypt(res_dict['response_data'])
            return response


# =============================

# c = Client('/home/wiz/.pokepay/config.ini')
# req = SendEcho('hello3')
# res = c.request(req)
# res.status_code

# >>> res
# <pokepay.response.echo.Echo object at 0x7f0d3b057fd0>
# >>> res.status
# 'ok'
# >>> res.message
# 'hello3'
# >>> res.body
# {'status': 'ok', 'message': 'hello3'}
# >>> res.elapsed
# datetime.timedelta(microseconds=115728)
# >>> res.status_code
# 200
# >>> res.ok
# True
# >>> res.headers
# {'Server': 'nginx/1.10.3 (Ubuntu)', 'Date': 'Sun, 12 Sep 2021 17:10:01 GMT', 'Content-Type': 'application/json', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Cache-Control': 'private', 'X-Frame-Options': 'DENY', 'X-Content-Type-Options': 'nosniff', 'Content-Encoding': 'gzip'}
# >>> res.url
# 'https://partnerapi-qa.pokepay.jp/echo'
