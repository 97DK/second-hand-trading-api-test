# common/logger.py
"""
日志管理模块
使用loguru进行日志记录
"""

import sys
from pathlib import Path
from loguru import logger
from config.settings import Config


class Logger:
    """日志管理类"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._setup_logger()
            self._initialized = True
    
    def _setup_logger(self):
        """配置日志"""
        config = Config()
        log_config = config.log_config
        
        # 移除默认handler
        logger.remove()
        
        # 控制台输出
        logger.add(
            sys.stdout,
            level=log_config['level'],
            format=log_config['format'],
            colorize=True
        )
        
        # 文件输出
        log_dir = Path(__file__).parent.parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        logger.add(
            log_dir / 'api_test_{time:YYYY-MM-DD}.log',
            level=log_config['level'],
            format=log_config['format'],
            rotation=log_config['rotation'],
            retention=log_config['retention'],
            encoding='utf-8'
        )
    
    def get_logger(self):
        """获取logger实例"""
        return logger
