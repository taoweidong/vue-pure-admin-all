@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

REM 切换到项目根目录
cd /d "%~dp0\..\.."

set VENV_DIR=venv

echo [INFO] Vue Pure Admin Service - 数据库配置切换工具
echo [INFO] 当前工作目录： 
cd
echo [INFO] 脚本目录: "%~dp0"
echo.

REM 激活虚拟环境（如果存在）
if exist "%VENV_DIR%" (
    echo [INFO] 激活虚拟环境...
    call "%VENV_DIR%\Scripts\activate.bat"
) else (
    echo [WARNING] 虚拟环境不存在，使用系统 Python 环境
)

REM 检查 Python 是否可用
echo [INFO] 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 未找到或未正确安装
    echo [ERROR] 请确保 Python 已安装并添加到 PATH 环境变量
    pause
    exit /b 1
)

REM 检查必要的模块
echo [INFO] 检查项目依赖...
python -c "import app" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 项目模块无法导入
    echo [ERROR] 请确保在正确的项目目录下执行脚本
    echo [ERROR] 当前目录： 
    cd
    pause
    exit /b 1
)

REM 检查 .env 文件是否存在
if not exist .env (
    echo [INFO] .env 文件不存在，从 .env.example 创建...
    REM 使用PowerShell以UTF-8编码复制文件
    powershell -Command "Get-Content '.env.example' -Encoding UTF8 | Set-Content '.env' -Encoding UTF8"
)

echo 请选择数据库类型：
echo 1) SQLite (推荐，无需额外配置)
echo 2) MySQL (需要预先安装和配置MySQL)
echo.
set /p choice=请输入选择 (1 或 2): 

REM 移除空格和换行符
set choice=%choice: =%

if "%choice%"=="1" (
    echo [INFO] 配置 SQLite 数据库...
    REM 更新 .env 文件
    powershell -Command "(Get-Content '.env') -replace '^DATABASE_URL=.*', 'DATABASE_URL=sqlite:///./db/vue_pure_admin.db' | Set-Content '.env' -Encoding UTF8"
    echo [SUCCESS] SQLite 配置完成！
    echo.
    echo [INFO] 配置信息：
    echo    数据库类型: SQLite
    echo    数据库文件: ./db/vue_pure_admin.db
    echo    优点: 零配置、开箱即用
) else if "%choice%"=="2" (
    echo [INFO] 配置 MySQL 数据库...
    echo.
    set /p host=MySQL 主机地址 (默认: localhost): 
    if "!host!"=="" set host=localhost
    
    set /p port=MySQL 端口 (默认: 3306): 
    if "!port!"=="" set port=3306
    
    set /p dbname=数据库名称 (默认: vue_pure_admin): 
    if "!dbname!"=="" set dbname=vue_pure_admin
    
    set /p username=用户名 (默认: root): 
    if "!username!"=="" set username=root
    
    set /p password=密码: 
    
    REM 构建连接字符串
    set "db_url=mysql+pymysql://!username!:!password!@!host!:!port!/!dbname!"
    
    REM 更新 .env 文件
    echo [INFO] 更新数据库配置: !db_url!
    REM 创建临时文件来处理特殊字符
    echo !db_url! > temp_db_url.txt
    powershell -Command "$url = Get-Content 'temp_db_url.txt' -Raw; $url = $url.Trim(); (Get-Content '.env') -replace '^DATABASE_URL=.*', ('DATABASE_URL=' + $url) | Set-Content '.env' -Encoding UTF8"
    del temp_db_url.txt
    
    echo [SUCCESS] MySQL 配置完成！
    echo.
    echo [INFO] 配置信息：
    echo    数据库类型: MySQL
    echo    主机: !host!:!port!
    echo    数据库: !dbname!
    echo    用户: !username!
    echo.
    echo [WARNING] 注意：请确保：
    echo    1. MySQL 服务已启动
    echo    2. 数据库 '!dbname!' 已创建
    echo    3. 用户 '!username!' 有足够权限
) else (
    echo [ERROR] 无效选择，退出。
    pause
    exit /b 1
)

echo.
echo [INFO] 初始化数据库...
echo [INFO] 当前工作目录： 
cd
echo [INFO] 执行命令: python -m app.infrastructure.database.init_db
echo.

python -m app.infrastructure.database.init_db
set db_init_result=%errorlevel%

echo.
echo [INFO] 数据库初始化命令执行完成，返回代码: %db_init_result%

if %db_init_result% equ 0 (
    echo [SUCCESS] 数据库初始化成功！
    echo.
    echo [INFO] 现在可以启动服务：
    echo    python -m app.main
) else (
    echo [ERROR] 数据库初始化失败，返回代码: %db_init_result%
    echo [ERROR] 请检查以下内容：
    echo    1. Python 环境是否正确
    echo    2. 依赖包是否已安装
    echo    3. 数据库配置是否正确
    echo    4. 文件权限是否充足
    pause
    exit /b %db_init_result%
)

pause