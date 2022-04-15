@echo off
SETLOCAL EnableDelayedExpansion
SET cnt=0
SET /a sum=0

java -classpath "D:\MAIN\CODING\Sem 4\JezykiSkryptowe\L1\Testowe\src" Sciezki -R -s | java -cp "D:\MAIN\CODING\Sem 4\JezykiSkryptowe\L2\Lab2\src" process --delimiter=" " --project=2,1 | sort /R