from tkinter import Tk

from pubsub import pub

from model import Model
from view import View
from watchdog.observers import Observer


class Controller:
    def __init__(self, parent):
        self.parent = parent
        self.model = Model()
        self.view = View(parent)

        observer = Observer()
        observer.schedule(self.view, f'{self.view.directory}', recursive=True)
        observer.start()
        self.view.setup()

        pub.subscribe(self.showpath_btn_pressed, "ShowPath_Button_Pressed")
        pub.subscribe(self.createdir_btn_pressed, "CreateNewDir_Button_Pressed")
        pub.subscribe(self.cleanup_btn_pressed, "CleanUp_Button_Pressed")
        pub.subscribe(self.edit_dir_name_btn_pressed, "Edit_Dir_Name_Button_Pressed")
        pub.subscribe(self.delete_ext_btn_pressed, "Delete_Ext_Button_Pressed")

    def createdir_btn_pressed(self, arg):
        self.model.createNewDir(arg)

    def showpath_btn_pressed(self):
        self.model.showPath()

    def cleanup_btn_pressed(self, arg1, arg2, deep, dated, shortcut):
        self.model.cleanup(arg1, arg2, deep, dated, shortcut)

    def edit_dir_name_btn_pressed(self, extension, dir_name):
        self.model.edit_ext_dir_name(extension, dir_name)

    def delete_ext_btn_pressed(self, extension):
        self.model.delete_ext(extension)


if __name__ == "__main__":
    root = Tk()
    WIDTH = 800
    HEIGHT = 400
    root.geometry("%sx%s" % (WIDTH, HEIGHT))
    root.minsize(400, 300)
    root.maxsize(1000, 800)
    root.title("DeskCleanUp")

    app = Controller(root)

    root.mainloop()
