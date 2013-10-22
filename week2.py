import sys
import binascii
import string
from Crypto.Cipher import AES

import Crypto.Util.Counter

def random(size=16):
    return open("/dev/urandom").read(size)
def encrypt(key, msg):
    c = strxor(key, msg)
    print
    print c.encode('hex')
    return c
    
def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])
key1 = "140b41b22a29beb4061bda66b6747e14"
key2 = "140b41b22a29beb4061bda66b6747e14"
c1 = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"
c2 = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"
a1 = "Basic CBC mode encryption needs padding."
a2 = "Our implementation uses rand. IV"
#end cbc

#ctr
key3 = "36f18357be4dbd77f050515c73fcf9f2"
c3 = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"
a3 = "CTR mode lets you build a stream cipher from a block cipher."
a4 = "Always avoid the two time pad!"
key4 = "36f18357be4dbd77f050515c73fcf9f2"
c4 = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"


class IVCounter(object):
    def __init__(self, startIV=""):
        self.x = 0
        self.IV = startIV
    def __call__(self):
        curIV = int(self.IV, 16)
        curIV += self.x
        self.x += 1
        ivHexStr = format(curIV, 'X')
        
        return binascii.unhexlify(ivHexStr)

def ctrdecrypt (key, c):
    IV = c[0:32]
    c = c[32:]
    ctr = IVCounter(startIV = IV)
    obj2 = AES.new(binascii.unhexlify(key), AES.MODE_CTR , counter=ctr)
    m = ""
    for i in range(0, len(c), 32):
        curc=c[i: i+32]
        if len(curc) == 32:
            mtemp= obj2.decrypt(binascii.unhexlify(curc))
            print mtemp
            m+=mtemp
        else: 
            mtemp= obj2.decrypt(binascii.unhexlify(curc))
            print mtemp
            m+=mtemp

    return m

print ctrdecrypt (key4, c4)

def cbcdecrypt (key, c):
    IV = c[0:32]
    c = c[32:]
    obj2 = AES.new(binascii.unhexlify(key), AES.MODE_ECB , binascii.unhexlify(IV))
    m = ""
    curiv = binascii.unhexlify(IV)
    for i in range(0, len(c), 32):
        curc=c[i: i+32]
        mtemp= obj2.decrypt(binascii.unhexlify(curc))
        curm = strxor(mtemp, curiv)
        curiv = binascii.unhexlify(curc)
        m+=curm

    return m

