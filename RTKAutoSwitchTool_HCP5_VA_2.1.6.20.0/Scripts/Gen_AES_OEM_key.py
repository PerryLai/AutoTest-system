import sys
import string
import random
import os

import ast
from binascii import *
from binascii import b2a_hex, a2b_hex

#f_AESkey = open('', 'wb')
os.chdir(sys.argv[2])

if(sys.argv[1] == 'aes128'):
	f_AESkey = open('OTP_AES128_OEM_KEY.bin', 'wb')
	key_len = 16
elif(sys.argv[1] == 'aes256'):
	f_AESkey = open('OTP_AES256_OEM_KEY.bin', 'wb')
	key_len = 32
else:#default
	f_AESkey = open('OTP_AES256_OEM_KEY.bin', 'wb')
	key_len = 32
	
	
AESkey_str = ''.join(chr(random.randint(0,255)) for _ in range(key_len))
#print "key str: \n", AESkey_str
#print "key str (hex): \n", b2a_hex(AESkey_str)

f_AESkey.write(AESkey_str)



