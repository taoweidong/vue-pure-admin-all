# -*- coding: utf-8 -*-
"""
应用配置模块
重新导出共享配置以保持向后兼容性
"""

from shared.kernel.config import Settings, get_settings

# 创建全局配置实例
settings = get_settings()

# 导出配置类和实例
__all__ = ['Settings', 'settings', 'get_settings']