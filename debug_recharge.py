import requests
import json

# 测试不同的充值场景
test_cases = [
    {"amount": "abc"},  # 非数字金额
    {"amount": 0.001},  # 金额小于0.01
    {"amount": 10000},  # 金额大于9999
    {},  # 金额为空
]

cookies = {
    'sessionid': 'afvnyrurxr3v8vxvfasgrlecsuydpret',
    'csrftoken': '1JVWBvi7RHvTBD6GKUPe34lfBnSBpS9y'
}

headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': 'C7XW9oWzC7VdSaxeCpJteuaPP2aw2i7UtGIIAJ4wjEgWjDtKc9ox7olUgfSXh06i'
}

for i, data in enumerate(test_cases):
    print(f"\n=== 测试用例 {i+1} ===")
    print(f"请求数据: {data}")
    
    response = requests.post(
        'http://localhost:8080/api/users/recharge/',
        json=data,
        cookies=cookies,
        headers=headers
    )
    
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    try:
        resp_json = response.json()
        print(f"JSON解析: {json.dumps(resp_json, ensure_ascii=False, indent=2)}")
    except:
        print("无法解析为JSON")