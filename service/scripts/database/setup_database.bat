@echo off
setlocal enabledelayedexpansion

REM 切换到项目根目录
cd /d "%~dp0\..\..\"

set VENV_DIR=venv

echo 🔧 Vue Pure Admin Service - 数据库配置切换工具
echo.

REM 激活虚拟环境（如果存在）
if exist "%VENV_DIR%" (
    echo 🔧 Activating virtual environment...
    call "%VENV_DIR%\Scripts\activate.bat"
)

REM 检查 .env 文件是否存在
if not exist .env (
    echo 📋 .env 文件不存在，从 .env.example 创建...
    copy .env.example .env >nul
)

echo 请选择数据库类型：
echo 1^) SQLite（推荐，无需额外配置）
echo 2^) MySQL（需要预先安装和配置MySQL）
echo.
set /p choice=请输入选择 (1 或 2): 

if "%choice%"=="1" (
    echo ✅ 配置 SQLite 数据库...
    REM 更新 .env 文件
    powershell -Command "(Get-Content .env) -replace '^DATABASE_URL=.*', 'DATABASE_URL=sqlite:///./db/vue_pure_admin.db' | Set-Content .env"
    echo ✅ SQLite 配置完成！
    echo.
    echo 📝 配置信息：
    echo    数据库类型: SQLite
    echo    数据库文件: ./db/vue_pure_admin.db
    echo    优点: 零配置、开箱即用
) else if "%choice%"=="2" (
    echo ⚙️ 配置 MySQL 数据库...
    echo.
    set /p host=MySQL 主机地址 ^(默认: localhost^): 
    if "!host!"=="" set host=localhost
    
    set /p port=MySQL 端口 ^(默认: 3306^): 
    if "!port!"=="" set port=3306
    
    set /p dbname=数据库名称 ^(默认: vue_pure_admin^): 
    if "!dbname!"=="" set dbname=vue_pure_admin
    
    set /p username=用户名 ^(默认: root^): 
    if "!username!"=="" set username=root
    
    set /p password=密码: 
    
    REM 构建连接字符串
    set db_url=mysql+pymysql://!username!:!password!@!host!:!port!/!dbname!
    
    REM 更新 .env 文件
    powershell -Command "(Get-Content .env) -replace '^DATABASE_URL=.*', 'DATABASE_URL=!db_url!' | Set-Content .env"
    
    echo ✅ MySQL 配置完成！
    echo.
    echo 📝 配置信息：
    echo    数据库类型: MySQL
    echo    主机: !host!:!port!
    echo    数据库: !dbname!
    echo    用户: !username!
    echo.
    echo ⚠️ 注意：请确保：
    echo    1. MySQL 服务已启动
    echo    2. 数据库 '!dbname!' 已创建
    echo    3. 用户 '!username!' 有足够权限
) else (
    echo ❌ 无效选择，退出。
    pause
    exit /b 1
)

echo.
echo 🔄 初始化数据库...
python -m app.infrastructure.database.init_db

if %errorlevel% equ 0 (
    echo ✅ 数据库初始化成功！
    echo.
    echo 🚀 现在可以启动服务：
    echo    python -m app.main
) else (
    echo ❌ 数据库初始化失败，请检查配置。
    pause
    exit /b 1
)

pause