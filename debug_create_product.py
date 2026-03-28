import requests
import json

# 测试商品创建接口
url = 'http://localhost:8080/api/products/'

# 登录获取 session
login_data = {
    'username': 'sssass',
    'password': 'TFBOYS2023'
}

session = requests.Session()
login_response = session.post(
    'http://localhost:8080/api/users/login/',
    json=login_data
)

print(f"登录状态: {login_response.status_code}")
print(f"登录响应: {login_response.text}")

if login_response.status_code == 200:
    # 获取 CSRF token
    csrf_response = session.get('http://localhost:8080/api/users/csrf-token/')
    csrf_token = csrf_response.json()['csrfToken']
    print(f"CSRF Token: {csrf_token}")
    
    # 准备商品数据
    data = {
        'title': '测试商品',
        'description': '这是一个测试商品',
        'category': 'book',
        'condition': 'seven',
        'price': '10.00',
        'inventory': '5',
        'dormitory_building': '1号楼'
    }
    
    # 设置 headers
    headers = {
        'X-CSRFToken': csrf_token
    }
    
    # 发送创建商品请求
    response = session.post(url, data=data, headers=headers)
    
    print(f"\n创建商品状态码: {response.status_code}")
    print(f"创建商品响应: {response.text}")
    
    try:
        resp_json = response.json()
        print(f"JSON解析: {json.dumps(resp_json, ensure_ascii=False, indent=2)}")
    except:
        print("无法解析为JSON")
else:
    print("登录失败，无法继续测试")