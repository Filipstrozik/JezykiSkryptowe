import string
import subprocess


class TextBuffer:
    text: string

    def __init__(self, path):
        self.read_from_file(path)

    def read_from_file(self, path):
        self.text = subprocess.check_output(f'type "{path}"', text=True, universal_newlines=True, shell=True)

    def show(self):
        print(self.text)
