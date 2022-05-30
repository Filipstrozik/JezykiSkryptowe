import json
import os
import subprocess
import threading
import tkinter as tk
import tkinter.messagebox
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pubsub import pub
from watchdog.events import FileSystemEventHandler


class View(FileSystemEventHandler):
    def __init__(self, parent):
        self.tree_view_width = 0
        ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")
        self.toolbar = None
        self.left_side = None
        self.right_top_side = None
        self.right_bottom_side = None
        self.main_side = None
        self.container = parent
        self.menubar = tk.Menu(self.container)
        self.container.config(menu=self.menubar)
        self.extensions_paths = json.load(open('My extension.json'))
        self.directory = str(Path.home() / 'Desktop')
        self.file_data = {}
        # self.sizes = []
        # self.dirs = []
        self.f = Figure(figsize=(1, 1), dpi=90)
        self.canvas = FigureCanvasTkAgg(self.f, self.right_top_side)

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

        # main_side_frame
        self.main_side = ctk.CTkFrame(master=self.container)

        # right_side_Frame
        self.right_side = ctk.CTkFrame(master=self.main_side, corner_radius=0, border_width=20)
        # right_side_bottom_frame
        self.right_bottom_side = ctk.CTkFrame(master=self.right_side, corner_radius=10, height=100)

        # right_side_top_frame
        self.right_top_side = ctk.CTkFrame(master=self.right_side, corner_radius=10)

        # left_side_frame
        self.left_side = ctk.CTkFrame(master=self.main_side, border_color="red")

        self.button = ctk.CTkButton(self.right_bottom_side, text="SHOW PATH", command=self.showPath)

        # dir_path_to_organize
        self.dir_path_to_organize_var = StringVar(self.right_bottom_side)
        self.dir_path_to_organize = ctk.CTkEntry(self.right_bottom_side, textvariable=self.dir_path_to_organize_var,
                                                 width=30)
        self.dir_path_to_organize_btn = ctk.CTkButton(self.right_bottom_side, text='SELECT DIRECTORY',
                                                      command=self.set_cleanup_dir)
        self.dir_path_to_organize_popup_btn = ctk.CTkButton(self.right_bottom_side, text='OPEN DIRECTORY',
                                                            command=self.set_cleanup_dir_popup)

        # dir_path_organized
        self.dir_path_organized_var = StringVar(self.right_bottom_side)
        self.dir_path_organized = ctk.CTkEntry(self.right_bottom_side, textvariable=self.dir_path_organized_var,
                                               width=30)
        self.dir_path_organized_btn = ctk.CTkButton(self.right_bottom_side, text='SELECT OUPUT PATH',
                                                    command=self.set_target_organized_path)
        self.dir_path_organized_popup_btn = ctk.CTkButton(self.right_bottom_side, text='OPEN DIRECTORY OUPUT',
                                                          command=self.set_target_organized_path_popup)

        # organized_dir_name
        self.organized_dir_name_label = ctk.CTkLabel(self.right_bottom_side, text="CUSTOM NAME", height=1)
        self.organized_dir_name_var = StringVar(self.right_bottom_side)
        self.organized_dir_name = ctk.CTkEntry(self.right_bottom_side, textvariable=self.organized_dir_name_var,
                                               width=30)

        self.newDirecoryLabel = ctk.CTkLabel(self.right_bottom_side, text="new directory", height=1)
        self.newNameTextBox = ctk.CTkEntry(self.right_bottom_side, height=1, width=20)

        self.btnCreateDir = ctk.CTkButton(self.right_bottom_side, text="create new directory",
                                          command=self.createNewDir)

        self.clean_up_label = ctk.CTkLabel(self.right_bottom_side, text="cleanup", height=1)
        # checkbox for recursive cleaning folders,
        self.recursive_clean_up_var = tk.IntVar()
        self.recursive_clean_up_checkbox = ctk.CTkCheckBox(self.right_bottom_side, text='deep',
                                                           variable=self.recursive_clean_up_var, onvalue=1, offvalue=0,
                                                           state='disabled')
        # chceckbox for adding date of files
        self.dated_clean_up_var = tk.IntVar()
        self.dated_clean_up_checkbox = ctk.CTkCheckBox(self.right_bottom_side, text='dated',
                                                       variable=self.dated_clean_up_var, onvalue=1, offvalue=0,
                                                       state='disabled')

        self.shortcut_var = tk.IntVar()
        self.shortcut_checkbox = ctk.CTkCheckBox(self.right_bottom_side, text='shortcut',
                                                 variable=self.shortcut_var, onvalue=1, offvalue=0, state='disabled')

        # only_view
        self.only_view_var = tk.IntVar()
        self.only_view_checkbox = ctk.CTkCheckBox(self.right_bottom_side, text='only view',
                                                  variable=self.only_view_var, onvalue=1, offvalue=0, state='disabled')

        self.clean_up_button = ctk.CTkButton(self.right_bottom_side, text="CLEANUP", command=self.clean_up,
                                             background='green', state='disabled')
        # self.clean_up_button['state'] = 'disabled'
        # undo_button
        self.undo_button = ctk.CTkButton(self.right_bottom_side, text="UNDO", command=self.undo, background='red',
                                         state='disabled')

        self.tv = ttk.Treeview(self.left_side, show='tree')
        self.ybar = tk.Scrollbar(self.left_side, orient=tk.VERTICAL,
                                 command=self.tv.yview)
        self.xbar = tk.Scrollbar(self.left_side, orient=tk.HORIZONTAL, command=self.tv.xview)

        self.tv.configure(yscrollcommand=self.ybar.set, xscrollcommand=self.xbar.set)

        self.tv.heading('#0', text='Dir：' + self.directory, anchor='w')
        self.tree_view_width = 0
        # self.tv.column('#0', minwidth=600, width=600, stretch=True, anchor=CENTER)
        self.path = os.path.abspath(self.directory)
        self.node = self.tv.insert('', 'end', text=self.path, open=True)
        self.open_progress_bar()
        self.traverse_dir(self.node, self.path, 1)
        print('szerokosc')
        self.tree_view_width *= 20

        # self.tv.column('#0', minwidth=(self.tree_view_width*10), width=600, stretch=True, anchor=CENTER)
        self.tv.column('#0', minwidth=self.tree_view_width, width=600,stretch=True, anchor=CENTER)
        self.tv.configure(yscrollcommand=self.ybar.set, xscrollcommand=self.xbar.set)

        print(self.tree_view_width)
        self.graph()
        self.top_progress.destroy()

    def check_fields(self, *args):
        i = len(self.organized_dir_name.get())
        j = len(self.dir_path_to_organize.get())
        k = len(self.dir_path_organized.get())
        if i > 0 and j > 0 and k > 0:
            self.recursive_clean_up_checkbox.config(state='normal')
            self.dated_clean_up_checkbox.config(state='normal')
            self.shortcut_checkbox.config(state='normal')
            self.only_view_checkbox.config(state='normal')
            self.clean_up_button.config(state='normal')
        else:
            self.recursive_clean_up_checkbox.config(state='disabled')
            self.dated_clean_up_checkbox.config(state='disabled')
            self.shortcut_checkbox.config(state='disabled')
            self.only_view_checkbox.config(state='disabled')
            self.clean_up_button.config(state='disabled')

    def setup_layout(self):

        self.main_side.pack(fill=BOTH, expand=True, padx=20, pady=20)

        self.ybar.pack(side='right', fill=tk.Y)
        self.xbar.pack(side='bottom', fill=tk.X)

        s = ttk.Style()
        s.configure('Treeview', rowheight=40)
        self.tv.pack(side='left', fill=Y)

        self.main_side.columnconfigure(0, weight=1)
        self.main_side.columnconfigure(1, weight=1)
        self.main_side.rowconfigure(0, weight=1)

        self.right_side.columnconfigure(0, weight=1)
        self.right_side.rowconfigure(0, weight=4)
        self.right_side.rowconfigure(1, weight=1)

        # self.left_side.grid(row=0, column=0, sticky="nsew") #bylo
        self.left_side.grid(row=0, column=0, sticky="nsew")

        self.right_side.grid(row=0, column=1, sticky="nsew")

        self.dir_path_to_organize_var.trace('w', self.check_fields)
        self.dir_path_to_organize.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=2)
        self.dir_path_to_organize_btn.grid(row=1, column=0, sticky="ew", padx=10, pady=2)
        self.dir_path_to_organize_popup_btn.grid(row=1, column=1, sticky="ew", padx=10, pady=2)

        self.dir_path_organized_var.trace("w", self.check_fields)
        self.dir_path_organized.grid(row=2, column=0, columnspan=2, sticky="new", padx=10, pady=2)
        self.dir_path_organized_btn.grid(row=3, column=0, sticky="ew", padx=10, pady=2)
        self.dir_path_organized_popup_btn.grid(row=3, column=1, sticky="ew", padx=10, pady=2)

        self.undo_button.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.organized_dir_name_label.grid(row=0, column=2, columnspan=2, sticky="sew", padx=10)
        self.organized_dir_name_var.trace('w', self.check_fields)
        self.organized_dir_name.grid(row=1, column=2, columnspan=2, sticky="new", padx=10, pady=10)

        self.recursive_clean_up_checkbox.grid(row=2, column=2, sticky="nsew")
        self.dated_clean_up_checkbox.grid(row=2, column=3, sticky="nsew")
        self.shortcut_checkbox.grid(row=3, column=2, sticky="nsew")
        self.only_view_checkbox.grid(row=3, column=3, sticky="nsew")
        self.clean_up_button.grid(row=4, column=2, columnspan=2, sticky="nsew")

        self.right_top_side.grid(row=0, column=0, sticky="nsew")
        # self.right_top_side.grid(row=0, column=0)

        self.right_bottom_side.grid(row=1, column=0, sticky="nsew")

        self.right_bottom_side.columnconfigure(0, weight=1)
        self.right_bottom_side.columnconfigure(1, weight=1)
        self.right_bottom_side.columnconfigure(2, weight=1)
        self.right_bottom_side.columnconfigure(3, weight=1)
        self.right_bottom_side.rowconfigure(0, weight=1)
        self.right_bottom_side.rowconfigure(1, weight=1)
        self.right_bottom_side.rowconfigure(2, weight=1)
        self.right_bottom_side.rowconfigure(3, weight=1)
        self.right_bottom_side.rowconfigure(4, weight=1)

        self.right_bottom_side.grid(row=1, column=0, sticky="nsew")

    # TODO zliczanie szerokosci potrzebnej do wyswietlenia w treeview
    def traverse_dir(self, parent, path, flag) -> float:
        acc = 0
        if flag == 1:
            no_dirs = len(os.listdir(path))
            x = 100.0 / no_dirs
        for d in os.listdir(path):
            full_path = os.path.join(path, d)
            isdir = os.path.isdir(full_path)
            if not isdir:
                file_size = float(os.path.getsize(full_path))
                acc += file_size
                if flag == 1:

                    self.file_data[d] = file_size
                    self.container.update_idletasks()
                    try:
                        self.pb['value'] += x
                    except:
                        pass
                size, postfix = self.format_bytes(file_size)
                text_to_insert = f'{d} [{"%.2f" % round(size, 2)} {postfix}]'
                # print(len(text_to_insert))
                self.tree_view_width = max(len(text_to_insert), self.tree_view_width)

                self.tv.insert(parent, 'end', text=text_to_insert, open=False)

            if isdir:
                if flag == 1:
                    p = subprocess.check_output(['powershell.exe',
                                                 f'((Get-ChildItem "{full_path}" -Recurse | Measure-Object -Property Length -Sum -ErrorAction Stop).Sum)'])  # result in Bytes

                    pString = str(p)
                    pString = pString[2:len(pString) - 5]
                    pString = pString.replace(",", ".")
                    fsize = float(pString)

                    self.file_data[d] = fsize
                    size, postfix = self.format_bytes(fsize)
                    text_to_insert = f'{d} [{"%.2f" % round(size, 2)} {postfix}]'
                    # print(len(text_to_insert))
                    self.tree_view_width = max(len(text_to_insert), self.tree_view_width)
                    id = self.tv.insert(parent, 'end', text=text_to_insert, open=False)
                    self.container.update_idletasks()
                    try:
                        self.pb['value'] += x
                    except:
                        pass
                else:
                    id = self.tv.insert(parent, 'end', text=f'{d}', open=False)
                self.traverse_dir(id, full_path, 0)

        return acc

    def format_bytes(self, size):
        # 2**10 = 1024
        power = 2 ** 10
        n = 0
        power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return size, power_labels[n] + 'B'

    def update_dir(self):
        for item in self.tv.get_children():
            self.tv.delete(item)
        self.file_data.clear()
        self.tv.heading('#0', text='Dir：' + self.directory, anchor='w')
        # self.tv.column('#0', minwidth=600, width=200, stretch=True, anchor=CENTER)
        self.path = os.path.abspath(self.directory)
        self.node = self.tv.insert('', 'end', text=self.path, open=True)
        self.tree_view_width = 0
        self.clear_graph()
        self.traverse_dir(self.node, self.path, 1)
        print('serokosc')
        self.tree_view_width *= 12
        print(self.tree_view_width)
        print('okno')
        print(self.left_side.winfo_width())
        self.tv.column('#0', minwidth=self.tree_view_width, width=self.left_side.winfo_width(), stretch=True, anchor=CENTER)
        # self.tv.column('#0', minwidth=(self.tree_view_width*20), width=600)
        self.graph()
        # self.setup_layout() #to nie dzialalo

        print('done')
        self.top_progress.destroy()
        return True

    def set_path(self):
        self.directory = tk.filedialog.askdirectory()
        self.open_progress_bar()
        t2 = threading.Thread(target=self.update_dir)
        t2.start()

    # dir_path_to_organize
    def set_cleanup_dir_popup(self):
        self.dir_path_to_organize.delete(0, END)
        self.dir_path_to_organize.insert(END, tk.filedialog.askdirectory())

    def set_cleanup_dir(self):
        self.dir_path_to_organize.delete(0, END)
        self.dir_path_to_organize.insert(END, self.getSelectedPath())

    def set_target_organized_path(self):
        self.dir_path_organized.delete(0, END)
        self.dir_path_organized.insert(END, self.getSelectedPath())

    def set_target_organized_path_popup(self):
        self.dir_path_organized.delete(0, END)
        self.dir_path_organized.insert(END, tk.filedialog.askdirectory())

    def set_target_organized_dir_name(self):
        self.organized_dir_name.get()

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
        try:
            item_iid = self.tv.selection()[0]
            parent_iid = self.tv.parent(item_iid)
            node = []

            while parent_iid != '':
                node.insert(0, self.tv.item(parent_iid)['text'])
                parent_iid = self.tv.parent(parent_iid)
            i = self.tv.item(item_iid, "text")
            path = os.path.join(*node, i)
            return path
        except IndexError:
            self.popup_error('Error!', 'No extension is selected! - select one.')
            return ''

    def createNewDir(self):
        newDirPath = os.path.join(self.getSelectedPath(), self.newNameTextBox.get())
        pub.sendMessage("CreateNewDir_Button_Pressed", arg=newDirPath)

    def clean_up(self):
        pub.sendMessage("CleanUp_Button_Pressed",
                        arg1=Path(self.dir_path_to_organize.get()),
                        arg2=(Path(self.dir_path_organized.get()) / self.organized_dir_name.get()),
                        deep=self.recursive_clean_up_var,
                        dated=self.dated_clean_up_var,
                        shortcut=self.shortcut_var,
                        only_view=self.only_view_var)

        self.dir_path_to_organize.delete(0, END)
        self.dir_path_organized.delete(0, END)
        self.organized_dir_name.delete(0, END)
        self.update_dir()
        self.undo_button.config(state='normal')

    def undo(self):
        pub.sendMessage("Undo_Button_Pressed")
        self.update_dir()
        self.undo_button.config(state='disabled')

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
            if len(self.change_dir_name.get()) > 0:
                edit_btn.config(state='normal')
            else:
                edit_btn.config(state='disabled')

        self.change_dir_name.trace('w', check_edit_btn)

        def check_add_btn(*args):
            i = len(self.new_ext_name.get())
            j = len(self.new_ext_dir_name.get())
            # print(i > 0 and j > 0 and self.new_ext_name.get().startswith('.'))
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

        sum = 0.0
        for size in self.file_data.values():  # chyba acc koncowo jest suma?
            sum += size

        self.file_data = dict(sorted(self.file_data.items(), key=lambda kv: kv[1], reverse=True))
        to_graph = {}
        for (key, value) in self.file_data.items():
            if value / sum > 0.02:
                if len(key) > 20:
                    key = key[:20]
                    key += '...'
                to_graph[key] = value

        print(self.file_data)

        self.f = Figure(figsize=(8, 6), dpi=90)
        self.a = self.f.add_subplot(111)


        self.a.pie(to_graph.values(), radius=0.7, labels=to_graph.keys(),
                   autopct=lambda x: '{size} {postfix}'.format(
                       size="%.2f" % round(self.format_bytes(x * sum / 100)[0], 2),
                       postfix=self.format_bytes(x * sum / 100)[1]),
                   textprops={'fontsize': 8})
        # f'"%.2f" % round(self.format_bytes(x * sum / 100)[0], 2)} {self.format_bytes(x * sum / 100)[0]}]'
        self.a.set_title(f'{self.directory}', size=10, weight='bold')
        # self.a.pie(self.sizes, radius=1, labels=self.dirs, shadow=True, autopct='%0.2f%%')
        # self.a.legend(loc="best")

        self.canvas = FigureCanvasTkAgg(self.f, self.right_top_side)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.right_top_side)
        self.canvas.get_tk_widget().pack(side=TOP, expand=True, padx=20, pady=20)
        # self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True, padx=20, pady=20)
        self.toolbar.update()
        # self.canvas._tkcanvas.pack()
        # self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    def clear_graph(self):
        print('usuwam graf')
        self.canvas.get_tk_widget().destroy()
        self.toolbar.destroy()

    def open_progress_bar(self):
        self.top_progress = Toplevel(self.container)
        self.top_progress.resizable(False, False)
        self.top_progress.geometry("300x20")
        self.pb = ttk.Progressbar(self.top_progress,
                                  orient='horizontal',
                                  mode='determinate',
                                  length=280)
        # self.pb.start(20)
        self.pb.pack()

    def popup_error(self, frame_text, info_text):
        tkinter.messagebox.showerror(frame_text, info_text)

    # def on_modified(self, event):
    #     if self.flag == 1:
    #         print('on_modified!')
    #         self.open_progress_bar()
    #         t2 = threading.Thread(target=self.update_dir)  # TODO to wcale nie dziala tak jak bysmy chcieli
    #         t2.start()
    #         t2.join()

    def on_created(self, event):
        print('on_created!')
        self.open_progress_bar()
        t2 = threading.Thread(target=self.update_dir)
        t2.start()
        t2.join()

    def on_deleted(self, event):
        print('on_deleted')
        self.open_progress_bar()
        t2 = threading.Thread(target=self.update_dir)
        t2.start()
        t2.join()


if __name__ == "__main__":
    root = ctk.CTk()
    WIDTH = 600
    HEIGHT = 400
    root.geometry("%sx%s" % (WIDTH, HEIGHT))
    root.title("DeskCleanUp")

    view = View(root)
    view.setup()
    root.mainloop()
