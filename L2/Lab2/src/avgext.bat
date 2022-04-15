@echo off
SETLOCAL EnableDelayedExpansion
SET cnt=0
SET /a sum=0
for /F "tokens=3" %%a in ('dir /S /-C *%1 ^| findstr /E "%1" ') do (
	set wiel=%%a
	set wiel=!wiel:~0,-3!
	set /a sum = !wiel! + !sum!
	set /a cnt = !cnt! + 1
)

echo %sum% KB
echo %cnt% - ilosc plikow
set /a result = %sum%/%cnt%
echo.
echo AVG = %result% KB

pause