"""
真实 AI API 客户端
支持多种 AI 服务提供商
"""

import httpx
import time
from typing import Dict, Any, Optional
from app.models import database as db_models


class AIAPIClient:
    """AI API 统一客户端"""
    
    def __init__(self, channel: db_models.Channel):
        self.channel = channel
        self.base_url = channel.base_url.rstrip('/')
        self.api_key = channel.api_key
        self.timeout = 60.0
    
    def _build_headers(self) -> Dict[str, str]:
        """构建请求头"""
        headers = {"Content-Type": "application/json"}
        
        if self.api_key:
            if self.channel.auth_type == "bearer":
                headers["Authorization"] = f"Bearer {self.api_key}"
            elif self.channel.auth_type == "api-key":
                headers["api-key"] = self.api_key
            elif self.channel.auth_type == "x-api-key":
                headers["x-api-key"] = self.api_key
        
        if self.channel.headers:
            headers.update(self.channel.headers)
        
        return headers
    
    async def chat_completion(
        self,
        model: str,
        messages: list,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        tools: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        统一的聊天完成接口
        支持 OpenAI、Anthropic 等格式
        """
        headers = self._build_headers()
        
        # 构建请求体
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        if tools:
            payload["tools"] = tools
        
        # 发送请求
        start_time = time.time()
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "data": data,
                        "response_time": response_time,
                        "status_code": response.status_code
                    }
                else:
                    return {
                        "success": False,
                        "error": f"HTTP {response.status_code}: {response.text}",
                        "response_time": response_time,
                        "status_code": response.status_code
                    }
            
            except httpx.TimeoutException:
                return {
                    "success": False,
                    "error": "Request timeout",
                    "response_time": self.timeout,
                    "status_code": 0
                }
            
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "response_time": time.time() - start_time,
                    "status_code": 0
                }
    
    async def test_speed(self, model: str) -> Dict[str, Any]:
        """速度测试"""
        messages = [
            {"role": "user", "content": "Hello! Please respond with a simple greeting."}
        ]
        
        result = await self.chat_completion(
            model=model,
            messages=messages,
            max_tokens=50
        )
        
        return result
    
    async def test_code_generation(self, model: str) -> Dict[str, Any]:
        """代码生成测试"""
        messages = [
            {
                "role": "user",
                "content": "Write a Python function to implement binary search. Only return the code, no explanation."
            }
        ]
        
        result = await self.chat_completion(
            model=model,
            messages=messages,
            max_tokens=500
        )
        
        if result["success"]:
            # 评估代码质量
            content = result["data"].get("choices", [{}])[0].get("message", {}).get("content", "")
            quality_score = self._evaluate_code_quality(content)
            result["quality_score"] = quality_score
        
        return result
    
    async def test_tool_calling(self, model: str) -> Dict[str, Any]:
        """工具调用测试"""
        messages = [
            {"role": "user", "content": "What's the weather like in San Francisco?"}
        ]
        
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get the current weather in a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city name"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ]
        
        result = await self.chat_completion(
            model=model,
            messages=messages,
            tools=tools,
            max_tokens=200
        )
        
        if result["success"]:
            # 检查是否正确调用了工具
            tool_calls = result["data"].get("choices", [{}])[0].get("message", {}).get("tool_calls", [])
            quality_score = 1.0 if tool_calls else 0.5
            result["quality_score"] = quality_score
        
        return result
    
    def _evaluate_code_quality(self, code: str) -> float:
        """评估代码质量"""
        score = 0.0
        
        # 检查是否包含函数定义
        if "def " in code:
            score += 0.3
        
        # 检查是否包含二分查找的关键元素
        if any(keyword in code.lower() for keyword in ["binary", "search", "mid", "left", "right"]):
            score += 0.3
        
        # 检查是否有循环或递归
        if "while" in code or "for" in code or code.count("binary_search") >= 2:
            score += 0.2
        
        # 检查是否有返回语句
        if "return" in code:
            score += 0.2
        
        return min(score, 1.0)
