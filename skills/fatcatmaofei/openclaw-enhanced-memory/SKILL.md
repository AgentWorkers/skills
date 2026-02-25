---
name: enhanced-memory
description: >
  OpenClaw代理的增强型内存系统：该系统取代了默认的单一文件`MEMORY.md`，采用了一种更为完善的内存管理架构：  
  - 内存数据按类别进行分层目录组织；  
  - 支持使用`[category:value]`标签进行索引，并支持多标签的AND查询；  
  - 具备自动生命周期管理功能（数据从“活跃状态”切换到“归档状态”，且永不被删除）；  
  - 提供智能的跨类别检索功能，能够自动将查询路由到相应的存储模块。  
  该系统能够为OpenClaw代理提供结构化、可搜索、且长期有效的存储解决方案（即数据可以长期保存且易于查询）。
---
# 增强型内存系统

这是一个结构化的内存管理系统，为你的 OpenClaw 代理提供**有序、可搜索且长期保存的数据存储方式**，取代了传统的单一 `MEMORY.md` 文件。

## 为什么需要这样的系统？

传统的 `MEMORY.md` 方式存在诸多问题：

- 文件不断增长，导致读取速度变慢，且占用大量系统资源；
- 没有分类机制，导致食物记录、项目笔记以及各种信息混杂在一起；
- 缺乏检索策略，导致代理需要重新读取所有数据，或者错过关键信息；
- 没有数据生命周期管理机制，导致旧数据长期占用内存空间。

而带有标签的内存管理系统能够有效解决这些问题。

## 核心特性

### 1. 分层目录结构

所有数据都存储在专门设计的目录中：

```
memory/
├── current/          # Active memories (last 6 months)
├── archived/         # Auto-archived older memories (permanent, never deleted)
│   └── YYYY-MM/      # Organized by month
├── RELATION/         # One file per person (relationship context)
├── food/             # Meal and food logs
├── training/         # Exercise and workout records
├── connections.md    # Global relationship graph
├── system/           # System config and logs
└── misc/             # Everything else
```

### 2. 基于标签的索引系统

可以在任何内存文件中的任意行使用 `[category:value]` 标记进行标记：

```markdown
## 2026-02-20

- Had lunch with Zhang Hao [人物:张浩东] [类型:聚餐] [地点:campus]
- Discussed the new project deadline [项目:openclaw] [类型:会议]
- Yoyo learned a new trick today [宠物:悠悠] [类型:milestone]
```

标签支持多标签组合搜索，从而能够精确找到所需的数据：

```bash
# Single tag search
python3 scripts/memory_tag_search.py "人物:张浩东"

# Multi-tag AND search (all tags must match)
python3 scripts/memory_tag_search.py "人物:王隆哲" "类型:开票信息"

# List all tags in the system
python3 scripts/memory_tag_search.py --list-tags

# List tags under a specific category
python3 scripts/memory_tag_search.py --list-tags --category 人物
```

### 3. 数据生命周期管理

数据会按照预设的规则自动老化处理，既不会被永久删除，也始终可以被访问：

| 存储时间 | 存储位置 | 状态       |
|---------|-----------|-----------|
| 0–6个月   | `memory/current/` | 活跃状态，自动检索 |
| 6–12个月   | `memory/archived/YYYY-MM/` | 归档状态，可按需查询 |
| 12个月以上 | `memory/archived/` | 永久归档，需手动查询 |

你可以手动运行数据生命周期管理脚本，也可以通过 cron 任务自动执行：

```bash
# Default: archive memories older than 6 months
python3 scripts/memory_lifecycle_manager.py

# Custom threshold (e.g., 90 days)
python3 scripts/memory_lifecycle_manager.py 90
```

### 4. 智能的跨类别检索机制

检索策略脚本会自动对查询内容进行分类，并在正确的目录中进行搜索：

```bash
python3 scripts/memory_retrieval_strategy.py "What did I eat yesterday?"
# → Searches memory/food/ + memory/current/

python3 scripts/memory_retrieval_strategy.py "How is Yoyo doing?"
# → Searches memory/RELATION/悠悠.md + memory/connections.md

python3 scripts/memory_retrieval_strategy.py "Yang Lingxiao"
# → Searches memory/RELATION/ + memory/connections.md
```

系统支持的查询类型包括：食物记录、训练信息、人际关系、宠物相关数据、系统状态、情绪记录、项目信息等。

## 相关脚本

| 脚本        | 功能                         |
|-------------|-----------------------------|
| `scripts/memory_tag_search.py` | 基于标签的索引和搜索功能（单标签/多标签组合查询，标签列表显示） |
| `scripts/memory_retrieval_strategy.py` | 智能检索机制，自动将查询定向到相应的数据目录 |
| `scripts/memory_lifecycle_manager.py` | 自动归档旧数据（可配置归档阈值，数据不会被删除） |

## 集成方式

### AGENTS.md

请将以下内容添加到你的 `AGENTS.md` 文件中的内存管理部分：

```markdown
## Memory

### Directory Structure
- `memory/current/` — active memories (6 months)
- `memory/archived/` — permanent archive
- `memory/RELATION/` — per-person relationship files
- `memory/food/` — meal logs
- `memory/training/` — workout logs

### Retrieval Strategy
- Exact queries (names, dates, codes) → `grep` the file system
- Fuzzy/semantic queries → `python3 scripts/memory_retrieval_strategy.py "<query>"`
- Tag search → `python3 scripts/memory_tag_search.py "<category>:<value>"`

### Tagging Convention
When writing memory entries, tag important lines:
  [人物:name] [类型:type] [地点:place] [项目:project] [情绪:mood]
```

### HEARTBEAT.md

请将定期内存维护任务添加到你的心跳检查列表（heartbeat checklist）中：

```markdown
## Memory Maintenance (every few days)
- [ ] Run `python3 scripts/memory_lifecycle_manager.py` to archive old memories
- [ ] Run `python3 scripts/memory_tag_search.py --list-tags` to review tag health
- [ ] Check `memory/current/` file count — if growing large, verify archival is running
```

### Cron 任务（可选）

你可以设置每月自动执行一次数据归档任务：

```bash
# Run on the 1st of every month at 03:00
0 3 1 * * cd /path/to/workspace && python3 scripts/memory_lifecycle_manager.py
```

## 自定义设置

- **归档阈值**：在 `memory_lifecycle_manager.py` 文件中修改 `ARCHIVE_THRESHOLD_days`（默认值为 180 天）；
- **查询模式**：在 `memory_retrieval_strategy.py` 文件中添加新的正则表达式模式；
- **数据目录**：在 `memory_lifecycle_manager.py` 文件中添加新的目录路径；
- **标签分类**：标签格式自由，只需在任何 `.md` 文件中使用 `[category:value]` 标记即可。

## 系统要求

- Python 3.8 及以上版本；
- 无需依赖任何外部库（仅使用标准 Python 库）。