# utils/excel_to_yaml.py
"""
Excel测试用例转换为YAML格式工具
将Excel中的测试用例批量转换为YAML文件
"""

import pandas as pd
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any
from common.logger import Logger


class ExcelToYamlConverter:
    """Excel转YAML转换器"""
    
    def __init__(self):
        self.logger = Logger().get_logger()
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        
    def convert_excel_to_yaml(self, excel_path: str, output_module: str = None):
        """
        转换Excel文件为YAML
        :param excel_path: Excel文件路径
        :param output_module: 输出模块名，如果为None则按模块列分组
        """
        try:
            # 读取Excel文件
            df = pd.read_excel(excel_path)
            self.logger.info(f"读取Excel文件成功，共 {len(df)} 行数据")
            
            # 按模块分组
            if output_module:
                grouped = {output_module: df}
            else:
                grouped = df.groupby('模块')
            
            # 转换每个模块
            for module_name, group_df in grouped:
                self._convert_module(group_df, str(module_name))
                
        except Exception as e:
            self.logger.error(f"转换失败: {str(e)}")
            raise
    
    def _convert_module(self, df: pd.DataFrame, module_name: str):
        """转换单个模块的数据"""
        # 创建模块目录
        module_dir = self.data_dir / module_name
        module_dir.mkdir(exist_ok=True)
        
        # 按接口分组
        api_groups = df.groupby(['接口名称', '接口路径', '请求方法'])
        
        for (api_name, path, method), group in api_groups:
            # 清理文件名
            filename = f"{api_name.replace('/', '_')}.yaml"
            
            # 构建YAML数据
            yaml_data = self._build_yaml_data(api_name, path, method, group)
            
            # 写入文件
            file_path = module_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, allow_unicode=True, indent=2, sort_keys=False)
            
            self.logger.info(f"生成YAML文件: {file_path}")
    
    def _build_yaml_data(self, api_name: str, path: str, method: str, df: pd.DataFrame) -> Dict[str, Any]:
        """构建YAML数据结构"""
        yaml_data = {
            'api_name': api_name,
            'path': path,
            'method': method.upper(),
            'content_type': 'application/json',
            'auth_required': self._infer_auth_required(api_name),
            'test_cases': []
        }
        
        # 转换每个测试用例
        for _, row in df.iterrows():
            case = self._convert_row_to_case(row)
            if case:
                yaml_data['test_cases'].append(case)
        
        return yaml_data
    
    def _infer_auth_required(self, api_name: str) -> bool:
        """推断是否需要认证"""
        no_auth_keywords = ['登录', '注册', 'csrf', 'token']
        return not any(keyword in api_name for keyword in no_auth_keywords)
    
    def _convert_row_to_case(self, row: pd.Series) -> Dict[str, Any]:
        """将Excel行转换为测试用例"""
        try:
            # 解析请求参数
            request_params = str(row.get('请求参数', ''))
            data = self._parse_params(request_params) if request_params and request_params != 'nan' else {}
            
            # 解析预期结果
            expected_status = int(row.get('预期状态码', 200))
            expected_message = str(row.get('预期响应', ''))
            
            # 生成标签
            tags = self._generate_tags(row)
            
            case = {
                'id': str(row.get('用例编号', '')),
                'name': str(row.get('测试场景', '')),
                'description': str(row.get('用例描述', '')),
                'data': data,
                'expected': {
                    'status_code': expected_status
                },
                'tags': tags
            }
            
            # 添加message断言（如果有）
            if expected_message and expected_message != 'nan':
                case['expected']['message'] = expected_message
                
            return case
            
        except Exception as e:
            self.logger.error(f"转换行失败: {str(e)}")
            return None
    
    def _parse_params(self, params_str: str) -> Dict[str, Any]:
        """解析参数字符串"""
        params_str = params_str.strip()
        
        # JSON格式
        if params_str.startswith('{') and params_str.endswith('}'):
            try:
                return json.loads(params_str)
            except:
                pass
        
        # key=value格式
        if '=' in params_str:
            result = {}
            pairs = params_str.split(',')
            for pair in pairs:
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    result[key.strip()] = self._convert_param_value(value.strip())
            return result
        
        return {}
    
    def _convert_param_value(self, value: str):
        """转换参数值类型"""
        if value.lower() in ['true', 'false']:
            return value.lower() == 'true'
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except:
            return value.strip('"\'')
    
    def _generate_tags(self, row: pd.Series) -> List[str]:
        """生成标签"""
        tags = []
        
        # 根据用例编号
        case_id = str(row.get('用例编号', ''))
        if 'SMOKE' in case_id.upper():
            tags.append('smoke')
        if 'P0' in case_id.upper():
            tags.append('p0')
        elif 'P1' in case_id.upper():
            tags.append('p1')
        elif 'P2' in case_id.upper():
            tags.append('p2')
        
        # 根据测试场景
        scene = str(row.get('测试场景', ''))
        if '成功' in scene or '正常' in scene:
            tags.extend(['正常场景', 'positive'])
        elif '失败' in scene or '异常' in scene:
            tags.extend(['异常场景', 'negative'])
        elif '边界' in scene or '极限' in scene:
            tags.extend(['边界值', 'boundary'])
        
        return list(set(tags))  # 去重


def main():
    """主函数 - 命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Excel测试用例转YAML工具')
    parser.add_argument('excel_file', help='Excel文件路径')
    parser.add_argument('-m', '--module', help='指定模块名')
    parser.add_argument('-o', '--output', help='输出目录')
    
    args = parser.parse_args()
    
    converter = ExcelToYamlConverter()
    converter.convert_excel_to_yaml(args.excel_file, args.module)


if __name__ == '__main__':
    main()
