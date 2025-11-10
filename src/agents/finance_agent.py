"""
财务分析智能体模块，负责新能源汽车行业的财务指标分析
"""

import json
import logging
from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, SiliconFlowChat

# 配置日志
logger = logging.getLogger(__name__)


class FinanceAgent(BaseAgent):
    """财务分析智能体"""
    
    def __init__(self, model_name: str, api_key: str, data_query, data_analyzer, system_prompt: str = ""):
        # 初始化LLM
        llm = SiliconFlowChat(api_key=api_key, model_name=model_name)
        
        super().__init__(
            name="FinanceAgent",
            description="负责新能源汽车行业的财务指标分析。",
            llm=llm,
            tools=["data_query", "data_analyzer"],
            system_prompt=system_prompt
        )
        
        # 保存工具引用
        self.data_query = data_query
        self.data_analyzer = data_analyzer
    
    def run(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行财务分析"""
        # 获取数据
        try:
            industry_data = self.data_query.get_data_summary("industry_overview")
            company_financial_data = self.data_query.get_data_summary("company_financial_summary")
            company_profitability = self.data_query.get_data_summary("company_profitability")
            company_rd_investment = self.data_query.get_data_summary("company_rd_investment")
        except Exception as e:
            logger.error(f"获取财务数据失败: {str(e)}")
            return {
                "status": "error",
                "error": f"获取财务数据失败: {str(e)}"
            }
            
        # 构建提示词
        user_prompt = f"""
        作为财务分析专家，请分析新能源汽车行业上市公司的财务表现。
        
        行业财务数据概览:
        {industry_data.get('summary', '')}
        
        公司财务摘要数据概览:
        {company_financial_data.get('summary', '')}
        
        公司盈利能力数据概览:
        {company_profitability.get('summary', '')}
        
        公司研发投入数据概览:
        {company_rd_investment.get('summary', '')}
        
        请关注：
        1. 行业整体盈利能力趋势
        2. 资产负债结构与偿债能力
        3. 成长性指标与投资价值
        4. 行业内主要公司的财务表现对比
        5. 研发投入与创新能力分析
        
        请以JSON格式返回分析结果，包含以下字段：
        - finance_summary: 行业财务表现分析总结
        - key_metrics: 关键财务指标分析
        - company_comparison: 主要公司财务表现对比
        - investment_insights: 投资价值分析
        - rd_analysis: 研发投入与创新能力分析
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
                "finance_summary": response,
                "key_metrics": {},
                "company_comparison": {},
                "investment_insights": "",
                "risk_factors": ""
            }
        
        self.results = results
        return results