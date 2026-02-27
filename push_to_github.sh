#!/bin/bash
# AISwitch GitHub 推送脚本

echo "🚀 准备推送 AISwitch v1.0.0 到 GitHub..."

# 请先在 GitHub 创建仓库，然后替换下面的 YOUR_USERNAME
GITHUB_USERNAME="YOUR_USERNAME"
REPO_NAME="AISwitch"

echo "📝 配置 remote..."
git remote add origin https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git 2>/dev/null || echo "Remote already exists"

echo "📤 推送主分支..."
git push -u origin main

echo "🏷️  推送标签..."
git push origin v1.0.0

echo "✅ 推送完成！"
echo "🌐 访问: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
