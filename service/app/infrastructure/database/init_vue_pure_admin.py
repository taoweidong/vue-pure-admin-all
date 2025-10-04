#!/usr/bin/env python3
"""
Vue Pure Admin 数据库初始化脚本
基于 service/db/init/vue_pure_admin.sql 文件的表结构
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from shared.kernel.config import get_settings
from loguru import logger


def create_database():
    """创建数据库（如果不存在）"""
    settings = get_settings()
    
    # 如果是SQLite，确保数据库文件目录存在
    if settings.DATABASE_URL.startswith('sqlite'):
        db_path = settings.DATABASE_URL.replace('sqlite:///', '')
        db_dir = os.path.dirname(db_path)
        if db_dir:
            Path(db_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"SQLite数据库路径: {db_path}")
        return
    
    # MySQL数据库创建逻辑
    if settings.DATABASE_URL.startswith('mysql'):
        # 解析数据库URL获取数据库名
        import re
        match = re.search(r'mysql\+pymysql://([^:]+):([^@]+)@([^:]+):(\d+)/([^?]+)', settings.DATABASE_URL)
        if match:
            user, password, host, port, database = match.groups()
            
            # 连接到MySQL服务器（不指定数据库）
            server_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/"
            engine = create_engine(server_url)
            
            with engine.connect() as conn:
                # 创建数据库（如果不存在）
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                logger.info(f"MySQL数据库 '{database}' 检查完成")
            
            engine.dispose()


def execute_sql_file(sql_file_path: str):
    """执行SQL文件"""
    settings = get_settings()
    
    if not os.path.exists(sql_file_path):
        logger.error(f"SQL文件不存在: {sql_file_path}")
        return False
    
    try:
        # 创建数据库引擎
        engine = create_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO)
        
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # 分割SQL语句（按分号分割，忽略空行和注释）
        sql_statements = []
        current_statement = []
        in_multiline_comment = False
        
        for line in sql_content.split('\n'):
            line = line.strip()
            
            # 跳过空行
            if not line:
                continue
            
            # 处理多行注释
            if line.startswith('/*'):
                in_multiline_comment = True
                continue
            if line.endswith('*/'):
                in_multiline_comment = False
                continue
            if in_multiline_comment:
                continue
                
            # 跳过单行注释
            if line.startswith('--') or line.startswith('#'):
                continue
                
            # 跳过MySQL特定设置和注释行
            if (line.startswith('SET FOREIGN_KEY_CHECKS') or 
                line.startswith('Navicat') or
                line.startswith('Source') or
                line.startswith('Target') or
                line.startswith('File Encoding') or
                line.startswith('Date:')):
                continue
            
            # 跳过DROP TABLE语句（SQLite可能不支持IF EXISTS的某些语法）
            if line.startswith('DROP TABLE IF EXISTS'):
                continue
                
            current_statement.append(line)
            
            # 如果行以分号结尾，表示语句结束
            if line.endswith(';'):
                statement = ' '.join(current_statement)
                if statement.strip() and not statement.strip().startswith('/*'):
                    sql_statements.append(statement)
                current_statement = []
        
        # 添加最后一个语句（如果没有以分号结尾）
        if current_statement:
            statement = ' '.join(current_statement)
            if statement.strip():
                sql_statements.append(statement)
        
        # 执行SQL语句
        with engine.connect() as conn:
            transaction = conn.begin()
            try:
                for statement in sql_statements:
                    if statement.strip():
                        logger.debug(f"执行SQL: {statement[:100]}...")
                        conn.execute(text(statement))
                
                transaction.commit()
                logger.info(f"成功执行SQL文件: {sql_file_path}")
                return True
                
            except Exception as e:
                transaction.rollback()
                logger.error(f"执行SQL文件失败: {e}")
                return False
                
    except Exception as e:
        logger.error(f"创建数据库连接失败: {e}")
        return False


def init_vue_pure_admin_database():
    """初始化Vue Pure Admin数据库"""
    logger.info("开始初始化Vue Pure Admin数据库...")
    
    # 1. 创建数据库
    create_database()
    
    # 2. 执行建表SQL文件
    sql_file_path = project_root / "db" / "init" / "vue_pure_admin.sql"
    
    if sql_file_path.exists():
        success = execute_sql_file(str(sql_file_path))
        if success:
            logger.info("Vue Pure Admin数据库初始化完成")
        else:
            logger.error("Vue Pure Admin数据库初始化失败")
    else:
        logger.error(f"SQL文件不存在: {sql_file_path}")


if __name__ == "__main__":
    init_vue_pure_admin_database()