#!/usr/bin/env python3
"""
简化的网络搜索功能测试脚本，只测试WebSearchTool
"""

import os
import sys
import logging
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置日志级别为DEBUG以查看详细信息
logging.basicConfig(level=logging.DEBUG)

from src.tools import WebSearchTool
from src.utils import load_env_variables

def main():
    """主函数"""
    print("开始测试网络搜索功能...")
    
    # 加载环境变量
    env_vars = load_env_variables()
    api_key = env_vars.get("DASHSCOPE_API_KEY")
    
    if not api_key:
        print("错误: 未找到DASHSCOPE_API_KEY环境变量")
        return 1
    
    # 创建工具实例
    web_search_tool = WebSearchTool(api_key=api_key)
    
    # 测试搜索功能
    try:
        print("\n测试政策搜索...")
        result = web_search_tool.search("新能源汽车政策")
        print(f"搜索状态: {result.get('status')}")
        print(f"结果数量: {result.get('count', 0)}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())