# GitHub 推送指南

## 准备工作

项目已完成本地 Git 初始化和提交，现在需要推送到 GitHub。

## 步骤

### 1. 在 GitHub 上创建仓库

访问 https://github.com/new 创建新仓库：
- Repository name: `AISwitch`
- Description: `AI 模型聚合和智能切换平台`
- Visibility: Public（或 Private）
- **不要**勾选 "Initialize this repository with a README"

### 2. 配置 Remote

将 `YOUR_GITHUB_USERNAME` 替换为你的 GitHub 用户名：

```bash
cd /Users/niko/projects/aiswitch
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/AISwitch.git
```

### 3. 推送代码

```bash
# 推送主分支
git push -u origin main

# 推送标签
git push origin v1.0.0
```

### 4. 验证

访问你的 GitHub 仓库页面，应该能看到：
- ✅ 所有代码文件
- ✅ README.md 显示在首页
- ✅ v1.0.0 标签在 Releases 中

## 可选：创建 Release

1. 访问仓库的 Releases 页面
2. 点击 "Draft a new release"
3. 选择 tag `v1.0.0`
4. Release title: `v1.0.0 - Initial Release`
5. 复制 CHANGELOG.md 中的内容到描述
6. 点击 "Publish release"

## 完成！

项目已成功发布到 GitHub 🎉

访问地址：`https://github.com/YOUR_GITHUB_USERNAME/AISwitch`
