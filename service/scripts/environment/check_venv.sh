#!/bin/bash

VENV_DIR="../../venv"

echo "[INFO] Virtual Environment Status Check"
echo "==================================="

# 检查虚拟环境是否存在
if [ -d "$VENV_DIR" ]; then
    echo "[SUCCESS] Virtual environment exists at: $VENV_DIR"
    
    # 检查虚拟环境是否完整
    if [ -f "$VENV_DIR/bin/activate" ] && [ -f "$VENV_DIR/bin/python" ]; then
        echo "[SUCCESS] Virtual environment appears to be complete"
        
        # 显示Python版本
        PYTHON_VERSION=$("$VENV_DIR/bin/python" --version 2>&1)
        echo "[INFO] Python version: $PYTHON_VERSION"
        
        # 显示pip版本
        PIP_VERSION=$("$VENV_DIR/bin/pip" --version 2>&1 | awk '{print $2}')
        echo "[INFO] Pip version: $PIP_VERSION"
        
        # 检查是否已安装依赖
        if [ -f "../../requirements.txt" ]; then
            echo ""
            echo "[INFO] Checking installed packages..."
            
            # 激活虚拟环境并检查包
            source "$VENV_DIR/bin/activate"
            
            # 检查核心依赖是否已安装
            CORE_PACKAGES="fastapi uvicorn sqlalchemy redis pydantic"
            MISSING_COUNT=0
            
            for package in $CORE_PACKAGES; do
                if "$VENV_DIR/bin/pip" show "$package" > /dev/null 2>&1; then
                    VERSION=$("$VENV_DIR/bin/pip" show "$package" | grep "Version:" | awk '{print $2}')
                    echo "  [SUCCESS] $package ($VERSION)"
                else
                    echo "  [ERROR] $package (not installed)"
                    MISSING_COUNT=$((MISSING_COUNT + 1))
                fi
            done
            
            if [ $MISSING_COUNT -eq 0 ]; then
                echo ""
                echo "[SUCCESS] All core dependencies are installed!"
            else
                echo ""
                echo "[WARNING] Some dependencies are missing"
                echo "[TIP] Run 'pip install -r requirements.txt' to install missing packages"
            fi
            
            deactivate
        fi
        
    else
        echo "[ERROR] Virtual environment is incomplete"
        echo "[TIP] Run 'scripts/environment/setup_venv.sh' to recreate the virtual environment"
    fi
    
else
    echo "[ERROR] Virtual environment not found"
    echo "[TIP] Run 'scripts/environment/setup_venv.sh' to create the virtual environment"
fi

echo ""

# 检查当前是否在虚拟环境中
if [ -n "$VIRTUAL_ENV" ]; then
    echo "[SUCCESS] Currently in virtual environment: $VIRTUAL_ENV"
else
    echo "[INFO] Not currently in a virtual environment"
    if [ -d "$VENV_DIR" ]; then
        echo "[TIP] To activate: source $VENV_DIR/bin/activate"
    fi
fi

echo ""
echo "[INFO] Available commands:"
echo "  scripts/environment/setup_venv.sh     - Create/recreate virtual environment"
echo "  start.sh          - Start service (auto-activates venv)"
echo "  source $VENV_DIR/bin/activate - Manually activate virtual environment"

read -p "Press Enter to continue..."