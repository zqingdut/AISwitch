from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import database as db_models
from app.services.config_gen import OpenClawConfigGenerator
import json

router = APIRouter()

@router.post("/generate")
def generate_config(
    top_n: int = 5,
    db: Session = Depends(get_db)
):
    """生成 OpenClaw 配置"""
    generator = OpenClawConfigGenerator(db)
    config_dict = generator.generate_config(top_n=top_n)
    
    if "error" in config_dict:
        raise HTTPException(status_code=400, detail=config_dict["error"])
    
    # 转换为格式化的 JSON 字符串
    config_text = json.dumps(config_dict, indent=2, ensure_ascii=False)
    
    return {
        "config": config_text,
        "models_count": top_n
    }

@router.get("/generate/{channel_id}")
def generate_config_for_channel(
    channel_id: int,
    top_n: int = 5,
    db: Session = Depends(get_db)
):
    """为特定渠道生成 OpenClaw 配置"""
    channel = db.query(db_models.Channel).filter(db_models.Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    generator = OpenClawConfigGenerator(db)
    config_dict = generator.generate_config_for_channel(channel_id, top_n=top_n)
    
    if "error" in config_dict:
        raise HTTPException(status_code=400, detail=config_dict["error"])
    
    # 转换为格式化的 JSON 字符串
    config_text = json.dumps(config_dict, indent=2, ensure_ascii=False)
    
    return {
        "config": config_text,
        "channel": channel.name,
        "models_count": len(config_dict.get("models", {}).get("providers", {}).get(channel.name.lower(), {}).get("models", []))
    }
