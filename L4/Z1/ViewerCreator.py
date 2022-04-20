import mimetypes
# from types import NoneType
from FileViewer import FileViewer
from ImageViewer import ImageViewer
from TextViewer import TextViewer


class ViewerCreator:

    def __init__(self):
        pass

    @staticmethod
    def __detect_viewer_type(path) -> type:
        mime = mimetypes.guess_type(path)[0]
        if mime is None:
            return type(None)

        if mime.__contains__('image'):
            return ImageViewer
        elif mime.__contains__('text'):
            return TextViewer


    def create_viewer(self, path):
        try:
            ins: FileViewer = self.__detect_viewer_type(path)(path)
            return ins
        except TypeError:
            print(f'error with quessing type: {path}')
            return None

