@echo off
reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\wallpaper.jpg" /f & RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters
