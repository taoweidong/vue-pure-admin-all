@echo off
chcp 65001 >nul 2>&1
echo [INFO] Starting Vue Pure Admin Service...

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM 虚拟环境目录
set VENV_DIR=venv

REM 创建虚拟环境（如果不存在）
if not exist "%VENV_DIR%" (
    echo [INFO] Creating virtual environment...
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created successfully
)

REM 激活虚拟环境
echo [INFO] Activating virtual environment...
call %VENV_DIR%\Scripts\activate.bat

if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [SUCCESS] Virtual environment activated

REM 升级pip
echo [INFO] Upgrading pip...
python -m ensurepip --upgrade >nul 2>&1
python -m pip install --upgrade pip >nul 2>&1

REM 安装依赖
echo [INFO] Installing dependencies...
pip install -r requirements.txt

REM 复制环境配置文件
if not exist .env (
    echo [INFO] Creating .env file from .env.example...
    copy .env.example .env
    echo [NOTICE] Please edit .env file with your configuration
)

REM 初始化数据库
echo [INFO] Initializing database...
python -m app.infrastructure.database.init_db

REM 启动服务
echo [INFO] Starting the service...
python -m app.main

pause