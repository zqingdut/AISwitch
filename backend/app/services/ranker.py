from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import database as db_models
from datetime import datetime, timedelta
from typing import List

class ModelRanker:
    """模型排名算法"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def update_all_rankings(self):
        """更新所有模型的排名"""
        models = self.db.query(db_models.Model).all()
        
        rankings = []
        for model in models:
            score = self._calculate_overall_score(model)
            rankings.append((model.id, score))
        
        # 按分数排序
        rankings.sort(key=lambda x: x[1], reverse=True)
        
        # 更新排名
        for rank, (model_id, scores) in enumerate(rankings, start=1):
            self._update_ranking(model_id, rank, scores)
        
        self.db.commit()
    
    def _calculate_overall_score(self, model: db_models.Model) -> dict:
        """计算模型的综合评分"""
        # 获取最近1小时的测试结果
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_results = self.db.query(db_models.TestResult).filter(
            db_models.TestResult.model_id == model.id,
            db_models.TestResult.tested_at >= one_hour_ago
        ).all()
        
        if not recent_results:
            # 没有测试结果，返回默认低分
            return {
                "overall": 0.0,
                "availability": 0.0,
                "speed": 0.0,
                "quality": 0.0
            }
        
        # 计算可用性分数（40%）
        availability_score = self._calculate_availability_score(recent_results)
        
        # 计算速度分数（30%）
        speed_score = self._calculate_speed_score(recent_results)
        
        # 计算质量分数（20%）
        quality_score = self._calculate_quality_score(recent_results)
        
        # 计算成本分数（10%）
        cost_score = self._calculate_cost_score(model)
        
        # 综合评分
        overall_score = (
            availability_score * 0.4 +
            speed_score * 0.3 +
            quality_score * 0.2 +
            cost_score * 0.1
        )
        
        return {
            "overall": overall_score,
            "availability": availability_score,
            "speed": speed_score,
            "quality": quality_score
        }
    
    def _calculate_availability_score(self, results: List[db_models.TestResult]) -> float:
        """计算可用性分数"""
        if not results:
            return 0.0
        
        success_count = sum(1 for r in results if r.success)
        return success_count / len(results)
    
    def _calculate_speed_score(self, results: List[db_models.TestResult]) -> float:
        """计算速度分数"""
        response_times = [r.response_time_ms for r in results if r.response_time_ms and r.success]
        
        if not response_times:
            return 0.0
        
        avg_response_time = sum(response_times) / len(response_times)
        
        # 速度评分：越快越好
        # < 1000ms: 1.0
        # 1000-3000ms: 0.8-1.0
        # 3000-5000ms: 0.5-0.8
        # > 5000ms: 0.0-0.5
        if avg_response_time < 1000:
            return 1.0
        elif avg_response_time < 3000:
            return 1.0 - (avg_response_time - 1000) / 2000 * 0.2
        elif avg_response_time < 5000:
            return 0.8 - (avg_response_time - 3000) / 2000 * 0.3
        else:
            return max(0.0, 0.5 - (avg_response_time - 5000) / 10000 * 0.5)
    
    def _calculate_quality_score(self, results: List[db_models.TestResult]) -> float:
        """计算质量分数"""
        quality_scores = [r.quality_score for r in results if r.quality_score is not None and r.success]
        
        if not quality_scores:
            return 0.0
        
        return sum(quality_scores) / len(quality_scores)
    
    def _calculate_cost_score(self, model: db_models.Model) -> float:
        """计算成本分数"""
        if model.cost_input is None or model.cost_output is None:
            return 0.5  # 未知成本，给中等分数
        
        # 假设平均输入1000 tokens，输出500 tokens
        avg_cost = model.cost_input * 1000 + model.cost_output * 500
        
        # 成本评分：越便宜越好
        # 免费: 1.0
        # < $0.01: 0.8-1.0
        # $0.01-0.05: 0.5-0.8
        # > $0.05: 0.0-0.5
        if avg_cost == 0:
            return 1.0
        elif avg_cost < 0.01:
            return 1.0 - avg_cost / 0.01 * 0.2
        elif avg_cost < 0.05:
            return 0.8 - (avg_cost - 0.01) / 0.04 * 0.3
        else:
            return max(0.0, 0.5 - (avg_cost - 0.05) / 0.1 * 0.5)
    
    def _update_ranking(self, model_id: int, rank: int, scores: dict):
        """更新模型排名"""
        ranking = self.db.query(db_models.ModelRanking).filter(
            db_models.ModelRanking.model_id == model_id
        ).first()
        
        if ranking:
            ranking.overall_score = scores["overall"]
            ranking.availability_score = scores["availability"]
            ranking.speed_score = scores["speed"]
            ranking.quality_score = scores["quality"]
            ranking.rank = rank
        else:
            ranking = db_models.ModelRanking(
                model_id=model_id,
                overall_score=scores["overall"],
                availability_score=scores["availability"],
                speed_score=scores["speed"],
                quality_score=scores["quality"],
                rank=rank
            )
            self.db.add(ranking)
