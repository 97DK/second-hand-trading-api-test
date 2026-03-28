#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速诊断脚本 - 测试 admin 接口
"""
import requests

base_url = 'http://localhost:8080'

print("=" * 60)
print("Admin 接口诊断测试")
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

# 测试 2: 登录 admin 用户
print("\n[步骤 2] 登录 admin 用户...")
session = requests.Session()
session.headers.update({'X-CSRFToken': csrf_token})

login_data = {
    'user_type': 'admin',
    'username': 'admin',
    'password': 'admin123'
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

# 测试 3: 尝试访问 admin 接口 (正确的路径)
print("\n[步骤 3] 测试正确的 API 路径：/api/users/admin/users/")
response = session.get(f'{base_url}/api/users/admin/users/')
print(f"状态码：{response.status_code}")
if response.status_code == 200:
    users = response.json()
    print(f"✓ 成功获取用户列表，共 {len(users)} 个用户")
    if users:
        print(f"第一个用户：{users[0].get('username')}")
else:
    print(f"✗ 失败：{response.text[:200]}")

# 测试 4: 尝试访问 admin 接口 (测试用例的错误路径)
print("\n[步骤 4] 测试错误的 API 路径：/users/admin/users/")
response = session.get(f'{base_url}/users/admin/users/')
print(f"状态码：{response.status_code}")
if response.status_code == 404:
    print("✗ 404 Not Found - 路径不存在")
else:
    print(f"响应：{response.text[:200]}")

print("\n" + "=" * 60)
print("诊断结论:")
print("=" * 60)
print("后端路由配置：/api/users/admin/users/")
print("测试用例配置：/users/admin/users/")
print("问题：测试用例缺少 '/api' 前缀")
print("=" * 60)
