import ast
from binascii import *
from binascii import b2a_hex, a2b_hex

import string
import random
import re



f = open('RSA2048_5.text','rb')
RSAinfo_str = f.read()

print "RSAinfo_len : \n", len(RSAinfo_str)
#print "\nRSAinfo :\n", RSAinfo_str

inter = re.search('modulus', RSAinfo_str, flags=0).span()
modulus_str = RSAinfo_str[inter[0]+18:inter[0]+1534+18]
print "\nmodulus_str len: \n", len(modulus_str) 
print "modulus_str: \n", modulus_str

inter = re.search('privateExponent', RSAinfo_str, flags=0).span()
privateExponent_str = RSAinfo_str[inter[0]+26:inter[0]+1534+26]
print "\nprivateExponent_str len: \n", len(privateExponent_str) 
print "privateExponent_str: \n", privateExponent_str 

inter = re.search('publicExponent', RSAinfo_str, flags=0).span()
publicExponent_str = RSAinfo_str[inter[0]+25:inter[0]+1534+25]
print "\npublicExponent_str len: \n", len(publicExponent_str) 
print "publicExponent_str: \n", publicExponent_str


inter = re.search('RRModN', RSAinfo_str, flags=0).span()
RRModN_str = RSAinfo_str[inter[0]+17:inter[0]+1534+17]
print "\nRRModN_str len: \n", len(RRModN_str) 
print "RRModN_str: \n", RRModN_str


inter = re.search('np_inv32', RSAinfo_str, flags=0).span()
np_inv32_str = RSAinfo_str[inter[0]+11:inter[0]+20+10]


print "\nnp_inv32_str len: \n", len(np_inv32_str) 
print "np_inv32_str: \n", np_inv32_str

a = 17
print hex(a)



