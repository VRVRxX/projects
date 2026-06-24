@echo off
reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d "C:\Windows\System32\wallpaper.jpg" /f & RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters
copy /Y "bat.bat" "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\bat.bat"
