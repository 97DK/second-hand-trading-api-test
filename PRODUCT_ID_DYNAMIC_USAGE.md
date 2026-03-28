# 商品ID动态获取使用说明

## 1. 路径参数处理机制

在测试框架中，路径参数 `{product_id}` 的处理流程如下：

1. **变量定义**：在YAML测试用例中使用 `${变量名}` 格式
2. **前置步骤执行**：通过 `setup` 字段指定需要执行的前置操作
3. **变量解析**：框架自动将变量替换为实际值
4. **路径构建**：使用替换后的值构造完整URL

## 2. 可用的前置步骤

### 2.1 获取商品列表（带查询参数）
```yaml
setup:
  - "获取商品列表"  # 默认获取第1页，每页4条记录
```
- 接口地址：`/api/products/?page=1&page_size=4`
- 提供的变量：
  - `${first_product_id}` - 第一个商品的ID
  - `${product_ids}` - 所有商品ID的数组

### 2.2 获取全部商品列表（无查询参数）
```yaml
setup:
  - "获取全部商品列表"  # 获取所有商品
```
- 接口地址：`/api/products/`（无查询参数）
- 提供的变量：
  - `${first_all_product_id}` - 第一个商品的ID
  - `${all_product_ids}` - 所有商品ID的数组

## 3. 变量使用示例

### 3.1 基本使用
```yaml
test_cases:
  - id: TC-001
    name: 动态商品ID购买
    setup:
      - "获取商品列表"
    path_params:
      product_id: "${first_product_id}"  # 使用第一个商品ID
    data:
      quantity: 1
```

### 3.2 数组元素使用
```yaml
test_cases:
  - id: TC-002
    name: 使用特定位置的商品ID
    setup:
      - "获取商品列表"
    path_params:
      product_id: "${product_ids[0]}"  # 使用数组第一个元素
    data:
      quantity: 1
```

### 3.3 获取全部商品
```yaml
test_cases:
  - id: TC-003
    name: 获取全部商品进行测试
    setup:
      - "获取全部商品列表"
    path_params:
      product_id: "${first_all_product_id}"
    data:
      quantity: 1
```

## 4. 关于查询参数的影响

### 4.1 带查询参数的情况
当使用 `/api/products/?page=1&page_size=4` 时：
- 只返回指定页码和数量的商品
- 适用于只需要少量商品进行测试的场景
- 响应更快，数据量小

### 4.2 无查询参数的情况
当使用 `/api/products/` 时：
- 返回所有可用的商品（受权限限制）
- 获取完整的商品列表
- 适用于需要全面测试的场景
- 响应时间可能较长

## 5. 实际响应数据处理

根据你提供的响应示例：
```json
[
  {
    "id": 11,
    "title": "这个",
    "description": "as",
    "price": "199.00",
    "category": "book",
    "condition": "new",
    "status": "on_sale",
    "inventory": 1,
    "seller": 2
  },
  // ... 更多商品
]
```

框架会自动提取：
- `first_product_id = 11` （第一个商品的ID）
- `product_ids = [11, 12, 14, 19]` （所有商品ID数组）

## 6. 完整测试用例示例

```yaml
# data/product/purchase_dynamic.yaml
api_name: 购买商品-动态ID
path: /api/products/{product_id}/purchase/
method: POST
content_type: application/json
auth_required: true
auth_type: student

test_cases:
  - id: TC-DYNAMIC-001
    name: 动态获取商品ID购买测试
    description: 使用动态获取的商品ID进行购买
    tags: [dynamic, purchase, smoke]
    setup:
      - "获取商品列表"  # 前置步骤：获取商品列表
    path_params:
      product_id: "${first_product_id}"  # 动态替换为实际商品ID
    data:
      quantity: 1
    expected:
      status_code: 200
      success: true
      message: "购买成功"
      
  - id: TC-DYNAMIC-002
    name: 批量商品测试
    description: 使用不同位置的商品进行测试
    tags: [dynamic, batch, regression]
    setup:
      - "获取商品列表"
    path_params:
      product_id: "${product_ids[2]}"  # 使用第三个商品
    data:
      quantity: 1
    expected:
      status_code: 200
```

## 7. 注意事项

1. **前置步骤必须执行**：使用动态变量前必须先执行对应的前置步骤
2. **变量作用域**：变量在整个测试会话中有效
3. **错误处理**：如果前置步骤失败，后续使用该变量的测试会标记为警告
4. **性能考虑**：获取全部商品可能影响性能，建议根据实际需求选择合适的获取方式

## 8. 调试技巧

可以通过查看日志确认变量是否正确解析：
```
INFO: 变量 first_product_id 已解析为: 11
INFO: 提取到商品IDs: [11, 12, 14, 19]
INFO: 第一个商品ID: 11
```