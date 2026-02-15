---
name: idea-coach
description: 这是一款由人工智能驱动的想法/问题/挑战管理工具，具备与 GitHub 的集成功能。它能够捕获用户提出的想法，对其进行分类和审核，并协助将这些想法上传到相应的代码仓库中。
version: 0.2.0
author: moinsen-dev
commands:
  - /idea - Capture a new idea, problem, or challenge
  - /idea_list - List active ideas (optionally filter by status/type)
  - /idea_due - Show ideas due for review
  - /idea_get - Get detailed info about an idea
  - /idea_update - Update idea status, importance, energy
  - /idea_review - Add review notes to an idea
  - /idea_drop - Mark idea as dropped (with reason)
  - /idea_done - Mark idea as completed
  - /idea_stats - Show statistics
  - /idea_link - Link idea to existing GitHub repo
  - /idea_ship - Create new GitHub repo for idea
  - /idea_repo - Show linked repo status
  - /idea_sync - Sync idea as GitHub issue
---

# Idea Coach

> 您在想法、问题和挑战方面的得力助手——现在支持与 GitHub 的集成！

## 功能介绍

Idea Coach 可帮助您：
- **记录** 新出现的想法、问题和挑战
- **按类型、领域、紧迫性和重要性进行分类**
- **定期回顾**（根据重要性，每天或每季度）
- **将想法提交到 GitHub 仓库**（准备就绪时）
- **跟踪进度**，并判断何时应该放弃某个想法

## 设计理念

**既要提出建设性意见，也要进行批判性分析。** Idea Coach 会：
- 建议放弃那些不值得追求的想法
- 在回顾过程中提出尖锐的问题
- 记录哪些想法最终被实现，哪些被长期搁置

## 命令操作

### 核心命令

| 命令 | 描述 |
|---------|-------------|
| `/idea <文本>` | 记录一个新的想法 |
| `/idea_list` | 列出所有活跃的想法 |
| `/idea_list --due` | 显示即将需要审核的想法 |
| `/idea_get <id>` | 获取想法的详细信息 |
| `/idea_update <id>` | 更新想法的属性 |
| `/idea_review <id>` | 为想法添加审核记录 |
| `/idea_drop <id>` | 将想法标记为“已放弃”（需提供理由） |
| `/idea_done <id>` | 将想法标记为“已完成” |
| `/idea_stats` | 显示统计信息 |

### GitHub 相关命令

| 命令 | 描述 |
|---------|-------------|
| `/idea_link <id> <owner/repo>` | 将想法链接到现有的 GitHub 仓库 |
| `/idea_ship <id>` | 为想法创建一个新的 GitHub 仓库 |
| `/idea_ship <id> --public` | 创建公共仓库 |
| `/idea_repo <id>` | 查看链接的仓库状态 |
| `/idea_sync <id>` | 在 GitHub 上创建/更新问题 |

## 属性分类

### 类型
- 💡 **idea** — 需要构建或创造的内容
- 🔧 **problem** — 需要解决的问题
- 🎯 **challenge** — 需要克服的挑战

### 状态流转流程
```
captured → exploring → developing → shipped/done
                ↓           ↓
             parked      blocked
                ↓
             dropped
```

### 重要性与审核周期

| 重要性 | 紧迫性 | 审核周期 |
|------------|--------|--------------|
| 非常重要 | 高 | 每天 |
| 非常重要 | * | 每周 |
| 重要 | 高 | 每周 |
| 重要 | * | 每两周 |
| 可有可无 | * | 每月 |
| 暂缓处理 | * | 每季度 |

## GitHub 集成

### 先决条件
- 安装并登录 `gh` CLI
- 如果尚未设置，请运行 `gh auth login`

### 工作流程示例
```
# 1. Capture idea
/idea "Build a CLI for task management"

# 2. Develop it
/idea_update abc123 --status developing

# 3. Ship it to GitHub
/idea_ship abc123

# 4. Or link to existing repo
/idea_link abc123 moinsen-dev/my-cli

# 5. Check repo status
/idea_repo abc123

# 6. Sync as GitHub issue
/idea_sync abc123
```

## CLI 使用方法
```bash
# Add idea
python scripts/coach.py add "Build something cool" --type idea --importance important

# List ideas
python scripts/coach.py list
python scripts/coach.py list --due
python scripts/coach.py list --github  # Only with linked repos

# GitHub operations
python scripts/coach.py link <id> owner/repo
python scripts/coach.py ship <id> --owner moinsen-dev
python scripts/coach.py repo-status <id>
python scripts/coach.py sync-issue <id> --labels enhancement,idea
```

## 数据存储

想法存储在 `~/.openclaw/idea-coach/ideas.json` 文件中

每个想法会记录以下信息：
- 基本信息（标题、描述、类型、领域）
- 状态和进度
- 紧迫性、重要性
- 审核计划和历史记录
- **GitHub 集成信息**（仓库链接、问题编号、同步时间）
- 交互记录

## 使用建议：
1. **快速记录** — 初步记录时不必过度思考
2. **如实审核** — 通过审核来淘汰过时的想法
3. **尽早提交** — 一旦想法有发展潜力，立即创建仓库
4. **同步问题** — 使用 GitHub 问题进行详细跟踪
5. **自由放弃** — 放弃一个想法是一个决定，而不是失败