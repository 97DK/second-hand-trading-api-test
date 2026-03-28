# config/settings.py
"""
项目配置文件
管理不同环境的配置信息
"""

import os
from typing import Dict, Any


class Config:
    """配置管理类"""
    
    # 环境配置
    ENVIRONMENTS = {
        'dev': {
            'base_url': 'http://localhost:8080',
            'timeout': 30,
            'debug': True
        },
        'test': {
            'base_url': 'http://test-api.example.com',
            'timeout': 30,
            'debug': False
        },
        'prod': {
            'base_url': 'https://api.example.com',
            'timeout': 30,
            'debug': False
        }
    }
    
    # 测试用户配置
    TEST_USERS = {
        'student': {
            'username': 'sssass',
            'password': 'TFBOYS2023',
            'user_type': 'student'
        },
        'evaluation_student': {  # 专门用于商品评价模块测试的用户
            'username': 'num3',
            'password': 'TFBOYS2023',
            'user_type': 'student'
        },
        'admin': {
            'username': 'admin',
            'password': 'admin123',
            'user_type': 'admin'
        },
        'unverified_student': {
            'username': 'num20',
            'password': 'TFBOYS2023',
            'user_type': 'student'
        }
    }
    
    # 日志配置
    LOG_CONFIG = {
        'level': 'INFO',
        'format': '{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}',
        'rotation': '500 MB',
        'retention': '7 days'
    }
    
    # 报告配置
    REPORT_CONFIG = {
        'html_report': True,
        'allure_report': True,
        'screenshot_on_failure': True
    }
    
    def __init__(self):
        self.env = os.getenv('TEST_ENV', 'dev')
        self.current_config = self.ENVIRONMENTS.get(self.env, self.ENVIRONMENTS['dev'])
        
    @property
    def base_url(self) -> str:
        return self.current_config['base_url']
        
    @property
    def timeout(self) -> int:
        return self.current_config['timeout']
        
    @property
    def debug(self) -> bool:
        return self.current_config['debug']
        
    @property
    def test_users(self) -> Dict[str, Dict[str, str]]:
        return self.TEST_USERS
        
    @property
    def log_config(self) -> Dict[str, Any]:
        return self.LOG_CONFIG
        
    @property
    def report_config(self) -> Dict[str, Any]:
        return self.REPORT_CONFIG
