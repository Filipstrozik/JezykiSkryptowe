import subprocess

from FileViewer import FileViewer
from TextBuffer import TextBuffer
from TextStats import TextStats


class TextViewer(FileViewer, TextBuffer):
    __stats: TextStats

    def __init__(self, path):
        FileViewer.__init__(self, path)
        TextBuffer.__init__(self, path)
        self.__stats = TextStats(self.text)

    def view(self):
        subprocess.Popen(['notepad.exe', self.path])

    def get_data(self) -> TextStats:
        return self.__stats
