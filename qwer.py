# -*- coding: utf-8 -*-
import hashlib
from hashlib import md5
from Crypto import Random
from base64 import b64encode, b64decode
import Crypto
import Crypto.Random
import base64
from Crypto.Cipher import AES

ENCRYPT_KEY = "abcdefghijklmnop"
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
# unpad = lambda s: s[:-ord(s[len(s) - 1:])]
unpad = lambda s: s[0:-ord(s[-1])]


class AESECBCipher:
    def __init__(self, key):
        # self.key = md5(key.encode('euc-kr')).hexdigest()
        # self.key = hashlib.sha256(key.encode('euc-kr')).digest()
        # self.key = hashlib.sha256(key.encode('utf8')).digest()
        # self.key = hashlib.sha256(key).digest()
        self.key = hashlib.md5(key).hexdigest()

    def encrypt(self, raw):
        raw = pad(raw)
        # cipher = AES.new(self.key, AES.MODE_ECB)
        cipher = AES.new(ENCRYPT_KEY, AES.MODE_ECB)
        return b64encode(cipher.encrypt(raw))

    def decrypt(self, cipher):
        cipher = b64decode(cipher)
        encryptor = AES.new(ENCRYPT_KEY, AES.MODE_ECB)
        plain = encryptor.decrypt(cipher)
        plain = plain[0:-ord(plain[-1])]
        return plain

    # def decrypt(self, enc):
    #     enc = b64decode(enc)
    #     cipher = AES.new(ENCRYPT_KEY, AES.MODE_ECB)
    #     # cipher = AES.new(self.key, AES.MODE_ECB)

    #     return unpad(cipher.decrypt(enc)).decode('utf8')

if __name__ == "__main__":
    plain = "01054734957"
    hoho = "jHfma1z38BjCqVcdvsMw3w=="

    test = AESECBCipher(ENCRYPT_KEY)
    aaa = test.encrypt(plain)
    print aaa
    print hoho
    bbb = test.decrypt(aaa)
    print bbb
    ccc = test.decrypt(hoho)
    print ccc
