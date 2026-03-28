"""
检查 num3 用户的已购买和已评价商品
"""
import requests

BASE_URL = "http://localhost:8080"

# 登录 num3
session = requests.Session()
response = session.get(f"{BASE_URL}/api/users/csrf-token/")
csrf_token = response.json().get('csrfToken')

login_data = {
    'user_type': 'student',
    'username': 'num3',
    'password': 'TFBOYS2023'
}

headers = {'X-CSRFToken': csrf_token, 'Content-Type': 'application/json'}

response = session.post(f"{BASE_URL}/api/users/login/", json=login_data, headers=headers)
print(f"登录状态：{response.status_code}")

if response.status_code == 200:
    # 获取已购买商品
    response = session.get(f"{BASE_URL}/api/products/bought-products/")
    print(f"\n已购买商品数量：{len(response.json())}")
    bought_ids = [p['id'] for p in response.json()]
    print(f"已购买商品 IDs: {bought_ids}")
    
    # 检查每个商品的评论状态
    print("\n=== 检查每个商品的评论状态 ===")
    evaluated_count = 0
    for product_id in bought_ids:
        response = session.get(f"{BASE_URL}/api/products/{product_id}/evaluate/")
        if response.status_code == 200 and len(response.json()) > 0:
            print(f"❌ 商品 {product_id}: 已评价")
            evaluated_count += 1
        else:
            print(f"✅ 商品 {product_id}: 未评价")
    
    print(f"\n总结：共 {len(bought_ids)} 个已购买商品，其中 {evaluated_count} 个已评价，{len(bought_ids)-evaluated_count} 个未评价")
else:
    print("登录失败")
