import subprocess

from FileViewer import FileViewer


class ImageViewer(FileViewer):

    def __init__(self, path):
        super().__init__(path)

    def view(self):
        subprocess.call(f'start msedge "{self.path}"', shell=True)
