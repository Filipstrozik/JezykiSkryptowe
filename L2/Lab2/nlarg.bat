@echo off
SETLOCAL EnableDelayedExpansion


dir /A-D /S /-C /r | java -cp "D:\MAIN\CODING\Sem 4\JezykiSkryptowe\L2\Lab2\src" process --select=. | sort /+18 /R | java -cp "D:\MAIN\CODING\Sem 4\JezykiSkryptowe\L2\Lab2\src" Head --lines=%1

dir /A-D /S /-C | sort /+18 /R | java -cp "D:\MAIN\CODING\Sem 4\JezykiSkryptowe\L2\Lab2\src" Head --lines=30