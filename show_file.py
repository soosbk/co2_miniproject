from tkinter import *

result=Tk()

def end_fun():
	result.destory()

def read_file(mode,file_name):

	
	try:

		if mode==1: #image file
			image=PhotoImage(file=file_path)
			Label(result, image=image).pack()


		elif mode==2:

			with open("file.txt") as f:
				data = f.readlines()[10]
			Label(result, image="[간단히보기모드]"+data).pack()

			
	except Exception as e:
		print(">> Warning while read_file) ",e)

	btn=Button(result,text="종료",command=end_fun)
	btn.pack()
	result.mainloop()








