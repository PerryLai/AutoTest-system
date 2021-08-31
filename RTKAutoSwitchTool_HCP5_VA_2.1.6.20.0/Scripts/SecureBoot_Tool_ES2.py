import sys
import Crypto
from Crypto.Cipher import AES
from Crypto.Hash import HMAC,SHA , SHA256, MD5, SHA512
from Crypto.PublicKey import RSA
#from Crypto import Random
from Crypto.Util import Counter
from base64 import *
import ast
from binascii import *
from binascii import b2a_hex, a2b_hex
import string
import random
import re

#--------------- Infomation -----------------#
#sys.argv[1] - secure boot mode
#sys.argv[2] - RSA mode
#sys.argv[3] - hash mode
#--------------------------------------------#

CONST_MD5 = 0
CONST_SHA1 = 1
CONST_SHA256 = 2

#Padding 
BS = AES.block_size #16
#print BS
pad = lambda s: s + ((BS - len(s)) % BS) * chr(0)
 
def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))
def sum(arg1, arg2):
	# Add both the parameters and return them."
	total = arg1 + arg2
	#print "Inside the function : ", total
	return total;
   
def aes_encrypt(plaintext, key):
	MODE = AES.MODE_ECB
	
	#---- AES Encryption ----
	cryptor = AES.new(key, MODE)
	ciphertext = cryptor.encrypt(plaintext)
	return ciphertext;
	
def aes_decrypt(ciphertext, key):
	MODE = AES.MODE_ECB
	
	#---- AES Decryption ----
	cryptor = AES.new(key, MODE)
	plaintext = cryptor.decrypt(ciphertext)
	return plaintext;	

def hash_mode_setting(select):
	if(select == 'md5'):
		hash_mode = CONST_MD5
	elif(select == 'sha1'):
		hash_mode = CONST_SHA1
	else:	
		hash_mode = CONST_SHA256
		
	return hash_mode;
	
def hash(data, mode):
	if(mode == CONST_MD5):
		h = MD5.new()
		h.update(data)
	elif(mode == CONST_SHA1):
		h = SHA.new()
		h.update(data)
	else:	
		h = SHA256.new()
		h.update(data)
		
	return h.digest();	

def pad_swap(data):
	#pad 
	data_len = len(data)
	#print "datalen:", data_len
	if(data_len%16 != 0):
		pad_num = 16 - (data_len%16)
	else:
		pad_num = 0
	#print "P&S padnum:", pad_num
	
	pad_data = data
	for index in range(0, pad_num, 1):
		pad_data += '\x00'
	
	#swap
	swap_data = ""
	for i in range(0, len(pad_data)/16, 1):
		for j in range(0, 16, 1):
			swap_data += pad_data[16*i + (15-j)]
		
	return swap_data;
	
def pad(data):
	#pad 
	data_len = len(data)
	#print "datalen:", data_len
	if(data_len%16 != 0):
		pad_num = 16 - (data_len%16)
	else:
		pad_num = 0
	#print "pad padnum:", pad_num
	
	pad_data = data
	for index in range(0, pad_num, 1):
		pad_data += '\x00'
			
	return pad_data;	

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
	
#command format: SecureBoot_Tool_ES2.py 1 3072 sha256
	
#read image bin file use sys.argv (path) as parameter
f_binfile = open('test.txt', 'rb')
plaintext = f_binfile.read()
#print "plaintext:\n", b2a_hex(plaintext)
#print "plaintext len:", len(plaintext)


#read AES key and reverse
f_AESkey = open('OTP_AES256_ES2.bin', 'rb')
AESkey = f_AESkey.read()
AESkey = AESkey[::-1]
#print "key str: \n",  b2a_hex(AESkey)


#read RSA information file
RSA_mode = sys.argv[2]
if(RSA_mode == '3072'):
	f = open('RSA3072.text','rb')
	RSA_mode_len = 384
else:
	f = open('RSA2048.text','rb')
	RSA_mode_len = 256	
	
	
#read hash mode from sys.argv[2]
hash_mode = hash_mode_setting(sys.argv[3])#sys.argv[1]=0: AES_HASH+RSA, sys.argv[2]=2:SHA1

if(sys.argv[1] != '0'):
	#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	#----------------------------------------------------- AES_HASH with Boot code -----------------------------------------------------------#
	# padding and swap 
	PS_plaintext  = pad_swap(plaintext)
	#print "PS_plaintext len :",  len(PS_plaintext)

	#------------- encrypt --------------
	aes_ciphertext = aes_encrypt(PS_plaintext, AESkey)
	#print "ciphertext : ",  aes_ciphertext

	# padding and swap 
	PS2_aes_ciphertext = pad_swap(aes_ciphertext)
	#print "\nPS2_aes_ciphertext: \n",  b2a_hex(PS2_aes_ciphertext)
	#print "\nPS2_aes_ciphertext len:",  len(PS2_aes_ciphertext)

	#------------- decrypt --------------
	#PS_plaintext = aes_decrypt(aes_ciphertext, AESkey)
	#print "PS_plaintext  : ", PS_plaintext

	hash_data = hash(PS_plaintext, hash_mode)
	#print "hash data  : ", b2a_hex(hash_data), " \nhash length: ", len(hash_data)

	#------------------------------------------------- RSA with boot code hash-------------------------------------------------------------------#
	RSAinfo_str = f.read()
	# ----------------- N ---------------------------
	keystring = parse_RSA_info('modulus', RSAinfo_str, RSA_mode)
	keydata = keystring.split();#split by space
	#print len(keydata), '\n'
	keyvalue=0
	for index in range(len(keydata)):
		#print "N index", index
		keybyte = keydata[index].strip(',')
		
		#print "keybyte ", keybyte
		tmp = long(keybyte, 16) << (8*index)	
		keyvalue += tmp

	n1=keyvalue

	# ----------------- e ---------------------------
	keystring = parse_RSA_info('publicExponent', RSAinfo_str, RSA_mode)
	keydata = keystring.split();#split by space
	#print len(keydata), '\n'
	keyvalue=0.
	for index in range(len(keydata)):
		keybyte = keydata[index].strip(',')
		tmp = long(keybyte, 16) << (8*index)	
		keyvalue += tmp 
	e1=keyvalue

	# ----------------- d ---------------------------
	keystring = parse_RSA_info('privateExponent', RSAinfo_str, RSA_mode)
	keydata = keystring.split();#split by space
	#print len(keydata), '\n'
	keyvalue=0
	for index in range(len(keydata)):
		keybyte = keydata[index].strip(',')
		tmp = long(keybyte, 16) << (8*index)	
		keyvalue += tmp
	
	d1=keyvalue
	
	# ----------------- RRmodN ---------------------------
	keystring = parse_RSA_info('RRModN', RSAinfo_str, RSA_mode)
	keydata = keystring.split();#split by space
	#print len(keydata), '\n'
	RRModN_str=''
	RRModN_hex_str=''
	for index in range(len(keydata)):
		keybyte = keydata[index].strip(',')
		RRModN_str += keybyte[2:4]
		RRModN_hex_str = RRModN_str.decode("hex")
	
	#print "RRmodN len:", len(RRModN_hex_str)
	#print "\nRRmodN:\n"+b2a_hex(RRModN_hex_str)
	
	#------------------------- Calculate RSA key -------------------------------
	n=long(n1)
	e=long(e1)
	d=long(d1)
	pub_key = RSA.construct((n,e))
	pri_key = RSA.construct((n,e,d))

	#print '\n- pub_key:\n', pub_key
	#print '- pri_key:\n', pri_key
	
	RSA_plaintext = hash_data
	#--------- Sign & verify ----------------#
	#----- sign -----
	RSA_signature = pri_key.sign(RSA_plaintext, '')
	#print '\nRSA_signature num:\n', hex(RSA_signature[0])

	tmp_str = hex(RSA_signature[0])[2:-1]
	while(len(tmp_str) < RSA_mode_len):
		tmp_str = '0'+ tmp_str
	RSA_sig_str = tmp_str.decode("hex")
	#print '\nRSA_signature:\n', b2a_hex(RSA_sig_str)
	#print "RSA_sig_str len :", len(RSA_sig_str)
	
	#f_3072ciphertext = open('RSA3072_ciphertext.bin','wb')
	#for index in range(len(RSA_sig_str)):
		#f_3072ciphertext.write("0x" + b2a_hex(RSA_sig_str[index]) + ", ")
	
	#----- verify -----
	RSA_iscorrect = pub_key.verify(RSA_plaintext,RSA_signature)
	if(RSA_iscorrect):
		print "PASS"
	else:
		print "FAIL"
	
	#--------------- AES_HASH with RSA ciphertext (Hash) -------------------#	
	# padding and swap 
	#PS_rsacipher  = pad_swap( RSA_ciphertext[0])
	PS_rsacipher  = pad_swap( RSA_sig_str)
	#print "\nPS_rsacipher : \n", b2a_hex(PS_rsacipher)

	# encrypt
	PS_rsacipher_aescipher = aes_encrypt(PS_rsacipher, AESkey)
	#print "\nPS_rsacipher_aescipher : \n", b2a_hex(PS_rsacipher_aescipher)

	# padding and swap 
	PS2_rsacipher_aescipher = pad_swap(PS_rsacipher_aescipher)
	#print "\nPS2_rsacipher_aescipher : \n", b2a_hex(PS2_rsacipher_aescipher)	
	
	#--------------- AES_HASH with RRmodeN str -------------------#
	# padding and swap 
	PS_RRmodN  = pad_swap( RRModN_hex_str)
	#print "\nPS_RRmodN : \n", b2a_hex(PS_RRmodN)

	# encrypt
	PS_RRmodN_aescipher = aes_encrypt(PS_RRmodN, AESkey)
	#print "\nPS_RRmodN_aescipher : \n", b2a_hex(PS_RRmodN_aescipher)

	# padding and swap 
	PS2_RRmodN_aescipher = pad_swap(PS_RRmodN_aescipher)
	#print "\nPS2_RRmodN_aescipher : \n", b2a_hex(PS2_RRmodN_aescipher)
	#print "PS2_RRmodN_aescipher \n" , b2a_hex(PS2_RRmodN_aescipher)

	#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	#-------------------------------------------- Combine Binary & Output Bin File (.bin) ----------------------------------------------------#

	flash_bootrom_str = PS2_aes_ciphertext + PS2_rsacipher_aescipher + PS2_RRmodN_aescipher
	#print "\nflash_bootrom_str : \n", flash_bootrom_str
	#print "\nflash_bootrom_str len : ", len(flash_bootrom_str)
	
	f_flash_bootrom = open('test_image.bin','wb')
	f_flash_bootrom.write(flash_bootrom_str)
	
else:
	#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	#----------------------------------------------------- HASH with Boot code -----------------------------------------------------------#
	PS_plaintext  = pad_swap(plaintext)
	#print "PS_plaintext len :",  len(PS_plaintext)
		
	hash_bootcode = hash(PS_plaintext, hash_mode)
	#print "hash data  : ", b2a_hex(hash_bootcode), " \nhash length: ", len(hash_bootcode)
	#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	#------------------------------------------------- RSA with boot code hash-------------------------------------------------------------------#
	RSAinfo_str = f.read()

	# ----------------- N ---------------------------
	keystring = parse_RSA_info('modulus', RSAinfo_str, RSA_mode)
	keydata = keystring.split();#split by space
	#print len(keydata), '\n'
	keyvalue=0
	N_str=''
	N_hex_str=''
	for index in range(len(keydata)):
		keybyte = keydata[index].strip(',')
		tmp = long(keybyte, 16) << (8*index)	
		keyvalue += tmp
		
		N_str += keybyte[2:4]
		N_hex_str = N_str.decode("hex")

	n1=keyvalue

	# ----------------- e ---------------------------
	keystring = parse_RSA_info('publicExponent', RSAinfo_str, RSA_mode)
	keydata = keystring.split();#split by space
	#print len(keydata), '\n'
	keyvalue=0.
	e_str=''
	e_hex_str=''
	for index in range(len(keydata)):
		keybyte = keydata[index].strip(',')
		tmp = long(keybyte, 16) << (8*index)	
		keyvalue += tmp 
		
		e_str += keybyte[2:4]
		e_hex_str = e_str.decode("hex")
		
	e1=keyvalue

	# ----------------- d ---------------------------
	keystring = parse_RSA_info('privateExponent', RSAinfo_str, RSA_mode)
	keydata = keystring.split();#split by space
	#print len(keydata), '\n'
	keyvalue=0
	d_str=''
	d_hex_str=''
	for index in range(len(keydata)):
		keybyte = keydata[index] = keydata[index].strip(',')
		tmp = long(keybyte, 16) << (8*index)	
		keyvalue += tmp
		
		d_str += keybyte[2:4]
		d_hex_str = d_str.decode("hex")
	
	d1=keyvalue
	
	# ----------------- RRmodN ---------------------------
	keystring = parse_RSA_info('RRModN', RSAinfo_str, RSA_mode)
	keydata = keystring.split();#split by space
	#print len(keydata), '\n'
	keyvalue=0
	RRModN_str=''
	RRModN_hex_str=''
	for index in range(len(keydata)):
		keybyte = keydata[index].strip(',')
		RRModN_str += keybyte[2:4]
		RRModN_hex_str = RRModN_str.decode("hex")
	
	
	#------------------------- Calculate RSA key -------------------------------
	n=long(n1)
	e=long(e1)
	d=long(d1)
	pub_key = RSA.construct((n,e))
	pri_key = RSA.construct((n,e,d))

	#print '\n- pub_key:\n', pub_key
	#print '- pri_key:\n', pri_key

	RSA_plaintext = hash_bootcode
	#--------- Sign & verify ----------------#
	#----- sign -----
	RSA_signature = pri_key.sign(RSA_plaintext, '')
	#print '\nRSA_signature:\n', hex(RSA_signature[0])

	tmp_str = hex(RSA_signature[0])[2:-1]
	if(len(tmp_str) < RSA_mode_len):
		tmp_str = '0'+ tmp_str
	RSA_sig_str = tmp_str.decode("hex")
	
	#print "\nRSA_sig_str :\n", b2a_hex(RSA_sig_str)
	#print "\nRSA_sig_str len :", len(RSA_sig_str)
	
	#----- verify -----
	RSA_iscorrect = pub_key.verify(RSA_plaintext,RSA_signature)
	if(RSA_iscorrect):
		print "PASS"
	else:
		print "FAIL"
	
	
	#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	#-------------------------------------------- Combine Binary & Output Bin File (.bin) ----------------------------------------------------#
	P_plaintext = pad(plaintext)
	
	#flash_bootrom_str = P_plaintext + RSA_ciphertext[0]
	flash_bootrom_str = P_plaintext + RSA_sig_str + RRModN_hex_str
	#print "\nflash_bootrom_str:\n", flash_bootrom_str
	#print "\nflash_bootrom_str len:\n", len(flash_bootrom_str)
	
	f_flash_bootrom = open('test_RSAonly_image.bin','wb')
	f_flash_bootrom.write(flash_bootrom_str)
	
	
#output bin file





