"""诊断已购买商品列表接口"""
import sys
sys.path.insert(0, '.')

from core.send_request import SendRequest
from config.settings import Config

def diagnose_bought_products():
    """诊断已购买商品接口"""
    request = SendRequest()
    
    # 使用 student 用户登录
    config = Config()
    user = config.test_users.get('student', {})
    
    print("=" * 80)
    print("步骤 1: 用户登录")
    print("=" * 80)
    login_success = request.login(
        user.get('user_type', 'student'),
        user.get('username'),
        user.get('password')
    )
    
    if not login_success:
        print("❌ 登录失败")
        return
    
    print(f"✅ 登录成功：{user.get('username')}")
    print(f"当前用户信息：{request._current_user}")
    
    print("\n" + "=" * 80)
    print("步骤 2: 获取已购买商品列表")
    print("=" * 80)
    
    request_data = {
        'method': 'GET',
        'path': '/api/products/bought-products/',
        'auth_required': True,
        'auth_type': 'student'
    }
    
    response = request.send(request_data)
    
    print(f"状态码：{response.status_code}")
    
    if response.status_code == 200:
        products = response.json()
        print(f"✅ 获取成功，共 {len(products)} 个已购买商品")
        
        if products:
            print("\n商品详情:")
            for i, product in enumerate(products[:5], 1):  # 只显示前 5 个
                print(f"\n{i}. 商品 ID: {product.get('id')}")
                print(f"   商品名称：{product.get('name', 'N/A')}")
                print(f"   购买者 ID: {product.get('buyer', 'N/A')}")
                print(f"   卖家 ID: {product.get('seller', 'N/A')}")
                print(f"   价格：{product.get('price', 'N/A')}")
            
            if len(products) > 5:
                print(f"\n... 还有 {len(products) - 5} 个商品")
        else:
            print("⚠️ 没有已购买商品")
    else:
        print(f"❌ 获取失败：{response.text}")
    
    print("\n" + "=" * 80)
    print("步骤 3: 验证商品 19 的购买关系")
    print("=" * 80)
    
    # 检查商品 19
    product_id = 19
    check_request = {
        'method': 'GET',
        'path': f'/api/products/{product_id}/evaluate/',
        'auth_required': True,
        'auth_type': 'student'
    }
    
    check_response = request.send(check_request)
    print(f"检查商品 {product_id} 的评价状态:")
    print(f"状态码：{check_response.status_code}")
    print(f"响应内容：{check_response.text}")
    
    if check_response.status_code == 200 and check_response.json():
        print(f"✅ 商品 {product_id} 未评价，可以提交评价")
    elif check_response.status_code == 404:
        print(f"❌ 商品 {product_id} 不存在或当前用户不是购买者")
    else:
        print(f"⚠️ 商品 {product_id} 已评价或其他状态")
    
    print("\n" + "=" * 80)
    print("诊断结论")
    print("=" * 80)
    
    if products:
        print("\n完整商品数据结构示例:")
        import json
        print(json.dumps(products[0], indent=2, ensure_ascii=False))
        
        # 检查是否有 buyer 字段或其他标识购买者的字段
        first_product = products[0]
        print(f"\n可用字段：{list(first_product.keys())}")
        
        # 尝试从不同角度验证购买关系
        print("\n尝试验证购买关系:")
        print(f"当前登录用户 ID: {request._current_user.get('id')}")
        print(f"当前登录用户名：{request._current_user.get('username')}")
        
        # 方法 1: 如果有 seller 字段，可以反向验证
        if 'seller' in first_product:
            seller_id = first_product['seller']
            print(f"商品卖家 ID: {seller_id}")
            if seller_id != request._current_user.get('id'):
                print("✅ 确认：当前用户不是卖家，说明是买家（因为是从 bought-products 接口返回的）")
            else:
                print("❌ 当前用户是卖家，这不是购买记录")
        else:
            print("⚠️ 没有 seller 字段，无法直接验证")
        
        # 方法 2: 通过评价接口反向验证
        print("\n通过评价接口验证:")
        for i, product in enumerate(products[:3], 1):
            pid = product.get('id')
            check_req = {
                'method': 'GET',
                'path': f'/api/products/{pid}/evaluate/',
                'auth_required': True,
                'auth_type': 'student'
            }
            check_resp = request.send(check_req)
            if check_resp.status_code == 200 and check_resp.json():
                print(f"  商品 {pid}: ✅ 可以评价（是购买者）")
            elif check_resp.status_code == 404:
                print(f"  商品 {pid}: ❌ 不能评价（不是购买者或商品不存在）")
            else:
                print(f"  商品 {pid}: ⚠️ 已评价或其他状态")
    else:
        print("⚠️ 没有已购买商品，无法验证")

if __name__ == '__main__':
    diagnose_bought_products()
