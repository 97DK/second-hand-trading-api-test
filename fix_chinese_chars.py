#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""修复中文字符问题"""

def fix_chinese_characters(file_path):
    """修复文件中的中文全角字符"""
    try:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换中文标点符号为英文
        replacements = {
            '：': ':',
            '（': '(',
            '）': ')',
            '，': ',',
            '“': '"',
            '”': '"',
            '；': ';',
            '。': '.',
            '？': '?',
            '！': '!',
            '【': '[',
            '】': ']',
            '《': '<',
            '》': '>',
            '—': '-',
            '…': '...',
            '、': ',',
            '·': '.'
        }
        
        for chinese_char, english_char in replacements.items():
            content = content.replace(chinese_char, english_char)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Successfully fixed Chinese characters in {file_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

if __name__ == "__main__":
    # 修复所有相关文件
    files_to_fix = [
        'core/send_request.py',
        'testcase/base_test.py',
        'common/read_yaml.py'
    ]
    
    for file_path in files_to_fix:
        fix_chinese_characters(file_path)
