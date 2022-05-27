from tkinter import Tk

from pubsub import pub

from model import Model
from view import View
from watchdog.observers import Observer
import customtkinter as ctk


class Controller:
    def __init__(self, parent):
        self.parent = parent
        self.model = Model()
        self.view = View(parent)

        observer = Observer()
        observer.schedule(self.view, f'{self.view.directory}', recursive=False)
        observer.start()
        self.view.setup()

        pub.subscribe(self.showpath_btn_pressed, "ShowPath_Button_Pressed")
        pub.subscribe(self.createdir_btn_pressed, "CreateNewDir_Button_Pressed")
        pub.subscribe(self.cleanup_btn_pressed, "CleanUp_Button_Pressed")
        pub.subscribe(self.edit_dir_name_btn_pressed, "Edit_Dir_Name_Button_Pressed")
        pub.subscribe(self.delete_ext_btn_pressed, "Delete_Ext_Button_Pressed")
        pub.subscribe(self.undo_btn_pressed, "Undo_Button_Pressed")

    def createdir_btn_pressed(self, arg):
        self.model.createNewDir(arg)

    def showpath_btn_pressed(self):
        self.model.showPath()

    def cleanup_btn_pressed(self, arg1, arg2, deep, dated, shortcut, only_view):
        self.model.cleanup(arg1, arg2, deep, dated, shortcut, only_view)

    def edit_dir_name_btn_pressed(self, extension, dir_name):
        self.model.edit_ext_dir_name(extension, dir_name)

    def delete_ext_btn_pressed(self, extension):
        self.model.delete_ext(extension)

    def undo_btn_pressed(self):
        self.model.undo(self.model.destination)


if __name__ == "__main__":
    root = ctk.CTk()
    WIDTH = 1000
    HEIGHT = 600
    root.geometry("%sx%s" % (WIDTH, HEIGHT))
    root.minsize(800, 600)
    root.maxsize(1920, 1080)
    root.title("DeskCleanUp")

    app = Controller(root)

    root.mainloop()
