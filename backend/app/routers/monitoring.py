"""
监控和健康检查
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db
from app.models import database as db_models
from datetime import datetime, timedelta
import psutil
import time

router = APIRouter()


@router.get("/health")
async def health_check():
    """基础健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.1.0"
    }


@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """详细健康检查"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    # 数据库检查
    try:
        db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "Database connection OK"
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": str(e)
        }
    
    # 系统资源检查
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_status["checks"]["system"] = {
            "status": "healthy",
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": disk.percent
        }
        
        # 资源告警
        if cpu_percent > 80 or memory.percent > 80 or disk.percent > 80:
            health_status["status"] = "degraded"
    
    except Exception as e:
        health_status["checks"]["system"] = {
            "status": "error",
            "message": str(e)
        }
    
    # 模型健康检查
    try:
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_tests = db.query(db_models.TestResult).filter(
            db_models.TestResult.tested_at >= one_hour_ago
        ).count()
        
        active_models = db.query(db_models.Model).filter(
            db_models.Model.is_active == True
        ).count()
        
        health_status["checks"]["models"] = {
            "status": "healthy",
            "active_models": active_models,
            "recent_tests": recent_tests
        }
    
    except Exception as e:
        health_status["checks"]["models"] = {
            "status": "error",
            "message": str(e)
        }
    
    return health_status


@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    """获取系统指标"""
    # 统计数据
    total_channels = db.query(db_models.Channel).count()
    active_channels = db.query(db_models.Channel).filter(
        db_models.Channel.is_active == True
    ).count()
    
    total_models = db.query(db_models.Model).count()
    active_models = db.query(db_models.Model).filter(
        db_models.Model.is_active == True
    ).count()
    
    total_tests = db.query(db_models.TestResult).count()
    
    # 最近24小时的测试
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    recent_tests = db.query(db_models.TestResult).filter(
        db_models.TestResult.tested_at >= one_day_ago
    ).count()
    
    successful_tests = db.query(db_models.TestResult).filter(
        db_models.TestResult.tested_at >= one_day_ago,
        db_models.TestResult.success == True
    ).count()
    
    success_rate = (successful_tests / recent_tests * 100) if recent_tests > 0 else 0
    
    return {
        "channels": {
            "total": total_channels,
            "active": active_channels
        },
        "models": {
            "total": total_models,
            "active": active_models
        },
        "tests": {
            "total": total_tests,
            "last_24h": recent_tests,
            "success_rate": round(success_rate, 2)
        },
        "timestamp": datetime.utcnow().isoformat()
    }
