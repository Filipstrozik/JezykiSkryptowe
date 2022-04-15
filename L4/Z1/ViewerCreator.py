import mimetypes

from FileViewer import FileViewer
from ImageViewer import ImageViewer
from TextViewer import TextViewer


class ViewerCreator:

    def __init__(self):
        pass

    @staticmethod
    def __detect_viewer_type(path) -> type:
        mime = mimetypes.guess_type(path)[0]
        if mime.__contains__('image'):
            return ImageViewer
        if mime.__contains__('text'):
            return TextViewer

    def create_viewer(self, path):
        instance: FileViewer = self.__detect_viewer_type(path)(path)
        return instance
