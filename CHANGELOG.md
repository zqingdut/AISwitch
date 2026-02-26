# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-27

### Added
- 🎉 Initial release of AISwitch
- 渠道管理功能（创建、编辑、删除、启用/禁用）
- 模型管理功能（创建、编辑、删除、启用/禁用）
- CSV 批量导入模型
- 模型测试框架（速度、代码生成、工具调用）
- 模型排名系统
- OpenClaw 配置自动生成
- Web UI 界面（Next.js + React + Tailwind CSS）
- RESTful API（FastAPI）
- SQLite 数据库支持
- API 文档（Swagger UI）

### Features
- 📊 支持多渠道 API 管理
- 🧪 三种测试类型：速度测试、代码生成测试、工具调用测试
- 🔄 智能模型排名算法
- ⚙️ 一键生成 OpenClaw 配置
- 📝 完整的 API 文档
- 🎨 现代化的 Web 界面

### Documentation
- README.md - 项目介绍和快速开始
- USAGE.md - 详细使用指南
- ROADMAP.md - 开发路线图
- LICENSE - MIT 许可证

### Technical Stack
- Frontend: Next.js 16.1.6, React 19, Tailwind CSS
- Backend: FastAPI, SQLAlchemy, SQLite
- Development: Python 3.14, Node.js

## [Unreleased]

### Planned for v1.1.0
- 真实 AI API 测试实现
- PostgreSQL 数据库支持
- Redis + Celery 异步任务
- 测试历史和数据可视化

### Planned for v2.0.0
- 用户认证和权限管理
- 监控和告警系统
- Docker 部署优化
- 性能优化和缓存
