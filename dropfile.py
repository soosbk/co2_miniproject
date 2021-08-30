# 01.22.2021

from pathlib import Path

from tkinter import filedialog
from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox

window=Tk()
window.title("image encryption program")    
window.geometry('320x400')  



def get():
    """
    Gets file/directory via drag and drop and return a Path object.
    Asks for file or directory via drag and drop, strips unneeded characters,
    and uses pathlib.Path to return a Path object.
    Returns:
    - (pathlib.PosixPath object): A pathlib.PosixPath object that can be 
    used to get file path, filname, extension, etc. 
    Sample Usage:
    - p = dropfile.get()
        - p = full path
        - p.parent = parent folder
        - p.stem = filename excluding extension
        - p.suffix = file extension
    """
    
    # Get input file/folder and strip characters
    f = input('\n Drop File: ')
    f = f.strip(" &'\"")
    f = f.replace("\ ", " ")
    # set Path object and return
    p = Path(f).resolve()
    return p
frame=Text(window,text=input("경로를 입력하세요"))
frame.pack()
#"출력 형태 선택(image, txt)"
#Entry(frame, ).pack()
#Label(window,text=).pack()
window.mainloop()