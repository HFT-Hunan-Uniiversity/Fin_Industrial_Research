"""
网络搜索工具模块，使用阿里云百炼平台的API进行实时搜索
"""

import json
import logging
import requests
import time
from typing import Dict, List, Any, Optional
from urllib.parse import quote

logger = logging.getLogger(__name__)


class WebSearchTool:
    """网络搜索工具类，使用阿里云百炼平台的WebSearch API"""
    
    def __init__(self, api_key: str):
        """
        初始化网络搜索工具
        
        Args:
            api_key: 阿里云百炼平台的API密钥
        """
        self.api_key = api_key
        # 尝试使用不同的API端点
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        执行网络搜索
        
        Args:
            query: 搜索查询字符串
            max_results: 最大返回结果数量
            
        Returns:
            搜索结果字典
        """
        try:
            # 构建请求数据 - 使用支持网络搜索的模型
            data = {
                "model": "qwen-max",  # 使用通义千问模型
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": f"请使用网络搜索功能，查找关于'{query}'的最新信息，并提供相关的网页链接和摘要。"
                        }
                    ]
                },
                "parameters": {
                    "result_format": "message",
                    "max_tokens": 1500,
                    "temperature": 0.7,
                    "enable_search": True  # 启用网络搜索功能
                }
            }
            
            logger.info(f"执行网络搜索: {query}")
            logger.info(f"请求数据: {json.dumps(data)}")
            
            # 发送请求
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            # 检查响应状态
            if response.status_code != 200:
                logger.error(f"搜索请求失败，状态码: {response.status_code}, 响应: {response.text}")
                return {
                    "status": "error",
                    "error": f"搜索请求失败，状态码: {response.status_code}",
                    "results": []
                }
            
            # 添加调试信息
            logger.info(f"API响应状态码: {response.status_code}")
            logger.info(f"API响应内容: {response.text[:500]}...")  # 只记录前500个字符
            
            # 解析响应
            try:
                response_json = response.json()
                logger.info(f"解析后的JSON: {json.dumps(response_json)[:500]}...")  # 只记录前500个字符
                
                # 提取模型回复
                if "output" in response_json and "choices" in response_json["output"]:
                    content = response_json["output"]["choices"][0]["message"]["content"]
                    
                    # 创建一个模拟的搜索结果
                    result = {
                        "title": f"关于{query}的搜索结果",
                        "content": content,
                        "url": "",
                        "snippet": content[:200] + "..." if len(content) > 200 else content
                    }
                    
                    return {
                        "status": "success",
                        "query": query,
                        "results": [result],
                        "count": 1
                    }
                else:
                    logger.error(f"响应格式不正确: {response_json}")
                    return {
                        "status": "error",
                        "error": "响应格式不正确",
                        "results": []
                    }
                    
            except json.JSONDecodeError as e:
                logger.error(f"无法解析JSON响应: {str(e)}")
                return {
                    "status": "error",
                    "error": f"无法解析JSON响应: {str(e)}",
                    "results": []
                }
            
        except Exception as e:
            logger.error(f"搜索过程中发生错误: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "results": []
            }
    
    def search_policies(self, industry: str = "新能源汽车", time_range: str = "最近一个月") -> Dict[str, Any]:
        """
        搜索特定行业的最新政策
        
        Args:
            industry: 行业名称
            time_range: 时间范围
            
        Returns:
            搜索结果字典
        """
        query = f"{industry} {time_range} 政策法规"
        return self.search(query)
    
    def search_news(self, industry: str = "新能源汽车", time_range: str = "最近一周") -> Dict[str, Any]:
        """
        搜索特定行业的最新新闻
        
        Args:
            industry: 行业名称
            time_range: 时间范围
            
        Returns:
            搜索结果字典
        """
        query = f"{industry} {time_range} 新闻动态"
        return self.search(query)
    
    def search_market_trends(self, industry: str = "新能源汽车") -> Dict[str, Any]:
        """
        搜索特定行业的市场趋势
        
        Args:
            industry: 行业名称
            
        Returns:
            搜索结果字典
        """
        query = f"{industry} 市场趋势 发展前景"
        return self.search(query)
    
    def _parse_sse_response(self, sse_text: str) -> List[Dict[str, Any]]:
        """
        解析SSE响应格式
        
        Args:
            sse_text: SSE格式的响应文本
            
        Returns:
            解析后的结果列表
        """
        results = []
        
        try:
            # 添加调试信息
            logger.info(f"开始解析SSE响应，总长度: {len(sse_text)}")
            
            # 按行分割响应文本
            lines = sse_text.strip().split('\n')
            logger.info(f"分割后行数: {len(lines)}")
            
            # 查找数据行
            for i, line in enumerate(lines):
                logger.debug(f"处理第{i+1}行: {line[:100]}...")  # 只记录前100个字符
                
                if line.startswith('data: '):
                    # 提取JSON数据
                    json_str = line[6:]  # 去掉 'data: ' 前缀
                    logger.debug(f"提取的JSON字符串: {json_str[:200]}...")  # 只记录前200个字符
                    
                    try:
                        # 解析JSON
                        data = json.loads(json_str)
                        logger.debug(f"解析后的JSON数据类型: {type(data)}")
                        
                        # 如果是搜索结果，添加到结果列表
                        if 'type' in data and data['type'] == 'search_result':
                            results.append(data['content'])
                            logger.info(f"添加搜索结果，当前总数: {len(results)}")
                        elif isinstance(data, dict) and 'title' in data:
                            # 直接是结果格式
                            results.append(data)
                            logger.info(f"添加直接结果，当前总数: {len(results)}")
                        else:
                            logger.debug(f"跳过非搜索结果数据: {data}")
                            
                    except json.JSONDecodeError as e:
                        logger.warning(f"无法解析JSON数据: {json_str}, 错误: {str(e)}")
                        continue
            
            logger.info(f"SSE解析完成，共找到 {len(results)} 个结果")
            return results
            
        except Exception as e:
            logger.error(f"解析SSE响应时发生错误: {str(e)}")
            return []
    
    def summarize_results(self, results: List[Dict[str, Any]], max_items: int = 5) -> str:
        """
        汇总搜索结果
        
        Args:
            results: 搜索结果列表
            max_items: 最大汇总项目数
            
        Returns:
            汇总文本
        """
        if not results:
            return "未找到相关结果"
        
        summary = f"找到 {len(results)} 条相关结果，以下是前 {min(max_items, len(results))} 条:\n\n"
        
        for i, result in enumerate(results[:max_items]):
            title = result.get('title', '无标题')
            url = result.get('url', '')
            snippet = result.get('snippet', result.get('description', ''))
            
            summary += f"{i+1}. {title}\n"
            if snippet:
                summary += f"   {snippet}\n"
            if url:
                summary += f"   链接: {url}\n"
            summary += "\n"
        
        return summary