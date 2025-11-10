"""
报告生成智能体模块，用于整合所有子智能体的输出，生成最终Markdown报告
"""

import json
import logging
from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, SiliconFlowChat

# 配置日志
logger = logging.getLogger(__name__)


class ReportAgent(BaseAgent):
    """报告生成智能体"""
    
    def __init__(self, model_name: str, api_key: str, system_prompt: str = ""):
        # 初始化LLM
        llm = SiliconFlowChat(api_key=api_key, model_name=model_name)
        
        super().__init__(
            name="ReportAgent",
            description="整合所有子智能体的输出，生成最终Markdown报告。",
            llm=llm,
            tools=[],
            system_prompt=system_prompt
        )
    
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """生成综合报告"""
        # 获取各智能体的结果
        macro_results = inputs.get("MacroAgent", {})
        finance_results = inputs.get("FinanceAgent", {})
        market_results = inputs.get("MarketAgent", {})
        policy_results = inputs.get("PolicyNewsAgent", {})  # 使用PolicyNewsAgent替代PolicyAgent
        forecast_results = inputs.get("ForecastAgent", {})
        
        # 构建提示词
        user_prompt = f"""
        请根据以下子智能体分析结果撰写一份完整的新能源汽车行业分析报告。
        
        宏观经济环境分析:
        {macro_results.get('macro_summary', '')}
        
        行业财务表现分析:
        {finance_results.get('finance_summary', '')}
        
        市场产销趋势分析:
        {market_results.get('market_trend_summary', '')}
        
        政策与环境影响分析:
        {policy_results.get('analysis', {}).get('policy_news_summary', '')}
        
        预测与展望分析:
        {forecast_results.get('forecast_summary', '')}
        
        请按照以下结构撰写报告：
        # 新能源汽车行业分析报告
        
        ## 一、宏观经济环境
        [基于宏观经济分析结果]
        
        ## 二、行业财务表现
        [基于财务分析结果]
        
        ## 三、市场产销趋势
        [基于市场分析结果]
        
        ## 四、政策与环境影响
        [基于政策分析结果]
        
        ## 五、预测与展望
        [基于预测分析结果]
        
        ## 六、结论与建议
        [综合各模块结果，总结行业趋势与投资启示]
        """
        
        # 调用LLM
        response = self._call_llm(user_prompt)
        
        # 返回报告内容
        results = {
            "report_content": response,
            "report_type": "markdown"
        }
        
        self.results = results
        return results