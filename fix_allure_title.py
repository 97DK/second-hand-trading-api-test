#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量移除所有测试文件中的 @allure.title 装饰器
"""

import os
import re

def remove_allure_title(file_path):
    """移除文件中的 allure.title 装饰器"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 直接移除包含 case_data 的 allure.title 行
    patterns = [
        r'^.*@allure\.title\(.*case_data.*\).*\r?\n',
        r'^.*@allure\.title\(.*case_data.*\).*\n'
    ]
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已处理：{file_path}")

def main():
    """主函数"""
    # 需要处理的文件列表
    files = [
        'testcase/test_base/test_base_api.py',
        'testcase/test_credit/test_credit_api.py',
        'testcase/test_evaluation/test_evaluation_api.py',
        'testcase/test_finance/test_finance_api.py',
        'testcase/test_product/test_product_api.py',
        'testcase/test_user/test_user_api.py'
    ]
    
    for file in files:
        if os.path.exists(file):
            remove_allure_title(file)
        else:
            print(f"文件不存在：{file}")
    
    print("\n批量处理完成！")

if __name__ == '__main__':
    main()
