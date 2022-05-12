import os
import shutil
from pathlib import Path
from extensions import extensions_paths
from datetime import date


class Model:
    def __init__(self):
        return

    def showPath(self):
        print('model - showpath function launched')

    def createNewDir(self, path):
        print(path)
        os.mkdir(path)

    def add_date_to_path(self, path: Path):
        #data wedlug dat to robic
        dated_path = path / f'{date.today().year}' / f'{date.today().month:02d}'
        dated_path.mkdir(parents=True, exist_ok=True)
        return dated_path

    #TODO chyba deep dziala ale inny sposob nazywania datami
    def cleanup(self, watch_path: Path, destination_root: Path, deep):

        for child in watch_path.iterdir():
            print(child, destination_root, deep.get(), child.name)
            if child.is_file() and child.suffix.lower() in extensions_paths:
                destination_path = destination_root / extensions_paths[child.suffix.lower()]
                destination_path = self.add_date_to_path(destination_path)
                shutil.move(src=child, dst=destination_path)
            if child.is_dir() and deep.get() == 1 and child.name != 'Cleaned': #to jest folder co robimy z folderem
                #rekursja ale inaczej (gleblej, tak samo)
                self.cleanup(child, destination_root, deep)