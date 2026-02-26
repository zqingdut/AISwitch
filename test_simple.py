#!/usr/bin/env python3
"""简化版 AISwitch 测试脚本 - 绕过代理"""
import urllib.request
import urllib.error
import json

BASE_URL = "http://localhost:8000"

def make_request(method, path, data=None):
    """发起 HTTP 请求"""
    url = f"{BASE_URL}{path}"
    
    if method == "GET":
        req = urllib.request.Request(url, method="GET")
    elif method == "POST":
        headers = {"Content-Type": "application/json"}
        json_data = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url, data=json_data, headers=headers, method="POST")
    else:
        raise ValueError(f"不支持的 HTTP 方法: {method}")
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode("utf-8")}
    except urllib.error.URLError as e:
        return 0, {"error": str(e.reason)}

def test_root():
    """测试根路径"""
    print("🔍 测试根路径...")
    status, data = make_request("GET", "/")
    if status == 200:
        print(f"✅ 根路径响应: {data}")
        return True
    else:
        print(f"❌ 根路径失败: HTTP {status}, {data}")
        return False

def test_health():
    """测试健康检查"""
    print("\n🔍 测试健康检查...")
    status, data = make_request("GET", "/health")
    if status == 200:
        print(f"✅ 健康检查通过: {data}")
        return True
    else:
        print(f"❌ 健康检查失败: HTTP {status}, {data}")
        return False

def test_create_channel():
    """测试创建渠道"""
    print("\n🔍 测试创建渠道...")
    data = {
        "name": "TestChannel",
        "base_url": "https://api.example.com/v1",
        "api_key": "test-api-key",
        "auth_type": "bearer"
    }
    status, response = make_request("POST", "/api/channels/", data)
    if status == 200:
        print(f"✅ 渠道创建成功: ID={response.get('id')}")
        return response
    elif status == 400 and "already exists" in str(response):
        print("✅ 渠道已存在")
        return {"id": 1, "name": "TestChannel"}
    else:
        print(f"❌ 渠道创建失败: HTTP {status}, {response}")
        return None

def test_get_channels():
    """测试获取渠道列表"""
    print("\n🔍 测试获取渠道列表...")
    status, data = make_request("GET", "/api/channels/")
    if status == 200:
        print(f"✅ 获取到 {len(data)} 个渠道")
        for ch in data:
            print(f"   - {ch['name']} (ID: {ch['id']})")
        return data
    else:
        print(f"❌ 获取渠道失败: HTTP {status}")
        return []

def test_create_model(channel_id):
    """测试创建模型"""
    print(f"\n🔍 测试创建模型 (Channel ID: {channel_id})...")
    data = {
        "channel_id": channel_id,
        "model_id": "gpt-4-test",
        "display_name": "GPT-4 Test",
        "context_window": 128000,
        "max_tokens": 4096,
        "supports_tools": True
    }
    status, response = make_request("POST", "/api/models/", data)
    if status == 200:
        print(f"✅ 模型创建成功: ID={response.get('id')}")
        return response
    else:
        print(f"❌ 模型创建失败: HTTP {status}, {response}")
        return None

def test_get_models():
    """测试获取模型列表"""
    print("\n🔍 测试获取模型列表...")
    status, data = make_request("GET", "/api/models/")
    if status == 200:
        print(f"✅ 获取到 {len(data)} 个模型")
        for m in data:
            print(f"   - {m.get('display_name', m['model_id'])}")
        return data
    else:
        print(f"❌ 获取模型失败: HTTP {status}")
        return []

def test_generate_config():
    """测试生成 OpenClaw 配置"""
    print("\n🔍 测试生成 OpenClaw 配置...")
    status, data = make_request("GET", "/api/config/openclaw?top_n=2")
    if status == 200:
        print("✅ OpenClaw 配置生成成功!")
        print("   Config Preview:")
        if "models" in data:
            providers = data["models"].get("providers", {})
            print(f"   - Providers: {list(providers.keys())}")
        if "agents" in data:
            defaults = data["agents"].get("defaults", {})
            model = defaults.get("model", {})
            print(f"   - Primary: {model.get('primary')}")
            print(f"   - Fallbacks: {model.get('fallbacks', [])}")
        return data
    else:
        print(f"❌ 配置生成失败: HTTP {status}, {data}")
        return None

def main():
    print("=" * 60)
    print("AISwitch API 简化测试 - 使用标准库 urllib")
    print("=" * 60)
    
    results = []
    
    # 1. 根路径
    results.append(("根路径", test_root()))
    
    # 2. 健康检查
    results.append(("健康检查", test_health()))
    
    # 3. 创建渠道
    channel = test_create_channel()
    results.append(("创建渠道", channel is not None))
    
    if channel:
        # 4. 获取渠道列表
        results.append(("获取渠道", len(test_get_channels()) > 0))
        
        # 5. 创建模型
        model = test_create_model(channel.get('id', 1))
        results.append(("创建模型", model is not None))
        
        if model:
            # 6. 获取模型列表
            models = test_get_models()
            results.append(("获取模型", len(models) > 0))
    
    # 7. 生成配置
    config = test_generate_config()
    results.append(("生成配置", config is not None))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    failed = sum(1 for _, result in results if not result)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:20s} {status}")
    
    print(f"\n总计: {passed} 通过, {failed} 失败")
    
    if failed == 0:
        print("\n🎉 所有测试通过！后端 API 功能正常！")
    else:
        print(f"\n⚠️ {failed} 个测试失败，需要修复")
    
    return failed == 0

if __name__ == "__main__":
    exit(0 if main() else 1)
