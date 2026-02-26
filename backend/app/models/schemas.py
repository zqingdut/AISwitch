from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Channel Schemas
class ChannelBase(BaseModel):
    name: str
    base_url: str
    api_key: Optional[str] = None
    auth_type: str = "bearer"
    headers: Optional[dict] = None
    is_active: bool = True

class ChannelCreate(ChannelBase):
    pass

class ChannelUpdate(BaseModel):
    name: Optional[str] = None
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    auth_type: Optional[str] = None
    headers: Optional[dict] = None
    is_active: Optional[bool] = None

class Channel(ChannelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Model Schemas
class ModelBase(BaseModel):
    name: str
    model_identifier: str
    display_name: Optional[str] = None
    context_window: Optional[int] = None
    max_tokens: Optional[int] = None
    supports_tools: bool = False
    supports_vision: bool = False
    cost_input: Optional[float] = None
    cost_output: Optional[float] = None
    is_active: bool = True

class ModelCreate(ModelBase):
    channel_id: int

class ModelUpdate(BaseModel):
    name: Optional[str] = None
    model_identifier: Optional[str] = None
    display_name: Optional[str] = None
    context_window: Optional[int] = None
    max_tokens: Optional[int] = None
    supports_tools: Optional[bool] = None
    supports_vision: Optional[bool] = None
    cost_input: Optional[float] = None
    cost_output: Optional[float] = None
    is_active: Optional[bool] = None

class ModelBatchCreate(BaseModel):
    channel_id: int
    models: List[ModelBase]

class Model(ModelBase):
    id: int
    channel_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Test Result Schemas
class TestResultBase(BaseModel):
    test_type: str
    success: bool
    response_time_ms: Optional[int] = None
    quality_score: Optional[float] = None
    error_message: Optional[str] = None

class TestResult(TestResultBase):
    id: int
    model_id: int
    tested_at: datetime
    
    class Config:
        from_attributes = True

# Model Ranking Schemas
class ModelRanking(BaseModel):
    model_id: int
    overall_score: float
    availability_score: float
    speed_score: float
    quality_score: float
    rank: int
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ModelWithRanking(Model):
    ranking: Optional[ModelRanking] = None
    channel: Channel

# OpenClaw Config Schema
class OpenClawConfig(BaseModel):
    models: dict
    agents: dict
