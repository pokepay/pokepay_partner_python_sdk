import base64
# pip install pycryptodomex
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome import Random
from Cryptodome.Util import Padding


def _base64_url_decode(str):
    return base64.urlsafe_b64decode(str + '=' * (-len(str) % 4))


def _base64_url_encode(bytes):
    return base64.urlsafe_b64encode(bytes).decode(encoding='utf-8').replace(
        '=', '')


def _encrypt(plaintext, key, block_size=16):
    iv = Random.get_random_bytes(block_size)
    key = _base64_url_decode(key)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_bytes = Padding.pad(plaintext.encode(encoding='utf-8'),
                                  block_size,
                                  style='pkcs7')
    print('plaintext_bytes', plaintext_bytes)
    ciphertext_bytes = cipher.encrypt(b'0' * block_size + plaintext_bytes)
    return _base64_url_encode(ciphertext_bytes)


def _decrypt(ciphertext, key, block_size=16):
    ciphertext_bytes = _base64_url_decode(ciphertext)
    print('ciphertext_bytes', ciphertext_bytes)
    print('len(ciphertext_bytes)', len(ciphertext_bytes))
    body = ciphertext_bytes[16:]
    iv = ciphertext_bytes[:16]
    key = _base64_url_decode(key)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_bytes = cipher.decrypt(body)
    pad_size = plaintext_bytes[-1]
    return plaintext_bytes[:-pad_size].decode(encoding='utf-8')


class AESCipher(object):
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext):
        return _encrypt(plaintext, self.key)

    def decrypt(self, ciphertext):
        return _decrypt(ciphertext, self.key)
