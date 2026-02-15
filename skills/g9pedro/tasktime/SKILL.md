---
name: tasktime
description: AI代理的CLI任务定时器——用于监控学习进度，并自动保存日志和生成可视化数据。该工具与ClawVault集成，以实现数据的持久存储。
metadata:
  openclaw:
    requires:
      bins: [tasktime]
    install:
      - id: node
        kind: node
        package: "@versatly/tasktime"
        bins: [tasktime, tt]
        label: Install TaskTime CLI (npm)
---

# tasktime Skill

这是一个用于AI代理的命令行（CLI）任务计时工具，可用来评估学习进度，并自动保存日志和生成可视化数据。

该工具是[ClawVault](https://clawvault.dev)生态系统的一部分，用于管理AI代理的内存数据。

## 安装

```bash
npm install -g @versatly/tasktime
```

## 快速参考

### 计时命令
```bash
tasktime start "Task description" --category coding   # Start timing
tasktime stop --notes "What I learned"                # Stop and save
tasktime status                                       # Show current task
tasktime now                                          # One-liner for prompts
```

### 任务历史记录与搜索
```bash
tasktime history                    # Recent tasks (alias: tt ls)
tasktime history -n 20              # Last 20 tasks
tasktime history -c coding          # Filter by category
tasktime search "auth"              # Full-text search
tasktime categories                 # List all categories
```

### 报告与图表
```bash
tasktime report                     # Full report with charts
tasktime report --days 30           # Last 30 days
tasktime chart --type bar           # Bar chart
tasktime chart --type spark         # Sparkline
tasktime chart --type line          # Line chart
```

### 与ClawVault的集成

**自动保存功能（v1.2.0及以上版本）：** 每个完成的任务都会自动保存到[ClawVault](https://clawvault.dev)中：

```bash
tasktime start "Build API" -c coding
# ... do the work ...
tasktime stop --notes "Finished in record time"
# ✅ Completed: Build API
# 🐘 Saved to ClawVault              ← automatic!
```

**手动同步与导出：**
```bash
tasktime sync                       # Sync full report to ClawVault
tasktime sync --days 30             # Sync last 30 days
tasktime export                     # Export as markdown
tasktime stop --no-vault            # Skip auto-save for one task
```

### 示例数据
```bash
tasktime seed                       # Seed sample data (empty DB only)
```

## 代理的使用场景

### 学习进度评估
通过跟踪类似任务所需的时间来衡量学习进度：

```bash
tt start "Implement OAuth flow" -c auth
# ... do the work ...
tt stop --notes "Used passport.js, took 20min less than last time"
```

### 同步到ClawVault
将任务数据保存到代理的内存存储系统中：

```bash
# After completing work
tasktime sync

# Or pipe export to clawvault
tasktime export | clawvault store --category research --title "Task Report"
```

更多信息：[clawvault.dev](https://clawvault.dev)

### 基于类别的分析
对任务进行分类，以了解时间分配情况：

```bash
tt report --days 7
# Shows time breakdown by category: coding, research, testing, docs, etc.
```

### 在shell提示中显示当前任务状态
在shell提示中显示当前正在进行的任务：

```bash
PS1='$(tasktime now) \$ '
# Shows: ⏱️ Build API (23m) $
```

## 数据存储

- 存储位置：`~/.tasktime/tasks.json`
- 数据格式：JSON（便携式、易于阅读）
- 无需依赖任何外部组件或数据库

## 相关工具

- [ClawVault](https://clawvault.dev) — AI代理的内存管理系统
- [OpenClaw](https://openclaw.ai) — AI代理平台

## 别名

- `tasktime` — 完整命令名称
- `tt` — 简短别名（功能相同）