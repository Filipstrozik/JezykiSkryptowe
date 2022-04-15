import subprocess
import sys

if __name__ == '__main__':

    if len(sys.argv) > 1:
        arg = sys.argv[1]

        returned_text = subprocess.check_output(
            f'java -classpath "D:\MAIN\CODING\Sem 4\JezykiSkryptowe\L1\Testowe\src" Sciezki -R -s | java -cp "D:\MAIN\CODING\Sem 4\JezykiSkryptowe\L2\Lab2\src" process --delimiter=" " --project=2,1 --select={arg}',
            shell=True, universal_newlines=True)
        lines = returned_text.split("\n")

        sum: int = 0
        cnt: int = 0
        for line in lines:
            words = line.split("\t")

            if len(words) > 2:
                words.pop(2)

            if len(words) == 2:
                if words[1].isdecimal():
                    pair = (int(words[1]), words[0].replace("-", ""))
                    sum += pair[0]
                    cnt += 1
        print("Avarage size of files with extension : " + arg)
        print(str(sum / cnt) + " Bytes")
    else:
        print("AVGEXT REGUIRES NAME OF FILES EXTENTION!")
