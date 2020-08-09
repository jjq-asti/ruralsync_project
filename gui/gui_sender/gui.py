#!/usr/bin/python3

from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from os import path, stat, getcwd
from math import ceil
from datetime import datetime
from zip_unzip import zipper
from database import db
from database.db import Files
#class Button(Button):
#    def __init__(self,root = None):
#        super().__init__(root,text="+", style="TButton")
#        self.pack(side=TOP)

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master,style="TFrame")
        self.master = master
        self.pack()
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        fileMenu = tk.Menu(menu)
        menu.add_cascade(label="file",menu=fileMenu)
        fileMenu.add_command(label="Open")
        self.carouselState = tk.IntVar()
        self.carouselState.set(0)
        self.item_id = None
        self.item = None
        self.rows = None
        self.create_widgets()

    def create_widgets(self):
        self.AddBtn = ttk.Button(self.master,text="+")
        self.AddBtn.pack(side=tk.TOP)
        self.AddBtn.bind("<Button-1>",self._openFileExplorer)
        self.TreeView = ttk.Treeview(self.master)
        self.TreeView["columns"] = (1,2,3)
        self.TreeView["selectmode"] = "browse"
        self.TreeView.column("#0", width=500, minwidth=150, stretch=False)
        self.TreeView.column(1, width=80, minwidth=80, stretch=False)
        self.TreeView.column(2, width=200, minwidth=200, stretch=False)
        self.TreeView.column(3, width=100, minwidth=100, stretch=False)
        self.TreeView.heading("#0",text="File Name", anchor=tk.W)
        self.TreeView.heading(1,text="Size", anchor=tk.W)
        self.TreeView.heading(2,text="Date Added", anchor=tk.W)
        self.TreeView.heading(3,text="Owner", anchor=tk.W)
        self.TreeView.bind('<Button-1>',self.handle_click)
        self.TreeView.pack()
        self._InitTreeView()
        self.BottomFrame = ttk.Frame(self.master,style="bottom.TFrame")
        self.BottomFrame.pack()
        self.Carousel = ttk.Checkbutton(self.BottomFrame,text="Carousel",variable=self.carouselState,style="TCheckbutton",command=self._Carousel)
        self.Carousel.pack(side=tk.LEFT,padx=30)

        self.RemoveButton = ttk.Button(self.BottomFrame,text="Remove",style="Remove.TButton",command = self._RemoveFile)
        self.RemoveButton.pack(side=tk.RIGHT,pady=15)

    def _InitTreeView(self):
        conn = db.connectDB("test.db")
        self.Filedb = Files(conn)
        self.rows = self.Filedb.getAllData()
        if len(self.rows) > 0:
            for i in self.rows:
                fileName = i[1] + "." + i[2]
                date = i[3]
                size = i[4]
                owner = i[6]
                tag = i[0]
                self.TreeView.insert("", 0, text=fileName, values=( size + " MB",date,owner),tags=tag)
            conn.close()
            del i

    def _RemoveFile(self):
        conn = db.connectDB("test.db")
        self.Filedb = Files(conn)
        print(self.item_id)
        self.Filedb.removeRecord(self.item_id)
        conn.commit()
        conn.close()
        self.TreeView.delete(self.item)

    def _Carousel(self):
        conn = db.connectDB("test.db")
        self.Filedb = Files(conn)
        rec = self.Filedb.getDataUsingId(self.item_id)
        print(rec)
        if rec[0] == self.item_id:
            abspath = path.join(rec[5],rec[1]) + "." + rec[2]
            print("CS ", self.carouselState.get())
            self.Filedb.updateCarousel(self.item_id,self.carouselState.get())
            conn.commit()
            conn.close()
            zipper.multizip(abspath,"/home/jay/ruralsync_project/files/"+rec[1]+"."+rec[2]+"_"+".zip")

    def _openFileExplorer(self,event):
        abspath = getcwd()
        fn = filedialog.askopenfilename(initialdir="~/Documents",title="Select a File",filetypes=( ("pdf files","*.pdf"),("all files","*.*") ) )
        if len(fn) > 0:
            fileName = path.basename(fn)
            filedir = path.dirname(fn)
            fileSize = ceil(stat(fn).st_size/1024)
            if fileSize > 1000:
                pass
                #zipper.multizip(fn,abspath)
            now = datetime.now()
            date = datetime.strftime(now,"%m-%d-%Y %H:%M")
            size = "{:.1f}".format(fileSize/1000)
            prep_data = { 
            "name": fileName, 
            "size": size,
            "date": date, 
            "dir" : filedir,
            "owner": "asti"
            }
            record = self._prepare_record(**prep_data)
            conn = db.connectDB("test.db")
            self.Filedb = Files(conn)
            id = self.Filedb.insertData(record)
            conn.commit()
            conn.close()
            self.TreeView.insert("", 0, text=fileName, values=( size + " MB",date,"ASTI"),tags=id)           

    def _prepare_record(self,**kwargs):
        name_xtension = kwargs["name"].split(".") 
        name = name_xtension[0]
        extension = name_xtension[1]
        size = kwargs["size"]
        date = kwargs["date"]
        fdir = kwargs["dir"] 
        carousel = 0
        owner = kwargs["owner"]

        return (name,extension,date,size,fdir,owner,carousel)

    def handle_click(self,event):
        if self.TreeView.identify_region(event.x, event.y) == "separator":
            return "break"
        elif self.TreeView.identify_region(event.x,event.y) == "cell" or self.TreeView.identify_region(event.x,event.y) == "tree":
            self.item = self.TreeView.identify('item', event.x, event.y)
            #print("ITEM IS " + item)
            item_content = self.TreeView.item(self.item)
            self.item_id = item_content["tags"][0]
            conn = db.connectDB("test.db")
            self.Filedb = Files(conn)
            CS = self.Filedb.getCarouselStatus(self.item_id)
            conn.close()
            self.carouselState.set(CS)
        



root = ttk.setup_master()
root.title("RuralSync")
root.geometry("1000x340")
root.resizable(False,False)
style = ttk.Style()
style.configure("TButton", background="tomato")
style.configure("Remove.TButton",background="red")
style.configure("bottom.TFrame", width=40)
app = Application(master=root)
#root.protocol("WM_DELETE_WINDOW",app.on_close_window)
app.mainloop()


