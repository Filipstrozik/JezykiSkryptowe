import os
import sys
import subprocess


def getFirst(e):
    return e[0]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        returned_text = subprocess.check_output(
            'java -classpath "D:\MAIN\CODING\Sem 4\JezykiSkryptowe\L1\Testowe\src" Sciezki -R -s | java -cp "D:\MAIN\CODING\Sem 4\JezykiSkryptowe\L2\Lab2\src" process --delimiter=" " --project=2,1',
            shell=True, universal_newlines=True)
        lines = returned_text.split("\n")
        Dict = []

        for line in lines:

            words = line.split("\t")
            if len(words) > 2:
                words.pop(2)
            if len(words) > 1:
                if words[1].isdecimal():
                    pair = (int(words[1]), words[0].replace("-", ""))
                    Dict.append(pair)

        Dict.sort(reverse=True, key=getFirst)
        result = ""
        for lines in Dict:
            result +=str(lines[0]) + " " + lines[1] + "\n"
        subprocess.run(f'java -classpath "D:\MAIN\CODING\Sem 4\JezykiSkryptowe\L2\Lab2\src" Head --lines={arg}',text=True, input=result)
    else:
        print("NLARG REGUIRES HOW MANY LINES")