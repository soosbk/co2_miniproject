from tkinter import filedialog
from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox

from encryption_fun import *
#AES 128bit -> key size=16bit

import binascii, os, random, struct
from Crypto.Util import Counter
from Crypto.Cipher import AES 


#---- fix ----
key_size = 16
block_size = 128


#random한 key, iv 생성
key = bytes([random.randint(0,block_size) for i in range(0,key_size)]) 
IV = bytes([random.randint(0,block_size) for i in range(0,key_size)]) 

#--------------


#---- 기본값 ----
aes_mode='ECB'
output_type=1


    



file_root='/'
dir_path='/'
#--------------

def value_get():
	global aes_mode
	global output_type
	global key
	global IV
	global dir_path
	aes_mode=mode.get()
	output_type=file_type.get()
	

	window.destroy()


def file_choose_button():
	global file_root
	file_root=filedialog.askopenfilename()


def dir_choose_button():
	global dir_path
	dir_path=filedialog.askdirectory(parent=window,initialdir="/",title='Please select a directory')
 
#----------------
aesmode=AES.MODE_ECB
def setAESMode(aes_mode):
	global aesmode
	if aes_mode=="ECB": aesmode=AES.MODE_ECB
	elif aes_mode=="CBC": aesmode=AES.MODE_CBC
	elif aes_mode=="CFB": aesmode=AES.MODE_CFB
	elif aes_mode=="OFB": aesmode=AES.MODE_OFB
	elif aes_mode=="CTR": aesmode = AES.MODE_CTR
	


#----------------

window=Tk()
window.title("image encryption program")	
window.geometry('320x400')	




#"출력 형태 선택(image, txt)"

Label(window,text="출력형태를 선택하세요").pack()
file_type=IntVar()
op1=Radiobutton(window,text="이미지",value=1,variable=file_type)
op1.select() #기본선택
op2=Radiobutton(window,text="텍스트파일",value=2,variable=file_type)

op1.pack()
op2.pack()

#"AES 모드 선택하기"
Label(window,text="AES 모드를 선택하세요").pack()

mode=Combobox(window,height=10,state="readonly")
mode['values']=('ECB','CBC','CFB','OFB','CTR')

mode.pack()

	
pcb=Button(window,text="이미지를 선택하세요",command=file_choose_button)
dcb=Button(window,text="저장할 위치를 선택하세요",command=dir_choose_button)
btn=Button(window,text="제출",command=value_get)


pcb.pack()
dcb.pack()
btn.pack()
window.mainloop()


setAESMode(aes_mode)
file_root_bmp=file_extension_change(file_root,1)
	
if output_type==1: #image 
	file_path=dir_path+file_extension_change(file_root_bmp,3,aes_mode)
	
	print(file_path)
	if aes_mode=='ECB': encrypt_bmp_file1(key, aesmode,  file_root_bmp, out_filename = file_path)
	elif aes_mode=="CTR":
		ctr_e = Counter.new(128)
		encrypt_bmp_file2(key, aesmode, ctr_e, file_root_bmp, out_filename = file_path)

	else: encrypt_bmp_file2(key, aesmode, IV, file_root_bmp, out_filename = file_path)


else: #txt
	file_path=dir_path+file_extension_change(file_root_bmp,2,aes_mode)
	print(file_path)

	if aes_mode=='ECB': encryption_txt1(key, aesmode, file_root_bmp, out_filename = file_path)
	
	elif aes_mode=="CTR":
		
		ctr_e = Counter.new(128)
		encryption_txt2(key, aesmode, ctr_e, file_root_bmp, out_filename = file_path)

	else: encryption_txt2(key, aesmode, IV, file_root_bmp, out_filename = file_path)



print(file_path)


image = Image.open(file_path)
 
image.show()
