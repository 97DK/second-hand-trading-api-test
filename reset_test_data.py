# reset_test_data.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""重置测试数据生成器配置"""

from config.test_data_generator import test_data_generator

if __name__ == '__main__':
    print("=" * 60)
    print("重置测试数据生成器配置")
    print("=" * 60)
    
    # 显示当前状态
    status = test_data_generator.get_current_status()
    print(f"\n当前状态:")
    print(f"  当前学号：{status['current_student_id']}")
    print(f"  当前用户名：{status['current_username']}")
    print(f"  已生成学号数量：{status['total_generated']['student_ids']}")
    print(f"  已生成用户名数量：{status['total_generated']['usernames']}")
    
    # 确认重置
    choice = input("\n是否重置为初始值？(y/n): ").strip().lower()
    if choice == 'y':
        test_data_generator.reset_config()
        print("\n✓ 配置已重置为初始值")
        print(f"  起始学号：20221080201")
        print(f"  起始用户名：num30")
    else:
        print("\n✗ 取消重置操作")
    
    print("=" * 60)
