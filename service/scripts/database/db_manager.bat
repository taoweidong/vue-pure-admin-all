@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

REM 切换到项目根目录
cd /d "%~dp0\..\..\"

set VENV_DIR=venv
set DB_DIR=.\db
set DB_FILE=%DB_DIR%\vue_pure_admin.db
set BACKUP_DIR=%DB_DIR%\backup

REM 激活虚拟环境（如果存在）
if exist "%VENV_DIR%" (
    echo [INFO] Activating virtual environment...
    call "%VENV_DIR%\Scripts\activate.bat"
)

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="init" goto init_database
if "%1"=="backup" goto backup_database
if "%1"=="restore" goto restore_database
if "%1"=="reset" goto reset_database
if "%1"=="info" goto show_info
goto help

:help
echo Vue Pure Admin Database Manager
echo.
echo Usage: %0 [command]
echo.
echo Commands:
echo   init       - 初始化数据库
echo   backup     - 备份数据库
echo   restore    - 恢复数据库
echo   reset      - 重置数据库（危险操作）
echo   info       - 显示数据库信息
echo   help       - 显示此帮助信息
echo.
goto end

:init_database
echo [INFO] 初始化数据库...
python -m app.infrastructure.database.init_db
if %errorlevel% equ 0 (
    echo [SUCCESS] 数据库初始化完成
) else (
    echo [ERROR] 数据库初始化失败
    exit /b 1
)
goto end

:backup_database
if not exist "%DB_FILE%" (
    echo [ERROR] 数据库文件不存在: %DB_FILE%
    exit /b 1
)

REM 确保备份目录存在
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM 生成备份文件名
for /f "tokens=1-4 delims=/ " %%i in ('date /t') do set mydate=%%i%%j%%k
for /f "tokens=1-2 delims=: " %%i in ('time /t') do set mytime=%%i%%j
set mytime=%mytime: =0%
set TIMESTAMP=%mydate%_%mytime%
set BACKUP_FILE=%BACKUP_DIR%\vue_pure_admin_%TIMESTAMP%.db

REM 复制数据库文件
copy "%DB_FILE%" "%BACKUP_FILE%" >nul

if %errorlevel% equ 0 (
    echo [SUCCESS] 数据库备份完成: %BACKUP_FILE%
    
    REM 压缩备份文件
    powershell -Command "Compress-Archive -Path '%BACKUP_FILE%' -DestinationPath '%BACKUP_FILE%.zip'"
    del "%BACKUP_FILE%"
    echo [INFO] 备份文件已压缩: %BACKUP_FILE%.zip
) else (
    echo [ERROR] 数据库备份失败
    exit /b 1
)
goto end

:restore_database
echo [INFO] 可用的备份文件:
dir /b "%BACKUP_DIR%\*.zip" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 没有找到备份文件
    exit /b 1
)

echo.
set /p BACKUP_NAME=请输入要恢复的备份文件名: 
set BACKUP_FILE=%BACKUP_DIR%\%BACKUP_NAME%

if not exist "%BACKUP_FILE%" (
    echo [ERROR] 备份文件不存在: %BACKUP_FILE%
    exit /b 1
)

echo [WARNING] 警告: 这将覆盖当前数据库!
set /p confirm=确认恢复 %BACKUP_FILE% 吗? (y/N): 

if /i "%confirm%"=="y" (
    REM 解压并恢复
    powershell -Command "Expand-Archive -Path '%BACKUP_FILE%' -DestinationPath '%TEMP%' -Force"
    copy "%TEMP%\vue_pure_admin_*.db" "%DB_FILE%" >nul
    
    if %errorlevel% equ 0 (
        echo [SUCCESS] 数据库恢复完成
    ) else (
        echo [ERROR] 数据库恢复失败
        exit /b 1
    )
) else (
    echo [INFO] 恢复操作已取消
)
goto end

:reset_database
echo [WARNING] 危险操作: 这将删除所有数据并重新初始化数据库!
set /p confirm=确认重置数据库吗? (y/N): 

if /i "%confirm%"=="y" (
    REM 先备份现有数据库
    if exist "%DB_FILE%" (
        echo [INFO] 自动备份当前数据库...
        call :backup_database
    )
    
    REM 删除数据库文件
    if exist "%DB_FILE%" del "%DB_FILE%"
    echo [INFO] 已删除现有数据库文件
    
    REM 重新初始化
    call :init_database
) else (
    echo [INFO] 重置操作已取消
)
goto end

:show_info
echo [INFO] 数据库信息:
echo    数据库文件: %DB_FILE%

if exist "%DB_FILE%" (
    for %%F in ("%DB_FILE%") do (
        echo    文件大小: %%~zF bytes
        echo    最后修改: %%~tF
    )
    
    REM 显示用户数量
    echo    正在查询用户数量...
    python -c "import sqlite3; conn = sqlite3.connect('db/vue_pure_admin.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM users'); print('   用户数量:', cursor.fetchone()[0]); conn.close()" 2>nul || echo    用户数量: 查询失败
) else (
    echo    状态: 数据库文件不存在
)

echo.
echo [INFO] 备份文件:
if exist "%BACKUP_DIR%\*.zip" (
    dir "%BACKUP_DIR%\*.zip" /b
) else (
    echo    无备份文件
)
goto end

:end
pause