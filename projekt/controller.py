from pathlib import Path
from tkinter import Tk

from view import View
from model import Model
from pubsub import pub


class Controller:
    def __init__(self, parent):
        self.parent = parent
        self.model = Model()
        self.view = View(parent)
        self.view.setup()

        pub.subscribe(self.showpath_btn_pressed, "ShowPath_Button_Pressed")
        pub.subscribe(self.createdir_btn_pressed, "CreateNewDir_Button_Pressed")
        pub.subscribe(self.cleanup_btn_pressed, "CleanUp_Button_Pressed")

    def createdir_btn_pressed(self, arg):
        print("controller  - createNewDir btn pressed")
        self.model.createNewDir(arg)

    def showpath_btn_pressed(self):
        print("controller  - showpath btn pressed")
        self.model.showPath()

    def cleanup_btn_pressed(self, arg1, arg2, deep, dated):
        print("controller  - cleanup btn pressed")
        self.model.cleanup(arg1, arg2, deep, dated)


if __name__ == "__main__":
    root = Tk()
    WIDTH = 800
    HEIGHT = 400
    root.geometry("%sx%s" % (WIDTH, HEIGHT))
    root.minsize(400,300)
    root.maxsize(1000,800)
    root.title("Deskonizer")

    app = Controller(root)
    root.mainloop()
