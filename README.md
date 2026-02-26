# AISwitch

<div align="center">

![AISwitch Logo](https://img.shields.io/badge/AISwitch-v1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.14-blue)
![Next.js](https://img.shields.io/badge/next.js-16.1.6-black)

**AI 模型聚合和智能切换平台**

自动监控、测试和切换最优 AI 模型

[快速开始](#快速开始) • [功能特性](#功能特性) • [文档](#文档) • [路线图](ROADMAP.md)

</div>

---

## 📖 简介

AISwitch 是一个 AI 模型聚合和智能切换平台，帮助你：

- 🔌 **统一管理**多个 AI API 渠道和模型
- 🧪 **自动测试**模型性能（速度、代码生成、工具调用）
- 📊 **智能排名**根据测试结果自动排序模型
- 🔄 **自动切换**到最优可用模型
- ⚙️ **一键生成** OpenClaw 配置文件

## ✨ 功能特性

### 渠道管理
- ✅ 支持多个 API 渠道（OpenAI、Anthropic、Azure 等）
- ✅ 灵活配置 Base URL 和 API Key
- ✅ 启用/禁用渠道控制

### 模型管理
- ✅ 完整的模型 CRUD 操作
- ✅ CSV 批量导入模型
- ✅ 模型参数配置（上下文窗口、工具支持等）
- ✅ 模型启用/禁用控制

### 模型测试
- ✅ **速度测试** - 测量响应时间
- ✅ **代码生成测试** - 评估代码质量
- ✅ **工具调用测试** - 验证函数调用能力
- ✅ 测试结果历史记录

### 智能排名
- ✅ 综合评分算法（可用性 40% + 速度 30% + 质量 20% + 成本 10%）
- ✅ 自动更新排名
- ✅ 排名可视化展示

### 配置生成
- ✅ 自动生成 OpenClaw 配置
- ✅ 支持主模型和备用模型配置
- ✅ 一键下载配置文件

## 🚀 快速开始

### 前置要求

- Python 3.14+
- Node.js 18+
- npm 或 yarn

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/yourusername/AISwitch.git
cd AISwitch
```

2. **后端设置**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **前端设置**
```bash
cd frontend
npm install
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件配置数据库等
```

5. **启动服务**

后端：
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

前端：
```bash
cd frontend
npm run dev
```

6. **访问应用**
- 前端：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

## 📚 文档

- [使用指南](USAGE.md) - 详细的使用说明
- [开发路线图](ROADMAP.md) - 未来计划和进度
- [更新日志](CHANGELOG.md) - 版本更新记录
- [API 文档](http://localhost:8000/docs) - 在线 API 文档

## 🏗️ 技术栈

### 前端
- **框架**: Next.js 16.1.6 (App Router)
- **UI**: React 19 + Tailwind CSS 4
- **语言**: TypeScript

### 后端
- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **异步**: httpx
- **语言**: Python 3.14

## 📊 项目结构

```
aiswitch/
├── frontend/              # Next.js 前端
│   ├── app/              # 页面和路由
│   ├── public/           # 静态资源
│   └── package.json
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── models/      # 数据模型
│   │   ├── routers/     # API 路由
│   │   ├── services/    # 业务逻辑
│   │   └── main.py      # 应用入口
│   └── requirements.txt
├── docker-compose.yml    # Docker 配置
├── README.md
├── USAGE.md
├── ROADMAP.md
└── CHANGELOG.md
```

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md)（即将推出）

## 📝 许可证

本项目采用 [MIT 许可证](LICENSE)

## 🗺️ 路线图

### v1.0.0 (当前版本)
- ✅ 基础功能实现
- ✅ Web UI 界面
- ✅ 模型测试框架
- ✅ 配置生成

### v1.1.0 (计划中)
- 🔄 真实 AI API 测试
- 🔄 PostgreSQL 支持
- 🔄 异步任务队列
- 🔄 数据可视化

### v2.0.0 (未来)
- 🔮 用户认证
- 🔮 监控告警
- 🔮 性能优化
- 🔮 企业级功能

查看完整路线图：[ROADMAP.md](ROADMAP.md)

## 💬 联系方式

- 问题反馈：[GitHub Issues](https://github.com/yourusername/AISwitch/issues)
- 功能建议：[GitHub Discussions](https://github.com/yourusername/AISwitch/discussions)

## ⭐ Star History

如果这个项目对你有帮助，请给我们一个 Star！

---

<div align="center">
Made with ❤️ by AISwitch Contributors
</div>
