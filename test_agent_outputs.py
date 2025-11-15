#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试智能体输出功能
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.coordinator import AnalysisCoordinator

def test_agent_outputs():
    """测试智能体输出功能"""
    print("初始化分析协调器...")
    
    # 初始化协调器
    try:
        coordinator = AnalysisCoordinator()
        print("✓ 分析协调器初始化成功")
    except Exception as e:
        print(f"✗ 初始化分析协调器失败: {str(e)}")
        return
    
    # 检查数据文件夹路径
    print("\n检查数据文件夹路径...")
    data_root = coordinator.data_loader.data_root_path
    print(f"数据根目录: {data_root}")
    
    # 检查各智能体使用的数据文件
    print("\n各智能体使用的数据文件:")
    
    # 宏观经济分析Agent
    print("\n【宏观经济分析Agent】")
    macro_files = [
        coordinator.data_loader._resolve_file_name("macro_economic_data"),
        coordinator.data_loader._resolve_file_name("cpi_data"),
        coordinator.data_loader._resolve_file_name("ppi_data")
    ]
    print(f"数据源: 宏观数据文件夹")
    print(f"数据文件: {macro_files}")
    for file in macro_files:
        file_path = os.path.join(data_root, file)
        exists = "✓" if os.path.exists(file_path) else "✗"
        print(f"  {exists} {file_path}")
    
    # 财务分析Agent
    print("\n【财务分析Agent】")
    finance_files = [
        coordinator.data_loader._resolve_file_name("industry_overview"),
        coordinator.data_loader._resolve_file_name("company_financial_summary"),
        coordinator.data_loader._resolve_file_name("company_profitability"),
        coordinator.data_loader._resolve_file_name("company_rd_investment")
    ]
    print(f"数据源: 财务数据文件夹")
    print(f"数据文件: {finance_files}")
    for file in finance_files:
        file_path = os.path.join(data_root, file)
        exists = "✓" if os.path.exists(file_path) else "✗"
        print(f"  {exists} {file_path}")
    
    # 市场分析Agent
    print("\n【市场分析Agent】")
    market_files = [
        coordinator.data_loader._resolve_file_name("production_sales_data"),
        coordinator.data_loader._resolve_file_name("charging_infrastructure"),
        coordinator.data_loader._resolve_file_name("brand_production_sales")
    ]
    print(f"数据源: 市场数据文件夹")
    print(f"数据文件: {market_files}")
    for file in market_files:
        file_path = os.path.join(data_root, file)
        exists = "✓" if os.path.exists(file_path) else "✗"
        print(f"  {exists} {file_path}")
    
    # 运行一个简单的分析来测试输出功能
    print("\n运行简单分析以测试输出功能...")
    try:
        # 只加载部分数据以加快测试速度
        load_results = coordinator.load_data([
            "macro_economic_data",
            "company_financial_summary",
            "production_sales_data"
        ])
        
        # 运行分析
        analysis_results = coordinator.run_analysis(["宏观经济", "财务", "市场"])
        
        # 显示智能体输出
        print("\n显示智能体输出内容和数据源信息:")
        coordinator.print_agent_outputs()
        
    except Exception as e:
        print(f"✗ 测试分析失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_agent_outputs()