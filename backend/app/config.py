"""
数据库配置管理
支持 SQLite 和 PostgreSQL
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    
    # 数据库配置 - 使用绝对路径避免启动目录问题
    DATABASE_URL: str = "sqlite:////Users/niko/projects/aiswitch/backend/aiswitch.db"
    
    # Redis 配置（可选）
    REDIS_URL: Optional[str] = None
    
    # API 配置
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    # CORS 配置
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Celery 配置（可选）
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
