---
name: ichiro-mind
version: 1.0.0
description: "**Ichiro-Mind：专为AI代理设计的终极统一内存系统。**  
采用四层架构（HOT → WARM → COLD → ARCHIVE），结合神经图谱、向量搜索、经验学习以及自动内存管理机制，旨在实现持久化、高效且智能的内存管理功能。"
author: "兵步一郎 & OpenClaw Community"
keywords: [memory, ai-agent, long-term-memory, neural-graph, vector-search, experience-learning, ichiro, unified-memory, persistent-context, smart-recall]
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      env:
        - OPENAI_API_KEY
      plugins:
        - memory-lancedb
---
# 🧠 Ichiro-Mind

> “Ichiro-Mind——将所有记忆层统一成一个智能系统。”

**Ichiro-Mind** 是专为 AI 代理设计的终极统一记忆系统，它将五种经过验证的记忆技术整合到了一个统一的架构中。该系统的名称源自其创造者对持久化、智能化记忆的构想。

## 🏗️ 架构概述

```
┌─────────────────────────────────────────────────────────────────┐
│                    🧠 ICHIRO-MIND                               │
│              "The Mind That Never Forgets"                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ⚡ HOT LAYER (Working RAM)        🔥 WARM LAYER (Neural Net)   │
│  ┌─────────────────────┐          ┌─────────────────────┐       │
│  │ SESSION-STATE.md    │◄────────►│ Associative Memory  │       │
│  │ • Real-time state   │  Sync    │ • Spreading recall  │       │
│  │ • WAL protocol      │          │ • Causal chains     │       │
│  │ • Survives compact  │          │ • Contradiction det │       │
│  └─────────────────────┘          └─────────────────────┘       │
│           │                                │                    │
│           ▼                                ▼                    │
│  💾 COLD LAYER (Vectors)         📚 ARCHIVE LAYER (Long-term)   │
│  ┌─────────────────────┐          ┌─────────────────────┐       │
│  │ LanceDB Store       │          │ MEMORY.md + Daily   │       │
│  │ • Semantic search   │          │ • Git-Notes Graph   │       │
│  │ • Auto-extraction   │          │ • Cloud backup      │       │
│  │ • Importance score  │          │ • Human-readable    │       │
│  └─────────────────────┘          └─────────────────────┘       │
│                                                                 │
│  🧹 HYGIENE ENGINE              🎓 LEARNING ENGINE              │
│  • Auto-cleanup                 • Decision tracking             │
│  • Deduplication                • Error learning                │
│  • Token optimization           • Entity evolution              │
└─────────────────────────────────────────────────────────────────┘
```

## ✨ 核心特性

### 1. 智能记忆路由
根据查询类型自动选择最佳的检索方法：

| 查询类型 | 方法 | 速度 |
|------------|--------|-------|
| 最新上下文 | HOT（SESSION-STATE）| <10ms |
| 事实与偏好 | COLD（向量搜索）| ~50ms |
| 因果关系 | WARM（神经图）| ~100ms |
| 长期决策 | ARCHIVE（Git-Notes）| ~200ms |

### 2. 自动记忆生命周期管理
```
Capture → Extract → Process → Store → Recall → Cleanup
   │          │         │        │       │        │
Input    Mem0/Auto   Importance  4-Layer  Smart   Periodic
Capture   Extraction   Scoring   Storage  Route   Hygiene
```

### 3. 带有扩散激活机制的神经图
- **非关键词搜索**——通过图谱遍历找到概念上相关的记忆
- **20 种突触类型**——时间、因果、语义、情感关联
- **赫布学习**——记忆会随着使用而增强
- **矛盾检测**——自动识别冲突信息

### 4. 经验学习
```
Decision → Action → Outcome → Lesson
    │         │        │         │
   Store    Track    Record    Learn
```
- 跟踪决策及其结果
- 从错误中学习
- 根据过去的模式提供建议

### 5. 智能记忆管理
- 自动清除无用的记忆
- 删除重复条目
- 优化内存使用效率
- 提供每月维护功能

## 🚀 快速入门

### 安装
```bash
clawhub install ichiro-mind
```

### 设置
```bash
# Initialize Ichiro-Mind
ichiro-mind init

# Configure MCP
ichiro-mind setup-mcp
```

### 基本使用
```python
from ichiro_mind import IchiroMind

# Initialize
mind = IchiroMind()

# Store memory (auto-routes to appropriate layer)
mind.remember(
    content="User prefers dark mode",
    category="preference",
    importance=0.9
)

# Recall with smart routing
result = mind.recall("What mode does user prefer?")

# Learn from experience
mind.learn(
    decision="Used SQLite for dev",
    outcome="slow_with_big_data",
    lesson="Use PostgreSQL for datasets >1GB"
)
```

## 📝 记忆层详解

### HOT 层 — SESSION-STATE.md
使用预写日志协议（Write-Ahead Log Protocol）的实时工作记忆。

**WAL 协议**：在响应之前写入数据，而不是之后。

### WARM 层 — 神经图
基于扩散激活机制的关联记忆系统。

```python
# Store with relationships
mind.remember(
    content="Use PostgreSQL for production",
    type="decision",
    tags=["database", "infrastructure"],
    relations=[
        {"type": "CAUSED_BY", "target": "performance_issues"},
        {"type": "LEADS_TO", "target": "better_scalability"}
    ]
)

# Deep recall
memories = mind.recall_deep(
    query="database decisions",
    depth=2  # Follow causal chains
)
```

### COLD 层 — 向量存储
使用 LanceDB 进行语义搜索。

```python
# Auto-captured from conversation
mind.auto_capture(text="User likes minimal UI")

# Semantic search
results = mind.search("user interface preferences")
```

### ARCHIVE 层 — 持久化存储
可被人类读取的长期记忆存储。

```
workspace/
├── MEMORY.md              # Curated long-term
└── memory/
    ├── 2026-03-07.md      # Daily log
    ├── decisions/         # Structured decisions
    ├── entities/          # People, projects, concepts
    └── lessons/           # Learned experiences
```

## 🛠️ 高级特性

### 记忆管理
```bash
# Audit memory
ichiro-mind audit

# Clean junk
ichiro-mind cleanup --dry-run
ichiro-mind cleanup --confirm

# Optimize tokens
ichiro-mind optimize
```

### 经验回放
```python
# Before making similar decision
similar = mind.get_lessons(context="database_choice")
# Returns past decisions and outcomes
```

### 实体跟踪
```python
# Track evolving entities
mind.track_entity(
    name="兵步一郎",
    type="person",
    attributes={
        "role": "creator",
        "interests": ["AI", "automation"],
        "preferences": {"ui": "minimal", "docs": "bilingual"}
    }
)

# Update entity
mind.update_entity("兵步一郎", {"last_contact": "2026-03-07"})
```

## 🔌 与 MCP 的集成
将配置添加到 `~/.openclaw/mcp.json` 文件中：

```json
{
  "mcpServers": {
    "ichiro-mind": {
      "command": "python3",
      "args": ["-m", "ichiro_mind.mcp"],
      "env": {
        "ICHIRO_MIND_BRAIN": "default"
      }
    }
  }
}
```

## 📊 性能指标

| 操作 | 延迟 | 吞吐量 |
|-----------|---------|------------|
| HOT 检索 | <10ms | 10K 次/秒 |
| WARM 检索 | ~100ms | 1K 次/秒 |
| COLD 搜索 | ~50ms | 500 次/秒 |
| ARCHIVE 读取 | ~200ms | 100 次/秒 |
| 存储记忆 | ~20ms | 5K 次/秒 |

## 🎯 使用场景

1. **长期项目**——在不同会话间保持上下文一致
2. **复杂决策**——追踪决策过程及其结果
3. **用户关系**——记住用户的偏好、历史行为和习惯
4. **错误预防**——从错误中学习，提供替代方案
5. **知识积累**——逐步建立领域专业知识

## 🧠 哲学理念

> “记忆不仅仅是存储工具，更是智能的体现。”

Ichiro-Mind 将记忆视为一种重要的资源：
- 记忆之间存在关联
- 记忆会随时间演变
- 记忆需要竞争用户的注意力
- 未使用的记忆会逐渐衰退
- 冲突的信息会被自动解决

## 📚 相关技术

- **elite-longterm-memory**——基础层架构
- **neural-memory**——关联图谱引擎
- **memory-hygiene**——记忆清理与优化
- **memory-setup**——记忆的配置与管理

## 🙏 致谢

由 **兵步一郎**（Ichiro）怀着对持久化、智能化 AI 记忆技术的热爱而开发。

该系统的设计灵感来源于 OpenClaw 生态系统中最好的记忆系统。

## 许可证

MIT 许可证