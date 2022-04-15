from abc import ABC, abstractmethod


class FileViewer(ABC):
    path = ''

    def __init__(self, path):
        self.path = path

    @abstractmethod
    def view(self):
        pass
