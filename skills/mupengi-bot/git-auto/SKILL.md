---
name: git-auto
description: Git工作区自动化（状态/提交/推送/日志/差异）
version: 1.0.0
author: 무펭이 🐧
---
# git-auto

**Git 工作区自动化** — 通过智能的默认设置简化日常的 Git 操作。包括状态检查、智能提交、安全推送以及差异分析等功能。

## 使用场景

- 查看多个仓库的工作区状态
- 根据已暂存的更改生成有意义的提交信息
- 在推送之前进行安全检查（如分支保护、冲突检测）
- 查看格式化的日志和差异信息
- 对单仓库的子目录执行批量操作

## 命令

### status
```bash
# Show concise workspace status
git-auto status
# Multi-repo status scan
git-auto status --all
```
返回：修改过的文件、未跟踪的文件、分支信息以及代码的领先/落后数量。

### commit
```bash
# Auto-generate commit message from diff
git-auto commit
# With explicit message
git-auto commit -m "feat: add user auth"
# Commit specific files
git-auto commit -f "src/auth.ts,src/types.ts"
```
行为：
1. 运行 `git diff --staged` 来分析更改
2. 生成常规的提交信息（如 `feat`、`fix`、`refactor`、`docs`、`chore` 等）
3. 在提交前验证提交信息的格式
4. 显示提交哈希值和提交摘要

### push
```bash
# Push current branch with safety checks
git-auto push
# Force push (with confirmation)
git-auto push --force
```
安全检查：
- 如果直接推送到 `main` 或 `master` 分支，会发出警告
- 检查是否存在上游分支的冲突
- 确认远程仓库是否存在

### log
```bash
# Last 10 commits, formatted
git-auto log
# Last N commits
git-auto log -n 20
# Filter by author
git-auto log --author "name"
```

### diff
```bash
# Staged changes
git-auto diff
# Working directory changes
git-auto diff --unstaged
# Between branches
git-auto diff main..feature-branch
```

## 智能提交信息格式

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 标准：
- `feat`：新增功能
- `fix`：修复错误
- `refactor`：代码重构
- `docs`：仅用于文档更新
- `chore`：维护任务
- `test`：添加/更新测试用例

## 集成

支持与任何 Git 仓库配合使用。无需额外配置，会自动检测 `.git` 目录和当前分支。可与 `code-review` 工具结合使用，进行提交前的代码审查。

## 错误处理

| 错误情况 | 处理方式 |
|-----------|----------|
| 非 Git 仓库 | 显示带有建议的错误信息 |
| 合并冲突 | 显示冲突文件并提示解决方案 |
- 无暂存更改 | 提示用户暂存更改或查看未暂存的文件 |
- 认证失败 | 建议用户刷新凭证 |
- HEAD 分支分离 | 发出警告并建议创建新分支 |