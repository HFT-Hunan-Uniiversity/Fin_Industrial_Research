"""
宏观经济分析智能体模块，用于分析宏观经济数据与行业趋势的关系
"""

import json
import logging
from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, SiliconFlowChat

# 配置日志
logger = logging.getLogger(__name__)


class MacroAgent(BaseAgent):
    """宏观经济分析智能体"""
    
    def __init__(self, model_name: str, api_key: str, data_query, data_analyzer, system_prompt: str = ""):
        # 初始化LLM
        llm = SiliconFlowChat(api_key=api_key, model_name=model_name)
        
        super().__init__(
            name="MacroAgent",
            description="分析宏观经济数据（GDP, CPI）与行业趋势的关系。",
            llm=llm,
            tools=["data_query", "data_analyzer"],
            system_prompt=system_prompt
        )
        
        # 保存工具引用
        self.data_query = data_query
        self.data_analyzer = data_analyzer
    
    def run(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行宏观经济分析"""
        # 获取数据
        try:
            gdp_data = self.data_query.get_data_summary("macro_economic_data")
            cpi_data = self.data_query.get_data_summary("cpi_data")
            ppi_data = self.data_query.get_data_summary("ppi_data")
        except Exception as e:
            logger.error(f"获取宏观经济数据失败: {str(e)}")
            return {
                "status": "error",
                "error": f"获取宏观经济数据失败: {str(e)}"
            }
            
        # 构建提示词
        user_prompt = f"""
        作为宏观经济分析专家，请分析以下GDP、CPI和PPI数据与新能源汽车行业的关系。
        
        GDP数据概览:
        {gdp_data.get('summary', '')}
        
        CPI数据概览:
        {cpi_data.get('summary', '')}
        
        PPI数据概览:
        {ppi_data.get('summary', '')}
        
        请关注：
        1. GDP增长与新能源汽车行业发展的相关性
        2. CPI变化对消费者购买新能源汽车意愿的影响
        3. PPI变化对新能源汽车制造成本的影响
        4. 宏观经济环境对行业整体发展的潜在影响
        
        请以JSON格式返回分析结果，包含以下字段：
        - macro_summary: 宏观经济环境分析总结
        - macro_corr_matrix: 宏观经济指标与行业发展的相关性分析
        - key_insights: 关键洞察列表
        - recommendations: 基于宏观环境的建议
        """
        
        # 调用LLM
        response = self._call_llm(user_prompt)
        
        # 尝试解析JSON
        try:
            results = json.loads(response)
        except json.JSONDecodeError:
            # 如果解析失败，返回原始文本
            results = {
                "macro_summary": response,
                "macro_corr_matrix": {},
                "key_insights": [],
                "recommendations": []
            }
        
        self.results = results
        return results