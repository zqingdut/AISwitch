#!/usr/bin/env python3
"""
AISwitch 端到端测试
模拟用户完整操作流程
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def print_step(step, desc):
    print(f"\n{'='*60}")
    print(f"步骤 {step}: {desc}")
    print('='*60)

def test_frontend_accessible():
    """测试前端是否可访问"""
    print_step(1, "测试前端可访问性")
    try:
        res = requests.get(FRONTEND_URL, timeout=5)
        if res.status_code == 200:
            print("✅ 前端页面可访问")
            return True
        else:
            print(f"❌ 前端返回状态码: {res.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端无法访问: {e}")
        return False

def test_backend_health():
    """测试后端健康状态"""
    print_step(2, "测试后端健康状态")
    try:
        res = requests.get(f"{BASE_URL}/health", timeout=5)
        if res.status_code != 200:
            print(f"❌ 后端返回状态码: {res.status_code}")
            return False
        
        data = res.json()
        print(f"✅ 后端健康状态: {data['status']}")
        
        # 详细健康检查
        res = requests.get(f"{BASE_URL}/api/monitoring/health/detailed", timeout=5)
        if res.status_code == 200:
            health = res.json()
            print(f"   - 数据库: {health['checks']['database']['status']}")
            print(f"   - CPU: {health['checks']['system']['cpu_percent']}%")
            print(f"   - 内存: {health['checks']['system']['memory_percent']}%")
            print(f"   - 活跃模型: {health['checks']['models']['active_models']}")
        return True
    except Exception as e:
        print(f"❌ 后端健康检查失败: {e}")
        return False

def test_channel_crud():
    """测试渠道 CRUD 操作"""
    print_step(3, "测试渠道管理功能")
    
    # 1. 获取现有渠道
    res = requests.get(f"{BASE_URL}/api/channels/")
    if res.status_code != 200:
        print(f"❌ 获取渠道列表失败: {res.status_code}")
        return False
    
    channels_before = res.json()
    print(f"📊 当前渠道数量: {len(channels_before)}")
    
    # 2. 创建新渠道
    new_channel = {
        "name": "测试渠道E2E",
        "base_url": "https://api.test-e2e.com/v1",
        "api_key": "sk-e2e-test",
        "is_active": True
    }
    res = requests.post(f"{BASE_URL}/api/channels/", json=new_channel)
    if res.status_code == 200:
        channel = res.json()
        channel_id = channel['id']
        print(f"✅ 创建渠道成功: {channel['name']} (ID: {channel_id})")
    else:
        print(f"❌ 创建渠道失败: {res.status_code}")
        return False
    
    # 3. 更新渠道
    update_data = {"name": "测试渠道E2E-已更新"}
    res = requests.put(f"{BASE_URL}/api/channels/{channel_id}/", json=update_data)
    if res.status_code == 200:
        print(f"✅ 更新渠道成功")
    else:
        print(f"❌ 更新渠道失败")
        return False
    
    # 4. 删除渠道
    res = requests.delete(f"{BASE_URL}/api/channels/{channel_id}/")
    if res.status_code == 200:
        print(f"✅ 删除渠道成功")
    else:
        print(f"❌ 删除渠道失败")
        return False
    
    return True

def test_model_crud():
    """测试模型 CRUD 操作"""
    print_step(4, "测试模型管理功能")
    
    # 获取一个渠道 ID
    res = requests.get(f"{BASE_URL}/api/channels/")
    channels = res.json()
    if not channels:
        print("❌ 没有可用的渠道")
        return False
    
    channel_id = channels[0]['id']
    
    # 1. 创建模型
    new_model = {
        "name": "测试模型E2E",
        "model_identifier": "test-model-e2e",
        "channel_id": channel_id,
        "display_name": "测试模型 E2E",
        "context_window": 8192,
        "supports_tools": True,
        "is_active": True
    }
    res = requests.post(f"{BASE_URL}/api/models/", json=new_model)
    if res.status_code == 200:
        model = res.json()
        model_id = model['id']
        print(f"✅ 创建模型成功: {model['name']} (ID: {model_id})")
    else:
        print(f"❌ 创建模型失败: {res.status_code} - {res.text}")
        return False
    
    # 2. 获取模型列表
    res = requests.get(f"{BASE_URL}/api/models/")
    models = res.json()
    print(f"📊 当前模型数量: {len(models)}")
    
    # 3. 删除测试模型
    res = requests.delete(f"{BASE_URL}/api/models/{model_id}/")
    if res.status_code == 200:
        print(f"✅ 删除模型成功")
    else:
        print(f"❌ 删除模型失败")
        return False
    
    return True

def test_model_ranking():
    """测试模型排名功能"""
    print_step(5, "测试模型排名功能")
    
    res = requests.get(f"{BASE_URL}/api/models/ranking")
    if res.status_code == 200:
        rankings = res.json()
        print(f"📊 排名模型数量: {len(rankings)}")
        for i, model in enumerate(rankings[:3], 1):
            print(f"   {i}. {model['name']} - 分数: {model['score']}")
        return True
    else:
        print(f"❌ 获取排名失败: {res.status_code}")
        return False

def test_config_generation():
    """测试配置生成功能"""
    print_step(6, "测试配置生成功能")
    
    res = requests.post(f"{BASE_URL}/api/config/generate")
    if res.status_code == 200:
        config = res.json()
        print(f"✅ 配置生成成功")
        print(f"   配置长度: {len(config['config'])} 字符")
        return True
    else:
        print(f"❌ 配置生成失败: {res.status_code}")
        return False

def test_monitoring_metrics():
    """测试监控指标"""
    print_step(7, "测试监控指标")
    
    res = requests.get(f"{BASE_URL}/api/monitoring/metrics")
    if res.status_code == 200:
        metrics = res.json()
        print(f"✅ 监控指标获取成功")
        print(f"   渠道: {metrics['channels']['total']} 总数, {metrics['channels']['active']} 活跃")
        print(f"   模型: {metrics['models']['total']} 总数, {metrics['models']['active']} 活跃")
        print(f"   测试: 最近24小时 {metrics['tests']['last_24h']} 次, 成功率 {metrics['tests']['success_rate']}%")
        return True
    else:
        print(f"❌ 获取监控指标失败: {res.status_code}")
        return False

def main():
    print("\n" + "="*60)
    print("AISwitch 端到端测试")
    print("="*60)
    
    results = []
    
    # 执行所有测试
    results.append(("前端可访问性", test_frontend_accessible()))
    results.append(("后端健康状态", test_backend_health()))
    results.append(("渠道管理", test_channel_crud()))
    results.append(("模型管理", test_model_crud()))
    results.append(("模型排名", test_model_ranking()))
    results.append(("配置生成", test_config_generation()))
    results.append(("监控指标", test_monitoring_metrics()))
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统运行正常。")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查。")
        return 1

if __name__ == "__main__":
    exit(main())
