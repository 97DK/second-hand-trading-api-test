"""
模拟测试框架执行 admin 测试
"""
import sys
sys.path.insert(0, '.')

from core.send_request import SendRequest
from config.settings import Config

# 创建请求处理器
request = SendRequest()

# 模拟第一个 admin 测试用例
case_data = {
    'api_name': '获取用户管理数据',
    'path': '/api/users/admin/users/',
    'method': 'GET',
    'content_type': 'application/json',
    'auth_required': True,
    'auth_type': 'admin',  # 使用 admin 账号
    'data': {}
}

print("=" * 80)
print("开始执行 admin 测试用例")
print("=" * 80)

# 发送请求
response = request.send(case_data)

print(f"\n响应状态码：{response.status_code}")
print(f"响应内容：{response.text[:300]}")

# 检查当前用户信息
config = Config()
current_user = request._current_user
if current_user:
    print(f"\n当前登录用户：{current_user.get('username')} (类型：{current_user.get('user_type')})")
else:
    print("\n当前未登录")

print("=" * 80)
