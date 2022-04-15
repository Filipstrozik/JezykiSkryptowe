from ImageViewer import ImageViewer
from TextViewer import TextViewer
from ViewerCreator import ViewerCreator

if __name__ == '__main__':

    pathpng = r'C:\Users\Filip Strózik\Documents\VPProjects\Activity Diagram1.png'
    pathtxt = r'D:\MAIN\CODING\Sem 4\Testowe\kat1\test.txt'

    tv: TextViewer = ViewerCreator().create_viewer(pathtxt)
    tv.get_data()
    tv.show()
    tv.view()
    tv.get_data().show()

    iv: ImageViewer = ViewerCreator().create_viewer(pathpng)
    iv.view()


