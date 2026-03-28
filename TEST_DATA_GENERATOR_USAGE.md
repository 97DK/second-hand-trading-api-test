# 测试数据生成器使用说明

## 功能概述

测试数据生成器用于在运行注册测试时自动生成递增的学号和用户名，避免数据重复冲突。

## 配置说明

### 起始值配置
- **学号**: 从 `20221080201` 开始，每次自动 +1
- **用户名**: 从 `num30` 开始，每次自动 +1（num31, num32, num33...）

### 配置文件
配置文件保存在：`apiautotest/test_data_config.json`

每次运行测试后会自动保存当前进度，下次运行时继续使用下一个号码。

## 使用方法

### 1. 查看当前状态
```bash
cd C:\Users\PC\PycharmProjects\pythonProject6\apiautotest
python check_test_data_status.py
```

示例输出：
```
============================================================
测试数据生成器当前状态
============================================================

📊 统计信息:
  当前学号：20221080204
  当前用户名：num33

📈 已生成数量:
  学号：3 个
  用户名：4 个

💡 下次运行将使用:
  学号：20221080204
  用户名：num33

============================================================
```

### 2. 重置为初始值
```bash
python reset_test_data.py
```

系统会提示确认是否重置，输入 `y` 确认后，学号和用户名将恢复到初始值。

### 3. 运行测试
正常运行测试即可，系统会自动使用下一个可用的学号和用户名：

```bash
# 运行所有注册测试
python -m pytest testcase/test_user/test_user_api.py::TestUserAPI::test_register -v

# 或者运行特定的测试
python run.py --module user --tag smoke
```

## 工作流程

1. **测试开始前**: 从配置文件读取当前学号和用户名
2. **每个测试用例**: 
   - 如果测试用例需要学号和用户名（非空），则自动生成新的
   - 学号和用户名各增加 1
   - 立即保存到配置文件
3. **测试结束后**: 配置文件保留最新状态

## 日志示例

```
2026-03-02 21:37:04 | INFO | config.test_data_generator:get_next_student_id:63 | 生成学号：20221080201 -> 下一个：20221080202
2026-03-02 21:37:04 | INFO | config.test_data_generator:get_next_username:74 | 生成用户名：num30 -> 下一个：num31
2026-03-02 21:37:04 | INFO | testcase.test_user.test_user_api:test_register:97 | 使用动态生成的数据 - 学号：20221080201, 用户名：num30
```

## 注意事项

1. **持久化存储**: 配置保存在 JSON 文件中，即使关闭终端或重启电脑，数据也不会丢失
2. **自动递增**: 每次运行测试都会自动使用新的学号和用户名
3. **重置功能**: 如果需要重新测试，可以使用 `reset_test_data.py` 重置
4. **适用范围**: 目前仅对 `register.yaml` 中的注册测试生效

## 文件清单

- `config/test_data_generator.py` - 数据生成器核心代码
- `check_test_data_status.py` - 查看当前状态工具
- `reset_test_data.py` - 重置配置工具
- `test_data_config.json` - 配置文件（自动生成）
