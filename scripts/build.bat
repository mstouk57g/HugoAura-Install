@echo off
title HugoAura 安装器 - 自动构建脚本
color 0A

echo ========================================
echo HugoAura 安装器自动构建脚本 (GitHub Actions)
echo ========================================
echo.

cd /d "%~dp0\.."

echo [1/6] 检查Python环境...
python --version
if %errorLevel% neq 0 (
    echo 错误: Python 未找到
    exit /b 1
)

echo [2/6] 检查依赖...
python -c "import pyinstaller; print('PyInstaller:', pyinstaller.__version__)" 2>nul
if %errorLevel% neq 0 (
    echo PyInstaller 未安装，正在安装...
    pip install pyinstaller>=6.14.1,<7.0.0
    if %errorLevel% neq 0 (
        echo PyInstaller 安装失败
        exit /b 1
    )
)

echo [3/6] 验证关键依赖...
python -c "import ttkbootstrap; print('ttkbootstrap: OK')" 2>nul
if %errorLevel% neq 0 (
    echo 警告: ttkbootstrap 未找到
)

python -c "import PIL; print('PIL: OK')" 2>nul
if %errorLevel% neq 0 (
    echo 警告: PIL/Pillow 未找到
)

python -c "import loguru; print('loguru: OK')" 2>nul
if %errorLevel% neq 0 (
    echo 警告: loguru 未找到
)

echo [4/6] 清理旧文件...
if exist "dist" rmdir /s /q "dist" 2>nul
if exist "build" rmdir /s /q "build" 2>nul
if exist "*.spec" del "*.spec" 2>nul

echo [5/6] 验证必要文件...
if not exist "hugoaura_installer.spec" (
    echo 错误: hugoaura_installer.spec 文件不存在
    exit /b 1
)

if not exist "src\app\public\aura.ico" (
    echo 警告: 图标文件不存在，继续构建...
)

echo [6/6] 开始构建...
echo 正在生成可执行文件（包含调试信息）...

REM
pyinstaller --clean --noconfirm=all hugoaura_installer.spec

if %errorLevel% == 0 (
    echo.
    echo ========================================
    echo 构建成功！
    echo ========================================
    if exist "dist\AuraInstaller.exe" (
        echo 可执行文件: dist\AuraInstaller.exe
        for %%I in ("dist\AuraInstaller.exe") do echo 文件大小: %%~zI 字节
        echo 构建完成时间: %date% %time%
        echo.
        echo 调试信息: 如果运行时出错，请查看生成的日志文件
        echo 日志位置: dist\ 目录下的 .log 文件
    ) else (
        echo 警告: 可执行文件未找到
        exit /b 1
    )
) else (
    echo.
    echo ========================================
    echo 构建失败！
    echo ========================================
    echo 错误代码: %errorLevel%
    echo 请检查上面的错误信息
    exit /b %errorLevel%
)

echo.
echo 构建流程完成