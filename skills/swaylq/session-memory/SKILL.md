---
name: session-memory
description: 用于AI代理的持久化内存工具包：支持保存上下文数据、根据相关性进行数据检索、整合分析结果、跨会话追踪代理的决策过程。具备设置数据重要性等级的功能、支持多关键词搜索、提供会话上下文加载器、支持数据的导出/导入以及内存使用统计功能。完全基于bash和Node.js实现，无需依赖任何第三方库。版本：2.0.0
homepage: https://github.com/voidborne-d/session-memory-skill
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["node"]}}}
---
# 会话记忆 🧠 v2.0  
为AI代理提供持久化存储功能：保存重要信息，快速检索相关内容，整合学习成果。  

**v2.0** 特点：  
- 基于相关性评分的搜索机制  
- 支持不同的重要性级别  
- 会话上下文加载功能  
- 提供数据导出/导入功能  
- 支持数据统计与编辑/删除操作  

## 快速入门  

```bash
# Save a memory (with optional importance)
MEMORY_IMPORTANCE=high ./scripts/save.sh "decision" "Chose Postgres over SQLite for scale"

# Recall with relevance scoring
./scripts/recall.sh "database" --limit 5

# Load session context (startup)
./scripts/context.sh --days 3

# Consolidate by topic
./scripts/consolidate.sh --since 2026-01-01

# Stats
./scripts/stats.sh
```  

---

## 命令  

### save.sh — 保存记忆数据  
```bash
./scripts/save.sh "topic" "content" [tags...]
```  
| 参数 | 默认值 | 说明 |  
|-------|---------|-------------|  
| `AGENT_MEMORY_DIR` | `~/.agent-memory` | 存储目录 |  
| `MEMORY_IMPORTANCE` | `normal` | 重要性级别：低 / 中 / 高 / 关键 |  

```bash
# Basic save
./scripts/save.sh "insight" "Users prefer dark mode 3:1" ui design

# High importance
MEMORY_IMPORTANCE=high ./scripts/save.sh "decision" "Migrated to TypeScript" refactor

# Critical (always surfaces in context.sh)
MEMORY_IMPORTANCE=critical ./scripts/save.sh "credential" "API key rotated, new one in vault"
```  

### recall.sh — 检索记忆数据  
```bash
./scripts/recall.sh "query" [--json] [--limit N] [--topic T] [--importance I] [--since YYYY-MM-DD]
```  
- **多关键词搜索**：所有关键词必须匹配  
- **相关性评分**：结合关键词匹配度、重要性和最新性进行判断  
- **过滤条件**：按主题、重要性级别或日期范围筛选  

```bash
./scripts/recall.sh "database migration"
./scripts/recall.sh "API" --topic decision --limit 20
./scripts/recall.sh "deploy" --since 2026-03-01 --json
./scripts/recall.sh "error" --importance high
```  

### context.sh — 会话启动时加载记忆数据  
```bash
./scripts/context.sh [--days N] [--limit N] [--json]
```  
- 加载与新会话最相关的记忆数据：  
  - 最近的N天内的记忆（默认为3条）  
  - 无论时间久远，重要性高的或关键的信息都会被加载  
  - 按重要性和最新性排序  
  - 按日期分组显示  

```bash
# Quick context
./scripts/context.sh

# Wider window
./scripts/context.sh --days 7 --limit 30

# For programmatic use
./scripts/context.sh --json
```  

### daily.sh — 日视图  
```bash
./scripts/daily.sh [YYYY-MM-DD] [--json]
```  

### topics.sh — 主题索引  
```bash
./scripts/topics.sh [--json]
```  

### consolidate.sh — 主题整合  
```bash
./scripts/consolidate.sh [--since YYYY-MM-DD] [--topic T] [--json]
```  
- 按主题对记忆数据进行分类，显示数量、日期范围、热门标签和最新条目，便于定期回顾  

### stats.sh — 记忆数据统计  
```bash
./scripts/stats.sh [--json]
```  
- 显示总条目数、日期范围、每日平均条目数、存储大小以及主题分布  

### edit.sh — 编辑或删除记忆数据  
```bash
./scripts/edit.sh <timestamp_ms> --content "new content"
./scripts/edit.sh <timestamp_ms> --topic "new topic"
./scripts/edit.sh <timestamp_ms> --importance critical
./scripts/edit.sh <timestamp_ms> --delete
```  

### export.sh — 导出记忆数据  
```bash
./scripts/export.sh [-o backup.json] [--since YYYY-MM-DD] [--topic T]
```  

### import.sh — 导入记忆数据  
```bash
./scripts/import.sh backup.json [--dry-run]
```  
- 通过时间戳进行去重处理，可多次安全运行  

### prune.sh — 归档旧记忆数据  
```bash
./scripts/prune.sh [days]
```  
- 将超过N天（默认为30天）的记忆数据移至`archive/`目录  

---

## 数据存储  
**存储格式说明：**  
每行数据都是一个JSON对象。  
```json
{"ts":1706793600000,"topic":"decision","content":"Chose X because Y","tags":["project"],"importance":"high"}
```  

## 重要性级别  
| 级别 | 使用场景 | 行为特点 |  
|-------|-------------|----------|  
| `low` | 背景信息、次要笔记 | 仅通过搜索可访问 |  
| `normal` | 标准记忆数据 | 显示在日视图中 |  
| `high` | 关键决策、重要见解 | 始终显示在会话界面中 |  
| `critical` | 重要凭证、紧急事项 | 始终显示在会话界面中，优先级最高 |  

## 推荐工作流程  
```bash
# Session start
./scripts/context.sh

# During work — save important things
./scripts/save.sh "decision" "..."
MEMORY_IMPORTANCE=high ./scripts/save.sh "insight" "..."

# End of session
./scripts/save.sh "summary" "Today: did X, decided Y, next step Z"

# Weekly review
./scripts/consolidate.sh --since $(date -u -d '7 days ago' +%Y-%m-%d)
./scripts/stats.sh

# Monthly maintenance
./scripts/prune.sh 60
./scripts/export.sh -o backup-$(date +%Y%m).json
```  

---

*由 [Voidborne](https://voidborne.org) 创建 🔹*