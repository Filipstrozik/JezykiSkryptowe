@ECHO OFF


IF %1==--dst (goto :niemasrc)

:jestsrc
set str1=%2
set str1=%str1:~0,-1%
set str2=%4
goto :poustaleniu

:niemasrc
set str1="%CD%"
set str2=%2

:poustaleniu
ECHO %str1%
ECHO %str2%

XCOPY /S /I %str1% %str2%



