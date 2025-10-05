#!/usr/bin/env python3
"""
更新用户密码脚本
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import update
from app.infrastructure.utils.auth import AuthService
from app.infrastructure.database.database import SessionLocal, engine
from app.domain.user.entities.user import User

def update_user_passwords():
    """更新用户密码为bcrypt哈希"""
    db = SessionLocal()
    
    try:
        # 创建AuthService实例
        auth_service = AuthService()
        
        # 更新admin用户密码
        admin_hash = auth_service.get_password_hash("admin123")
        db.execute(
            update(User).where(User.username == "admin").values(password=admin_hash)
        )
        print("Updated admin password")
        
        # 更新common用户密码
        common_hash = auth_service.get_password_hash("common123")
        db.execute(
            update(User).where(User.username == "common").values(password=common_hash)
        )
        print("Updated common user password")
        
        db.commit()
        print("Password update completed successfully")
        
    except Exception as e:
        print(f"Error updating passwords: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_user_passwords()