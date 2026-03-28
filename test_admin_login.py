"""
测试 admin 账号登录
"""
import requests

BASE_URL = "http://localhost:8080"

# 获取 CSRF Token
session = requests.Session()
response = session.get(f"{BASE_URL}/api/users/csrf-token/")
csrf_token = response.json().get('csrfToken')
print(f"CSRF Token: {csrf_token[:10]}...")

# 登录 admin 账号
login_data = {
    'user_type': 'admin',
    'username': 'admin',
    'password': 'admin123'
}

headers = {
    'X-CSRFToken': csrf_token,
    'Content-Type': 'application/json'
}

response = session.post(
    f"{BASE_URL}/api/users/login/",
    json=login_data,
    headers=headers
)

print(f"Login Status Code: {response.status_code}")
print(f"Login Response: {response.json()}")

if response.status_code == 200:
    # 尝试访问 admin 接口
    response = session.get(f"{BASE_URL}/api/users/admin/users/")
    print(f"\nAdmin API Status Code: {response.status_code}")
    print(f"Admin API Response: {response.text[:200]}")
else:
    print("登录失败！")
