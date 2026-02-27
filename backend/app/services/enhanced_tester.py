"""
增强的模型测试引擎
使用真实 AI API 进行测试
"""

from sqlalchemy.orm import Session
from app.models import database as db_models
from app.services.ai_client import AIAPIClient
from typing import Dict, Any
import asyncio


class EnhancedModelTester:
    """增强的模型测试引擎"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def test_model(self, model_id: int, test_type: str = "speed"):
        """测试单个模型"""
        model = self.db.query(db_models.Model).filter(
            db_models.Model.id == model_id
        ).first()
        
        if not model:
            return
        
        channel = model.channel
        if not channel or not channel.is_active:
            return
        
        # 创建 AI 客户端
        client = AIAPIClient(channel)
        
        # 根据测试类型执行测试
        if test_type == "speed":
            result = await client.test_speed(model.model_identifier)
            self._save_test_result(model_id, "speed", result)
        
        elif test_type == "code":
            result = await client.test_code_generation(model.model_identifier)
            self._save_test_result(model_id, "code", result)
        
        elif test_type == "tool":
            result = await client.test_tool_calling(model.model_identifier)
            self._save_test_result(model_id, "tool", result)
        
        else:
            # 执行所有测试
            speed_result = await client.test_speed(model.model_identifier)
            self._save_test_result(model_id, "speed", speed_result)
            
            code_result = await client.test_code_generation(model.model_identifier)
            self._save_test_result(model_id, "code", code_result)
            
            if model.supports_tools:
                tool_result = await client.test_tool_calling(model.model_identifier)
                self._save_test_result(model_id, "tool", tool_result)
        
        self.db.commit()
    
    def _save_test_result(self, model_id: int, test_type: str, result: Dict[str, Any]):
        """保存测试结果"""
        test_result = db_models.TestResult(
            model_id=model_id,
            test_type=test_type,
            success=result.get("success", False),
            response_time_ms=int(result.get("response_time", 0) * 1000),
            quality_score=result.get("quality_score"),
            error_message=result.get("error")
        )
        self.db.add(test_result)
    
    async def test_multiple_models(self, model_ids: list, test_type: str = "speed"):
        """批量测试多个模型"""
        tasks = []
        for model_id in model_ids:
            task = self.test_model(model_id, test_type)
            tasks.append(task)
        
        await asyncio.gather(*tasks, return_exceptions=True)
