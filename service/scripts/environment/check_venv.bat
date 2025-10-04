@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

set VENV_DIR=..\..\venv

echo [INFO] Virtual Environment Status Check
echo ===================================

REM 检查虚拟环境是否存在
if exist "%VENV_DIR%" (
    echo [SUCCESS] Virtual environment exists at: %VENV_DIR%
    
    REM 检查虚拟环境是否完整
    if exist "%VENV_DIR%\Scripts\activate.bat" (
        if exist "%VENV_DIR%\Scripts\python.exe" (
            echo [SUCCESS] Virtual environment appears to be complete
            
            REM 显示Python版本
            for /f "tokens=*" %%i in ('"%VENV_DIR%\Scripts\python.exe" --version 2^>^&1') do set PYTHON_VERSION=%%i
            echo [INFO] Python version: !PYTHON_VERSION!
            
            REM 显示pip版本
            for /f "tokens=2" %%i in ('"%VENV_DIR%\Scripts\pip.exe" --version 2^>^&1') do set PIP_VERSION=%%i
            echo [INFO] Pip version: !PIP_VERSION!
            
            REM 检查是否已安装依赖
            if exist "..\..\requirements.txt" (
                echo.
                echo [INFO] Checking installed packages...
                
                REM 激活虚拟环境并检查包
                call "%VENV_DIR%\Scripts\activate.bat"
                
                REM 检查核心依赖是否已安装
                set CORE_PACKAGES=fastapi uvicorn sqlalchemy redis pydantic
                set MISSING_COUNT=0
                
                for %%p in (!CORE_PACKAGES!) do (
                    pip show %%p >nul 2>&1
                    if !errorlevel! equ 0 (
                        for /f "tokens=2" %%v in ('pip show %%p ^| findstr "Version:"') do (
                            echo   [SUCCESS] %%p (%%v)
                        )
                    ) else (
                        echo   [ERROR] %%p (not installed)
                        set /a MISSING_COUNT+=1
                    )
                )
                
                if !MISSING_COUNT! equ 0 (
                    echo.
                    echo [SUCCESS] All core dependencies are installed!
                ) else (
                    echo.
                    echo [WARNING] Some dependencies are missing
                    echo [TIP] Run 'pip install -r requirements.txt' to install missing packages
                )
                
                call deactivate
            )
            
        ) else (
            echo [ERROR] Virtual environment is incomplete (missing python.exe)
            echo [TIP] Run 'scripts\environment\setup_venv.bat' to recreate the virtual environment
        )
    ) else (
        echo [ERROR] Virtual environment is incomplete (missing activate.bat)
        echo [TIP] Run 'scripts\environment\setup_venv.bat' to recreate the virtual environment
    )
    
) else (
    echo [ERROR] Virtual environment not found
    echo [TIP] Run 'scripts\environment\setup_venv.bat' to create the virtual environment
)

echo.

REM 检查当前是否在虚拟环境中
if defined VIRTUAL_ENV (
    echo [SUCCESS] Currently in virtual environment: %VIRTUAL_ENV%
) else (
    echo [INFO] Not currently in a virtual environment
    if exist "%VENV_DIR%" (
        echo [TIP] To activate: %VENV_DIR%\Scripts\activate.bat
    )
)

echo.
echo [INFO] Available commands:
echo   scripts\environment\setup_venv.bat     - Create/recreate virtual environment
echo   start.bat          - Start service (auto-activates venv)
echo   %VENV_DIR%\Scripts\activate.bat - Manually activate virtual environment

pause