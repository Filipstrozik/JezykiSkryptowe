import os
import pathlib
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
from tkinter import filedialog
from pathlib import Path
from pubsub import pub


class View:
    def __init__(self, parent):
        self.container = parent
        self.menubar = tk.Menu(self.container)
        self.container.config(menu=self.menubar)

    def setup(self):

        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label="Open", command=self.set_path)

        self.main_side = tk.Frame(self.container)
        self.right_side = tk.Frame(self.container)

        self.button = tk.Button(self.right_side, text="SHOW PATH", command=self.showPath)

        self.newDirecoryLabel = tk.Label(self.right_side, text="new directory", height=1)
        self.newNameTextBox = tk.Text(self.right_side, height=1, width=20)

        self.btnCreateDir = tk.Button(self.right_side, text="create new directory", command=self.createNewDir)

        self.clean_up_label = tk.Label(self.right_side, text="cleanup", height=1)
        #checkbox for recursive cleaning folders,
        self.recursive_clean_up_var = tk.IntVar()

        self.recursive_clean_up_checkbox = tk.Checkbutton(self.right_side, text='deep clean up', variable=self.recursive_clean_up_var, onvalue=1, offvalue=0)
        #chceckbox for adding date of files not today!
        self.dated_clean_up_var = tk.IntVar()
        self.dated_clean_up_checkbox = tk.Checkbutton(self.right_side, text='dated clean up',
                                                          variable=self.dated_clean_up_var, onvalue=1, offvalue=0)

        self.clean_up_button = tk.Button(self.right_side, text="clean", command=self.clean_up)

        self.left_side = tk.Frame(self.container)

        self.tv = ttk.Treeview(self.left_side, show='tree')
        self.ybar = tk.Scrollbar(self.left_side, orient=tk.VERTICAL,
                                 command=self.tv.yview)
        self.xbar = tk.Scrollbar(self.left_side, orient=tk.HORIZONTAL, command=self.tv.xview)
        self.tv.configure(yscrollcommand=self.ybar.set, xscrollcommand=self.xbar.set)

        # self.directory = r'D:\MAIN\CODING\Sem 4'
        self.directory = str(Path.home() / 'Desktop')
        self.tv.heading('#0', text='Dir：' + self.directory, anchor='w')
        self.tv.column('#0', minwidth=600, width=400, stretch=True, anchor=CENTER)
        self.path = os.path.abspath(self.directory)
        self.node = self.tv.insert('', 'end', text=self.path, open=True)
        self.traverse_dir(self.node, self.path)

    def traverse_dir(self, parent, path): #this should update, if exists dont go deeper.
        for d in os.listdir(path):
            full_path = os.path.join(path, d)
            # print(d, os.path.getsize(full_path))
            isdir = os.path.isdir(full_path)
            if not isdir:
                id = self.tv.insert(parent, 'end', text=f'{d} [{os.path.getsize(full_path)}]', open=False)
            if isdir:
                id = self.tv.insert(parent, 'end', text=f'{d}', open=False)
                self.traverse_dir(id, full_path)

    def update_dir(self):
        for item in self.tv.get_children():
            self.tv.delete(item)
        self.tv.heading('#0', text='Dir：' + self.directory, anchor='w')
        # self.tv.column('#0', minwidth=600, width=200, stretch=True, anchor=CENTER)
        self.path = os.path.abspath(self.directory)
        self.node = self.tv.insert('', 'end', text=self.path, open=True)
        self.traverse_dir(self.node, self.path)

    def set_path(self):
        self.directory = tk.filedialog.askdirectory()
        self.update_dir()

    def setup_layout(self):

        self.ybar.pack(side='right', fill=tk.Y)
        self.xbar.pack(side='bottom', fill=tk.X)
        self.tv.pack(side='left', fill=Y)
        # self.tv.grid(row=0, column=0)
        self.left_side.pack(side='left', fill=Y)

        self.newDirecoryLabel.pack(fill=BOTH)
        self.newNameTextBox.pack(fill=BOTH)
        self.button.pack(fill=BOTH)
        self.btnCreateDir.pack(fill=BOTH)

        self.clean_up_label.pack(fill=BOTH)
        self.recursive_clean_up_checkbox.pack(fill=BOTH)
        self.dated_clean_up_checkbox.pack(fill=BOTH)
        self.clean_up_button.pack(fill=BOTH)


        self.right_side.pack(side='right', fill=BOTH)

    def showPath(self):  # redundancja
        item_iid = self.tv.selection()[0]
        parent_iid = self.tv.parent(item_iid)
        node = []

        while parent_iid != '':
            node.insert(0, self.tv.item(parent_iid)['text'])
            parent_iid = self.tv.parent(parent_iid)
        i = self.tv.item(item_iid, "text")
        path = os.path.join(*node, i)
        pub.sendMessage("ShowPath_Button_Pressed")
        return path

    def getSelectedPath(self):
        item_iid = self.tv.selection()[0]
        parent_iid = self.tv.parent(item_iid)
        node = []

        while parent_iid != '':
            node.insert(0, self.tv.item(parent_iid)['text'])
            parent_iid = self.tv.parent(parent_iid)
        i = self.tv.item(item_iid, "text")
        path = os.path.join(*node, i)
        return path

    def createNewDir(self):
        newDirPath = os.path.join(self.getSelectedPath(), self.newNameTextBox.get("1.0",'end-1c'))
        pub.sendMessage("CreateNewDir_Button_Pressed", arg=newDirPath)

    def clean_up(self):
        print(Path(self.getSelectedPath()))
        print(type(Path(self.getSelectedPath())))

        pub.sendMessage("CleanUp_Button_Pressed",
                        arg1=Path(self.getSelectedPath()),
                        arg2 = (Path(self.getSelectedPath()) / 'Cleaned'),
                        deep =self.recursive_clean_up_var,
                        dated = self.dated_clean_up_var)


if __name__ == "__main__":

    root = Tk()
    WIDTH = 600
    HEIGHT = 400
    root.geometry("%sx%s" % (WIDTH, HEIGHT))
    root.title("Deskonizer")


    view = View(root)
    view.setup()
    root.mainloop()
