
import binascii
import string
import urllib2
import sys

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

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:          
            #print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding
c0 = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
c = c0[32:]
print len(c)
IV = c0[0:32]
padxor =   "00000000000000000000000000000001"

print len(padxor)
querystr = "testc"
po = PaddingOracle()


for i in range(0,255,1):
    g = "000000000000000000000000000000"
    g = g + chr(i).encode('hex')
    print guessxor
    cprime = strxor(strxor(g , padxor) , c)
    
    querystr = IV + cprime
    #print querystr
    if po.query(querystr):
        print "404!"
        print querystr



