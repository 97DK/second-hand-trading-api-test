#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试所有模块导入是否正常
"""

def test_all_imports():
    """测试所有关键模块的导入"""
    try:
        # 测试基础模块
        from config.settings import Config
        print("✓ Config 导入成功")
        
        from config.dynamic_vars import dynamic_vars
        print("✓ dynamic_vars 导入成功")
        
        from common.logger import Logger
        print("✓ Logger 导入成功")
        
        # 测试核心模块
        from core.send_request import SendRequest
        print("✓ SendRequest 导入成功")
        
        # 测试测试模块
        from testcase.base_test import BaseTest
        print("✓ BaseTest 导入成功")
        
        print("\n🎉 所有模块导入测试通过！")
        return True
        
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 其他错误: {e}")
        return False

if __name__ == "__main__":
    success = test_all_imports()
    exit(0 if success else 1)