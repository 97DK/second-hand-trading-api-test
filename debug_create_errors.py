import requests
import json

# 测试商品创建的各种异常情况
session = requests.Session()

# 登录
login_data = {
    'username': 'sssass',
    'password': 'TFBOYS2023'
}

login_response = session.post(
    'http://localhost:8080/api/users/login/',
    json=login_data
)

if login_response.status_code == 200:
    # 获取 CSRF token
    csrf_response = session.get('http://localhost:8080/api/users/csrf-token/')
    csrf_token = csrf_response.json()['csrfToken']
    
    headers = {
        'X-CSRFToken': csrf_token
    }
    
    # 测试各种异常情况
    test_cases = [
        {
            'name': '标题为空',
            'data': {
                'title': '',
                'description': '测试描述',
                'category': 'book',
                'condition': 'seven',
                'price': '10.00',
                'inventory': '5',
                'dormitory_building': '1号楼'
            }
        },
        {
            'name': '价格为空',
            'data': {
                'title': '测试商品',
                'description': '测试描述',
                'category': 'book',
                'condition': 'seven',
                'price': '',
                'inventory': '5',
                'dormitory_building': '1号楼'
            }
        },
        {
            'name': '库存为空',
            'data': {
                'title': '测试商品',
                'description': '测试描述',
                'category': 'book',
                'condition': 'seven',
                'price': '10.00',
                'inventory': '',
                'dormitory_building': '1号楼'
            }
        }
    ]
    
    for case in test_cases:
        print(f"\n=== 测试用例: {case['name']} ===")
        response = session.post(
            'http://localhost:8080/api/products/',
            data=case['data'],
            headers=headers
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        try:
            resp_json = response.json()
            print(f"JSON解析: {json.dumps(resp_json, ensure_ascii=False, indent=2)}")
        except:
            print("无法解析为JSON")
else:
    print("登录失败")