#!/usr/bin/env python3
"""AISwitch API 测试脚本"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ 健康检查通过")

def test_create_channel():
    """测试创建渠道"""
    print("\n🔍 测试创建渠道...")
    channel_data = {
        "name": "OpenRouter",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": "sk-or-test-key",
        "auth_type": "bearer"
    }
    response = requests.post(f"{BASE_URL}/api/channels/", json=channel_data)
    assert response.status_code == 200
    channel = response.json()
    print(f"✅ 渠道创建成功: {channel['name']} (ID: {channel['id']})")
    return channel

def test_get_channels():
    """测试获取渠道列表"""
    print("\n🔍 测试获取渠道列表...")
    response = requests.get(f"{BASE_URL}/api/channels/")
    assert response.status_code == 200
    channels = response.json()
    print(f"✅ 获取到 {len(channels)} 个渠道")
    return channels

def test_create_model(channel_id):
    """测试创建模型"""
    print("\n🔍 测试创建单个模型...")
    model_data = {
        "channel_id": channel_id,
        "model_id": "gpt-4",
        "display_name": "GPT-4",
        "context_window": 128000,
        "max_tokens": 4096,
        "supports_tools": True,
        "supports_vision": False,
        "cost_input": 0.03,
        "cost_output": 0.06
    }
    response = requests.post(f"{BASE_URL}/api/models/", json=model_data)
    assert response.status_code == 200
    model = response.json()
    print(f"✅ 模型创建成功: {model['display_name']} (ID: {model['id']})")
    return model

def test_batch_create_models(channel_id):
    """测试批量创建模型"""
    print("\n🔍 测试批量创建模型...")
    batch_data = {
        "channel_id": channel_id,
        "models": [
            {
                "model_id": "claude-3-opus",
                "display_name": "Claude 3 Opus",
                "context_window": 200000,
                "max_tokens": 4096,
                "supports_tools": True,
                "cost_input": 0.015,
                "cost_output": 0.075
            },
            {
                "model_id": "gemini-pro",
                "display_name": "Gemini Pro",
                "context_window": 32000,
                "max_tokens": 2048,
                "supports_tools": True,
                "cost_input": 0.0005,
                "cost_output": 0.0015
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/api/models/batch", json=batch_data)
    assert response.status_code == 200
    models = response.json()
    print(f"✅ 批量创建成功: {len(models)} 个模型")
    return models

def test_get_models():
    """测试获取模型列表"""
    print("\n🔍 测试获取模型列表...")
    response = requests.get(f"{BASE_URL}/api/models/")
    assert response.status_code == 200
    models = response.json()
    print(f"✅ 获取到 {len(models)} 个模型")
    for model in models:
        print(f"   - {model['display_name']} ({model['model_id']})")
    return models

def test_trigger_test(model_id):
    """测试触发模型测试"""
    print(f"\n🔍 测试触发模型测试 (ID: {model_id})...")
    response = requests.post(f"{BASE_URL}/api/test/trigger/{model_id}")
    assert response.status_code == 200
    result = response.json()
    print(f"✅ 测试已触发: {result['message']}")
    return result

def test_get_model_health(model_id):
    """测试获取模型健康状态"""
    print(f"\n🔍 测试获取模型健康状态 (ID: {model_id})...")
    response = requests.get(f"{BASE_URL}/api/test/health/{model_id}")
    assert response.status_code == 200
    health = response.json()
    print(f"✅ 健康状态: {health['status']}")
    return health

def test_update_rankings():
    """测试更新排名"""
    print("\n🔍 测试更新模型排名...")
    response = requests.post(f"{BASE_URL}/api/test/update-rankings")
    assert response.status_code == 200
    result = response.json()
    print(f"✅ 排名更新已触发: {result['message']}")
    return result

def test_get_rankings():
    """测试获取排名"""
    print("\n🔍 测试获取模型排名...")
    response = requests.get(f"{BASE_URL}/api/models/ranking")
    assert response.status_code == 200
    rankings = response.json()
    print(f"✅ 获取到 {len(rankings)} 个模型排名")
    return rankings

def test_generate_openclaw_config():
    """测试生成 OpenClaw 配置"""
    print("\n🔍 测试生成 OpenClaw 配置...")
    response = requests.get(f"{BASE_URL}/api/config/openclaw?top_n=3")
    assert response.status_code == 200
    config = response.json()
    print("✅ OpenClaw 配置生成成功")
    print(json.dumps(config, indent=2))
    return config

def main():
    """运行所有测试"""
    print("=" * 60)
    print("AISwitch API 功能测试")
    print("=" * 60)
    
    try:
        # 1. 健康检查
        test_health()
        
        # 2. 创建渠道
        channel = test_create_channel()
        
        # 3. 获取渠道列表
        test_get_channels()
        
        # 4. 创建单个模型
        test_create_model(channel["id"])
        
        # 5. 批量创建模型
        test_batch_create_models(channel["id"])
        
        # 6. 获取模型列表
        models = test_get_models()
        
        # 7. 触发测试（只测试第一个模型）
        if models:
            test_trigger_test(models[0]["id"])
            time.sleep(2)  # 等待测试完成
            test_get_model_health(models[0]["id"])
        
        # 8. 更新排名
        test_update_rankings()
        time.sleep(1)
        
        # 9. 获取排名
        test_get_rankings()
        
        # 10. 生成 OpenClaw 配置
        test_generate_openclaw_config()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
