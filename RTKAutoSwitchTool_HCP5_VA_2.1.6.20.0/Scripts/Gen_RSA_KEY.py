import sys
import string
import random
import re
import ast
from binascii import *
from binascii import b2a_hex, a2b_hex
import Crypto
from Crypto.PublicKey import RSA



	
def parse_RSA_info(pattern, RSAinfo_str, RSAmode):
	data_len = 0
	if(RSAmode == '2048'):
		data_len = 1535
	else:
		data_len = 2303
		
	if(pattern == 'modulus'):
		inter = re.search('modulus', RSAinfo_str, flags=0).span()
		tar_str = RSAinfo_str[inter[0]+18:inter[0]+data_len+18]
	elif(pattern == 'privateExponent'):
		inter = re.search('privateExponent', RSAinfo_str, flags=0).span()
		tar_str = RSAinfo_str[inter[0]+26:inter[0]+data_len+26] 
	elif(pattern == 'publicExponent'):
		inter = re.search('publicExponent', RSAinfo_str, flags=0).span()
		tar_str = RSAinfo_str[inter[0]+25:inter[0]+data_len+25]	
	elif(pattern == 'RRModN'):
		inter = re.search('RRModN', RSAinfo_str, flags=0).span()
		tar_str = RSAinfo_str[inter[0]+17:inter[0]+data_len+17]
	else:
		inter = re.search('np_inv32', RSAinfo_str, flags=0).span()
		temp_str = RSAinfo_str[inter[0]+11:inter[0]+20+13]
		tar_str = temp_str.strip(' \n\t\r;c')
		
	#print "\ntar_str len: \n", len(tar_str) 
	#print "tar_str: \n", tar_str
	return tar_str;
	

RSAmode = sys.argv[1]

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#------------------------------------------------- RSA with boot code hash-------------------------------------------------------------------#
if(RSAmode == '2048'):
	f = open('RSA2048.text','rb')
else:
	f = open('RSA3072.text','rb')	
RSAinfo_str = f.read()

# ----------------- N ---------------------------
keystring = parse_RSA_info('modulus', RSAinfo_str, RSAmode)
keydata = keystring.split();#split by space
#print len(keydata), '\n'
N_str=''
N_hex_str=''
for index in range(len(keydata)):
	keybyte = keydata[index].strip(',')	
	N_str += keybyte[2:4]
	N_hex_str = N_str.decode("hex")
		

# ----------------- e ---------------------------
keystring = parse_RSA_info('publicExponent', RSAinfo_str, RSAmode)
keydata = keystring.split();#split by space
#print len(keydata), '\n'
e_str=''
e_hex_str=''
for index in range(len(keydata)):
	keybyte = keydata[index].strip(',')	
	e_str += keybyte[2:4]
	e_hex_str = e_str.decode("hex")
	

# ----------------- d ---------------------------
keystring = parse_RSA_info('privateExponent', RSAinfo_str, RSAmode)
keydata = keystring.split();#split by space
#print len(keydata), '\n'
d_str=''
d_hex_str=''
for index in range(len(keydata)):
	keybyte = keydata[index].strip(',')
	d_str += keybyte[2:4]
	d_hex_str = d_str.decode("hex")	

# ----------------- RRmodN ---------------------------
keystring = parse_RSA_info('RRModN', RSAinfo_str, RSAmode)
keydata = keystring.split();#split by space
#print len(keydata), '\n'
keyvalue=0
RRModN_str=''
RRModN_hex_str=''
for index in range(len(keydata)):
	keybyte = keydata[index].strip(',')
	RRModN_str += keybyte[2:4]
	RRModN_hex_str = RRModN_str.decode("hex")
	

# ----------------- np_inv32 ---------------------------
keystring = parse_RSA_info('np_inv32', RSAinfo_str, RSAmode)

tmp_hex_str = hex(int(keystring))[2:18].strip('L')
#print "tmp_hex_str: \n", tmp_hex_str
if(len(tmp_hex_str)%2 < 16):
	tmp_hex_str = '0'+ tmp_hex_str
#print tmp_hex_str[1], "  ", tmp_hex_str[2], "  ", tmp_hex_str[15], "  ", tmp_hex_str[16]

tmp_np_inv32_hex_str = ''
for index in range(7, -1, -2):
	tmp_np_inv32_hex_str += tmp_hex_str[index:index+2]
for index in range(15, 7, -2):
	tmp_np_inv32_hex_str += tmp_hex_str[index:index+2]
	
np_inv32_hex_str = tmp_np_inv32_hex_str.decode("hex")
#print "np_inv32_hex_str: \n",  b2a_hex(np_inv32_hex_str)



# ----------------- Gen Bin ---------------------------
RSA_key_info = np_inv32_hex_str + N_hex_str + e_hex_str
f_RSA_key = open('OTP_RSA_KEY.bin','wb')
f_RSA_key.write(RSA_key_info)


	