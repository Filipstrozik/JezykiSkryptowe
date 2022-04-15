ECHO OFF

SET LPARAM= %*

javac KodPowrotu.java
java KodPowrotu %LPARAM%

SET /A KOD=%ERRORLEVEL%
SET /A COUNTER = 1

SETLOCAL EnableDelayedExpansion

FOR %%A in (%LPARAM%) DO (

IF !COUNTER! EQU %KOD% (ECHO najczesciej wystepuje slowo %%A)

SET /A COUNTER +=1
)
IF %KOD% EQU 0 (ECHO parametry nie wystapuja w tekscie ani razu, albo nie podano parametrow)

pause