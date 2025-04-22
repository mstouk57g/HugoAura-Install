@echo off
echo Cleaning up previous builds...
rmdir /s /q dist
rmdir /s /q build
del /q /f *.spec

echo Building Aura Installer executable...

poetry run pyinstaller ^
    --noconfirm ^
    --onefile ^
    --console ^
    --name AuraInstaller ^
    src/main.py

echo Build finished. Check the 'dist' folder.
pause
