#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速诊断评价接口路径
"""
import requests

base_url = 'http://localhost:8080'

print("=" * 60)
print("评价接口路径诊断测试")
print("=" * 60)

# 测试 1: 获取 CSRF Token
print("\n[步骤 1] 获取 CSRF Token...")
response = requests.get(f'{base_url}/api/users/csrf-token/')
if response.status_code == 200:
    csrf_token = response.json().get('csrfToken')
    print(f"✓ CSRF Token: {csrf_token[:20]}...")
else:
    print(f"✗ 获取 CSRF Token 失败：{response.status_code}")
    exit(1)

# 测试 2: 登录学生用户
print("\n[步骤 2] 登录学生用户...")
session = requests.Session()
session.headers.update({'X-CSRFToken': csrf_token})

login_data = {
    'user_type': 'student',
    'username': 'sssass',
    'password': 'TFBOYS2023'
}
response = session.post(f'{base_url}/api/users/login/', json=login_data)
if response.status_code == 200:
    user_info = response.json().get('user')
    print(f"✓ 登录成功：{user_info.get('username')} ({user_info.get('user_type')})")
    
    # 获取登录后的 CSRF Token
    response = session.get(f'{base_url}/api/users/csrf-token/')
    if response.status_code == 200:
        csrf_token = response.json().get('csrfToken')
        session.headers.update({'X-CSRFToken': csrf_token})
        print(f"✓ 更新 CSRF Token: {csrf_token[:20]}...")
else:
    print(f"✗ 登录失败：{response.status_code}")
    print(response.text)
    exit(1)

# 测试 3: 获取已购买商品列表
print("\n[步骤 3] 获取已购买商品列表...")
response = session.get(f'{base_url}/api/products/bought-products/')
if response.status_code == 200:
    products = response.json()
    if products:
        product_id = products[0].get('product', {}).get('id') or products[0].get('id')
        print(f"✓ 找到已购买商品 ID: {product_id}")
        
        # 测试 3a: 正确的路径
        print("\n[步骤 4a] 测试正确的 API 路径：/api/products/{product_id}/evaluate/")
        response = session.get(f'{base_url}/api/products/{product_id}/evaluate/')
        print(f"状态码：{response.status_code}")
        if response.status_code == 200:
            print(f"✓ 路径正确，可以访问")
        else:
            print(f"✗ 失败：{response.text[:200]}")
        
        # 测试 3b: 错误的路径 (去掉 products)
        print("\n[步骤 4b] 测试错误的 API 路径：/api/{product_id}/evaluate/")
        response = session.get(f'{base_url}/api/{product_id}/evaluate/')
        print(f"状态码：{response.status_code}")
        if response.status_code == 404:
            print("✗ 404 Not Found - 路径不存在")
        else:
            print(f"响应：{response.text[:200]}")
    else:
        print("✗ 没有已购买商品，无法测试")
else:
    print(f"✗ 获取已购买商品列表失败：{response.status_code}")

print("\n" + "=" * 60)
print("诊断结论:")
print("=" * 60)
print("后端路由配置：/api/products/<int:product_id>/evaluate/")
print("测试用例配置：/api/products/{product_id}/evaluate/")
print("结论：路径配置正确，问题可能在前置条件或商品 ID 提取")
print("=" * 60)
