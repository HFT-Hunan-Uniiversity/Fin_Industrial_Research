"""
市场分析智能体模块，用于分析行业产销趋势、市场结构与渗透率
"""

import json
import logging
from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, SiliconFlowChat

# 配置日志
logger = logging.getLogger(__name__)


class MarketAgent(BaseAgent):
    """市场分析智能体"""
    
    def __init__(self, model_name: str, api_key: str, data_query, data_analyzer, system_prompt: str = ""):
        # 初始化LLM
        llm = SiliconFlowChat(api_key=api_key, model_name=model_name)
        
        super().__init__(
            name="MarketAgent",
            description="分析行业产销趋势、市场结构与渗透率。",
            llm=llm,
            tools=["data_query", "data_analyzer"],
            system_prompt=system_prompt
        )
        
        # 保存工具引用
        self.data_query = data_query
        self.data_analyzer = data_analyzer
    
    def run(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行市场分析"""
        # 获取数据
        try:
            production_data = self.data_query.get_data_summary("production_sales_data")
            charging_data = self.data_query.get_data_summary("charging_infrastructure")
            brand_data = self.data_query.get_data_summary("brand_production_sales")
        except Exception as e:
            logger.error(f"获取市场数据失败: {str(e)}")
            return {
                "status": "error",
                "error": f"获取市场数据失败: {str(e)}"
            }
            
        # 构建提示词
        user_prompt = f"""
        作为市场分析专家，请分析新能源汽车市场的产销趋势和结构变化。
        
        产销数据概览:
        {production_data.get('summary', '')}
        
        充电设施数据概览:
        {charging_data.get('summary', '')}
        
        品牌产销数据概览:
        {brand_data.get('summary', '')}
        
        请关注：
        1. 产销量的季节性变化和长期趋势
        2. 主要厂商的市场份额变化
        3. 充电基础设施与市场发展的关系
        4. 市场渗透率变化及未来空间
        5. 不同品牌的市场表现对比
        
        请以JSON格式返回分析结果，包含以下字段：
        - market_trend_summary: 市场产销趋势分析总结
        - penetration_rate: 市场渗透率分析
        - manufacturer_analysis: 主要厂商分析
        - brand_comparison: 品牌市场表现对比
        - infrastructure_insights: 基础设施建设洞察
        - market_forecast: 市场发展趋势预测
        """
        
        # 调用LLM
        response = self._call_llm(user_prompt)
        
        # 尝试解析JSON
        try:
            results = json.loads(response)
        except json.JSONDecodeError:
            # 如果解析失败，返回原始文本
            results = {
                "market_trend_summary": response,
                "penetration_rate": {},
                "manufacturer_analysis": {},
                "brand_comparison": {},
                "infrastructure_insights": "",
                "market_forecast": ""
            }
        
        self.results = results
        return results