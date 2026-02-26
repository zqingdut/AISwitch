import httpx
import time
import json
from sqlalchemy.orm import Session
from app.models import database as db_models
from typing import Dict, Any

class ModelTester:
    """模型测试引擎"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def test_model(self, model_id: int, test_type: str = "speed"):
        """测试单个模型"""
        model = self.db.query(db_models.Model).filter(db_models.Model.id == model_id).first()
        if not model:
            return
        
        channel = model.channel
        
        # 根据测试类型执行相应测试
        if test_type == "speed":
            result = await self._test_speed(model, channel)
            self._save_test_result(model_id, "speed", result)
        elif test_type == "code":
            result = await self._test_code_generation(model, channel)
            self._save_test_result(model_id, "code", result)
        elif test_type == "tool":
            result = await self._test_tool_calling(model, channel)
            self._save_test_result(model_id, "tool", result)
        else:
            # 执行所有测试
            speed_result = await self._test_speed(model, channel)
            code_result = await self._test_code_generation(model, channel)
            tools_result = await self._test_tool_calling(model, channel)
            
            self._save_test_result(model_id, "speed", speed_result)
            self._save_test_result(model_id, "code", code_result)
            self._save_test_result(model_id, "tool", tools_result)
        
        self.db.commit()
    
    async def _test_speed(self, model: db_models.Model, channel: db_models.Channel) -> Dict[str, Any]:
        """速度测试"""
        try:
            headers = self._build_headers(channel)
            payload = {
                "model": model.model_identifier,
                "messages": [{"role": "user", "content": "Hello, how are you?"}],
                "max_tokens": 50
            }
            
            start_time = time.time()
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{channel.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
            end_time = time.time()
            
            response_time_ms = int((end_time - start_time) * 1000)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "response_time_ms": response_time_ms,
                    "quality_score": None,
                    "error_message": None
                }
            else:
                return {
                    "success": False,
                    "response_time_ms": response_time_ms,
                    "quality_score": None,
                    "error_message": f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "response_time_ms": None,
                "quality_score": None,
                "error_message": str(e)
            }
    
    async def _test_code_generation(self, model: db_models.Model, channel: db_models.Channel) -> Dict[str, Any]:
        """代码生成质量测试"""
        try:
            headers = self._build_headers(channel)
            payload = {
                "model": model.model_identifier,
                "messages": [{
                    "role": "user",
                    "content": "Write a Python function to implement quicksort algorithm. Only return the code, no explanation."
                }],
                "max_tokens": 500
            }
            
            start_time = time.time()
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{channel.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
            end_time = time.time()
            
            response_time_ms = int((end_time - start_time) * 1000)
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # 简单的质量评分：检查是否包含关键代码元素
                quality_score = self._evaluate_code_quality(content)
                
                return {
                    "success": True,
                    "response_time_ms": response_time_ms,
                    "quality_score": quality_score,
                    "error_message": None
                }
            else:
                return {
                    "success": False,
                    "response_time_ms": response_time_ms,
                    "quality_score": None,
                    "error_message": f"HTTP {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "response_time_ms": None,
                "quality_score": None,
                "error_message": str(e)
            }
    
    async def _test_tool_calling(self, model: db_models.Model, channel: db_models.Channel) -> Dict[str, Any]:
        """工具调用支持测试"""
        if not model.supports_tools:
            return {
                "success": False,
                "response_time_ms": None,
                "quality_score": None,
                "error_message": "Model does not support tool calling"
            }
        
        try:
            headers = self._build_headers(channel)
            payload = {
                "model": model.model_identifier,
                "messages": [{
                    "role": "user",
                    "content": "What's the weather like in San Francisco?"
                }],
                "tools": [{
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "Get the current weather in a location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {"type": "string", "description": "The city name"}
                            },
                            "required": ["location"]
                        }
                    }
                }],
                "max_tokens": 200
            }
            
            start_time = time.time()
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{channel.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
            end_time = time.time()
            
            response_time_ms = int((end_time - start_time) * 1000)
            
            if response.status_code == 200:
                data = response.json()
                tool_calls = data.get("choices", [{}])[0].get("message", {}).get("tool_calls", [])
                
                # 检查是否正确调用了工具
                quality_score = 1.0 if tool_calls else 0.5
                
                return {
                    "success": True,
                    "response_time_ms": response_time_ms,
                    "quality_score": quality_score,
                    "error_message": None
                }
            else:
                return {
                    "success": False,
                    "response_time_ms": response_time_ms,
                    "quality_score": None,
                    "error_message": f"HTTP {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "response_time_ms": None,
                "quality_score": None,
                "error_message": str(e)
            }
    
    def _build_headers(self, channel: db_models.Channel) -> Dict[str, str]:
        """构建请求头"""
        headers = {"Content-Type": "application/json"}
        
        if channel.api_key:
            if channel.auth_type == "bearer":
                headers["Authorization"] = f"Bearer {channel.api_key}"
            else:
                headers["Authorization"] = channel.api_key
        
        if channel.headers:
            headers.update(channel.headers)
        
        return headers
    
    def _evaluate_code_quality(self, code: str) -> float:
        """评估代码质量（简单版本）"""
        score = 0.0
        
        # 检查是否包含函数定义
        if "def " in code:
            score += 0.3
        
        # 检查是否包含快速排序的关键元素
        if "pivot" in code.lower() or "partition" in code.lower():
            score += 0.3
        
        # 检查是否有递归调用
        if code.count("quicksort") >= 2 or code.count("sort") >= 2:
            score += 0.2
        
        # 检查是否有返回语句
        if "return" in code:
            score += 0.2
        
        return min(score, 1.0)
    
    def _save_test_result(self, model_id: int, test_type: str, result: Dict[str, Any]):
        """保存测试结果"""
        test_result = db_models.TestResult(
            model_id=model_id,
            test_type=test_type,
            success=result["success"],
            response_time_ms=result["response_time_ms"],
            quality_score=result["quality_score"],
            error_message=result["error_message"]
        )
        self.db.add(test_result)
