# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-02-28

### Added - Phase 2 Complete ✅

#### 测试历史数据可视化
- ✅ Analytics API 路由
  - 测试历史趋势数据
  - 模型性能对比
  - 测试类型分布统计
  - 单个模型性能趋势
- ✅ 数据可视化页面
  - 测试趋势折线图（成功率、响应时间）
  - 模型性能对比柱状图
  - 测试类型分布饼图
  - 模型详细统计表格
- ✅ 时间范围筛选（7/14/30天）
- ✅ Recharts 图表库集成

#### Tailscale 远程访问支持
- ✅ CORS 配置支持 Tailscale IP
- ✅ 前端 API 配置统一管理
- ✅ 环境变量支持（.env.local）
- ✅ 所有页面使用动态 API_BASE_URL

#### Real AI API Testing
- ✅ AIAPIClient for unified API calls across providers
- ✅ Support for OpenAI, Anthropic, and other AI services
- ✅ Multiple authentication methods (Bearer, API-Key, X-API-Key)
- ✅ Enhanced error handling and timeout control
- ✅ Improved code quality evaluation

### Changed
- Updated API version from 1.0.0 to 1.1.0
- Enhanced navigation with Analytics link
- Improved frontend API configuration management

### Technical Stack Updates
- Added: recharts for data visualization
- Added: cryptography, passlib, python-jose
- Added: psutil for system monitoring

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
