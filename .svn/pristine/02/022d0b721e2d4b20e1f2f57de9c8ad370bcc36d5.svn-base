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
	ciphertext = cryptor.encrypt(pad(plaintext))
	return ciphertext;
	
def aes_decrypt(ciphertext, key):
	MODE = AES.MODE_ECB
	
	#---- AES Decryption ----
	cryptor = AES.new(key, MODE)
	plaintext = cryptor.decrypt(ciphertext)
	return plaintext;	

def hash_mode_setting(select):
	if(select == '0'):
		hash_mode = CONST_MD5
	elif(select == '1'):
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
	#print "padnum:", pad_num
	
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
	#print "padnum:", pad_num
	
	pad_data = data
	for index in range(0, pad_num, 1):
		pad_data += '\x00'
			
	return pad_data;	

def parse_RSA_info(pattern, RSAinfo_str):
	if(pattern == 'modulus'):
		inter = re.search('modulus', RSAinfo_str, flags=0).span()
		tar_str = RSAinfo_str[inter[0]+18:inter[0]+1535+18]
	elif(pattern == 'privateExponent'):
		inter = re.search('privateExponent', RSAinfo_str, flags=0).span()
		tar_str = RSAinfo_str[inter[0]+26:inter[0]+1535+26] 
	elif(pattern == 'publicExponent'):
		inter = re.search('publicExponent', RSAinfo_str, flags=0).span()
		tar_str = RSAinfo_str[inter[0]+25:inter[0]+1535+25]	
	elif(pattern == 'RRModN'):
		inter = re.search('RRModN', RSAinfo_str, flags=0).span()
		tar_str = RSAinfo_str[inter[0]+17:inter[0]+1535+17]
	else:
		inter = re.search('np_inv32', RSAinfo_str, flags=0).span()
		temp_str = RSAinfo_str[inter[0]+11:inter[0]+20+13]
		tar_str = temp_str.strip(' \n\t\r;c')
		
	#print "\ntar_str len: \n", len(tar_str) 
	#print "tar_str: \n", tar_str
	return tar_str;
	
	
#read image bin file use sys.argv (path) as parameter
#f_binfile = open('gpio4.bin', 'rb')
f_binfile = open(sys.argv[3], 'rb')

plaintext = f_binfile.read()
#plaintext = "0123456789abcdef1234567"
#plaintext = "1111111111111111111111111111111111111111111111111111111111111111"

#read AES key
#f_AESkey = open('OTP_AES256_OEM_KEY_tooltest.bin', 'rb')
f_AESkey = open(sys.argv[5], 'rb')

AESkey = f_AESkey.read()
#print "key str: \n", AESkey
#key = '12345678876543211234567887654321'

#read rsa information file
f = open(sys.argv[4],'rb')

#read hash mode from sys.argv[2]
hash_mode = hash_mode_setting(sys.argv[2])

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
	#print "PS2_aes_ciphertext : ",  PS2_aes_ciphertext

	#------------- decrypt --------------
	PS_plaintext = aes_decrypt(aes_ciphertext, AESkey)
	#print "PS_plaintext  : ", PS_plaintext


	hash_data = hash(PS_plaintext, hash_mode)
	#print "hash data  : ", hash_data, " \nhash length: ", len(hash_data)

	#PS_data = pad_swap(plaintext)
	#print "PS_data: ", PS_data


	#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	#------------------------------------------------- RSA with boot code hash-------------------------------------------------------------------#
	#f = open('RSA2048_2.text','rb')
	RSAinfo_str = f.read()
	

	# ----------------- N ---------------------------
	keystring = parse_RSA_info('modulus', RSAinfo_str)
	keydata = keystring.split();#split by space
	#print len(keydata), '\n'
	keyvalue=0
	N_str=''
	N_hex_str=''
	for index in range(len(keydata)):
		#print "N index", index
		keybyte = keydata[index].strip(',')
		
		#print "keybyte ", keybyte
		tmp = long(keybyte, 16) << (8*index)	
		keyvalue += tmp
		
		N_str += keybyte[2:4]
		N_hex_str = N_str.decode("hex")

	#print "N_hex_str len :", len(N_hex_str)
	#print "N_hex_str  :", N_hex_str		
	#print '\n- N Key value:\n', keyvalue
	n1=keyvalue

	# ----------------- e ---------------------------
	keystring = parse_RSA_info('publicExponent', RSAinfo_str)
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
		
	#print '\n- e Key value:\n', keyvalue
	e1=keyvalue

	# ----------------- d ---------------------------
	keystring = parse_RSA_info('privateExponent', RSAinfo_str)
	keydata = keystring.split();#split by space
	#print len(keydata), '\n'
	keyvalue=0
	d_str=''
	d_hex_str=''
	for index in range(len(keydata)):
		keybyte = keydata[index].strip(',')
		tmp = long(keybyte, 16) << (8*index)	
		keyvalue += tmp
		
		d_str += keybyte[2:4]
		d_hex_str = d_str.decode("hex")
	
	#print '\n- d Key value:\n', keyvalue
	d1=keyvalue
	
	'''
	# ----------------- RRmodN ---------------------------
	keystring = parse_RSA_info('RRModN', RSAinfo_str)
	keydata = keystring.split();#split by space
	#print len(keydata), '\n'
	keyvalue=0
	RRModN_str=''
	RRModN_hex_str=''
	for index in range(len(keydata)):
		keybyte = keydata[index].strip(',')
		#tmp = long(keybyte, 16) << (8*index)	
		#keyvalue += tmp
		
		RRModN_str += keybyte[2:4]
		RRModN_hex_str = RRModN_str.decode("hex")

	#print "\nRRModN_hex_str len :", len(RRModN_hex_str)
	#print "RRModN_hex_str  :\n", RRModN_hex_str		
	
	# ----------------- np_inv32 ---------------------------
	keystring = parse_RSA_info('np_inv32', RSAinfo_str)
	#print "upinv32: ", hex(int(keystring))[2:18]
	
	
	#print "upinv32: ", hex(int(keystring))[2:18].strip('L')
	np_inv32_hex_str = hex(int(keystring))[2:18].strip('L')
	if(len(np_inv32_hex_str)%2 != 0):
		np_inv32_hex_str = '0'+ np_inv32_hex_str
	
	#print "upinv32: ", np_inv32_hex_str
	np_inv32_hex_str = np_inv32_hex_str.decode("hex")
	#np_inv32_hex_str = hex(int(keystring))[2:18].decode("hex")
	#print "np_inv32_hex_str len :", len(np_inv32_hex_str)
	#print "np_inv32_hex_str  :\n", np_inv32_hex_str
	'''


	#------------------------- Calculate RSA key -------------------------------
	n=long(n1)
	e=long(e1)
	d=long(d1)
	pub_key = RSA.construct((n,e))
	pri_key = RSA.construct((n,e,d))

	#print '\n- pub_key:\n', pub_key
	#print '- pri_key:\n', pri_key

	RSA_plaintext = hash_data
	#RSA_plaintext = plaintext
	#print '\nplaintext:\n', RSA_plaintext, "\n", b2a_hex(RSA_plaintext), "\n", len(RSA_plaintext) #plaintext

	'''
	f = open('RSA_MD5_plaintext_100k.txt', 'w')
	plaintext_hex = b2a_hex(RSA_plaintext)
	#print len(plaintext_hex)
	for index in range(0, len(plaintext_hex), 2):
		str1 = "0x" + plaintext_hex[index] + plaintext_hex[index+1] + ", "
		#print str
		f.write(str1)
	'''
	#-------- Encrypt & Decrypt -------------#	
	#----- encrypted -----
	RSA_ciphertext = pub_key.encrypt(RSA_plaintext, '')
	#print '\nRSA Ciphertext:\n', b2a_hex(RSA_ciphertext[0])


	#f = open('RSA_Ciphertext.txt', 'w')
	f_binary = open('Test_RSA_AES_pattern.bin', 'wb')
	f_binary.write(RSA_ciphertext[0])

	#----- decrypted -----
	RSA_de_plaintext = pri_key.decrypt(RSA_ciphertext)
	#print '\nRSA plaintext:\n', RSA_de_plaintext, "\n", b2a_hex(RSA_de_plaintext) #plaintext

	#--------- Sign & verify ----------------#
	
	#----- sign -----
	RSA_signature = pri_key.sign(RSA_plaintext, '')
	#print '\nRSA_signature:\n', hex(RSA_signature[0])

	#RSA_sig_str = str(hex(RSA_signature[0]))
	#RSA_sig_str = format(RSA_signature[0], 'x')
	tmp_str = hex(RSA_signature[0])[2:-1]
	if(len(tmp_str)%2 != 0):
		tmp_str = '0'+ tmp_str
	#print "tmp str \n", tmp_str
	#print "tmp str len \n", len(tmp_str)
	#RSA_sig_str = hex(RSA_signature[0])[2:-1].decode("hex")
	RSA_sig_str = tmp_str.decode("hex")
	#print "\nRSA_sig_str :\n", b2a_hex(RSA_sig_str)
	#print "\nRSA_sig_str len :", len(RSA_sig_str)

	#for index in range(512, 1, -2):
	sig_text = ""
	for index in range(2, 514, 2):
		sig_text += RSA_sig_str[index:index+2]
		#str = "0x" + RSA_sig_str[index] + RSA_sig_str[index+1] + ", "
		#sig_str += str
		#print str
		#f.write(str)
	#print "\nSig_text :\n", sig_text
	
	f_test = open('RSA_test.txt','wb')
	for index in range(0, 513, 2):
		str = "0x" + tmp_str[index:index+2] + ", "
		#print str
		f_test.write(str)
	
	'''
	#----- verify -----
	RSA_iscorrect = pub_key.verify(RSA_plaintext,RSA_signature)
	if(RSA_iscorrect):
		#print "PASS"
	else:
		#print "FAIL"
	'''
	#--------------- AES_HASH with RSA ciphertext -------------------#	
	# padding and swap 
	PS_rsacipher  = pad_swap( RSA_ciphertext[0])
	#print "\nPS_rsacipher : \n", b2a_hex(PS_rsacipher)

	# encrypt
	PS_rsacipher_aescipher = aes_encrypt(PS_rsacipher, AESkey)
	#print "\nPS_rsacipher_aescipher : \n", b2a_hex(PS_rsacipher_aescipher)

	# padding and swap 
	PS2_rsacipher_aescipher = pad_swap(PS_rsacipher_aescipher)
	#print "\nPS2_rsacipher_aescipher : \n", b2a_hex(PS2_rsacipher_aescipher)	
	

	#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	#-------------------------------------------- Combine Binary & Output Bin File (.bin) ----------------------------------------------------#

	flash_bootrom_str = PS2_aes_ciphertext + PS2_rsacipher_aescipher
	#print "\nflash_bootrom_str : \n", flash_bootrom_str
	#print "\nflash_bootrom_str len : ", len(flash_bootrom_str)
	
	f_flash_bootrom = open(sys.argv[6] + '\\flash_bootrom_code_tooltest.bin','wb')
	f_flash_bootrom.write(flash_bootrom_str)
	
else:
	#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	#----------------------------------------------------- HASH with Boot code -----------------------------------------------------------#
	
	PS_plaintext  = pad_swap(plaintext)
	#print "PS_plaintext len :",  len(PS_plaintext)
	
	'''
	#------------- encrypt --------------
	aes_ciphertext = aes_encrypt(PS_plaintext, AESkey)
	#print "ciphertext : ",  aes_ciphertext

	# padding and swap 
	PS2_aes_ciphertext = pad_swap(aes_ciphertext)
	#print "PS2_aes_ciphertext : ",  PS2_aes_ciphertext
	'''
	
	hash_bootcode = hash(PS_plaintext, hash_mode)
    
	#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	#------------------------------------------------- RSA with boot code hash-------------------------------------------------------------------#
	#f = open('RSA2048_3.text','rb')
	f = open(sys.argv[4],'rb')
	RSAinfo_str = f.read()
	

	# ----------------- N ---------------------------
	keystring = parse_RSA_info('modulus', RSAinfo_str)
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

	#print "N_hex_str len :", len(N_hex_str)
	#print "N_hex_str  :", N_hex_str		
	#print '\n- N Key value:\n', keyvalue
	n1=keyvalue

	# ----------------- e ---------------------------
	keystring = parse_RSA_info('publicExponent', RSAinfo_str)
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
		
	#print '\n- e Key value:\n', keyvalue
	e1=keyvalue

	# ----------------- d ---------------------------
	keystring = parse_RSA_info('privateExponent', RSAinfo_str)
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
	
	#print '\n- d Key value:\n', keyvalue
	d1=keyvalue
	
	'''
	# ----------------- RRmodN ---------------------------
	keystring = parse_RSA_info('RRModN', RSAinfo_str)
	keydata = keystring.split();#split by space
	#print len(keydata), '\n'
	keyvalue=0
	RRModN_str=''
	RRModN_hex_str=''
	for index in range(len(keydata)):
		keybyte = keydata[index].strip(',')
		#tmp = long(keybyte, 16) << (8*index)	
		#keyvalue += tmp
		
		RRModN_str += keybyte[2:4]
		RRModN_hex_str = RRModN_str.decode("hex")

	#print "\nRRModN_hex_str len :", len(RRModN_hex_str)
	#print "RRModN_hex_str  :\n", RRModN_hex_str		
	
	# ----------------- np_inv32 ---------------------------
	keystring = parse_RSA_info('np_inv32', RSAinfo_str)
	#print "upinv32: ", hex(int(keystring))
	#print "upinv32: ", hex(int(keystring))[2:18]
	np_inv32_hex_str = hex(int(keystring))[2:18].decode("hex")
	#print "np_inv32_hex_str len :", len(np_inv32_hex_str)
	#print "np_inv32_hex_str  :\n", np_inv32_hex_str
	'''
	
	#------------------------- Calculate RSA key -------------------------------
	n=long(n1)
	e=long(e1)
	d=long(d1)
	pub_key = RSA.construct((n,e))
	pri_key = RSA.construct((n,e,d))

	#print '\n- pub_key:\n', pub_key
	#print '- pri_key:\n', pri_key

	RSA_plaintext = hash_bootcode
	#RSA_plaintext = plaintext
	#print '\nplaintext:\n', RSA_plaintext, "\n", b2a_hex(RSA_plaintext), "\n", len(RSA_plaintext) #plaintext

	'''
	f = open('RSA_MD5_plaintext_100k.txt', 'w')
	plaintext_hex = b2a_hex(RSA_plaintext)
	#print len(plaintext_hex)
	for index in range(0, len(plaintext_hex), 2):
		str1 = "0x" + plaintext_hex[index] + plaintext_hex[index+1] + ", "
		#print str
		f.write(str1)
	'''
	#-------- Encrypt & Decrypt -------------#	
	#----- encrypted -----
	RSA_ciphertext = pub_key.encrypt(RSA_plaintext, '')
	#print '\nCiphertext:\n', b2a_hex(RSA_ciphertext[0])


	#f = open('RSA_Ciphertext.txt', 'w')
	f_binary = open('Test_RSA_AES_pattern.bin', 'wb')
	f_binary.write(RSA_ciphertext[0])

	#----- decrypted -----
	RSA_de_plaintext = pri_key.decrypt(RSA_ciphertext)
	#print '\nplaintext:\n', RSA_de_plaintext, "\n", b2a_hex(RSA_de_plaintext) #plaintext

	#--------- Sign & verify ----------------#
	#----- sign -----
	RSA_signature = pri_key.sign(RSA_plaintext, '')
	#print '\nRSA_signature:\n', hex(RSA_signature[0])

	#RSA_sig_str = str(hex(RSA_signature[0]))
	#RSA_sig_str = format(RSA_signature[0], 'x')
	tmp_str = hex(RSA_signature[0])[2:-1]
	if(len(tmp_str)%2 != 0):
		tmp_str = '0'+ tmp_str
	#print "tmp str \n", tmp_str
	#RSA_sig_str = hex(RSA_signature[0])[2:-1].decode("hex")
	RSA_sig_str = tmp_str.decode("hex")
	
	#print "\nRSA_sig_str :\n", b2a_hex(RSA_sig_str)
	#print "\nRSA_sig_str len :", len(RSA_sig_str)
	
	#----- verify -----
	RSA_iscorrect = pub_key.verify(RSA_plaintext,RSA_signature)
	#if(RSA_iscorrect):
		#print "PASS"
	#else:
		#print "FAIL"
	
	#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	#-------------------------------------------- Combine Binary & Output Bin File (.bin) ----------------------------------------------------#
	P_plaintext = pad(plaintext)
	
	flash_bootrom_str = P_plaintext + RSA_ciphertext[0]

	#print "\nflash_bootrom_str:\n", flash_bootrom_str
	#print "\nflash_bootrom_str len:\n", len(flash_bootrom_str)
	
	#f_flash_bootrom = open('FW_NoSB_SHA256.bin','wb')
	f_flash_bootrom = open(sys.argv[6] + '\\FW_NoSB_SHA256.bin','wb')

	f_flash_bootrom.write(flash_bootrom_str)
	
	
#output bin file





