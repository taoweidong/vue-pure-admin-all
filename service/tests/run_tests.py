#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试统一入口
用于运行所有单元测试并生成测试报告
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(coverage=True, html_report=True, xml_report=True, verbose=True):
    """运行测试"""
    
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # 基础pytest命令
    cmd = ["python", "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        # 添加覆盖率参数
        cmd.extend([
            "--cov=app",
            "--cov-branch",
            "--cov-fail-under=65",
            "--cov-report=term-missing"
        ])
        
        if html_report:
            cmd.append("--cov-report=html:tests/reports/coverage_html")
        
        if xml_report:
            cmd.append("--cov-report=xml:tests/reports/coverage.xml")
    
    # 添加测试报告
    cmd.extend([
        "--junit-xml=tests/reports/junit.xml",
        "--html=tests/reports/report.html",
        "--self-contained-html"
    ])
    
    # 测试目录
    cmd.append("tests/")
    
    print(f"运行命令: {' '.join(cmd)}")
    
    # 创建报告目录
    reports_dir = Path("tests/reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # 运行测试
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("\\n测试被用户中断")
        return 1
    except Exception as e:
        print(f"运行测试时出错: {e}")
        return 1


def run_specific_tests(test_pattern):
    """运行指定的测试"""
    cmd = [
        "python", "-m", "pytest",
        "-v",
        "--cov=app",
        "--cov-report=term-missing",
        "-k", test_pattern
    ]
    
    return subprocess.run(cmd, check=False).returncode


def run_test_categories():
    """按类别运行测试"""
    categories = {
        "auth": "test_auth",
        "users": "test_users", 
        "roles": "test_roles",
        "menus": "test_menus",
        "departments": "test_departments",
        "api": "test_*_api",
        "services": "test_*_service",
        "models": "test_*_model"
    }
    
    print("可用的测试类别:")
    for key, pattern in categories.items():
        print(f"  {key}: {pattern}")
    
    category = input("请选择要运行的测试类别 (或直接回车运行所有测试): ").strip()
    
    if not category:
        return run_tests()
    
    if category in categories:
        return run_specific_tests(categories[category])
    else:
        print(f"未知的测试类别: {category}")
        return 1


def check_coverage(min_coverage=65):
    """检查测试覆盖率"""
    coverage_file = Path("tests/reports/coverage.xml")
    
    if not coverage_file.exists():
        print("覆盖率报告文件不存在，请先运行测试")
        return False
    
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        
        # 查找总覆盖率
        coverage_elem = root.find(".//coverage")
        if coverage_elem is not None:
            line_rate = float(coverage_elem.get("line-rate", 0)) * 100
            branch_rate = float(coverage_elem.get("branch-rate", 0)) * 100
            
            print(f"\\n覆盖率报告:")
            print(f"  行覆盖率: {line_rate:.2f}%")
            print(f"  分支覆盖率: {branch_rate:.2f}%")
            
            if line_rate >= min_coverage:
                print(f"✅ 覆盖率达标 (>= {min_coverage}%)")
                return True
            else:
                print(f"❌ 覆盖率不达标 (< {min_coverage}%)")
                return False
        
    except Exception as e:
        print(f"解析覆盖率报告出错: {e}")
        return False
    
    return False


def clean_reports():
    """清理测试报告"""
    reports_dir = Path("tests/reports")
    if reports_dir.exists():
        import shutil
        shutil.rmtree(reports_dir)
        print("测试报告已清理")
    else:
        print("没有找到测试报告目录")


def install_dependencies():
    """安装测试依赖"""
    dependencies = [
        "pytest-cov",
        "pytest-html",
        "pytest-xvfb",
        "pytest-mock"
    ]
    
    for dep in dependencies:
        try:
            __import__(dep.replace("-", "_"))
            print(f"✅ {dep} 已安装")
        except ImportError:
            print(f"⚠️  {dep} 未安装，正在安装...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep])


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="单元测试运行工具")
    parser.add_argument("--no-coverage", action="store_true", help="不生成覆盖率报告")
    parser.add_argument("--no-html", action="store_true", help="不生成HTML报告")
    parser.add_argument("--no-xml", action="store_true", help="不生成XML报告")
    parser.add_argument("--quiet", action="store_true", help="安静模式")
    parser.add_argument("--pattern", "-k", help="运行匹配模式的测试")
    parser.add_argument("--category", action="store_true", help="按类别运行测试")
    parser.add_argument("--check-coverage", action="store_true", help="检查覆盖率")
    parser.add_argument("--clean", action="store_true", help="清理测试报告")
    parser.add_argument("--install-deps", action="store_true", help="安装测试依赖")
    
    args = parser.parse_args()
    
    if args.install_deps:
        install_dependencies()
        return 0
    
    if args.clean:
        clean_reports()
        return 0
    
    if args.check_coverage:
        success = check_coverage()
        return 0 if success else 1
    
    if args.category:
        return run_test_categories()
    
    if args.pattern:
        return run_specific_tests(args.pattern)
    
    # 运行所有测试
    return run_tests(
        coverage=not args.no_coverage,
        html_report=not args.no_html,
        xml_report=not args.no_xml,
        verbose=not args.quiet
    )


if __name__ == "__main__":
    sys.exit(main())