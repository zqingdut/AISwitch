# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-02-27

### Added - Phase 2 & 3 Complete

#### Real AI API Testing
- ✅ AIAPIClient for unified API calls across providers
- ✅ Support for OpenAI, Anthropic, and other AI services
- ✅ Multiple authentication methods (Bearer, API-Key, X-API-Key)
- ✅ Enhanced error handling and timeout control
- ✅ Improved code quality evaluation

#### Database & Infrastructure
- ✅ PostgreSQL support with connection pooling
- ✅ Database migration script (SQLite → PostgreSQL)
- ✅ Environment-based configuration management
- ✅ Settings class for centralized config

#### Async Task Queue
- ✅ Celery integration with Redis backend
- ✅ Async model testing tasks
- ✅ Scheduled tasks (hourly tests, ranking updates)
- ✅ Task status tracking

#### Security & Authentication
- ✅ API key encryption using Fernet
- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ User model with role-based access control
- ✅ API Token management

#### Monitoring & Health
- ✅ Detailed health check endpoints
- ✅ System resource monitoring (CPU, memory, disk)
- ✅ Database connection health checks
- ✅ Metrics endpoint with statistics
- ✅ Model health tracking

### Changed
- Updated API version from 1.0.0 to 1.1.0
- Enhanced testing router to use Celery tasks
- Improved database connection handling

### Technical Stack Updates
- Added: cryptography, passlib, python-jose
- Added: psutil for system monitoring
- Added: celery, redis for async tasks
- Added: psycopg2-binary for PostgreSQL

---

## [1.0.0] - 2026-02-27

### Added
- 🎉 Initial release of AISwitch
- 渠道管理功能（创建、编辑、删除、启用/禁用）
- 模型管理功能（创建、编辑、删除、CSV 导入）
- 模型测试框架（速度、代码生成、工具调用）
- 智能排名系统
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

---

## [Unreleased]

### Planned for v2.0.0
- 前端数据可视化（图表）
- 性能优化和缓存
- Docker 部署优化
- CI/CD 流程
- 完整的单元测试覆盖
