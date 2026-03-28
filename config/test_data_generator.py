# config/test_data_generator.py
"""测试数据生成器 - 用于生成递增的学号和用户名"""

import os
import json
from pathlib import Path
from common.logger import Logger


class TestDataGenerator:
    """测试数据生成器类"""
    
    def __init__(self):
        self.logger = Logger().get_logger()
        # 配置文件路径
        self.config_file = Path(__file__).parent.parent / 'test_data_config.json'
        # 默认配置
        self.default_config = {
            'student_id_start': 20221080201,  # 学号起始值
            'student_id_current': 20221080201,  # 当前学号
            'username_start': 'num30',  # 用户名起始值
            'username_current': 'num30',  # 当前用户名
            'username_counter': 30  # 用户名计数器
        }
        # 加载或初始化配置
        self.config = self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.logger.info(f"从 {self.config_file} 加载配置")
                    # 确保所有键都存在
                    for key, value in self.default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                self.logger.error(f"加载配置文件失败：{e}，使用默认配置")
                return self.default_config.copy()
        else:
            self.logger.info(f"配置文件不存在，使用默认配置")
            return self.default_config.copy()
    
    def _save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            self.logger.info(f"配置已保存到 {self.config_file}")
        except Exception as e:
            self.logger.error(f"保存配置文件失败：{e}")
    
    def get_next_student_id(self):
        """获取下一个学号"""
        current = self.config['student_id_current']
        # 更新为下一个值
        self.config['student_id_current'] = current + 1
        # 保存配置
        self._save_config()
        self.logger.info(f"生成学号：{current} -> 下一个：{current + 1}")
        return str(current)
    
    def get_next_username(self):
        """获取下一个用户名"""
        current = self.config['username_current']
        # 更新为下一个值
        self.config['username_counter'] += 1
        self.config['username_current'] = f"num{self.config['username_counter']}"
        # 保存配置
        self._save_config()
        self.logger.info(f"生成用户名：{current} -> 下一个：{self.config['username_current']}")
        return current
    
    def reset_config(self):
        """重置配置到初始值"""
        self.config = self.default_config.copy()
        self._save_config()
        self.logger.info("配置已重置为初始值")
    
    def get_current_status(self):
        """获取当前状态"""
        return {
            'current_student_id': self.config['student_id_current'],
            'current_username': self.config['username_current'],
            'total_generated': {
                'student_ids': self.config['student_id_current'] - self.config['student_id_start'],
                'usernames': self.config['username_counter'] - self.default_config['username_counter'] + 1
            }
        }


# 全局单例
test_data_generator = TestDataGenerator()
