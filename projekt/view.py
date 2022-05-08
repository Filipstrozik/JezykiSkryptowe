import os
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *

from pubsub import pub


class View:
    def __init__(self, parent):
        self.container = parent

    def setup(self):

        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):

        self.main_side = tk.Frame(self.container)
        self.right_side = tk.Frame(self.container)
        self.button = tk.Button(self.right_side, text="SHOW PATH", command=self.showPath)

        self.newNameTextBox = tk.Text(self.right_side, height=3, width=10)
        self.btnCreateDir = tk.Button(self.right_side, text="create new directory", command=self.createNewDir)

        self.label = tk.Label(self.container, text="prawa strona", font=100)

        self.left_side = tk.Frame(self.container)

        self.tv = ttk.Treeview(self.left_side, show='tree')
        self.ybar = tk.Scrollbar(self.left_side, orient=tk.VERTICAL,
                                 command=self.tv.yview)
        self.tv.configure(yscroll=self.ybar.set, height=20)
        self.directory = r'D:\MAIN\CODING\Sem 4'
        self.tv.heading('#0', text='Dir：' + self.directory, anchor='w')
        self.tv.column('#0', minwidth=100, width=400, stretch=True, )
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

    def setup_layout(self):

        self.ybar.pack(side='right', fill=tk.Y)
        self.tv.pack(side='left')
        self.left_side.pack(side='left')
        self.newNameTextBox.pack(side='right')
        self.button.pack(side="right")
        self.btnCreateDir.pack(side="right")
        self.right_side.pack(side='right')

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
        self.traverse_dir(self.node, self.path)



if __name__ == "__main__":
    root = Tk()
    WIDTH = 600
    HEIGHT = 400
    root.geometry("%sx%s" % (WIDTH, HEIGHT))
    root.title("Deskonizer")

    view = View(root)
    view.setup()
    root.mainloop()
