from ImageViewer import ImageViewer
from MultipleAccumulate import MultipleAccumulate
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

    arglist = [1, 2, 3, 4, 5]

    def add(x, y):
        return x + y

    def subtract(x, y):
        return x - y

    def multiply(x, y):
        return x * y

    ma = MultipleAccumulate(arglist, add, subtract, multiply)
    print(ma.get_data())

    for sth in [tv, ma]:
        sth.get_data()
