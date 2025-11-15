#!/usr/bin/env python3
"""
测试网络搜索功能
"""

import os
import sys
import json
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.tools import WebSearchTool
from src.agents import PolicyNewsAgent
from src.utils import load_env_variables

def test_web_search_tool():
    """测试网络搜索工具"""
    print("=" * 50)
    print("测试网络搜索工具")
    print("=" * 50)
    
    # 加载环境变量
    env_vars = load_env_variables()
    api_key = env_vars.get("DASHSCOPE_API_KEY")
    
    if not api_key:
        print("错误: 未找到DASHSCOPE_API_KEY环境变量")
        return False
    
    # 创建工具实例
    web_search_tool = WebSearchTool(api_key=api_key)
    
    # 测试搜索功能
    try:
        # 测试政策搜索
        print("\n1. 测试政策搜索...")
        policies = web_search_tool.search_policies("新能源汽车")
        print(f"找到 {policies.get('count', 0)} 条相关政策:")
        for i, policy in enumerate(policies.get('results', [])[:2], 1):
            print(f"  {i}. {policy.get('title', '无标题')}")
            print(f"     {policy.get('snippet', policy.get('description', '无摘要'))[:100]}...")
        
        # 测试新闻搜索
        print("\n2. 测试新闻搜索...")
        news = web_search_tool.search_news("汽车行业")
        print(f"找到 {news.get('count', 0)} 条相关新闻:")
        for i, item in enumerate(news.get('results', [])[:2], 1):
            print(f"  {i}. {item.get('title', '无标题')}")
            print(f"     {item.get('snippet', item.get('description', '无摘要'))[:100]}...")
        
        # 测试市场趋势搜索
        print("\n3. 测试市场趋势搜索...")
        trends = web_search_tool.search_market_trends("电动汽车")
        print(f"找到 {trends.get('count', 0)} 条相关趋势:")
        for i, trend in enumerate(trends.get('results', [])[:2], 1):
            print(f"  {i}. {trend.get('title', '无标题')}")
            print(f"     {trend.get('snippet', trend.get('description', '无摘要'))[:100]}...")
        
        print("\n✅ 网络搜索工具测试成功!")
        return True
        
    except Exception as e:
        print(f"\n❌ 网络搜索工具测试失败: {str(e)}")
        return False

def test_policy_news_agent():
    """测试政策新闻智能体"""
    print("\n" + "=" * 50)
    print("测试政策新闻智能体")
    print("=" * 50)
    
    # 加载环境变量
    env_vars = load_env_variables()
    siliconflow_api_key = env_vars.get("SILICONFLOW_API_KEY")
    dashscope_api_key = env_vars.get("DASHSCOPE_API_KEY")
    
    if not siliconflow_api_key:
        print("错误: 未找到SILICONFLOW_API_KEY环境变量")
        return False
    
    if not dashscope_api_key:
        print("错误: 未找到DASHSCOPE_API_KEY环境变量")
        return False
    
    # 创建智能体实例
    agent = PolicyNewsAgent(
        model_name="Qwen/Qwen2.5-7B-Instruct",
        api_key=siliconflow_api_key,
        dashscope_api_key=dashscope_api_key
    )
    
    # 测试智能体
    try:
        print("\n运行政策新闻智能体分析...")
        result = agent.run(inputs={"industry": "新能源汽车"})
        
        # 打印分析结果摘要
        print("\n✅ 政策新闻智能体分析完成!")
        print("\n分析结果摘要:")
        
        if "policy_search" in result and result["policy_search"].get("status") == "success":
            print(f"- 找到 {result['policy_search'].get('count', 0)} 条相关政策")
        
        if "news_search" in result and result["news_search"].get("status") == "success":
            print(f"- 找到 {result['news_search'].get('count', 0)} 条相关新闻")
        
        if "market_search" in result and result["market_search"].get("status") == "success":
            print(f"- 找到 {result['market_search'].get('count', 0)} 条市场趋势")
        
        if "analysis" in result:
            print("- 已生成影响分析")
        
        # 保存详细结果
        output_dir = Path("output/test_results")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_dir / "policy_news_test.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细结果已保存到: {output_dir / 'policy_news_test.json'}")
        return True
        
    except Exception as e:
        print(f"\n❌ 政策新闻智能体测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("开始测试网络搜索功能...")
    
    # 测试网络搜索工具
    tool_success = test_web_search_tool()
    
    # 测试政策新闻智能体
    agent_success = test_policy_news_agent()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    if tool_success and agent_success:
        print("✅ 所有测试通过!")
        return 0
    else:
        print("❌ 部分测试失败!")
        return 1

if __name__ == "__main__":
    sys.exit(main())