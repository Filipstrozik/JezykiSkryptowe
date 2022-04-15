import os

if __name__ == '__main__':

    napis = input(' napisz wyrazy korych mam szukac\n')
    print('pisz tekst\n')
    # print(os.system('cmd /c "cd D:\MAIN\CODING\Sem 4\JezykiSkryptowe\L1\Testowe\src '
    #                 '&& javac Main.java '
    #                 '&& java Main "' + napis))
    kodPowrotu = os.system('cmd /c "cd D:\MAIN\CODING\Sem 4\JezykiSkryptowe\L1\Testowe\src '
                    '&& javac KodPowrotu.java '
                    '&& java KodPowrotu "' + napis)
    print(kodPowrotu)
