from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from app.db.database import get_db
from app.models import database as db_models
from app.models import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Model])
def get_models(
    channel_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取所有模型"""
    query = db.query(db_models.Model)
    if channel_id:
        query = query.filter(db_models.Model.channel_id == channel_id)
    models = query.offset(skip).limit(limit).all()
    return models

@router.get("/ranking")
def get_model_rankings(db: Session = Depends(get_db)):
    """获取模型排名"""
    models = db.query(db_models.Model).join(
        db_models.ModelRanking,
        db_models.Model.id == db_models.ModelRanking.model_id,
        isouter=True
    ).join(
        db_models.Channel
    ).order_by(
        db_models.ModelRanking.rank.asc()
    ).all()
    
    result = []
    for model in models:
        ranking = model.ranking
        result.append({
            "id": model.id,
            "name": model.name,
            "model_identifier": model.model_identifier,
            "rank": ranking.rank if ranking else 999,
            "score": ranking.overall_score if ranking else 0,
            "channel": {
                "name": model.channel.name,
                "base_url": model.channel.base_url
            }
        })
    
    return result

@router.get("/{model_id}", response_model=schemas.Model)
def get_model(model_id: int, db: Session = Depends(get_db)):
    """获取单个模型"""
    model = db.query(db_models.Model).filter(db_models.Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model

@router.post("/", response_model=schemas.Model)
def create_model(model: schemas.ModelCreate, db: Session = Depends(get_db)):
    """创建新模型"""
    # 检查渠道是否存在
    channel = db.query(db_models.Channel).filter(db_models.Channel.id == model.channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    db_model = db_models.Model(**model.model_dump())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

@router.put("/{model_id}", response_model=schemas.Model)
def update_model(model_id: int, model: schemas.ModelUpdate, db: Session = Depends(get_db)):
    """更新模型"""
    db_model = db.query(db_models.Model).filter(db_models.Model.id == model_id).first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    update_data = model.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_model, key, value)
    
    db.commit()
    db.refresh(db_model)
    return db_model

@router.post("/batch", response_model=List[schemas.Model])
def create_models_batch(batch: schemas.ModelBatchCreate, db: Session = Depends(get_db)):
    """批量创建模型"""
    # 检查渠道是否存在
    channel = db.query(db_models.Channel).filter(db_models.Channel.id == batch.channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    db_models_list = []
    for model_data in batch.models:
        db_model = db_models.Model(
            channel_id=batch.channel_id,
            **model_data.model_dump()
        )
        db_models_list.append(db_model)
    
    db.add_all(db_models_list)
    db.commit()
    
    for model in db_models_list:
        db.refresh(model)
    
    return db_models_list

@router.post("/import")
async def import_models_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """从 CSV 文件导入模型
    CSV 格式: name,model_identifier,channel_id,is_active
    """
    # 读取 CSV
    content = await file.read()
    csv_file = io.StringIO(content.decode('utf-8'))
    reader = csv.DictReader(csv_file)
    
    db_models_list = []
    errors = []
    
    for idx, row in enumerate(reader, start=2):  # 从第2行开始（第1行是标题）
        try:
            # 验证必填字段
            if not row.get('name') or not row.get('model_identifier') or not row.get('channel_id'):
                errors.append(f"Row {idx}: Missing required fields (name, model_identifier, channel_id)")
                continue
            
            channel_id = int(row['channel_id'])
            
            # 检查渠道是否存在
            channel = db.query(db_models.Channel).filter(db_models.Channel.id == channel_id).first()
            if not channel:
                errors.append(f"Row {idx}: Channel {channel_id} not found")
                continue
            
            db_model = db_models.Model(
                name=row['name'],
                model_identifier=row['model_identifier'],
                channel_id=channel_id,
                display_name=row.get('display_name'),
                context_window=int(row['context_window']) if row.get('context_window') else None,
                max_tokens=int(row['max_tokens']) if row.get('max_tokens') else None,
                supports_tools=row.get('supports_tools', '').lower() in ['true', '1', 'yes'],
                supports_vision=row.get('supports_vision', '').lower() in ['true', '1', 'yes'],
                cost_input=float(row['cost_input']) if row.get('cost_input') else None,
                cost_output=float(row['cost_output']) if row.get('cost_output') else None,
                is_active=row.get('is_active', 'true').lower() in ['true', '1', 'yes']
            )
            db_models_list.append(db_model)
        except Exception as e:
            errors.append(f"Row {idx}: {str(e)}")
    
    if db_models_list:
        db.add_all(db_models_list)
        db.commit()
    
    return {
        "message": f"Imported {len(db_models_list)} models successfully",
        "imported": len(db_models_list),
        "errors": errors if errors else None
    }

@router.delete("/{model_id}")
def delete_model(model_id: int, db: Session = Depends(get_db)):
    """删除模型"""
    db_model = db.query(db_models.Model).filter(db_models.Model.id == model_id).first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    db.delete(db_model)
    db.commit()
    return {"message": "Model deleted successfully"}
