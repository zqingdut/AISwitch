from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    base_url = Column(String(500), nullable=False)
    api_key = Column(Text)
    auth_type = Column(String(50), default="bearer")
    headers = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    models = relationship("Model", back_populates="channel", cascade="all, delete-orphan")

class Model(Base):
    __tablename__ = "models"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    name = Column(String(200), nullable=False)
    model_identifier = Column(String(200), nullable=False)
    display_name = Column(String(200))
    context_window = Column(Integer)
    max_tokens = Column(Integer)
    supports_tools = Column(Boolean, default=False)
    supports_vision = Column(Boolean, default=False)
    cost_input = Column(Float)
    cost_output = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    channel = relationship("Channel", back_populates="models")
    test_results = relationship("TestResult", back_populates="model", cascade="all, delete-orphan")
    ranking = relationship("ModelRanking", back_populates="model", uselist=False, cascade="all, delete-orphan")

class TestResult(Base):
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    test_type = Column(String(50), nullable=False)  # speed, code, tools
    success = Column(Boolean, nullable=False)
    response_time_ms = Column(Integer)
    quality_score = Column(Float)
    error_message = Column(Text)
    tested_at = Column(DateTime(timezone=True), server_default=func.now())
    
    model = relationship("Model", back_populates="test_results")

class ModelRanking(Base):
    __tablename__ = "model_rankings"
    
    model_id = Column(Integer, ForeignKey("models.id"), primary_key=True)
    overall_score = Column(Float)
    availability_score = Column(Float)
    speed_score = Column(Float)
    quality_score = Column(Float)
    rank = Column(Integer)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    model = relationship("Model", back_populates="ranking")
