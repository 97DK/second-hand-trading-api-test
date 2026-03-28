import requests
import json

# 测试不同的提现场景
test_cases = [
    {"amount": ""},  # 金额为空
    {"amount": 0.001},  # 金额小于0.01
    {"amount": 100000},  # 金额大于余额
]

cookies = {
    'sessionid': '5oma73g0qxl2847bh0z3egg0ygld8hw1',
    'csrftoken': 'jSb0goY8QKJ7VMdIKPE0tPCHhrjnwQxf'
}

headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': 'z30MJnxmm7hChAngbUlQ1ZohdqSZrD2bIL1CPBlk2HQz2cqOLzPGkEQOkH1cNjpg'
}

for i, data in enumerate(test_cases):
    print(f"\n=== 测试用例 {i+1} ===")
    print(f"请求数据: {data}")
    
    response = requests.post(
        'http://localhost:8080/api/users/withdraw/',
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