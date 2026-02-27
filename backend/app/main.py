from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.routers import channels, models, testing, config, monitoring

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AISwitch API",
    description="AI 模型聚合和智能切换平台",
    version="1.1.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(channels.router, prefix="/api/channels", tags=["channels"])
app.include_router(models.router, prefix="/api/models", tags=["models"])
app.include_router(testing.router, prefix="/api/test", tags=["testing"])
app.include_router(config.router, prefix="/api/config", tags=["config"])
app.include_router(monitoring.router, prefix="/api/monitoring", tags=["monitoring"])

@app.get("/")
async def root():
    return {
        "message": "AISwitch API",
        "version": "1.1.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.1.0"}
