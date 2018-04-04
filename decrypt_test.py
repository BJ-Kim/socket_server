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

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

def decrypt(cipher):
    encryptor = AES.new(getKey(), AES.MODE_CBC, IV=gen_random_iv())
    print cipher
    plain = encryptor.decrypt(cipher)
    print plain
    plain = plain[0:-ord(plain[-1])]
    print plain
    return plain

def getKey():
    print hashlib.sha256(ENCRYPT_KEY.encode()).digest()
    return hashlib.sha256(ENCRYPT_KEY.encode()).digest()
    # return hashlib.md5(ENCRYPT_KEY).hexdigest()[:16]

def gen_random_iv():
    # print Crypto.Random.new().read(AES.block_size)
    # return Crypto.Random.new().read(AES.block_size)
    return Crypto.Random.OSRNG.posix.new().read(AES.block_size)

def gen_sha256_hashed_key_salt(key):
    salt1 = hashlib.sha256(key).digest()
    return hashlib.sha256(salt1+key).digest()

class AESCipher:
    def __init__(self, key):
        self.key = md5(key.encode('utf8')).hexdigest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode('utf8')

def md5key(key):
    return md5(key.encode('utf8')).hexdigest()

def qwer(pop):
    # encryptor = AES.new(gen_sha256_hashed_key_salt(ENCRYPT_KEY), AES.MODE_CBC, IV=gen_random_iv())
    print "==================================="
    print ENCRYPT_KEY
    key = md5key(ENCRYPT_KEY)
    print key
    print "==================================="
    encryptor = AES.new(md5key(ENCRYPT_KEY), AES.MODE_CBC, IV=gen_random_iv())
    plain = encryptor.decrypt(pop)
    plain = plain[0:-ord(plain[-1])]
    return plain

def encrypt(plain):
    import pdb; pdb.set_trace()
    length = AES.block_size - (len(plain) % AES.block_size)
    plain += chr(length)*length
    iv = gen_random_iv()
    print "==================================="
    print ENCRYPT_KEY
    key = md5key(ENCRYPT_KEY)
    print key
    print "==================================="
    # encryptor = AES.new(gen_sha256_hashed_key_salt(key), AES.MODE_CBC, IV=iv)
    encryptor = AES.new(md5key(key), AES.MODE_CBC, IV=iv)
    cipher = encryptor.encrypt(plain)
    return cipher
    # return {'cipher': encryptor.encrypt(plain), 'iv': iv}

if __name__ == "__main__":
    plain = "01054734957"
    hoho = "jHfma1z38BjCqVcdvsMw3w=="

    test = AESCipher(ENCRYPT_KEY)
    aa = test.encrypt(plain)
    bb = test.decrypt(aa)
    cc = test.decrypt(hoho)
    import pdb; pdb.set_trace()

    # enc = encrypt(plain)
    # print "******************************"
    # print enc
    # print "******************************"
    # import pdb; pdb.set_trace()
    # sss = qwer(enc)
    # print "******************************"
    # print sss
    # print "******************************"


    # ddd = qwer(test)

    # decryptTelNo = decrypt(test)
