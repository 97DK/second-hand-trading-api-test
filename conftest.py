# conftest.py
"""
pytest配置文件
定义全局fixture和钩子函数
"""

import pytest
import os
from config.settings import Config


def pytest_configure(config):
    """pytest配置初始化"""
    # 设置环境变量
    env = os.getenv('TEST_ENV', 'dev')
    os.environ['TEST_ENV'] = env
    
    # 注册markers
    config.addinivalue_line(
        "markers", "smoke: 冒烟测试用例"
    )
    config.addinivalue_line(
        "markers", "regression: 回归测试用例"
    )
    config.addinivalue_line(
        "markers", "p0: P0级别用例（核心功能）"
    )
    config.addinivalue_line(
        "markers", "p1: P1级别用例（重要功能）"
    )
    config.addinivalue_line(
        "markers", "p2: P2级别用例（一般功能）"
    )


def pytest_collection_modifyitems(config, items):
    """测试用例收集后修改"""
    # 根据环境过滤用例
    env = os.getenv('TEST_ENV', 'dev')
    if env == 'prod':
        # 生产环境只运行P0用例
        skip_marker = pytest.mark.skip(reason="非生产环境用例")
        for item in items:
            if 'p0' not in item.keywords:
                item.add_marker(skip_marker)


@pytest.fixture(scope="session")
def test_config():
    """测试配置fixture"""
    return Config()


@pytest.fixture(scope="function", autouse=True)
def setup_test_environment():
    """每个测试函数前自动执行的setup"""
    # 可以在这里添加全局的测试环境准备逻辑
    pass


@pytest.fixture(scope="function")
def login_student():
    """学生用户登录fixture"""
    # 这里可以返回预定义的学生用户信息
    # 或者返回None，让测试自行处理登录
    return {
        'username': 'sssass',
        'password': 'TFBOYS2023',
        'user_type': 'student'
    }


@pytest.fixture(scope="function")
def login_admin():
    """管理员用户登录fixture"""
    return {
        'username': 'admin',
        'password': 'admin123',
        'user_type': 'admin'
    }


@pytest.fixture(scope="function")
def clean_test_data():
    """清理测试数据fixture"""
    # 可以在这里添加测试数据清理逻辑
    yield
    # 清理后置操作
