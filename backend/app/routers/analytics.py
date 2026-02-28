from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import List, Optional
from app.db.database import get_db
from app.models import database as db_models

router = APIRouter()

@router.get("/test-history")
def get_test_history(
    model_id: Optional[int] = None,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """获取测试历史趋势数据"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(
        func.date(db_models.TestResult.tested_at).label('date'),
        db_models.TestResult.test_type,
        func.count(db_models.TestResult.id).label('total'),
        func.sum(func.cast(db_models.TestResult.success, db_models.Integer)).label('success_count'),
        func.avg(db_models.TestResult.response_time_ms).label('avg_response_time')
    ).filter(
        db_models.TestResult.tested_at >= start_date
    )
    
    if model_id:
        query = query.filter(db_models.TestResult.model_id == model_id)
    
    results = query.group_by(
        func.date(db_models.TestResult.tested_at),
        db_models.TestResult.test_type
    ).order_by(
        func.date(db_models.TestResult.tested_at)
    ).all()
    
    return [
        {
            "date": r.date.isoformat(),
            "test_type": r.test_type,
            "total": r.total,
            "success_count": r.success_count or 0,
            "success_rate": (r.success_count or 0) / r.total if r.total > 0 else 0,
            "avg_response_time": round(r.avg_response_time, 2) if r.avg_response_time else None
        }
        for r in results
    ]

@router.get("/model-comparison")
def get_model_comparison(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """获取模型对比数据"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    results = db.query(
        db_models.Model.id,
        db_models.Model.name,
        func.count(db_models.TestResult.id).label('total_tests'),
        func.sum(func.cast(db_models.TestResult.success, db_models.Integer)).label('success_count'),
        func.avg(db_models.TestResult.response_time_ms).label('avg_response_time'),
        func.avg(db_models.TestResult.quality_score).label('avg_quality')
    ).join(
        db_models.TestResult
    ).filter(
        db_models.TestResult.tested_at >= start_date,
        db_models.Model.is_active == True
    ).group_by(
        db_models.Model.id,
        db_models.Model.name
    ).all()
    
    return [
        {
            "model_id": r.id,
            "model_name": r.name,
            "total_tests": r.total_tests,
            "success_count": r.success_count or 0,
            "success_rate": round((r.success_count or 0) / r.total_tests * 100, 2) if r.total_tests > 0 else 0,
            "avg_response_time": round(r.avg_response_time, 2) if r.avg_response_time else None,
            "avg_quality": round(r.avg_quality, 2) if r.avg_quality else None
        }
        for r in results
    ]

@router.get("/test-type-distribution")
def get_test_type_distribution(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """获取测试类型分布"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    results = db.query(
        db_models.TestResult.test_type,
        func.count(db_models.TestResult.id).label('count'),
        func.sum(func.cast(db_models.TestResult.success, db_models.Integer)).label('success_count')
    ).filter(
        db_models.TestResult.tested_at >= start_date
    ).group_by(
        db_models.TestResult.test_type
    ).all()
    
    return [
        {
            "test_type": r.test_type,
            "count": r.count,
            "success_count": r.success_count or 0,
            "success_rate": round((r.success_count or 0) / r.count * 100, 2) if r.count > 0 else 0
        }
        for r in results
    ]

@router.get("/performance-trends")
def get_performance_trends(
    model_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """获取单个模型的性能趋势"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # 验证模型存在
    model = db.query(db_models.Model).filter(db_models.Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    results = db.query(
        func.date(db_models.TestResult.tested_at).label('date'),
        func.count(db_models.TestResult.id).label('total'),
        func.sum(func.cast(db_models.TestResult.success, db_models.Integer)).label('success_count'),
        func.avg(db_models.TestResult.response_time_ms).label('avg_response_time'),
        func.min(db_models.TestResult.response_time_ms).label('min_response_time'),
        func.max(db_models.TestResult.response_time_ms).label('max_response_time')
    ).filter(
        db_models.TestResult.model_id == model_id,
        db_models.TestResult.tested_at >= start_date
    ).group_by(
        func.date(db_models.TestResult.tested_at)
    ).order_by(
        func.date(db_models.TestResult.tested_at)
    ).all()
    
    return {
        "model_id": model_id,
        "model_name": model.name,
        "trends": [
            {
                "date": r.date.isoformat(),
                "total": r.total,
                "success_count": r.success_count or 0,
                "success_rate": round((r.success_count or 0) / r.total * 100, 2) if r.total > 0 else 0,
                "avg_response_time": round(r.avg_response_time, 2) if r.avg_response_time else None,
                "min_response_time": r.min_response_time,
                "max_response_time": r.max_response_time
            }
            for r in results
        ]
    }
