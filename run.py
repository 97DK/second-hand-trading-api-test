# run.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
接口自动化测试运行入口
"""

import pytest
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='接口自动化测试运行入口')
    parser.add_argument('--env', default='dev', help='测试环境: dev/test/prod')
    parser.add_argument('--module', help='指定模块: user/product/admin等')
    parser.add_argument('--tag', help='运行标签: smoke/regression/p0/p1/p2')
    parser.add_argument('--report', action='store_true', help='生成 HTML 报告')
    parser.add_argument('--allure', action='store_true', help='生成 Allure 报告')
    return parser.parse_args()


def build_pytest_args(args):
    """构建pytest参数"""
    pytest_args = []

    # 设置环境变量
    os.environ['TEST_ENV'] = args.env

    # 指定测试路径
    if args.module:
        pytest_args.append(f'testcase/test_{args.module}/')
    else:
        pytest_args.append('testcase/')

    # 按标签运行
    if args.tag:
        pytest_args.extend(['-m', args.tag])

    # 详细输出
    pytest_args.append('-v')
    pytest_args.append('-s')
    pytest_args.append('--tb=short')

    # 生成 HTML 报告
    if args.report:
        report_dir = Path(__file__).parent / 'reports' / 'html'
        report_dir.mkdir(parents=True, exist_ok=True)
        report_file = report_dir / f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
        pytest_args.extend([
            f'--html={report_file}',
            '--self-contained-html'
        ])
        print(f"HTML 报告将保存到：{report_file}")
    
    # 生成 Allure 报告
    if args.allure:
        # 统一使用 reports 目录下的子文件夹
        allure_results_dir = Path(__file__).parent / 'reports' / 'allure-results'
        allure_results_dir.mkdir(parents=True, exist_ok=True)
        pytest_args.extend([
            f'--alluredir={allure_results_dir}'
        ])
        print(f"Allure 原始数据将保存到：{allure_results_dir}")
        print(f"提示：运行 'allure generate reports/allure-results -o reports/allure-report --clean' 生成可视化报告")

    return pytest_args


def main():
    """主函数"""
    args = parse_args()

    print("=" * 60)
    print("接口自动化测试开始")
    print(f"环境: {args.env}")
    print(f"模块: {args.module or '所有'}")
    print(f"标签: {args.tag or '所有'}")
    print("=" * 60)

    pytest_args = build_pytest_args(args)
    exit_code = pytest.main(pytest_args)

    print("=" * 60)
    print(f"测试完成，退出码：{exit_code}")
    print("=" * 60)
        
    # 如果生成了 Allure 报告，提示用户查看
    if args.allure:
        print("\nAllure 报告已生成！")
        print("请运行以下命令查看报告：")
        print(f"allure serve reports/allure-results")
        print("或")
        print(f"allure generate reports/allure-results -o reports/allure-report --clean && allure open reports/allure-report\n")

    return exit_code


if __name__ == '__main__':
    sys.exit(main())