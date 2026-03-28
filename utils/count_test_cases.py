# utils/count_test_cases.py
"""统计所有测试用例数量"""

from common.read_yaml import ReadYamlData

def count_all_test_cases():
    """统计所有模块的测试用例数量"""
    reader = ReadYamlData()
    
    modules = ['user', 'admin', 'product', 'appeal', 'credit', 'evaluation', 'finance', 'wish']
    total_cases = 0
    
    print("=" * 50)
    print("测试用例统计")
    print("=" * 50)
    
    for module in modules:
        files = reader.get_all_module_files(module)
        if not files:
            continue
            
        print(f"\n{module.upper()} 模块:")
        print(f"  文件数量: {len(files)}")
        
        module_total = 0
        for filename in files:
            cases = reader.get_testcase_yaml(module, filename)
            case_count = len(cases)
            print(f"    {filename}: {case_count} 个用例")
            module_total += case_count
        
        print(f"  模块总计: {module_total} 个用例")
        total_cases += module_total
    
    print("\n" + "=" * 50)
    print(f"总测试用例数: {total_cases}")
    print("=" * 50)
    
    return total_cases

if __name__ == '__main__':
    count_all_test_cases()
