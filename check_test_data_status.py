# check_test_data_status.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""查看测试数据生成器当前状态"""

from config.test_data_generator import test_data_generator

if __name__ == '__main__':
    print("=" * 60)
    print("测试数据生成器当前状态")
    print("=" * 60)
    
    status = test_data_generator.get_current_status()
    
    print(f"\n📊 统计信息:")
    print(f"  当前学号：{status['current_student_id']}")
    print(f"  当前用户名：{status['current_username']}")
    print(f"\n📈 已生成数量:")
    print(f"  学号：{status['total_generated']['student_ids']} 个")
    print(f"  用户名：{status['total_generated']['usernames']} 个")
    
    print(f"\n💡 下次运行将使用:")
    print(f"  学号：{status['current_student_id']}")
    print(f"  用户名：{status['current_username']}")
    
    print("\n" + "=" * 60)
