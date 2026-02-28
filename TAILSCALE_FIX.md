# Tailscale 连接问题修复

## 问题描述
手机通过 Tailscale 连接 AISwitch 项目时无法获取数据。

## 根本原因
1. **前端硬编码问题**：所有页面硬编码了 `http://localhost:8000`，导致手机浏览器无法连接到后端
2. **CORS 限制**：后端只允许 localhost 和 127.0.0.1 的跨域请求

## 修复方案

### 1. 后端 CORS 配置更新
文件：`backend/app/main.py`

```python
# 添加 Tailscale IP 到允许列表
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://100.67.188.28:3000",  # 本机 Tailscale IP
        "http://100.65.239.127:3000",  # 手机 Tailscale IP
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. 前端 API 配置统一
创建 `frontend/lib/api.ts`：

```typescript
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

创建 `frontend/.env.local`：

```
NEXT_PUBLIC_API_URL=http://100.67.188.28:8000
```

### 3. 更新所有前端页面
- `app/channels/page.tsx` - 渠道管理
- `app/models/page.tsx` - 模型管理
- `app/test/page.tsx` - 模型测试
- `app/config/page.tsx` - 配置生成

所有页面统一使用 `API_BASE_URL` 替代硬编码的 localhost。

## 使用方法

### 本地开发
```bash
# 使用默认 localhost
npm run dev
```

### Tailscale 访问
```bash
# 设置环境变量
echo "NEXT_PUBLIC_API_URL=http://100.67.188.28:8000" > frontend/.env.local

# 重启前端服务
cd frontend
npm run dev
```

### 手机访问
1. 确保手机和电脑都连接到 Tailscale
2. 在手机浏览器访问：`http://100.67.188.28:3000`
3. 前端会自动连接到 `http://100.67.188.28:8000` 后端

## 验证步骤

1. **检查后端监听**：
   ```bash
   ps aux | grep uvicorn
   # 应该看到 --host 0.0.0.0 --port 8000
   ```

2. **检查 Tailscale 状态**：
   ```bash
   tailscale status
   # 确认本机和手机的 IP 地址
   ```

3. **测试后端连接**：
   ```bash
   curl http://100.67.188.28:8000/health
   # 应该返回 {"status":"healthy","version":"1.1.0"}
   ```

4. **手机浏览器测试**：
   - 访问 `http://100.67.188.28:3000`
   - 检查浏览器控制台是否有 CORS 错误
   - 测试各个功能页面

## 注意事项

1. **环境变量优先级**：`.env.local` > `.env`
2. **重启要求**：修改 `.env.local` 后必须重启 Next.js 开发服务器
3. **CORS 安全**：生产环境应该使用更严格的 CORS 配置
4. **IP 地址变化**：Tailscale IP 可能会变化，需要相应更新配置

## 待修复问题（v1.1.0）

根据 PROGRESS.md，以下任务待完成：

- [ ] PostgreSQL 数据库迁移
- [ ] Redis + Celery 异步任务系统
- [ ] 测试历史数据可视化
- [ ] 单元测试覆盖
- [ ] 前端环境变量管理优化（支持动态配置）

## 修复时间
2026-02-28 11:34 GMT+8
