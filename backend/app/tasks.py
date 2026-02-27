"""
异步任务定义
"""

from app.celery_app import celery_app
from app.db.database import SessionLocal
from app.services.enhanced_tester import EnhancedModelTester
from app.services.ranker import ModelRanker
import asyncio


@celery_app.task(name="test_model_async")
def test_model_async(model_id: int, test_type: str = "speed"):
    """异步测试模型"""
    db = SessionLocal()
    try:
        tester = EnhancedModelTester(db)
        asyncio.run(tester.test_model(model_id, test_type))
        return {"status": "success", "model_id": model_id}
    except Exception as e:
        return {"status": "error", "model_id": model_id, "error": str(e)}
    finally:
        db.close()


@celery_app.task(name="update_rankings_async")
def update_rankings_async():
    """异步更新排名"""
    db = SessionLocal()
    try:
        ranker = ModelRanker(db)
        ranker.update_all_rankings()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    finally:
        db.close()


@celery_app.task(name="scheduled_test_all_models")
def scheduled_test_all_models():
    """定时测试所有模型"""
    from app.models.database import Model
    
    db = SessionLocal()
    try:
        models = db.query(Model).filter(Model.is_active == True).all()
        
        for model in models:
            test_model_async.delay(model.id, "speed")
        
        return {"status": "success", "models_count": len(models)}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    finally:
        db.close()


# 定时任务配置
celery_app.conf.beat_schedule = {
    "test-all-models-every-hour": {
        "task": "scheduled_test_all_models",
        "schedule": 3600.0,  # 每小时执行一次
    },
    "update-rankings-every-30min": {
        "task": "update_rankings_async",
        "schedule": 1800.0,  # 每30分钟执行一次
    },
}
