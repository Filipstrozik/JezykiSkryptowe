import os
import tkinter as tk
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from pubsub import pub
from extensions import extensions_paths


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
        self.setmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.menubar.add_cascade(label='Set', menu=self.setmenu)
        self.setmenu.add_command(label="change extension directory names", command=self.open_popup)
        self.filemenu.add_command(label="Open", command=self.set_path)

        self.main_side = tk.Frame(self.container)
        self.right_side = tk.Frame(self.container)

        self.button = tk.Button(self.right_side, text="SHOW PATH", command=self.showPath)

        self.dir_path_to_organize = Text(self.right_side, height=1, width=40)
        self.dir_path_to_organize_btn = Button(self.right_side, text='set dir to clean', command=self.set_cleanup_dir)

        self.dir_path_organized = Text(self.right_side, height=1, width=40)
        self.dir_path_organized_btn = Button(self.right_side, text='set organized dir path',
                                             command=self.set_target_organized_path)

        self.organized_dir_name_label = tk.Label(self.right_side, text="write your custom name of organized dir",
                                                 height=1)
        self.organized_dir_name = Text(self.right_side, height=1, width=40)

        self.newDirecoryLabel = tk.Label(self.right_side, text="new directory", height=1)
        self.newNameTextBox = tk.Text(self.right_side, height=1, width=20)

        self.btnCreateDir = tk.Button(self.right_side, text="create new directory", command=self.createNewDir)

        self.clean_up_label = tk.Label(self.right_side, text="cleanup", height=1)
        # checkbox for recursive cleaning folders,
        self.recursive_clean_up_var = tk.IntVar()

        self.recursive_clean_up_checkbox = tk.Checkbutton(self.right_side, text='deep clean up',
                                                          variable=self.recursive_clean_up_var, onvalue=1, offvalue=0)
        # chceckbox for adding date of files not today!
        self.dated_clean_up_var = tk.IntVar()
        self.dated_clean_up_checkbox = tk.Checkbutton(self.right_side, text='dated clean up',
                                                      variable=self.dated_clean_up_var, onvalue=1, offvalue=0)

        self.shortcut_var = tk.IntVar()
        self.shortcut_checkbox = tk.Checkbutton(self.right_side, text='create shortcut',
                                                variable=self.shortcut_var, onvalue=1, offvalue=0)

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

    def setup_layout(self):

        self.ybar.pack(side='right', fill=tk.Y)
        self.xbar.pack(side='bottom', fill=tk.X)
        self.tv.pack(side='left', fill=Y)
        # self.tv.grid(row=0, column=0)
        self.left_side.pack(side='left', fill=Y)

        self.clean_up_label.pack(fill=BOTH)

        self.dir_path_to_organize.pack(fill=BOTH)
        self.dir_path_to_organize_btn.pack(fill=BOTH)

        self.dir_path_organized.pack()
        self.dir_path_organized_btn.pack(fill=BOTH)

        self.organized_dir_name_label.pack()
        self.organized_dir_name.pack(fill=BOTH)

        self.recursive_clean_up_checkbox.pack(fill=BOTH)
        self.dated_clean_up_checkbox.pack(fill=BOTH)
        self.shortcut_checkbox.pack(fill=BOTH)
        self.clean_up_button.pack(fill=BOTH)

        self.right_side.pack(side='right', fill=BOTH)

        self.graph()

    def traverse_dir(self, parent, path):  # this should update, if exists dont go deeper.
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

    def set_cleanup_dir(self):  # TODO usuwanie jezeli cos jest aktualnie, i to powino byc zablokowane
        self.dir_path_to_organize.insert(END, chars=self.getSelectedPath())

    def set_target_organized_path(self):
        self.dir_path_organized.insert(END,
                                       chars=self.getSelectedPath())  # TODO usuwanie jezeli cos jest aktualnie a to nie zablokowane

    def set_target_organized_dir_name(self):
        self.organized_dir_name.get("1.0", 'end-1c')

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
        newDirPath = os.path.join(self.getSelectedPath(), self.newNameTextBox.get("1.0", 'end-1c'))
        pub.sendMessage("CreateNewDir_Button_Pressed", arg=newDirPath)

    def clean_up(self):
        pub.sendMessage("CleanUp_Button_Pressed",
                        arg1=Path(self.dir_path_to_organize.get("1.0", 'end-1c')),
                        arg2=(Path(self.dir_path_organized.get("1.0", 'end-1c')) / self.organized_dir_name.get("1.0",
                                                                                                               'end-1c')),
                        deep=self.recursive_clean_up_var,
                        dated=self.dated_clean_up_var,
                        shortcut=self.shortcut_var)
        self.update_dir()

    def open_popup(self):
        self.top = Toplevel(self.container)
        self.top.resizable(False, False)
        self.top.geometry("400x600")
        self.top.title("Setting extensions directory names")
        columns = ('extension', 'directory name')
        self.ext = ttk.Treeview(self.top, columns=columns, show='headings')
        self.ext.heading('extension', text='extension')
        self.ext.heading('directory name', text='name of directory')
        for row in extensions_paths:
            self.ext.insert('', tk.END, values=(row, extensions_paths[row]))

        self.dir_name_text = Text(self.top, height=1)
        edit_btn = Button(self.top, text='edit directory name', command=self.edit_dir_name)
        self.add_new_ext_text = Text(self.top, height=1)
        self.add_new_ext_dir_name_text = Text(self.top, height=1)
        add_new_ext_dir_btn = Button(self.top, text="add new ext - dir name", command=self.add_new_ext_dir)
        delete_row_ext_dir_btn = Button(self.top, text='select & delete', command=self.delete_ext_dir)

        self.ext.pack(fill=Y)
        self.dir_name_text.pack()
        edit_btn.pack()
        self.add_new_ext_text.pack()
        self.add_new_ext_dir_name_text.pack()
        add_new_ext_dir_btn.pack()
        delete_row_ext_dir_btn.pack()

    def delete_ext_dir(self):
        cur_item = self.ext.focus()
        pub.sendMessage("Delete_Ext_Button_Pressed", extension=self.ext.item(cur_item)['values'][0])
        self.ext.delete(cur_item)

    def edit_dir_name(self):
        cur_item = self.ext.focus()
        pub.sendMessage("Edit_Dir_Name_Button_Pressed", extension=self.ext.item(cur_item)['values'][0],
                        dir_name=self.dir_name_text.get("1.0", 'end-1c'))
        self.update_ext_tree()

    def add_new_ext_dir(self):
        ext = self.add_new_ext_text.get("1.0", 'end-1c')
        dir_name = self.add_new_ext_dir_name_text.get("1.0", 'end-1c')
        pub.sendMessage("Edit_Dir_Name_Button_Pressed", extension=ext, dir_name=dir_name)
        self.update_ext_tree()

    def update_ext_tree(self):
        for item in self.ext.get_children():
            self.ext.delete(item)
        for row in extensions_paths:
            self.ext.insert('', tk.END, values=(row, extensions_paths[row]))

    def graph(self):
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8])
        dirs_size = np.random.normal(100, 100, 50)
        plt.hist(dirs_size, 50)
        plt.show()

if __name__ == "__main__":
    root = Tk()
    WIDTH = 600
    HEIGHT = 400
    root.geometry("%sx%s" % (WIDTH, HEIGHT))
    root.title("DeskCleanUp")

    view = View(root)
    view.setup()
    root.mainloop()
