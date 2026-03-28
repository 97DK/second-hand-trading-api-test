# core/data_driver.py
import pytest
import allure
from typing import Dict, Any, List, Callable, Optional
from common.read_yaml import ReadYamlData
from common.logger import Logger


class DataDriver:
    """
    数据驱动核心类
    从data/模块名/*.yaml 读取测试数据
    """

    def __init__(self):
        self.yaml_reader = ReadYamlData()
        self.logger = Logger().get_logger()

    def parametrize(self, module: str, filename: str,
                    ids: Optional[Callable] = None,
                    filter_func: Optional[Callable] = None):
        """
        返回pytest参数化装饰器
        :param module: 模块名（user, product, admin等）
        :param filename: YAML文件名
        :param ids: 用例ID生成函数
        :param filter_func: 过滤函数
        """
        cases = self.yaml_reader.get_testcase_yaml(module, filename)

        # 应用过滤
        if filter_func:
            cases = [c for c in cases if filter_func(c)]

        # 生成用例ID
        if ids is None:
            case_ids = [f"{c.get('id', 'unknown')}_{c.get('name', '')[:20]}" for c in cases]
        else:
            case_ids = ids(cases) if callable(ids) else [str(i) for i in range(len(cases))]

        self.logger.info(f"参数化加载: {module}/{filename} -> {len(cases)} 个用例")

        return pytest.mark.parametrize(
            "case_data",
            cases,
            ids=case_ids
        )

    def parametrize_module(self, module: str):
        """
        加载模块下所有YAML文件
        :param module: 模块名
        """
        files = self.yaml_reader.get_all_module_files(module)
        all_cases = []

        for filename in files:
            cases = self.yaml_reader.get_testcase_yaml(module, filename)
            all_cases.extend(cases)

        return all_cases