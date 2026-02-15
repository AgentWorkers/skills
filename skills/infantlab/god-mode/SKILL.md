---
name: god-mode
description: 开发者监督与AI代理培训功能：适用于查看各个仓库的项目状态、同步GitHub数据，或根据提交模式分析`agents.md`文件的内容。
metadata: {"openclaw": {"requires": {"bins": ["gh", "sqlite3", "jq"]}}}
user-invocable: true
---

# god-mode 技能

> 为 OpenClaw 提供开发者监督和 AI 代理的辅导功能。

## 概述

**god-mode** 可让您全面了解所有编码项目的状况，并帮助您编写更优秀的 AI 代理指令。

**主要功能：**
- 多项目状态仪表板
- 从 GitHub（未来将支持 Azure/GitLab）逐步同步数据
- 根据提交模式分析代理指令
- 使用本地 SQLite 缓存以加快查询速度

## 快速入门

```bash
# First-run setup
god setup

# Add a project
god projects add github:myuser/myrepo

# Sync data
god sync

# See overview
god status

# Analyze your agents.md
god agents analyze myrepo
```

## 命令

### `god status [project]`
显示所有项目的概览，或查看单个项目的详细信息：
```bash
god status              # All projects
god status myproject    # One project in detail
```

### `god sync [project] [--force]`
从仓库中获取/更新数据：
```bash
god sync                # Incremental sync all
god sync myproject      # Just one project
god sync --force        # Full refresh (ignore cache)
```

### `god projects`
管理已配置的项目：
```bash
god projects                        # List all
god projects add github:user/repo   # Add project
god projects remove myproject       # Remove project
```

### `god agents analyze <project>`
根据提交历史分析 `agents.md` 文件：
```bash
god agents analyze myproject
```

找出代理指令与实际工作模式之间的差距，并提出改进建议。

### `god agents generate <project>`（即将推出）
通过分析仓库结构为新项目生成 `agents.md` 文件。

## 配置

配置文件：`~/.config/god-mode/config.yaml`

```yaml
projects:
  - id: github:user/repo
    name: My Project      # Display name
    priority: high        # high/medium/low
    tags: [work, api]
    local: ~/code/myrepo  # Local clone path

sync:
  initialDays: 90         # First sync lookback
  commitsCacheMinutes: 60

analysis:
  agentFiles:             # Files to search for
    - agents.md
    - AGENTS.md
    - CLAUDE.md
    - .github/copilot-instructions.md
```

## 数据存储

所有数据存储在 `~/.god-mode/` 目录下：
- `cache.db` - SQLite 数据库（包含提交记录、Pull Request、问题及分析结果）
- `contexts/` - 保存的工作区上下文（版本 0.2）

## 认证

god-mode 使用您现有的 CLI 认证机制：

| 提供商 | CLI | 设置方式 |
|----------|-----|-------|
| GitHub | `gh` | `gh auth login` |
| Azure | `az` | `az login` |
| GitLab | `glab` | `glab auth login` |

**god-mode 不会存储任何令牌。** 我们依赖您已信任的 CLI 进行认证。

## 系统要求

- `gh` - GitHub CLI（用于访问 GitHub 仓库）
- `sqlite3` - 数据库工具
- `jq` - JSON 处理工具

## 示例

### 早晨检查
```bash
god status
# See all projects at a glance
# Notice any stale PRs or quiet projects
```

### 切换项目前
```bash
god status myproject
# See recent activity, open PRs, issues
# Remember where you left off
```

### 改进您的 AI 助手
```bash
god agents analyze myproject
# Get suggestions based on your actual commit patterns
# Apply recommendations to your agents.md
```

### 周度回顾
```bash
god status
# Review activity across all projects
# Identify projects needing attention
```

## 代理工作流程

### 每日简报（心跳检测）
```markdown
# HEARTBEAT.md
- Run `god status` and summarize:
  - Projects with stale PRs (>3 days)
  - Projects with no activity (>5 days)
  - Open PRs needing review
```

### 代理分析（定时任务）
```yaml
# Weekly agent instruction review
schedule: "0 9 * * 1"  # Monday 9am
task: |
  Run `god agents analyze` on high-priority projects.
  If gaps found, notify with suggestions.
```

## 故障排除

### “gh: 命令未找到”
请安装 GitHub CLI：https://cli.github.com/

### “未登录 GitHub”
运行：`gh auth login`

### “未配置任何项目”
添加项目：`god projects add github:user/repo`

### 数据过期
强制刷新：`god sync --force`

---

*OpenClaw 社区技能*  
*许可证：MIT*  
*仓库地址：https://github.com/InfantLab/god-mode-skill*