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
def numstr(x):
    num=(30-x)/2 + 1
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)
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
            if e.code == 404 or e.code == 200:
                return True # good padding
            return False # bad padding
c0 = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"

c1 = c0[32:64]
c2 = c0[64:96]
c3 = c0[96:]

IV = c0[0:32]

querystr = "testc"
po = PaddingOracle()
foundg = "00000000000000000000000000000000"
foundnum = "00000000000000000000000000000000"
foundi = ""
# for x in range(30,0,-2):

#     start = x
#     end = 30-x
#     padxortemp = "0" * x + numstr(x) + "0" * end
#     padxor = strxor(binascii.unhexlify(padxortemp), binascii.unhexlify(foundnum))
#     padxor = padxor.encode('hex')
#     print padxor

#     for i in range(0,255,1):
#         gtemp = "0" * x + chr(i).encode('hex') + "0" * end
#         g = strxor(binascii.unhexlify(gtemp), binascii.unhexlify(foundg))
#         g = g.encode('hex')
#         cprime = strxor(binascii.unhexlify(g) , binascii.unhexlify(padxor))
#         cprime = strxor(cprime , binascii.unhexlify(c2))
#         cprime = cprime.encode('hex')
#         querystr = IV + c1 + cprime  + c3

#         if po.query(querystr):
#             print querystr
#             print chr(i)
#             print gtemp
#             print foundg
#             foundg = strxor(binascii.unhexlify(gtemp),binascii.unhexlify(foundg))
#             foundg = foundg.encode('hex')
#             foundnum = strxor(binascii.unhexlify(padxortemp),binascii.unhexlify(foundnum))
#             foundnum = foundnum.encode('hex')
#             break
for x in range(30,0,-2):
    found = 0
    start = x /2
    end = (30-x) /2 + 1
    padstr = ""
    if end >10:
        padstr = str(end)
    else:
        padstr = "0" + str(end)
    padxor = "00" * start + padstr * end 
    print padxor    




    for i in range(0,255,1):
        #gtemp = "00" * start + chr(i).encode('hex') + "00" * (end-1)
        gtemp = "000000000000000000000000000000" + chr(i).encode('hex')
        print gtemp
        g = strxor(binascii.unhexlify(gtemp), binascii.unhexlify(foundg))
        g = g.encode('hex')
        cprime = strxor(binascii.unhexlify(gtemp) , binascii.unhexlify(c2))
        cprime = strxor(binascii.unhexlify(padxor), cprime)
        cprime = cprime.encode('hex')
        querystr = IV + c1 + cprime  + c3

        if po.query(querystr):
            print querystr
            foundg = strxor(binascii.unhexlify(gtemp),binascii.unhexlify(foundg))
            foundg = foundg.encode('hex')
            foundi = chr(i).encode('hex') + foundi
            found = 1
            break
    if found != 1:
        print "failed"
        break
print foundi
print binascii.unhexlify(foundi)
