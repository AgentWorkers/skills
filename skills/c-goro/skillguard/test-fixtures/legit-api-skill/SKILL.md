---
name: github-issues
description: 通过 API 获取和管理 GitHub 问题
metadata: {"openclaw": {"requires": {"env": ["GITHUB_TOKEN"], "bins": ["curl"]}}}
---

# GitHub 问题

此技能允许您列出、创建和管理 GitHub 问题。

## 使用方法
- “显示仓库 X 的未解决问题”
- “在仓库 Z 中创建一个名为 Y 的新问题”

## 配置
请在您的环境中设置 `GITHUB_TOKEN`，使用个人访问令牌。对于私有仓库，该令牌需要具有 `repo` 权限。