# AISwitch - 使用指南

## 系统状态

✅ **前端**: http://localhost:3000  
✅ **后端 API**: http://localhost:8000  
✅ **API 文档**: http://localhost:8000/docs

## 已完成功能

### 1. 渠道管理
- ✅ 创建、编辑、删除渠道
- ✅ 配置 API 密钥和 Base URL
- ✅ 启用/禁用渠道

### 2. 模型管理
- ✅ 创建、编辑、删除模型
- ✅ CSV 批量导入
- ✅ 配置模型参数（上下文窗口、工具支持等）
- ✅ 启用/禁用模型

### 3. 模型测试
- ✅ 速度测试
- ✅ 代码生成测试
- ✅ 工具调用测试
- ✅ 查看测试结果

### 4. 配置生成
- ✅ 查看模型排名
- ✅ 生成 OpenClaw 配置
- ✅ 下载配置文件

## 快速开始

### 1. 添加渠道
访问 http://localhost:3000/channels，点击"添加渠道"：
```json
{
  "name": "OpenAI",
  "base_url": "https://api.openai.com/v1",
  "api_key": "sk-your-key",
  "is_active": true
}
```

### 2. 添加模型
访问 http://localhost:3000/models，点击"添加模型"：
```json
{
  "name": "GPT-4",
  "model_identifier": "gpt-4",
  "channel_id": 1,
  "display_name": "GPT-4 Turbo",
  "context_window": 128000,
  "supports_tools": true,
  "is_active": true
}
```

### 3. CSV 批量导入
CSV 格式：
```csv
name,model_identifier,channel_id,is_active
GPT-4,gpt-4,1,true
GPT-3.5,gpt-3.5-turbo,1,true
Claude 3.5,claude-3-5-sonnet-20241022,2,true
```

### 4. 运行测试
1. 访问 http://localhost:3000/test
2. 选择要测试的模型
3. 选择测试类型（速度/代码/工具）
4. 点击"开始测试"

### 5. 生成配置
1. 访问 http://localhost:3000/config
2. 查看模型排名
3. 点击"生成配置"
4. 复制或下载配置文件

## API 示例

### 创建渠道
```bash
curl -X POST http://localhost:8000/api/channels/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "OpenAI",
    "base_url": "https://api.openai.com/v1",
    "api_key": "sk-your-key",
    "is_active": true
  }'
```

### 创建模型
```bash
curl -X POST http://localhost:8000/api/models/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "GPT-4",
    "model_identifier": "gpt-4",
    "channel_id": 1,
    "display_name": "GPT-4 Turbo",
    "context_window": 128000,
    "supports_tools": true,
    "is_active": true
  }'
```

### 运行测试
```bash
curl -X POST http://localhost:8000/api/test/run \
  -H "Content-Type: application/json" \
  -d '{
    "model_ids": [1, 2],
    "test_type": "speed"
  }'
```

### 生成配置
```bash
curl -X POST http://localhost:8000/api/config/generate
```

## 数据库结构

### 渠道 (channels)
- id: 主键
- name: 渠道名称
- base_url: API 基础 URL
- api_key: API 密钥
- is_active: 是否启用

### 模型 (models)
- id: 主键
- name: 模型名称
- model_identifier: 模型标识符
- channel_id: 所属渠道
- display_name: 显示名称
- context_window: 上下文窗口大小
- supports_tools: 是否支持工具调用
- is_active: 是否启用

### 测试结果 (test_results)
- id: 主键
- model_id: 模型 ID
- test_type: 测试类型
- success: 是否成功
- response_time_ms: 响应时间
- quality_score: 质量分数

### 模型排名 (model_rankings)
- model_id: 模型 ID
- overall_score: 综合分数
- availability_score: 可用性分数
- speed_score: 速度分数
- quality_score: 质量分数
- rank: 排名

## 技术栈

**前端**
- Next.js 16.1.6
- React 19.2.3
- Tailwind CSS 4

**后端**
- FastAPI
- SQLAlchemy
- SQLite (开发环境)
- httpx (异步 HTTP 客户端)

## 下一步

### 待实现功能
- [ ] PostgreSQL + Redis 集成
- [ ] Celery 异步任务队列
- [ ] 实际 AI API 调用测试
- [ ] 更复杂的排名算法
- [ ] 用户认证和权限管理
- [ ] 测试历史和趋势分析
- [ ] 自动化定时测试
- [ ] 告警和通知

## 故障排除

### 后端无法启动
```bash
cd /Users/niko/projects/aiswitch/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端无法启动
```bash
cd /Users/niko/projects/aiswitch/frontend
npm run dev
```

### 数据库重置
```bash
rm /Users/niko/projects/aiswitch/backend/aiswitch.db
# 重启后端服务会自动创建新数据库
```

## 联系方式

如有问题，请查看：
- API 文档: http://localhost:8000/docs
- 项目 README: /Users/niko/projects/aiswitch/README.md
