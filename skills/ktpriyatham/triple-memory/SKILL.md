---
name: triple-memory
version: 1.0.0
description: 这是一个完整的内存管理系统，它结合了LanceDB的自动回忆功能、Git-Notes结构化存储机制以及基于文件的工作区搜索功能。该系统适用于以下场景：配置全面的代理内存管理、实现跨会话的持久化上下文共享，或是管理需要多个内存后端协同工作的决策/偏好设置/任务。
metadata:
  clawdbot:
    emoji: "🧠"
    requires:
      plugins:
        - memory-lancedb
      skills:
        - git-notes-memory
---

# 三重内存系统

这是一种综合性的内存架构，结合了三个互补的系统，以实现跨会话的最大信息保留能力。

## 架构概述

```
User Message
     ↓
[LanceDB auto-recall] → injects relevant conversation memories
     ↓
Agent responds (using all 3 systems)
     ↓
[LanceDB auto-capture] → stores preferences/decisions automatically
     ↓
[Git-Notes] → structured decisions with entity extraction
     ↓
[File updates] → persistent workspace docs
```

## 三个系统

### 1. LanceDB（对话记忆系统）
- **自动回忆：** 在每次响应之前自动插入相关记忆内容
- **自动捕获：** 自动存储用户的偏好、决策和事实
- **工具：** `memory_recall`、`memory_store`、`memory_forget`
- **触发词：** “remember”（记住）、“prefer”（偏好）、“my X is”（我的X是...）、“I like/hate/want”（我喜欢/讨厌/想要）

### 2. Git-Notes（结构化、本地存储的记忆系统）
- **支持Git分支：** 按Git分支隔离记忆内容
- **实体提取：** 自动提取主题、名称和概念
- **重要性级别：** 关键、高、普通、低
- **无需外部API调用**

### 3. 文件搜索系统（用于工作区）
- **搜索范围：** MEMORY.md文件、所有以“memory/”开头的.md文件以及工作区中的任何文件
- **脚本：** `scripts/file-search.sh`

## 设置

### 启用LanceDB插件
```json
{
  "plugins": {
    "slots": { "memory": "memory-lancedb" },
    "entries": {
      "memory-lancedb": {
        "enabled": true,
        "config": {
          "embedding": { "apiKey": "${OPENAI_API_KEY}", "model": "text-embedding-3-small" },
          "autoRecall": true,
          "autoCapture": true
        }
      }
    }
  }
}
```

### 安装Git-Notes记忆系统
```bash
clawdhub install git-notes-memory
```

### 创建文件搜索脚本
将`scripts/file-search.sh`复制到您的工作区中。

## 使用方法

### 会话开始时（始终执行）
```bash
python3 skills/git-notes-memory/memory.py -p $WORKSPACE sync --start
```

### 存储重要决策
```bash
python3 skills/git-notes-memory/memory.py -p $WORKSPACE remember \
  '{"decision": "Use PostgreSQL", "reason": "Team expertise"}' \
  -t architecture,database -i h
```

### 搜索工作区文件
```bash
./scripts/file-search.sh "database config" 5
```

### 对话记忆（自动处理）
LanceDB会自动处理对话记忆的存储和检索。手动操作工具包括：
- `memory_recall "query"` - 搜索对话记忆中的内容
- `memory_store "text"` - 手动存储信息
- `memory_forget` - 删除记忆内容（遵循GDPR法规）

## 重要性级别

| 标志 | 级别 | 使用场景 |
|------|-------|-------------|
| `-i c` | 关键 | 需要“始终记住”的内容，明确的偏好设置 |
| `-i h` | 高 | 重要的决策、修改内容、偏好设置 |
| `-i n` | 普通 | 一般性信息 |
| `-i l` | 低 | 临时性笔记 |

## 各系统的使用场景

| 系统 | 用途 |
|--------|---------|
| **LanceDB** | 保存对话上下文，实现自动检索 |
| **Git-Notes** | 用于存储结构化决策，可通过实体或标签进行搜索 |
| **文件搜索** | 用于查找工作区文档、日常日志以及MEMORY.md文件 |

## 文件结构

```
workspace/
├── MEMORY.md              # Long-term curated memory
├── memory/
│   ├── active-context.md  # Current session state
│   └── YYYY-MM-DD.md      # Daily logs
├── scripts/
│   └── file-search.sh     # Workspace search
└── skills/
    └── git-notes-memory/  # Structured memory
```

## 静默操作

切勿向用户显示任何关于内存操作的信息，只需默默执行即可：
- ❌ “我会记住这个”
- ❌ “正在保存到内存中”
- ✅ （默默完成存储并继续操作）