import requests
import configparser
import json
import uuid
import pytz
from datetime import datetime
from urllib.parse import urlparse
from .crypto import AESCipher


def _current_timestamp(tz):
    if not (tz):
        tz = 'Asia/Tokyo'
    timezone_obj = pytz.timezone(tz)
    now = datetime.now(tz=timezone_obj)
    return now.isoformat()


def _timeout_params(timeout, connection_timeout):
    if not (timeout):
        timeout = 5.0
    if not (connection_timeout):
        connection_timeout = 5.0
    return (float(connection_timeout), float(timeout))


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
        self.connection_timeout = profile.get('CONNECTTIMEOUT')
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
        response = self.session.post(
            url=self.api_base_url + request_object.path,
            data=params,
            timeout=_timeout_params(self.timeout, self.connection_timeout))
        if response.ok:
            res_dict = json.loads(response.content)
            decrypt_data_str = self.cipher.decrypt(res_dict['response_data'])
            decrypt_data = json.loads(decrypt_data_str)
            return request_object.response_class(response, decrypt_data)
        else:
            return response
