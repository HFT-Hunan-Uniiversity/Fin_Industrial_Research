#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试数据路径配置
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.tools.mapped_data_loader import MappedDataLoader

def test_data_paths():
    """测试数据路径配置"""
    print("测试数据路径配置...")
    
    # 测试不同的数据路径配置
    test_paths = [
        "data",           # 当前目录下的data文件夹
        "../data",        # 上级目录的data文件夹
        "../../数据",     # 上上级目录的"数据"文件夹
    ]
    
    for path in test_paths:
        print(f"\n测试数据路径: {path}")
        full_path = project_root / path
        print(f"完整路径: {full_path}")
        print(f"路径存在: {full_path.exists()}")
        
        if full_path.exists():
            files = list(full_path.glob("*"))
            print(f"目录中的文件: {[f.name for f in files if f.is_file()]}")
    
    # 测试数据加载器
    print("\n\n测试数据加载器...")
    
    # 使用当前.env配置
    data_root_path = os.environ.get("DATA_ROOT_PATH", "../data")
    print(f"使用数据路径: {data_root_path}")
    
    try:
        loader = MappedDataLoader(data_root_path=data_root_path)
        
        # 列出可用文件
        available_files = loader.list_available_files()
        print("实际文件列表:")
        for file in available_files['actual_files']:
            print(f"  - {file}")
        
        print("\n映射文件列表:")
        for logical, info in available_files['mapped_files'].items():
            status = '✓' if info['exists'] else '✗'
            print(f"  {status} {logical} -> {info['actual_file']} ({info['description']})")
        
        # 尝试加载一个文件
        test_file = "宏观经济数据.csv"
        print(f"\n尝试加载文件: {test_file}")
        try:
            df = loader.load_data(test_file)
            print(f"成功加载 {test_file}，形状: {df.shape}")
            print(f"列名: {list(df.columns)}")
        except Exception as e:
            print(f"加载失败: {str(e)}")
            
    except Exception as e:
        print(f"创建数据加载器失败: {str(e)}")

if __name__ == "__main__":
    test_data_paths()