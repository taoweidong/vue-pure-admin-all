#!/bin/bash

# 虚拟环境状态检查脚本

VENV_DIR="../../venv"

echo "🔍 Virtual Environment Status Check"
echo "==================================="

# 检查虚拟环境是否存在
if [ -d "$VENV_DIR" ]; then
    echo "✅ Virtual environment exists at: $VENV_DIR"
    
    # 检查虚拟环境是否完整
    if [ -f "$VENV_DIR/bin/activate" ] && [ -f "$VENV_DIR/bin/python" ]; then
        echo "✅ Virtual environment appears to be complete"
        
        # 显示Python版本
        PYTHON_VERSION=$("$VENV_DIR/bin/python" --version 2>&1)
        echo "📋 Python version: $PYTHON_VERSION"
        
        # 显示pip版本
        PIP_VERSION=$("$VENV_DIR/bin/pip" --version 2>&1 | cut -d' ' -f2)
        echo "📦 Pip version: $PIP_VERSION"
        
        # 检查是否已安装依赖
        if [ -f "../../requirements.txt" ]; then
            echo ""
            echo "📋 Checking installed packages..."
            
            # 激活虚拟环境并检查包
            source "$VENV_DIR/bin/activate"
            
            # 检查核心依赖是否已安装
            CORE_PACKAGES=("fastapi" "uvicorn" "sqlalchemy" "redis" "pydantic")
            MISSING_PACKAGES=()
            
            for package in "${CORE_PACKAGES[@]}"; do
                if pip show "$package" >/dev/null 2>&1; then
                    VERSION=$(pip show "$package" | grep "Version:" | cut -d' ' -f2)
                    echo "  ✅ $package ($VERSION)"
                else
                    echo "  ❌ $package (not installed)"
                    MISSING_PACKAGES+=("$package")
                fi
            done
            
            if [ ${#MISSING_PACKAGES[@]} -eq 0 ]; then
                echo ""
                echo "🎉 All core dependencies are installed!"
            else
                echo ""
                echo "⚠️ Missing dependencies: ${MISSING_PACKAGES[*]}"
                echo "💡 Run 'pip install -r requirements.txt' to install missing packages"
            fi
            
            deactivate
        fi
        
    else
        echo "❌ Virtual environment is incomplete"
        echo "💡 Run './scripts/environment/setup_venv.sh' to recreate the virtual environment"
    fi
    
else
    echo "❌ Virtual environment not found"
    echo "💡 Run './scripts/environment/setup_venv.sh' to create the virtual environment"
fi

echo ""

# 检查当前是否在虚拟环境中
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Currently in virtual environment: $VIRTUAL_ENV"
else
    echo "ℹ️ Not currently in a virtual environment"
    if [ -d "$VENV_DIR" ]; then
        echo "💡 To activate: source $VENV_DIR/bin/activate"
    fi
fi

echo ""
echo "🛠️ Available commands:"
echo "  ./scripts/environment/setup_venv.sh    - Create/recreate virtual environment"
echo "  ./start.sh         - Start service (auto-activates venv)"
echo "  source venv/bin/activate - Manually activate virtual environment"