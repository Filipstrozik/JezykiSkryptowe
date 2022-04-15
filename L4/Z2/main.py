# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from MultipleAccumulate import MultipleAccumulate
from TextViewer import TextViewer


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    list = [1,2,3,4,5]


    def add(x, y):
        return x + y


    def subtract(x, y):
        return x - y


    def multiply(x, y):
        return x * y


    ma = MultipleAccumulate(list, add, subtract, multiply)
    print(ma.get_data())

    tv = TextViewer()
    tv.get_data()

    for sth in [TextViewer(),MultipleAccumulate(list, add, subtract, multiply)]:
        sth.get_data()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
