from tkinter import filedialog

import crypto 
import sys 
sys.modules['Crypto'] = crypto

from Crypto.Random import get_random_bytes 
from Crypto.Util import Counter
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES 
# base64 모듈 --> 암호문을 64개의 아스키코드 상 문자로 변환
from base64 import b64encode
from pathlib import Path

import binascii, os, random, struct
import json
from PIL import Image   #bmp file로 부터 bit 타입 일끼


#=======================================

def file_extension_change(file_root,option,aes_mode=None):
	dot=0
	for i in range(len(file_root)-1,0,-1):
			if file_root[i]=='.': 
				dot=i
				break
	
		
	if(option==1):
		im=Image.open(file_root)
		file_root_bmp=file_root[0:dot+1]
		file_root_bmp+='bmp'
		im.save(file_root_bmp)
		return file_root_bmp
	

	elif(option==2):  #txt로 옮기기
		bar=0
		for i in range(dot,0,-1):
			if file_root[i]=='/':
				bar=i
				break

		file_root_txt=file_root[bar:dot]
		file_root_txt+=aes_mode+'.txt'
		return file_root_txt


	elif(option==3): #bmp 파일로 변경하기
		bar=0
		for i in range(dot,0,-1):
			if file_root[i]=='/':
				bar=i
				break

		file_root_txt=file_root[bar:dot+1]
		file_root_txt+=aes_mode+'.bmp'
		return file_root_txt



def convert2RGB(data):
	r, g, b = tuple(map(lambda d: [data[i] for i in range(0,len(data))\
	if i % 3 == d], [0, 1, 2]))



	pixels = tuple(zip(r,g,b))
	return pixels



def encryption_txt1(key, mode,in_filename, out_filename = None): # 2번에서 호출 시 전달받음 ->ECB
	im = Image.open(in_filename)
	data = im.convert("RGB").tobytes()
	original = len(data)
	# PKCS7 Padding
	pad_len = 16 - len(data) % 16
	pad = pad_len.to_bytes(1, byteorder='big', signed = False) * pad_len
	data += pad
    # Encryption by given mode
	encryptor = AES.new(key, mode)
	encrypted = convert2RGB(encryptor.encrypt(data)[:original])
	ciphertext = json.dumps(encrypted).encode('utf8')
	encfile = open(out_filename, 'wb') # 새 텍스트파일을 생성해서 염 
	encfile.write(ciphertext) # 암호문을 저장함
	print ("{} is encrypted.".format(in_filename))

def encryption_txt2(key, mode,iv, in_filename, out_filename = None): # 2번에서 호출 시 전달받음 ->ECB
	im = Image.open(in_filename)
	data = im.convert("RGB").tobytes()
	original = len(data)
	# PKCS7 Padding
	pad_len = 16 - len(data) % 16
	pad = pad_len.to_bytes(1, byteorder='big', signed = False) * pad_len
	data += pad
    # Encryption by given mode
	encryptor = AES.new(key, mode)
	encrypted = convert2RGB(encryptor.encrypt(data)[:original])
	ciphertext = json.dumps(tuple(iv)+encrypted).encode('utf8')
	encfile = open(out_filename, 'wb') # 새 텍스트파일을 생성해서 염 
	encfile.write(ciphertext) # 암호문을 저장함
	print ("{} is encrypted.".format(in_filename))

def encrypt_bmp_file1(key, mode, in_filename, out_filename = None):
	# Get RGB data from BMP file
	im = Image.open(in_filename)
	data = im.convert("RGB").tobytes()
	original = len(data)
	# PKCS7 Padding
	pad_len = 16 - len(data) % 16
	pad = pad_len.to_bytes(1, byteorder='big', signed = False) * pad_len
	data += pad
	# Encryption by given mode
	encryptor = AES.new(key, mode)
	encrypted = convert2RGB(encryptor.encrypt(data)[:original])
	# Create a new PIL Image object and
	
	# save the old image data into the new image.
	im2 = Image.new(im.mode, im.size)
	im2.putdata(encrypted)
	# Save image
	im2.save(out_filename)
	print ("{} is encrypted.".format(in_filename))

def encrypt_bmp_file2(key, mode, iv,in_filename, out_filename = None):
	# Get RGB data from BMP file
	im = Image.open(in_filename)
	data = im.convert("RGB").tobytes()
	original = len(data)
	# PKCS7 Padding
	pad_len = 16 - len(data) % 16
	pad = pad_len.to_bytes(1, byteorder='big', signed = False) * pad_len
	data += pad
	# Encryption by given mode
	if mode==AES.MODE_CTR: encryptor = AES.new(key, mode,counter =iv)
	else: encryptor = AES.new(key, mode,iv)

	encrypted = convert2RGB(encryptor.encrypt(data)[:original])
	# Create a new PIL Image object and
	
	# save the old image data into the new image.
	im2 = Image.new(im.mode, im.size)
	im2.putdata(encrypted)
	# Save image
	im2.save(out_filename)
	print ("{} is encrypted.".format(in_filename))
