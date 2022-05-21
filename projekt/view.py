import json
import os
import subprocess
import tkinter as tk
import tkinter.messagebox
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
import threading
from watchdog.events import FileSystemEventHandler


class View(FileSystemEventHandler):
    def __init__(self, parent):
        self.container = parent
        self.menubar = tk.Menu(self.container)
        self.container.config(menu=self.menubar)
        self.extensions_paths = json.load(open('My extension.json'))
        self.directory = str(Path.home() / 'Desktop')
        self.sizes = []
        self.dirs = []

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

        self.dir_path_to_organize = Text(self.right_side, height=1, width=30)
        self.dir_path_to_organize_btn = Button(self.right_side, text='set dir to clean', command=self.set_cleanup_dir)

        self.dir_path_organized = Text(self.right_side, height=1, width=30)
        self.dir_path_organized_btn = Button(self.right_side, text='set organized dir path',
                                             command=self.set_target_organized_path)

        self.organized_dir_name_label = tk.Label(self.right_side, text="write your custom name of organized dir",
                                                 height=1)
        self.organized_dir_name = Text(self.right_side, height=1, width=30)

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
        self.clean_up_button['state'] = 'disabled'

        self.left_side = tk.Frame(self.container)

        self.tv = ttk.Treeview(self.left_side, show='tree')
        self.ybar = tk.Scrollbar(self.left_side, orient=tk.VERTICAL,
                                 command=self.tv.yview)
        self.xbar = tk.Scrollbar(self.left_side, orient=tk.HORIZONTAL, command=self.tv.xview)
        self.tv.configure(yscrollcommand=self.ybar.set, xscrollcommand=self.xbar.set)

        # self.directory = r'D:\MAIN\CODING\Sem 4'

        self.tv.heading('#0', text='Dir：' + self.directory, anchor='w')
        self.tv.column('#0', minwidth=600, width=400, stretch=True, anchor=CENTER)
        self.path = os.path.abspath(self.directory)
        self.node = self.tv.insert('', 'end', text=self.path, open=True)
        self.traverse_dir(self.node, self.path, 1)

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


    def traverse_dir(self, parent, path, flag) -> int:  # this should update, if exists dont go deeper.
        acc = 0
        for d in os.listdir(path):
            full_path = os.path.join(path, d)
            # print(d, os.path.getsize(full_path))
            isdir = os.path.isdir(full_path)
            if not isdir:
                acc += os.path.getsize(full_path)
                self.tv.insert(parent, 'end', text=f'{d} [{os.path.getsize(full_path)}]', open=False)
            if isdir:
                if flag == 1:
                    p = subprocess.check_output(['powershell.exe',
                                             f'((Get-ChildItem {full_path} -Recurse | Measure-Object -Property Length -Sum -ErrorAction Stop).Sum / 1MB)'])

                    pString = str(p)
                    pString = pString[2:len(pString) - 5]
                    pString = pString.replace(",",".")
                    fsize = float(pString)
                    self.sizes.append(fsize)
                    self.dirs.append(d)
                    id = self.tv.insert(parent, 'end', text=f'{d} [{fsize}]', open=False)
                else:
                    id = self.tv.insert(parent, 'end', text=f'{d}', open=False)
                self.traverse_dir(id, full_path, 0)
        return acc

    def update_dir(self):
        for item in self.tv.get_children():
            self.tv.delete(item)
        self.tv.heading('#0', text='Dir：' + self.directory, anchor='w')
        # self.tv.column('#0', minwidth=600, width=200, stretch=True, anchor=CENTER)
        self.path = os.path.abspath(self.directory)
        self.node = self.tv.insert('', 'end', text=self.path, open=True)
        self.traverse_dir(self.node, self.path, 1)
        self.graph()



    def set_path(self):

        self.open_progress_bar()

        self.directory = tk.filedialog.askdirectory()

        threading.Thread(target=self.update_dir()).start()  # TODO to wcale nie dziala tak jak bysmy chcieli

        self.top_progress.destroy()

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
        self.dir_path_to_organize.delete("1.0", 'end-1c')
        self.dir_path_organized.delete("1.0", 'end-1c')
        self.organized_dir_name.delete("1.0", 'end-1c')
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
        self.extensions_paths = json.load(open('My extension.json'))
        for row in self.extensions_paths:
            self.ext.insert('', tk.END, values=(row, self.extensions_paths[row]))

        self.change_dir_name = tk.StringVar(self.top)
        self.dir_name_text = Entry(self.top, textvariable=self.change_dir_name)

        edit_btn = Button(self.top, text='edit directory name', command=self.edit_dir_name, state='disabled')

        self.new_ext_name = tk.StringVar(self.top)
        self.add_new_ext_text = Entry(self.top, textvariable=self.new_ext_name)

        self.new_ext_dir_name = tk.StringVar(self.top)
        self.add_new_ext_dir_name_text = Entry(self.top, textvariable=self.new_ext_dir_name)

        self.focus = tk.StringVar(self.top, value=self.ext.focus())
        self.focus_entry = Entry(self.top, textvariable=self.focus)

        add_new_ext_dir_btn = Button(self.top, text="add new ext - dir name", command=self.add_new_ext_dir,
                                     state='disabled')
        delete_row_ext_dir_btn = Button(self.top, text='select & delete', command=self.delete_ext_dir, state='normal')

        self.ext.pack(fill=Y)
        self.dir_name_text.pack()
        edit_btn.pack()
        self.add_new_ext_text.pack()
        self.add_new_ext_dir_name_text.pack()
        add_new_ext_dir_btn.pack()
        delete_row_ext_dir_btn.pack()

        def check_edit_btn(*args):
            if (len(self.change_dir_name.get()) > 0):
                edit_btn.config(state='normal')
            else:
                edit_btn.config(state='disabled')

        self.change_dir_name.trace('w', check_edit_btn)

        def check_add_btn(*args):
            i = len(self.new_ext_name.get())
            j = len(self.new_ext_dir_name.get())
            print(i)
            print(j)
            print(i > 0 and j > 0 and self.new_ext_name.get().startswith('.'))
            if i > 0 and j > 0 and self.new_ext_name.get().startswith('.'):
                print('enable')
                add_new_ext_dir_btn.config(state='normal')
            else:
                print('disable')
                add_new_ext_dir_btn.config(state='disabled')

        self.new_ext_name.trace('w', check_add_btn)
        self.new_ext_dir_name.trace('w', check_add_btn)

        # def check_delete_btn(*args):
        #     print('sprawdzam')
        #     if len(self.ext.focus()) > 0:
        #         delete_row_ext_dir_btn.config(state='normal')
        #     else:
        #         delete_row_ext_dir_btn.config(state='disabled')
        #
        # self.focus.trace('w', check_delete_btn)

    def delete_ext_dir(self):
        try:
            cur_item = self.ext.focus()
            pub.sendMessage("Delete_Ext_Button_Pressed", extension=self.ext.item(cur_item)['values'][0])
            self.ext.delete(cur_item)
            self.update_ext_tree()
        except IndexError:
            self.popup_error('Error!', 'No extension is selected! - select one.')

    def edit_dir_name(self):
        cur_item = self.ext.focus()
        try:
            pub.sendMessage("Edit_Dir_Name_Button_Pressed", extension=self.ext.item(cur_item)['values'][0],
                            dir_name=self.dir_name_text.get())
            self.update_ext_tree()
            self.dir_name_text.delete(0, END)
        except IndexError:
            self.popup_error('Error!', 'No extension is selected! - select one.')

    def add_new_ext_dir(self):
        ext = self.add_new_ext_text.get()
        dir_name = self.add_new_ext_dir_name_text.get()
        pub.sendMessage("Edit_Dir_Name_Button_Pressed", extension=ext, dir_name=dir_name)
        self.update_ext_tree()
        self.add_new_ext_text.delete(0, END)
        self.add_new_ext_dir_name_text.delete(0, END)

    def update_ext_tree(self):
        for item in self.ext.get_children():
            self.ext.delete(item)
        self.extensions_paths = json.load(open('My extension.json'))
        for row in self.extensions_paths:
            self.ext.insert('', tk.END, values=(row, self.extensions_paths[row]))

    def graph(self):

        # stockListExp = ['AMZN', 'AAPL', 'JETS', 'CCL', 'NCLH']
        # stockSplitExp = [15, 25, 40, 10, 10]

        f = Figure()
        f = Figure(figsize=(5, 5), dpi=80)
        a = f.add_subplot(111)

        a.pie(self.sizes, radius=1, labels=self.dirs, shadow=True, autopct='%0.2f%%')
        a.legend(loc="best")
        # a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5,7,4,4,7,9,7,9])

        canvas = FigureCanvasTkAgg(f)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    def open_progress_bar(self):
        self.top_progress = Toplevel(self.container)
        self.top_progress.resizable(False, False)
        self.top_progress.geometry("300x20")
        self.pb = ttk.Progressbar(self.top_progress,
                                  orient='horizontal',
                                  mode='indeterminate',
                                  length=280)
        self.pb.start(10)
        self.pb.pack()

    def popup_error(self, frame_text, info_text):
        tkinter.messagebox.showerror(frame_text, info_text)

    def on_modified(self, event):
        self.update_dir()


if __name__ == "__main__":
    root = Tk()
    WIDTH = 600
    HEIGHT = 400
    root.geometry("%sx%s" % (WIDTH, HEIGHT))
    root.title("DeskCleanUp")

    view = View(root)
    view.setup()
    root.mainloop()
