@echo off
echo Cleaning up previous builds...
rmdir /s /q dist
rmdir /s /q build
del /q /f *.spec

echo Building Aura Installer executable...

cd src/

pyinstaller ^
    --noconfirm ^
    --onefile ^
    --console ^
    --name AuraInstaller ^
    main.py

move ./dist ../dist

echo Build finished. Check the 'dist' folder.
pause
