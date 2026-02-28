from sqlalchemy.orm import Session
from app.models import database as db_models
from typing import Dict, Any, List

class OpenClawConfigGenerator:
    """OpenClaw 配置生成器"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_config(self, top_n: int = 5) -> Dict[str, Any]:
        """生成 OpenClaw 配置（所有渠道）"""
        # 获取活跃模型（不依赖排名）
        top_models = self.db.query(db_models.Model).filter(
            db_models.Model.is_active == True
        ).limit(top_n).all()
        
        if not top_models:
            return {"error": "No active models available"}
        
        # 按渠道分组
        channels_dict = {}
        for model in top_models:
            channel = model.channel
            if not channel or not channel.is_active:
                continue
            if channel.id not in channels_dict:
                channels_dict[channel.id] = {
                    "channel": channel,
                    "models": []
                }
            channels_dict[channel.id]["models"].append(model)
        
        if not channels_dict:
            return {"error": "No active channels with models"}
        
        # 生成配置
        providers = {}
        for channel_id, data in channels_dict.items():
            channel = data["channel"]
            models = data["models"]
            
            provider_key = self._sanitize_name(channel.name)
            providers[provider_key] = {
                "baseUrl": channel.base_url,
                "apiKey": channel.api_key or "YOUR_API_KEY",
                "api": "openai-completions",
                "models": [self._format_model(m) for m in models]
            }
            
            if channel.headers:
                providers[provider_key]["headers"] = channel.headers
        
        # 设置主模型和备用模型
        primary_model = top_models[0]
        primary_provider = self._sanitize_name(primary_model.channel.name)
        primary_model_id = f"{primary_provider}/{primary_model.model_identifier}"
        
        fallbacks = []
        for model in top_models[1:]:
            provider = self._sanitize_name(model.channel.name)
            fallbacks.append(f"{provider}/{model.model_identifier}")
        
        config = {
            "models": {
                "providers": providers
            },
            "agents": {
                "defaults": {
                    "model": {
                        "primary": primary_model_id,
                        "fallbacks": fallbacks
                    }
                }
            }
        }
        
        return config
    
    def generate_config_for_channel(self, channel_id: int, top_n: int = 5) -> Dict[str, Any]:
        """为特定渠道生成 OpenClaw 配置"""
        channel = self.db.query(db_models.Channel).filter(
            db_models.Channel.id == channel_id
        ).first()
        
        if not channel:
            return {"error": "Channel not found"}
        
        # 获取该渠道的排名前 N 的模型
        models = self.db.query(db_models.Model).filter(
            db_models.Model.channel_id == channel_id
        ).join(
            db_models.ModelRanking,
            isouter=True
        ).order_by(
            db_models.ModelRanking.rank.asc()
        ).limit(top_n).all()
        
        if not models:
            return {"error": "No models available for this channel"}
        
        provider_key = self._sanitize_name(channel.name)
        
        config = {
            "models": {
                "providers": {
                    provider_key: {
                        "baseUrl": channel.base_url,
                        "apiKey": channel.api_key or "YOUR_API_KEY",
                        "api": "openai-completions",
                        "models": [self._format_model(m) for m in models]
                    }
                }
            },
            "agents": {
                "defaults": {
                    "model": {
                        "primary": f"{provider_key}/{models[0].model_identifier}",
                        "fallbacks": [f"{provider_key}/{m.model_identifier}" for m in models[1:]]
                    }
                }
            }
        }
        
        if channel.headers:
            config["models"]["providers"][provider_key]["headers"] = channel.headers
        
        return config
    
    def _format_model(self, model: db_models.Model) -> Dict[str, Any]:
        """格式化模型配置"""
        model_config = {
            "id": model.model_identifier,
            "name": model.display_name or model.name,
            "reasoning": False,
            "input": ["text"]
        }
        
        if model.supports_vision:
            model_config["input"].append("image")
        
        if model.context_window:
            model_config["contextWindow"] = model.context_window
        
        if model.max_tokens:
            model_config["maxTokens"] = model.max_tokens
        
        if model.cost_input is not None or model.cost_output is not None:
            model_config["cost"] = {
                "input": model.cost_input or 0,
                "output": model.cost_output or 0,
                "cacheRead": 0,
                "cacheWrite": 0
            }
        
        return model_config
    
    def _sanitize_name(self, name: str) -> str:
        """清理名称，使其适合作为配置键"""
        return name.lower().replace(" ", "-").replace("_", "-")
