from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models import database as db_models
from app.models import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Channel])
def get_channels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取所有渠道"""
    channels = db.query(db_models.Channel).offset(skip).limit(limit).all()
    return channels

@router.get("/{channel_id}", response_model=schemas.Channel)
def get_channel(channel_id: int, db: Session = Depends(get_db)):
    """获取单个渠道"""
    channel = db.query(db_models.Channel).filter(db_models.Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel

@router.post("/", response_model=schemas.Channel)
def create_channel(channel: schemas.ChannelCreate, db: Session = Depends(get_db)):
    """创建新渠道"""
    # 检查名称是否已存在
    existing = db.query(db_models.Channel).filter(db_models.Channel.name == channel.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Channel name already exists")
    
    db_channel = db_models.Channel(**channel.model_dump())
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

@router.put("/{channel_id}", response_model=schemas.Channel)
def update_channel(channel_id: int, channel: schemas.ChannelUpdate, db: Session = Depends(get_db)):
    """更新渠道"""
    db_channel = db.query(db_models.Channel).filter(db_models.Channel.id == channel_id).first()
    if not db_channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    update_data = channel.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_channel, key, value)
    
    db.commit()
    db.refresh(db_channel)
    return db_channel

@router.delete("/{channel_id}")
def delete_channel(channel_id: int, db: Session = Depends(get_db)):
    """删除渠道"""
    db_channel = db.query(db_models.Channel).filter(db_models.Channel.id == channel_id).first()
    if not db_channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    db.delete(db_channel)
    db.commit()
    return {"message": "Channel deleted successfully"}
