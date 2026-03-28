# common/read_excel.py
import pandas as pd
import os
import ast
from typing import List, Dict, Any
from pathlib import Path
from .logger import Logger


class ReadExcel:
    """
    读取Excel测试用例文件
    将Excel中的测试用例转换为标准格式
    """

    def __init__(self):
        self.logger = Logger().get_logger()
        self.base_dir = Path(__file__).parent.parent
        self.excel_path = self.base_dir / "data" / "接口测试用例.xlsx"

    def read_all_cases(self) -> List[Dict[str, Any]]:
        """
        读取所有测试用例
        :return: 测试用例列表
        """
        try:
            df = pd.read_excel(self.excel_path, sheet_name=0)
            self.logger.info(f"成功读取Excel文件，共 {len(df)} 行数据")

            cases = []
            for _, row in df.iterrows():
                case = self._convert_row_to_case(row)
                if case:
                    cases.append(case)

            return cases
        except Exception as e:
            self.logger.error(f"读取Excel文件失败: {str(e)}")
            return []

    def read_cases_by_module(self, module: str) -> List[Dict[str, Any]]:
        """
        按模块读取测试用例
        :param module: 模块名（如：用户认证、商品管理）
        :return: 测试用例列表
        """
        all_cases = self.read_all_cases()
        return [case for case in all_cases if case.get('module') == module]

    def read_case_by_id(self, case_id: str) -> Dict[str, Any]:
        """
        根据用例ID读取测试用例
        :param case_id: 用例编号（如：TC-AUTH-001）
        :return: 测试用例
        """
        all_cases = self.read_all_cases()
        for case in all_cases:
            if case.get('id') == case_id:
                return case
        return {}

    def _convert_row_to_case(self, row) -> Dict[str, Any]:
        """
        将Excel行转换为测试用例字典
        """
        try:
            # 解析请求参数
            request_params = row.get('请求参数', '')
            if pd.isna(request_params) or request_params == '无':
                request_data = {}
            else:
                request_data = self._parse_request_params(str(request_params))

            # 构建测试用例
            case = {
                'id': str(row.get('用例编号', '')),
                'name': str(row.get('测试场景', '')),
                'module': str(row.get('模块', '')),
                'api_name': str(row.get('接口名称', '')),
                'path': str(row.get('接口路径', '')),
                'method': str(row.get('请求方法', 'GET')).upper(),
                'data': request_data,
                'expected': {
                    'status_code': int(row.get('预期状态码', 200)),
                    'message': str(row.get('预期响应', ''))
                },
                'tags': self._generate_tags(row)
            }

            return case
        except Exception as e:
            self.logger.error(f"转换行数据失败: {str(e)}")
            return None

    def _parse_request_params(self, params_str: str) -> Dict[str, Any]:
        """
        解析请求参数
        处理格式：{"key":"value"} 或 key=value,key2=value2
        """
        params_str = params_str.strip()

        # 如果是JSON格式
        if params_str.startswith('{') and params_str.endswith('}'):
            try:
                return ast.literal_eval(params_str)
            except:
                try:
                    import json
                    return json.loads(params_str)
                except:
                    pass

        # 如果是key=value格式
        if '=' in params_str and ',' in params_str:
            result = {}
            pairs = params_str.split(',')
            for pair in pairs:
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    result[key.strip()] = self._parse_value(value.strip())
            return result

        return {}

    def _parse_value(self, value: str):
        """解析参数值"""
        if value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except:
            return value

    def _generate_tags(self, row) -> List[str]:
        """生成标签"""
        tags = []

        # 根据用例编号判断优先级
        case_id = str(row.get('用例编号', ''))
        if 'BASE' in case_id:
            tags.extend(['基础接口', 'p0'])
        elif 'AUTH' in case_id:
            tags.extend(['用户认证', 'p0'])
        elif 'PROD' in case_id:
            tags.extend(['商品管理', 'p0'])
        elif 'ADMIN' in case_id:
            tags.extend(['管理员', 'p0'])

        # 根据测试场景判断类型
        scene = str(row.get('测试场景', ''))
        if '成功' in scene or '正常' in scene:
            tags.append('smoke')
        elif '空' in scene or '缺失' in scene:
            tags.append('参数异常')
        elif '不存在' in scene or '错误' in scene:
            tags.append('业务异常')