#!/usr/bin/python3

from tkinter import filedialog, Menu
from tkinter import ttk as tk
from os import path, stat, getcwd
from math import ceil
from zip_unzip import zipper

class Button(tk.Button):
    def __init__(self,root = None):
        super().__init__(root,text="+")
        self.pack(side="top")

    def click(self,func):
        def func_wrapper(str_param):
            print(str_param + "of" + func.__name__)

    def setWidgetName(name):
        self.widgetName = "btn"

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        menu = Menu(self.master)
        self.master.config(menu=menu)
        fileMenu = Menu(menu)
        menu.add_cascade(label="file",menu=fileMenu)
        fileMenu.add_command(label="Open")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        btn1 = Button(self.master)
        btn1.bind("<Button-1>",self._openFileExplorer)

    def _openFileExplorer(self,event):
        abspath = getcwd()
        fn = filedialog.askopenfilename(initialdir="~",title="Select a File",filetypes=( ("pdf files","*.pdf"), ) )
        if len(fn) > 0:
            #basedir = path.dirname(abspath)
            if ceil(stat(fn).st_size/1024) > 1000:
                zipper.multizip(fn,abspath)
    def _compress_file(file):
        print("compressing file")





root = tk.setup_master()
root.title("RuralSync")
root.geometry("300x300")
style = tk.Style()
app = Application(master=root)
app.mainloop()


