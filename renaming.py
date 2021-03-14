# Python program to create 
# a file explorer in Tkinter

import PIL.Image

from os import listdir,fsdecode,rename
from os.path import isfile, join, splitext
import pathlib

# import all components
# from the tkinter library
from tkinter import *
from tkinter import ttk, messagebox

# import filedialog module
from tkinter import filedialog

# Goable vaiables
Ext = (".jpg", ".jpeg")
FileList = []
FileListWithTime = []
Girectoryname = None
ProcessDone = True

# Create the windows window
windows = Tk()
  
# Set window title
windows.title('图片文件名修改器 - v0.2 - 作者:Yihua @ Mar 1, 2021')
  
# Set window size
# window.geometry("700x500")
  
#Set window background color
windows.config(background = "white")

content = ttk.Frame(windows, padding=(3,3,12,12))
frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=700, height=500)
namelbl = ttk.Label(content, text="自定义后辍")
name = ttk.Entry(content)
listbox = Listbox(content, height=5)
listScrollbar = ttk.Scrollbar(content, orient=VERTICAL, command=listbox.yview)
ExistingName = BooleanVar(value=False)
i = BooleanVar(value=False)

# Function for opening the 
# file explorer window
def onClick(var):
    global ExistingName
    ExistingName = var.get()

    if var:
        var = False
    else:
        var = True
    print (ExistingName)


        
def browseFiles():
    directoryname = filedialog.askdirectory()
      
    # Change label contents
    if directoryname:
        listbox.delete(0,'end')
        global Girectoryname,Ext,ProcessFiles, FileList,FileListWithTime
        Girectoryname = directoryname
        ext = Ext
        onlyfiles = [f for f in listdir(directoryname) if isfile(join(directoryname, f)) if f.lower().endswith(tuple(ext))]
        label_file_explorer.configure(text="已选择文件目录: "+directoryname+" 共发现 %d 个图片文件" % len(onlyfiles))

        filesString = ''
        for eachFile in onlyfiles:
            imageFile = directoryname + "/" + eachFile    
            img = PIL.Image.open(imageFile)
            exif_data = img._getexif()
            try:
                ImageDate = exif_data[36867]
            except:
                ImageDate = None
            if ImageDate:
                listbox.insert('end', '%s 【可修改】' % eachFile)
                FileList.insert(1, eachFile)
                FileListWithTime.insert(1, ImageDate)
            else:
                listbox.insert('end', '%s 【无法读取到拍摄日期】' % eachFile)

        listbox.update_idletasks()
        ProcessFiles = False

def processDurectory():
    global Girectoryname,Ext,ProcessFiles,FileList,FileListWithTime,ExistingName
    directoryname = Girectoryname
    ext = Ext
    entryString = name.get()
    
    if not ProcessFiles:
        confirm = messagebox.askyesnocancel(title="确认执行", message="请先做好文件备份，点击确认继续对所有【可修改】项目重命名。")

        if confirm and directoryname:
            listbox.delete(0,'end')
            processCounter = 0
            print(FileList)
            print(FileListWithTime)
            if len(FileList) == len(FileListWithTime):
                for fileIndex in range(len(FileList)):
                    filename = FileList[fileIndex]
                    newFileName = FileListWithTime[fileIndex].replace(':', '')
                    newFileName = newFileName.replace(' ', '_')
                    if ExistingName:
                        newFileName += ("_"+ splitext(filename)[0])
                    if entryString:
                        newFileName += ("_"+entryString)
                    newFileName = newFileName + pathlib.Path(filename).suffix
                    rename(directoryname + "/" + filename, directoryname + "/" + newFileName)
                    processCounter = processCounter+1
                    listbox.insert('end', '%s ===> %s【修改成功】' % (filename, newFileName))
                FileListWithTime = []
                FileList = []
                ProcessFiles = True
                messagebox.showinfo(title="成功处理完成", message="处理完成 %d 个文件。" % processCounter)
                label_file_explorer.configure(text="成功处理完成 %d 个文件。" % processCounter)
            else:
                messagebox.showerror(title="错误", message="内部错误，code=11")
    else:
        messagebox.showerror(title="请重新选择目录", message="不能重复执行，请重新选择目录后再次尝试。")
        
                                                                                                  

  
# Create a File Explorer label


label_file_explorer = ttk.Label(content, text="请先选择文件目录", foreground="blue")

ok = ttk.Button(content, text="Okay")
button_explore = ttk.Button(content, text = "浏览文件目录", command = browseFiles) 
button_process = ttk.Button(content, text = "执行修改", command = processDurectory) 
keepExistingName = ttk.Checkbutton(content, text="保留原文件名", variable=i,  onvalue=True, offvalue=False, command=lambda i=i: onClick(i))

cancel = ttk.Button(content, text="Cancel")


content.grid(column=0, row=0, sticky=(N, S, E, W))

listbox['yscrollcommand'] = listScrollbar.set

frame.grid(column=0, row=0, columnspan=3, rowspan=3, sticky=(N, S, E, W))
listbox.grid(column=0, row=0, columnspan=3, rowspan=3,sticky=(N,W,E,S))

namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), padx=5)
name.grid(column=3, row=1, columnspan=2, sticky=(N,E,W), pady=5, padx=5)
keepExistingName.grid(column=3, row=2, columnspan=2, sticky=(N,W), pady=5, padx=5)

label_file_explorer.grid(column=1, row=4)
button_explore.grid(column=3, row=4)
button_process.grid(column=4, row=4)

windows.columnconfigure(0, weight=1)
windows.rowconfigure(0, weight=1)

content.rowconfigure(1, weight=1)
content.rowconfigure(2, weight=1)

content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)




# Let the window wait for any events
windows.mainloop()
