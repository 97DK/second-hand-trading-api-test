#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试文件路径解析
"""
from pathlib import Path
import sys

def test_file_path_resolution():
    print("=== 测试文件路径解析 ===")
    
    # 模拟 send_request.py 中的路径解析逻辑
    base_dir = Path(__file__).parent  # apiautotest目录
    print(f"基础目录: {base_dir}")
    print(f"基础目录是否存在: {base_dir.exists()}")
    
    filename = "product.jpg"
    file_path = base_dir / filename
    print(f"构造的文件路径: {file_path}")
    print(f"文件是否存在: {file_path.exists()}")
    
    if file_path.exists():
        print(f"文件大小: {file_path.stat().st_size} bytes")
    else:
        print("文件查找失败!")
        # 尝试其他可能的路径
        print("\n尝试其他路径:")
        possible_paths = [
            Path.cwd() / filename,
            Path.cwd().parent / "apiautotest" / filename,
            Path("product.jpg"),
            Path("../product.jpg"),
        ]
        
        for i, path in enumerate(possible_paths):
            print(f"  路径{i+1}: {path} -> 存在: {path.exists()}")

if __name__ == "__main__":
    test_file_path_resolution()