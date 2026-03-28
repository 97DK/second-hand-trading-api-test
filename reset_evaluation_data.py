# 重置评价测试数据脚本
"""
用于清空已评价商品 ID 记录，让测试重新获取未评价商品
"""

import sys
sys.path.insert(0, '.')

from config.dynamic_vars import dynamic_vars

print("=" * 60)
print("重置评价测试数据")
print("=" * 60)

# 查看当前状态
evaluated_ids = dynamic_vars.get_var('evaluated_product_ids', [])
print(f"\n当前已评价商品 IDs: {evaluated_ids}")

bought_ids = dynamic_vars.get_var('bought_product_ids', [])
print(f"当前已购买商品 IDs: {bought_ids}")

first_bought_id = dynamic_vars.get_var('first_bought_product_id')
print(f"当前使用的商品 ID: {first_bought_id}")

# 清空已评价商品记录
print("\n" + "=" * 60)
print("执行清空操作...")
print("=" * 60)

dynamic_vars.set_var('evaluated_product_ids', [])
print("✓ 已清空 evaluated_product_ids")

# 可选：清空其他相关变量
# dynamic_vars.set_var('bought_product_ids', [])
# dynamic_vars.set_var('first_bought_product_id', None)

print("\n" + "=" * 60)
print("重置完成！现在可以重新运行测试了")
print("=" * 60)
print("\n运行命令:")
print("python -m pytest testcase/test_evaluation/test_evaluation_api.py -v")
