---
name: gh
description: "使用 GitHub CLI（gh）来执行核心的 GitHub 操作：验证用户身份（auth status）、创建/克隆/分支仓库（repo create/clone/fork）、处理问题（issues）、提交拉取请求（pull requests）、发布新版本（releases），以及进行基本的仓库管理。可以通过 CLI 来触发各种请求，以管理 GitHub 仓库、拉取请求（PRs）或问题（issues）。"
---

# GitHub CLI (gh)

## 概述
使用 `gh` 可以通过终端执行经过身份验证的 GitHub 操作。建议使用明确且可重复执行的命令，并将操作结果（URL）反馈给用户。

## 快速检查
- 身份验证状态：
```bash
gh auth status
```
- 当前仓库上下文：
```bash
gh repo view --json nameWithOwner,url,defaultBranchRef
```

## 核心工作流程

### 创建仓库（默认为私有仓库）
```bash
gh repo create OWNER/NAME --private --confirm --description "..."
```
如果在本地仓库中运行，请使用 `--source . --remote origin --push`。

### 克隆/分支
```bash
gh repo clone OWNER/NAME
```
```bash
gh repo fork OWNER/NAME --clone
```

### 问题（Issues）
- 列出问题：
```bash
gh issue list --limit 20
```
- 创建问题：
```bash
gh issue create --title "..." --body "..."
```
- 评论问题：
```bash
gh issue comment <num> --body "..."
```

### 提交请求（Pull Requests）
- 从当前分支创建提交请求：
```bash
gh pr create --title "..." --body "..."
```
- 列出提交请求：
```bash
gh pr list --limit 20
```
- 查看提交请求：
```bash
gh pr view <num> --web
```
- 合并提交请求（请使用明确的方法）：
```bash
gh pr merge <num> --merge
```

### 发布版本（Releases）
```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes "..."
```

## 安全提示
- 在执行破坏性操作（如删除、强制推送）之前，请确认目标仓库和所有者。
- 对于私有仓库，请确保在创建仓库时设置 `--private` 选项。
- 在自动化脚本中，建议使用 `--confirm` 选项以避免交互式提示。