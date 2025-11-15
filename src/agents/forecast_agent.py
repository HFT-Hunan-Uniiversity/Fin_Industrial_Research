"""
预测分析智能体模块，用于根据历史趋势预测下一期市场走势
"""

import json
import logging
from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, SiliconFlowChat

# 配置日志
logger = logging.getLogger(__name__)


class ForecastAgent(BaseAgent):
    """预测分析智能体"""
    
    def __init__(self, model_name: str, api_key: str, system_prompt: str = ""):
        # 初始化LLM
        llm = SiliconFlowChat(api_key=api_key, model_name=model_name)
        
        super().__init__(
            name="ForecastAgent",
            description="根据历史趋势预测下一期市场走势。",
            llm=llm,
            tools=[],
            system_prompt=system_prompt
        )
    
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """执行预测分析"""
        # 获取数据
        industry_data = inputs.get("industry_data")
        production_data = inputs.get("production_data")
        
        # 构建提示词
        user_prompt = f"""
        作为预测分析专家，请基于历史数据预测新能源汽车行业未来发展趋势。
        
        行业财务数据概览:
        {industry_data.get('summary', '')}
        
        产销数据概览:
        {production_data.get('summary', '')}
        
        请关注：
        1. 行业增长率的短期和中期预测
        2. 市场结构可能的变化
        3. 技术发展对市场的影响
        4. 风险因素与不确定性分析
        
        请以JSON格式返回分析结果，包含以下字段：
        - forecast_summary: 预测分析总结
        - growth_forecast: 增长率预测
        - market_structure_changes: 市场结构变化预测
        - technology_impact: 技术发展影响分析
        - risk_factors: 风险因素分析
        """
        
        # 调用LLM
        response = self._call_llm(user_prompt)
        
        # 尝试解析JSON
        try:
            results = json.loads(response)
        except json.JSONDecodeError:
            # 如果解析失败，返回原始文本
            results = {
                "forecast_summary": response,
                "growth_forecast": {},
                "market_structure_changes": {},
                "technology_impact": "",
                "risk_factors": ""
            }
        
        self.results = results
        return results