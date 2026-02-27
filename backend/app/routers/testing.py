from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.db.database import get_db
from app.models import database as db_models
from app.models import schemas
from app.services.tester import ModelTester
from app.services.enhanced_tester import EnhancedModelTester
from app.services.ranker import ModelRanker

router = APIRouter()

class TestRequest(BaseModel):
    model_ids: List[int]
    test_type: str = "speed"

@router.post("/run")
async def run_tests(
    request: TestRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """运行模型测试"""
    if not request.model_ids:
        raise HTTPException(status_code=400, detail="No models specified")
    
    # 验证模型存在
    models = db.query(db_models.Model).filter(
        db_models.Model.id.in_(request.model_ids)
    ).all()
    
    if len(models) != len(request.model_ids):
        raise HTTPException(status_code=404, detail="Some models not found")
    
    # 使用 Celery 异步任务
    from app.tasks import test_model_async
    
    for model_id in request.model_ids:
        test_model_async.delay(model_id, request.test_type)
    
    return {
        "message": f"Tests started for {len(request.model_ids)} models",
        "model_ids": request.model_ids,
        "test_type": request.test_type
    }

@router.get("/results")
def get_test_results(
    model_id: int = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """获取测试结果"""
    query = db.query(
        db_models.TestResult,
        db_models.Model.name.label('model_name')
    ).join(db_models.Model)
    
    if model_id:
        query = query.filter(db_models.TestResult.model_id == model_id)
    
    results = query.order_by(
        db_models.TestResult.tested_at.desc()
    ).limit(limit).all()
    
    return [
        {
            "model_id": r.TestResult.model_id,
            "model_name": r.model_name,
            "test_type": r.TestResult.test_type,
            "success": r.TestResult.success,
            "response_time": r.TestResult.response_time_ms / 1000 if r.TestResult.response_time_ms else None,
            "error_message": r.TestResult.error_message,
            "created_at": r.TestResult.tested_at.isoformat()
        }
        for r in results
    ]

@router.get("/health/{model_id}")
def get_model_health(model_id: int, db: Session = Depends(get_db)):
    """获取模型健康状态"""
    model = db.query(db_models.Model).filter(db_models.Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # 获取最近的测试结果
    recent_results = db.query(db_models.TestResult).filter(
        db_models.TestResult.model_id == model_id
    ).order_by(db_models.TestResult.tested_at.desc()).limit(10).all()
    
    if not recent_results:
        return {
            "model_id": model_id,
            "status": "unknown",
            "message": "No test results available"
        }
    
    # 计算成功率
    success_count = sum(1 for r in recent_results if r.success)
    success_rate = success_count / len(recent_results)
    
    # 计算平均响应时间
    response_times = [r.response_time_ms for r in recent_results if r.response_time_ms]
    avg_response_time = sum(response_times) / len(response_times) if response_times else None
    
    status = "healthy" if success_rate >= 0.8 else "degraded" if success_rate >= 0.5 else "unhealthy"
    
    return {
        "model_id": model_id,
        "model_name": model.name,
        "status": status,
        "success_rate": success_rate,
        "avg_response_time_ms": avg_response_time,
        "recent_tests": len(recent_results)
    }

@router.post("/update-rankings")
async def update_rankings(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """更新模型排名"""
    ranker = ModelRanker(db)
    background_tasks.add_task(ranker.update_all_rankings)
    
    return {"message": "Ranking update triggered", "status": "running"}
