#!/bin/bash

# 数据库管理脚本

# 切换到项目根目录
cd "$(dirname "$0")/../.."

VENV_DIR="venv"
DB_DIR="./db"
DB_FILE="$DB_DIR/vue_pure_admin.db"
BACKUP_DIR="$DB_DIR/backup"

# 激活虚拟环境（如果存在）
activate_venv() {
    if [ -d "$VENV_DIR" ]; then
        echo "[INFO] Activating virtual environment..."
        source "$VENV_DIR/bin/activate"
    fi
}

show_help() {
    echo "Vue Pure Admin Database Manager"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  init       - 初始化数据库"
    echo "  backup     - 备份数据库"
    echo "  restore    - 恢复数据库"
    echo "  reset      - 重置数据库（危险操作）"
    echo "  info       - 显示数据库信息"
    echo "  help       - 显示此帮助信息"
    echo ""
}

init_database() {
    activate_venv
    echo "[INFO] 初始化数据库..."
    python -m app.infrastructure.database.init_db
    if [ $? -eq 0 ]; then
        echo "[SUCCESS] 数据库初始化完成"
    else
        echo "[ERROR] 数据库初始化失败"
        exit 1
    fi
}

backup_database() {
    if [ ! -f "$DB_FILE" ]; then
        echo "[ERROR] 数据库文件不存在: $DB_FILE"
        exit 1
    fi
    
    # 确保备份目录存在
    mkdir -p "$BACKUP_DIR"
    
    # 生成备份文件名
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/vue_pure_admin_$TIMESTAMP.db"
    
    # 复制数据库文件
    cp "$DB_FILE" "$BACKUP_FILE"
    
    if [ $? -eq 0 ]; then
        echo "[SUCCESS] 数据库备份完成: $BACKUP_FILE"
        
        # 压缩备份文件
        gzip "$BACKUP_FILE"
        echo "[INFO] 备份文件已压缩: $BACKUP_FILE.gz"
        
        # 显示备份文件大小
        BACKUP_SIZE=$(du -h "$BACKUP_FILE.gz" | cut -f1)
        echo "[INFO] 备份文件大小: $BACKUP_SIZE"
    else
        echo "[ERROR] 数据库备份失败"
        exit 1
    fi
}

restore_database() {
    echo "[INFO] 可用的备份文件:"
    ls -la "$BACKUP_DIR"/*.gz 2>/dev/null | nl
    
    if [ $? -ne 0 ]; then
        echo "[ERROR] 没有找到备份文件"
        exit 1
    fi
    
    echo ""
    read -p "请输入要恢复的备份文件编号: " choice
    
    # 获取选中的备份文件
    BACKUP_FILE=$(ls "$BACKUP_DIR"/*.gz 2>/dev/null | sed -n "${choice}p")
    
    if [ -z "$BACKUP_FILE" ]; then
        echo "[ERROR] 无效的选择"
        exit 1
    fi
    
    echo "[WARNING] 警告: 这将覆盖当前数据库!"
    read -p "确认恢复 $BACKUP_FILE 吗? (y/N): " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        # 解压并恢复
        gunzip -c "$BACKUP_FILE" > "$DB_FILE"
        
        if [ $? -eq 0 ]; then
            echo "[SUCCESS] 数据库恢复完成"
        else
            echo "[ERROR] 数据库恢复失败"
            exit 1
        fi
    else
        echo "[INFO] 恢复操作已取消"
    fi
}

reset_database() {
    echo "[WARNING] 危险操作: 这将删除所有数据并重新初始化数据库!"
    read -p "确认重置数据库吗? (y/N): " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        # 先备份现有数据库
        if [ -f "$DB_FILE" ]; then
            echo "[INFO] 自动备份当前数据库..."
            backup_database
        fi
        
        # 删除数据库文件
        rm -f "$DB_FILE"
        echo "[INFO] 已删除现有数据库文件"
        
        # 重新初始化
        init_database
    else
        echo "[INFO] 重置操作已取消"
    fi
}

show_info() {
    echo "[INFO] 数据库信息:"
    echo "   数据库文件: $DB_FILE"
    
    if [ -f "$DB_FILE" ]; then
        DB_SIZE=$(du -h "$DB_FILE" | cut -f1)
        echo "   文件大小: $DB_SIZE"
        echo "   最后修改: $(stat -c %y "$DB_FILE")"
        
        # 显示表数量
        TABLE_COUNT=$(sqlite3 "$DB_FILE" ".tables" | wc -w)
        echo "   表数量: $TABLE_COUNT"
        
        # 显示用户数量
        USER_COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM users;" 2>/dev/null || echo "N/A")
        echo "   用户数量: $USER_COUNT"
    else
        echo "   状态: 数据库文件不存在"
    fi
    
    echo ""
    echo "[INFO] 备份文件:"
    if [ -d "$BACKUP_DIR" ] && [ "$(ls -A $BACKUP_DIR)" ]; then
        ls -lah "$BACKUP_DIR"/*.gz 2>/dev/null | while read line; do
            echo "   $line"
        done
    else
        echo "   无备份文件"
    fi
}

# 主逻辑
case "${1:-help}" in
    init)
        init_database
        ;;
    backup)
        backup_database
        ;;
    restore)
        restore_database
        ;;
    reset)
        reset_database
        ;;
    info)
        show_info
        ;;
    help|*)
        show_help
        ;;
esac