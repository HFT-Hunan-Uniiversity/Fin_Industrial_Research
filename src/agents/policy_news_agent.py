"""
政策新闻搜索智能体模块，用于实时搜索最新的政策和新闻信息
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from .base_agent import BaseAgent, SiliconFlowChat
from ..tools import WebSearchTool

# 配置日志
logger = logging.getLogger(__name__)


class PolicyNewsAgent(BaseAgent):
    """政策新闻搜索智能体"""
    
    def __init__(self, model_name: str, api_key: str, dashscope_api_key: str, system_prompt: str = ""):
        # 初始化LLM
        llm = SiliconFlowChat(api_key=api_key, model_name=model_name)
        
        # 初始化网络搜索工具
        self.web_search = WebSearchTool(dashscope_api_key)
        
        super().__init__(
            name="PolicyNewsAgent",
            description="实时搜索最新的政策和新闻信息，为行业分析提供最新动态。",
            llm=llm,
            tools=["web_search"],
            system_prompt=system_prompt or "你是一个专业的政策新闻分析专家，擅长搜索和分析最新的政策法规和行业新闻。"
        )
    
    def run(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行政策新闻搜索和分析"""
        # 获取行业参数，默认为新能源汽车
        industry = inputs.get("industry", "新能源汽车")
        time_range = inputs.get("time_range", "最近一个月")
        
        logger.info(f"开始搜索 {industry} 行业的最新政策和新闻，时间范围: {time_range}")
        
        # 搜索政策信息
        policy_results = self._search_policies(industry, time_range)
        
        # 搜索新闻信息
        news_results = self._search_news(industry, time_range)
        
        # 搜索市场趋势
        market_results = self._search_market_trends(industry)
        
        # 构建分析提示词
        user_prompt = f"""
        作为政策新闻分析专家，请基于以下搜索结果，分析 {industry} 行业的最新动态。
        
        最新政策信息:
        {policy_results.get('summary', '')}
        
        最新新闻动态:
        {news_results.get('summary', '')}
        
        市场趋势信息:
        {market_results.get('summary', '')}
        
        请关注：
        1. 最新政策对行业发展的潜在影响
        2. 行业热点新闻反映的市场变化
        3. 市场趋势与政策环境的协同性
        4. 未来可能出现的政策调整和市场机会
        
        请以JSON格式返回分析结果，包含以下字段：
        - policy_news_summary: 政策新闻分析总结
        - key_policy_changes: 关键政策变化列表
        - market_impact: 对市场的影响分析
        - emerging_opportunities: 新兴机会分析
        - potential_risks: 潜在风险分析
        - recommendations: 基于最新动态的建议
        """
        
        # 调用LLM进行分析
        response = self._call_llm(user_prompt)
        
        # 尝试解析JSON
        try:
            analysis_results = json.loads(response)
        except json.JSONDecodeError:
            # 如果解析失败，返回原始文本
            analysis_results = {
                "policy_news_summary": response,
                "key_policy_changes": [],
                "market_impact": "",
                "emerging_opportunities": "",
                "potential_risks": "",
                "recommendations": ""
            }
        
        # 合并搜索结果和分析结果
        results = {
            "search_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "industry": industry,
            "time_range": time_range,
            "policy_search": policy_results,
            "news_search": news_results,
            "market_search": market_results,
            "analysis": analysis_results
        }
        
        self.results = results
        return results
    
    def _search_policies(self, industry: str, time_range: str) -> Dict[str, Any]:
        """搜索政策信息"""
        try:
            results = self.web_search.search_policies(industry, time_range)
            if results.get("status") == "success":
                summary = self.web_search.summarize_results(results.get("results", []))
                return {
                    "status": "success",
                    "count": results.get("count", 0),
                    "summary": summary,
                    "results": results.get("results", [])
                }
            else:
                return {
                    "status": "error",
                    "error": results.get("error", "未知错误"),
                    "summary": "政策搜索失败",
                    "results": []
                }
        except Exception as e:
            logger.error(f"搜索政策信息时发生错误: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "summary": "政策搜索过程中发生错误",
                "results": []
            }
    
    def _search_news(self, industry: str, time_range: str) -> Dict[str, Any]:
        """搜索新闻信息"""
        try:
            results = self.web_search.search_news(industry, time_range)
            if results.get("status") == "success":
                summary = self.web_search.summarize_results(results.get("results", []))
                return {
                    "status": "success",
                    "count": results.get("count", 0),
                    "summary": summary,
                    "results": results.get("results", [])
                }
            else:
                return {
                    "status": "error",
                    "error": results.get("error", "未知错误"),
                    "summary": "新闻搜索失败",
                    "results": []
                }
        except Exception as e:
            logger.error(f"搜索新闻信息时发生错误: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "summary": "新闻搜索过程中发生错误",
                "results": []
            }
    
    def _search_market_trends(self, industry: str) -> Dict[str, Any]:
        """搜索市场趋势"""
        try:
            results = self.web_search.search_market_trends(industry)
            if results.get("status") == "success":
                summary = self.web_search.summarize_results(results.get("results", []))
                return {
                    "status": "success",
                    "count": results.get("count", 0),
                    "summary": summary,
                    "results": results.get("results", [])
                }
            else:
                return {
                    "status": "error",
                    "error": results.get("error", "未知错误"),
                    "summary": "市场趋势搜索失败",
                    "results": []
                }
        except Exception as e:
            logger.error(f"搜索市场趋势时发生错误: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "summary": "市场趋势搜索过程中发生错误",
                "results": []
            }
    
    def get_latest_policies(self, industry: str = "新能源汽车", days: int = 30) -> List[Dict[str, Any]]:
        """获取最近N天的政策信息"""
        time_range = f"最近{days}天"
        results = self._search_policies(industry, time_range)
        if results.get("status") == "success":
            return results.get("results", [])
        return []
    
    def get_latest_news(self, industry: str = "新能源汽车", days: int = 7) -> List[Dict[str, Any]]:
        """获取最近N天的新闻信息"""
        time_range = f"最近{days}天"
        results = self._search_news(industry, time_range)
        if results.get("status") == "success":
            return results.get("results", [])
        return []
    
    def get_policy_news_summary(self, industry: str = "新能源汽车", days: int = 30) -> str:
        """获取政策和新闻摘要"""
        # 获取政策信息
        policies = self.get_latest_policies(industry, days)
        policy_summary = self.web_search.summarize_results(policies, max_items=3)
        
        # 获取新闻信息
        news = self.get_latest_news(industry, min(days, 7))  # 新闻获取时间范围较短
        news_summary = self.web_search.summarize_results(news, max_items=3)
        
        # 组合摘要
        summary = f"## {industry}行业最新政策动态\n\n{policy_summary}\n\n"
        summary += f"## {industry}行业最新新闻动态\n\n{news_summary}"
        
        return summary