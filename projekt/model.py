import os

class Model:
    def __init__(self):
        return

    def showPath(self):
        print('model - showpath function launched')

    def createNewDir(self, path):
        print(path)
        os.mkdir(path)