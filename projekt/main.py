import os
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry('600x400')

main_side = tk.Frame(root)
right_side = tk.Frame(root)
button = tk.Button()
label = tk.Label(root, text="prawa strona", font=100)


left_side = tk.Frame(root)



tv = ttk.Treeview(left_side, show='tree')
ybar = tk.Scrollbar(left_side, orient=tk.VERTICAL,
                    command=tv.yview)
tv.configure(yscroll=ybar.set, height=20)
directory = r'D:\MAIN\CODING\Sem 4'
tv.heading('#0', text='Dir：' + directory, anchor='w')
tv.column('#0', minwidth=100, width=400, stretch=True, )
path = os.path.abspath(directory)
node = tv.insert('', 'end', text=path, open=True)


def traverse_dir(parent, path):
    for d in os.listdir(path):
        full_path = os.path.join(path, d)
        # print(d, os.path.getsize(full_path))
        isdir = os.path.isdir(full_path)
        if not isdir:
            id = tv.insert(parent, 'end', text=f'{d} [{os.path.getsize(full_path)}]', open=False)
        if isdir:
            id = tv.insert(parent, 'end', text=f'{d}', open=False)
            traverse_dir(id, full_path)


traverse_dir(node, path)
print(tv.selection())

ybar.pack(side= 'right', fill=tk.Y)
tv.pack(side= 'left')
left_side.pack(side ='left')
label.pack(side= 'right')

root.mainloop()
