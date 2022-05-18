import os, sys
import shutil
from pathlib import Path
from extensions import extensions_paths
from datetime import date
import time
import winshell
from win32com.client import Dispatch


class Model:
    def __init__(self):
        return

    def showPath(self):
        print('model - showpath function launched')

    def createNewDir(self, path):
        print(path)
        os.mkdir(path)

    def add_date_to_path(self, path: Path, child: Path):
        # data wedlug dat to robic
        child_date = time.ctime(os.path.getctime(child))
        child_year = child_date[-4:]
        child_month = child_date[4:7]
        dated_path = path / f'{child_year}' / f'{child_month}'
        dated_path.mkdir(parents=True, exist_ok=True)
        return dated_path

    def cleanup(self, watch_path: Path, destination_root: Path, deep, dated, shortcut):

        for child in watch_path.iterdir():
            print(child, destination_root, deep.get(), child.name)
            if child.is_file() and child.suffix.lower() in extensions_paths:
                destination_path = destination_root / extensions_paths[child.suffix.lower()]
                if dated.get() == 1:
                    destination_path = self.add_date_to_path(destination_path, child)
                else:
                    destination_path.mkdir(parents=True, exist_ok=True)
                shutil.move(src=child, dst=destination_path)
            if child.is_dir() and deep.get() == 1 and child.name != 'Cleaned':  # to jest folder co robimy z folderem
                self.cleanup(child, destination_root, deep, shortcut)
        if shortcut == 1:
            print('creating schortcut')
            short = destination_root.stem
            self.create_shortcut(watch_path, str(destination_root), name=short)


    #TODO to sie gubi poniewaz nie tworzymy skrótu do pliku tylko do folderu najlepiej.
    def create_shortcut(self, path, target='', name='shortcut'):
        link_filepath = os.path.join(path, name)
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(link_filepath)
        shortcut.Targetpath = target
        shortcut.save()

    def edit_ext_dir_name(self, extension, dir_name):
        extensions_paths[extension] = dir_name

    def delete_ext(self, extension):
        extensions_paths.pop(extension)

if __name__ == "__main__":
    model = Model()
