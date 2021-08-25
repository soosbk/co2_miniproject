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




def encryption_txt(window, imgfile_path, key_size, block_size, aes_mode): # 1번에서 호출 시 전달받음
    imgfile = open(imgfile_path, 'rb') # 이미지파일을 염
    plaintext = imgfile.read() # 읽어서 저장한 것으로 평문
    paddedtext = pad(plaintext, block_size) # 평문을 패딩함
    key = get_random_bytes(key_size) # 키를 생성함
    if aes_mode == 'ECB': # 모드를 선택함
        cipher = AES.new(key, AES.MODE_ECB) # ECB 모드의 AES 객체를 생성함
        ciphertext = cipher.encrypt(paddedtext) # 패딩한 평문을 암호화 함
        ciphertext = b64encode(ciphertext) # 이를 아스키코드 상 문자로 변환한 것으로 암호문
    if aes_mode == 'CBC': # 모드를 선택함
        iv = get_random_bytes(AES.block_size) # 초기화벡터를 생성함
        cipher = AES.new(key, AES.MODE_CBC, iv) # CBC 모드의 AES 객체를 생성함
        ciphertext = cipher.encrypt(paddedtext) # 패딩한 평문을 암호화 함
        ciphertext = b64encode(iv + ciphertext) # 이를 아스키코드 상 문자로 변환한 것으로 암호문
    dir_path = filedialog.askdirectory(parent=window,initialdir="/",title='Please select a directory')
    print(dir_path)
    dir_path+=file_extension_change(imgfile_path,2)
    encfile = open(dir_path, 'wb') # 새 텍스트파일을 생성해서 염 
    encfile.write(ciphertext) # 암호문을 저장함
    return dir_path


def convert2RGB(data):
	r, g, b = tuple(map(lambda d: [data[i] for i in range(0,len(data))\
	if i % 3 == d], [0, 1, 2]))



	pixels = tuple(zip(r,g,b))
	return pixels


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
	encryptor = AES.new(key.encode("utf8"), mode)
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
	encryptor = AES.new(key.encode("utf8"), mode,iv.encode("utf8"))
	encrypted = convert2RGB(encryptor.encrypt(data)[:original])
	# Create a new PIL Image object and
	
	# save the old image data into the new image.
	im2 = Image.new(im.mode, im.size)
	im2.putdata(encrypted)
	# Save image
	im2.save(out_filename)
	print ("{} is encrypted.".format(in_filename))
def encryption_image1(key, mode, iv,in_filename, out_filename = None):
	# Get RGB data from BMP file
	im = Image.open(in_filename)
	data = im.convert("RGB").tobytes()
	original = len(data)
	# PKCS7 Padding
	pad_len = 16 - len(data) % 16
	pad = pad_len.to_bytes(1, byteorder='big', signed = False) * pad_len
	data += pad
	# Encryption by given mode
	encryptor = AES.new(key.encode("utf8"), mode,iv.encode("utf8"))
	encrypted = convert2RGB(encryptor.encrypt(data)[:original])
	# Create a new PIL Image object and
	
	# save the old image data into the new image.
	im2 = Image.new(im.mode, im.size)
	im2.putdata(encrypted)
	# Save image
	im2.save(out_filename)
	print ("{} is encrypted.".format(in_filename))

def decryption(encfile_path, imgfile_ext, key, block_size, aes_mode): # 1번에서 호출 시 전달받음
    encfile = open(encfile_path, 'rb') # 텍스트파일을 염
    ciphertext = encfile.read() # 읽어서 저장한 것으로 암호문
    ciphertext = b64decode(ciphertext) # 이를 b'...' 이런 이진데이터로 다시 변환함  
    if aes_mode == 'ECB': # 앞서 암호화 한 모드대로
        decipher = AES.new(key, AES.MODE_ECB) # ECB 모드의 AES 객체를 생성함
        deciphertext = decipher.decrypt(ciphertext) # 복호화 함
    if aes_mode == 'CBC': # 앞서 암호화 한 모드대로
        decipher = AES.new(key, AES.MODE_CBC, ciphertext[:AES.block_size]) # CBC 모드의 AES 객체를 생성함
        deciphertext = decipher.decrypt(ciphertext[AES.block_size:]) # 복호화 함
    plaintext = unpad(deciphertext, block_size) # 언패딩한 것으로 평문
    decfile = open('this is decrypted'+imgfile_ext, 'wb') # 새 이미지파일을 생성해서 염 --> 확장자는 원본 이미지파일과 같아야 함
    decfile.write(plaintext) # 평문을 저장함
