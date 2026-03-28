# common/read_yaml.py
import yaml
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from functools import lru_cache
from .logger import Logger


class ReadYamlData:
    """
    读取YAML测试数据文件
    data/目录下直接存放各模块的YAML文件
    """

    _instance = None
    _logger = Logger().get_logger()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_testcase_yaml(self, module: str, filename: str) -> List[Dict[str, Any]]:
        """
        获取测试用例数据
        :param module: 模块名(user, product, admin等)
        :param filename: YAML文件名
        :return: 测试用例列表
        """
        base_dir = Path(__file__).parent.parent
        file_path = base_dir / "data" / module / filename

        if not file_path.exists():
            self._logger.error(f"YAML文件不存在: {file_path}")
            return []

        test_data = self._read_yaml(file_path)
        processed_cases = self._process_yaml_data(test_data, module, filename)

        self._logger.info(f"从 {module}/{filename} 加载了 {len(processed_cases)} 个测试用例")
        return processed_cases

    @lru_cache(maxsize=128)
    def _read_yaml(self, file_path: Path) -> Dict[str, Any]:
        """读取YAML文件(带缓存)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data or {}
        except Exception as e:
            self._logger.error(f"读取YAML文件失败 {file_path}: {str(e)}")
            return {}

    def _process_yaml_data(self, data: Dict, module: str, filename: str) -> List[Dict]:
        """处理YAML数据"""
        api_info = {
            'api_name': data.get('api_name', ''),
            'path': data.get('path', ''),
            'method': data.get('method', 'GET'),
            'content_type': data.get('content_type', 'application/json'),
            'auth_required': data.get('auth_required', True),
            'auth_type': data.get('auth_type'),
            'headers': data.get('headers', {}),
            'module': module,
            'source_file': filename
        }

        cases = []
        for case in data.get('test_cases', []):
            case_data = {
                **api_info,
                'id': case.get('id'),
                'name': case.get('name'),
                'description': case.get('description', ''),
                'data': case.get('data', {}),
                'path_params': case.get('path_params', {}),
                'query_params': case.get('query_params', {}),
                'files': case.get('files', {}),
                'expected': case.get('expected', {}),
                'setup': case.get('setup', []),
                'teardown': case.get('teardown', []),
                'tags': case.get('tags', []),
            }
            cases.append(case_data)

        return cases

    def get_all_module_files(self, module: str) -> List[str]:
        """获取模块下所有YAML文件"""
        base_dir = Path(__file__).parent.parent / "data" / module
        if not base_dir.exists():
            return []

        return [f.name for f in base_dir.glob("*.yaml")]