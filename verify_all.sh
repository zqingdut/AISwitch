#!/bin/bash
# AISwitch 完整功能验证脚本

echo "=========================================="
echo "AISwitch 功能验证"
echo "=========================================="

BASE_URL="http://localhost:8000"

# 1. 健康检查
echo -e "\n1. 健康检查"
curl -s $BASE_URL/health | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅' if d.get('status')=='healthy' else '❌')"

# 2. 渠道列表
echo -e "\n2. 渠道列表"
curl -s $BASE_URL/api/channels/ | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'✅ {len(d)} 个渠道' if isinstance(d, list) else '❌')"

# 3. 模型列表
echo -e "\n3. 模型列表"
curl -s $BASE_URL/api/models/ | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'✅ {len(d)} 个模型' if isinstance(d, list) else '❌')"

# 4. 模型排名
echo -e "\n4. 模型排名"
curl -s $BASE_URL/api/models/ranking | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'✅ {len(d)} 个排名' if isinstance(d, list) else '❌')"

# 5. 配置生成
echo -e "\n5. 配置生成"
curl -s -X POST $BASE_URL/api/config/generate | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅' if 'config' in d else f'❌ {d.get(\"detail\", d)}')"

# 6. 监控健康
echo -e "\n6. 监控健康检查"
curl -s $BASE_URL/api/monitoring/health/detailed | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅' if d.get('status')=='healthy' else '❌')"

# 7. 监控指标
echo -e "\n7. 监控指标"
curl -s $BASE_URL/api/monitoring/metrics | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅' if 'channels' in d else '❌')"

# 8. 模型测试
echo -e "\n8. 模型测试"
curl -s -X POST $BASE_URL/api/test/run -H "Content-Type: application/json" -d '{"model_ids":[1],"test_type":"speed"}' | python3 -c "import sys,json; content=sys.stdin.read().strip(); d=json.loads(content) if content else {}; print('✅' if 'message' in d else '❌')" 2>/dev/null || echo "❌"

echo -e "\n=========================================="
