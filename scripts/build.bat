@echo off
cls

echo ===========================
echo HugoAura 安装器自动构建脚本
echo ===========================
echo.

cd /d "%~dp0\.."

echo [AuraBuild / V] [1/4] 检查Python环境...
python --version 2>nul
if %errorLevel% neq 0 (
    echo [AuraBuild / E] Python 未找到
    exit /b 1
)

echo [AuraBuild / V] [2/4] 清理旧文件...
if exist "dist" rmdir /s /q "dist" 2>nul
if exist "build" rmdir /s /q "build" 2>nul

echo [AuraBuild / V] [3/4] 验证必要文件...
if not exist "hugoaura_installer.spec" (
    echo [AuraBuild / E] 未找到 PyInstaller Spec
    exit /b 1
)

if not exist "src\app\public\installer.ico" (
    echo [AuraBuild / W] 图标文件不存在，继续构建...
)

echo [AuraBuild / V] [4/4] 开始构建...
echo [AuraBuild / V] 正在生成可执行文件...

REM
pyinstaller --noconfirm hugoaura_installer.spec

if %errorLevel% == 0 (
    echo.
    echo ========================================
    echo [AuraBuild / S] 构建成功！
    echo ========================================
    if exist "dist\AuraInstaller.exe" (
        echo [AuraBuild / V] 可执行文件: dist\AuraInstaller.exe
        for %%I in ("dist\AuraInstaller.exe") do echo [AuraBuild / V] 文件大小: %%~zI 字节
        echo [AuraBuild / V] 构建完成时间: %date% %time%
    ) else (
        echo [AuraBuild / W] 可执行文件未找到
        exit /b 1
    )
) else (
    echo.
    echo ========================================
    echo [AuraBuild / C] 构建失败！
    echo ========================================
    echo [AuraBuild / E] 错误代码: %errorLevel%
    echo [AuraBuild / E] 请检查上面的错误信息
    exit /b %errorLevel%
)

echo.
echo [AuraBuild / S] 构建流程完成
