from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import json
import logging
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.outputs import ChatResult, ChatGeneration
import requests

# 配置日志
logger = logging.getLogger(__name__)

class SiliconFlowChat(BaseChatModel):
    """硅基流动API的Chat模型封装"""
    
    api_key: str
    model_name: str = "deepseek-ai/DeepSeek-R1"
    base_url: str = "https://api.siliconflow.cn/v1"
    temperature: float = 0.1
    max_tokens: int = 4000
    
    def __init__(self, api_key: str, model_name: str = "deepseek-ai/DeepSeek-R1", 
                 base_url: str = "https://api.siliconflow.cn/v1", **kwargs):
        super().__init__(
            api_key=api_key,
            model_name=model_name,
            base_url=base_url,
            **kwargs
        )
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs,
    ) -> ChatResult:
        """生成聊天响应"""
        # 转换消息格式
        api_messages = []
        for message in messages:
            if isinstance(message, SystemMessage):
                api_messages.append({"role": "system", "content": message.content})
            elif isinstance(message, HumanMessage):
                api_messages.append({"role": "user", "content": message.content})
            else:
                # 默认作为用户消息处理
                api_messages.append({"role": "user", "content": message.content})
        
        # 调用API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "messages": api_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False
        }
        
        if stop:
            data["stop"] = stop
        
        try:
            # 记录请求详情
            logger.debug(f"API请求URL: {self.base_url}/chat/completions")
            logger.debug(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )
            
            # 记录响应详情
            logger.debug(f"响应状态码: {response.status_code}")
            logger.debug(f"响应内容: {response.text}")
            
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            generation = ChatGeneration(message=HumanMessage(content=content))
            return ChatResult(generations=[generation])
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP错误: {str(e)}")
            logger.error(f"响应内容: {e.response.text if e.response else '无响应'}")
            raise
        except Exception as e:
            logger.error(f"调用硅基流动API失败: {str(e)}")
            raise
    
    @property
    def _llm_type(self) -> str:
        return "siliconflow-chat"


class BaseAgent(ABC):
    """智能体基类"""
    
    def __init__(self, name: str, description: str, llm: BaseChatModel, 
                 tools: List[str], system_prompt: str = ""):
        self.name = name
        self.description = description
        self.llm = llm
        self.tools = tools
        self.system_prompt = system_prompt
        self.results = {}
    
    @abstractmethod
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """执行智能体任务"""
        pass
    
    def _create_messages(self, user_prompt: str) -> List[BaseMessage]:
        """创建消息列表"""
        messages = []
        if self.system_prompt:
            messages.append(SystemMessage(content=self.system_prompt))
        messages.append(HumanMessage(content=user_prompt))
        return messages
    
    def _call_llm(self, user_prompt: str) -> str:
        """调用LLM生成响应"""
        messages = self._create_messages(user_prompt)
        # 检查LLM类型并调用相应的方法
        if hasattr(self.llm, 'invoke'):
            response = self.llm.invoke(messages)
        elif hasattr(self.llm, '_generate'):
            response = self.llm._generate([messages])
            response = response.generations[0][0].text
        elif hasattr(self.llm, '__call__'):
            response = self.llm(messages)
        else:
            raise ValueError(f"LLM对象 {type(self.llm)} 不支持调用")
        
        # 处理不同类型的响应
        if hasattr(response, 'content'):
            return response.content
        elif isinstance(response, str):
            return response
        elif hasattr(response, 'text'):
            return response.text
        else:
            return str(response)
    
    def save_results(self, results: Dict[str, Any], output_path: str) -> None:
        """保存结果到文件"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            logger.info(f"结果已保存到: {output_path}")
        except Exception as e:
            logger.error(f"保存结果失败: {str(e)}")