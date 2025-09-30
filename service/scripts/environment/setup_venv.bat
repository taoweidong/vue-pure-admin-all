@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

set VENV_DIR=..\..\venv

echo [INFO] Python Virtual Environment Setup
echo ====================================

REM 检查Python版本
:check_python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo [INFO] Found Python %PYTHON_VER%

REM 检查版本是否满足要求
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.8+ is required, found %PYTHON_VER%
    pause
    exit /b 1
)

REM 创建虚拟环境
:create_venv
if exist "%VENV_DIR%" (
    echo [WARNING] Virtual environment already exists at %VENV_DIR%
    set /p confirm=Do you want to recreate it? (y/N): 
    if /i "!confirm!"=="y" (
        echo [INFO] Removing existing virtual environment...
        rmdir /s /q "%VENV_DIR%"
    ) else (
        echo [SUCCESS] Using existing virtual environment
        goto setup_dependencies
    )
)

echo [INFO] Creating virtual environment...
python -m venv "%VENV_DIR%"

if %errorlevel% equ 0 (
    echo [SUCCESS] Virtual environment created successfully
) else (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

REM 激活虚拟环境并安装依赖
:setup_dependencies
echo [INFO] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [SUCCESS] Virtual environment activated
where python
python --version

REM 升级pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM 安装依赖
if exist "..\..\requirements.txt" (
    echo [INFO] Installing dependencies from requirements.txt...
    pip install -r "..\..\requirements.txt"
    
    if %errorlevel% equ 0 (
        echo [SUCCESS] Dependencies installed successfully
    ) else (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo [WARNING] requirements.txt not found, skipping dependency installation
)

REM 显示使用说明
:show_usage
echo.
echo [SUCCESS] Virtual environment setup completed!
echo.
echo [INFO] Usage Instructions:
echo    To activate the virtual environment:
echo    ^> %VENV_DIR%\Scripts\activate.bat
echo.
echo    To deactivate:
echo    ^> deactivate
echo.
echo    To start the service:
echo    ^> start.bat
echo.
echo [TIP] The start.bat script will automatically use this virtual environment

pause