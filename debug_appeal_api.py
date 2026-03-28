"""
调试申诉管理接口的 500 错误
"""
import requests

BASE_URL = "http://localhost:8080"

# 登录管理员账号
session = requests.Session()

# 1. 先获取 CSRF Token
print("=" * 60)
print("步骤 1: 获取 CSRF Token")
print("=" * 60)
response = session.get(f"{BASE_URL}/api/users/login/")
csrf_token = response.cookies.get('csrftoken')
print(f"CSRF Token: {csrf_token}")

# 2. 登录管理员
print("\n" + "=" * 60)
print("步骤 2: 登录管理员账号")
print("=" * 60)
login_data = {
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
print(f"登录状态码：{response.status_code}")
print(f"登录响应：{response.text[:200]}")

if response.status_code == 200:
    user_info = response.json()
    print(f"登录用户：{user_info.get('username')} (类型：{user_info.get('user_type')})")
    
    # 3. 获取待申诉列表
    print("\n" + "=" * 60)
    print("步骤 3: 获取待申诉列表")
    print("=" * 60)
    response = session.get(f"{BASE_URL}/api/products/admin/appeals/")
    print(f"状态码：{response.status_code}")
    appeals = response.json()
    print(f"申诉数量：{len(appeals)}")
    
    if len(appeals) > 0:
        first_appeal_id = appeals[0]['id']
        print(f"第一个申诉 ID: {first_appeal_id}")
        
        # 4. 尝试通过申诉
        print("\n" + "=" * 60)
        print("步骤 4: 尝试通过申诉")
        print("=" * 60)
        approve_data = {
            'evaluation_id': first_appeal_id,
            'action': 'approve',
            'response_content': '申诉通过，维持原评价'
        }
        print(f"请求数据：{approve_data}")
        
        try:
            response = session.post(
                f"{BASE_URL}/api/products/admin/appeals/",
                json=approve_data,
                headers=headers
            )
            print(f"状态码：{response.status_code}")
            print(f"响应内容类型：{response.headers.get('content-type')}")
            
            if response.status_code == 200:
                print(f"响应：{response.json()}")
            else:
                # 输出错误详情
                print(f"\n错误详情:")
                print(f"响应前 500 字符：{response.text[:500]}")
                
        except Exception as e:
            print(f"请求异常：{e}")
    else:
        print("⚠️ 没有待申诉记录，尝试手动创建一个")
        
        # 尝试发送一个空请求看错误
        print("\n" + "=" * 60)
        print("步骤 5: 发送测试请求（带无效 ID）")
        print("=" * 60)
        test_data = {
            'evaluation_id': 99999,
            'action': 'approve',
            'response_content': '测试'
        }
        print(f"请求数据：{test_data}")
        
        try:
            response = session.post(
                f"{BASE_URL}/api/products/admin/appeals/",
                json=test_data,
                headers=headers
            )
            print(f"状态码：{response.status_code}")
            print(f"响应内容类型：{response.headers.get('content-type')}")
            print(f"响应前 500 字符：{response.text[:500]}")
        except Exception as e:
            print(f"请求异常：{e}")
else:
    print("登录失败，无法继续测试")
