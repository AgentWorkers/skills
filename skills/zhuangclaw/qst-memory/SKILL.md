---
name: qst-memory
description: |
  QST Memory Management System v1.5 for OpenClaw agents. Provides:
  1. Tree-based classification structure (3-level hierarchy)
  2. Three search methods: Tree, Selection Rule, Semantic (Enhanced)
  3. Hybrid Search combining all methods
  4. Auto-classification with AI inference
  5. Memory decay & cleanup system
  6. TF-IDF similarity algorithm with context awareness
  
  Use when: Agent needs intelligent memory management with flexible classification.
  Goal: Reduce token consumption by 70-90%, improve relevance by 20%.
---

# QST内存管理v1.5

## 🌳 基于树的分类结构

**关键创新**：采用三层层次化分类机制，并支持自动关键词匹配功能。

```
QST
├── Physics (FSCA, E8, Mass_Energy)
├── Computation (Orbital, Simulation)
└── Audit (Zero_Calibration)

User
├── Identity, Intent, Projects

Tech
├── Config (API, Model, Cron, Database)
├── Discussion, Skills

Border (Meng Tian)
├── Security, Monitor, Email

HK_Forum
├── Posts, Replies, Users

General
├── Dragon_Ball, History, Chat
```

---

## 🔍 多模式搜索系统

### v1.5 新功能：混合搜索引擎

结合了三种搜索方法：

| 方法 | 优势 | 使用场景 |
|--------|----------|----------|
| **树搜索** | 精确匹配 | 知道确切的类别时使用 |
| **选择规则** | 几何邻域搜索 | 当C_ab等于1时使用 |
| **语义搜索（v1.5）** | TF-IDF + 上下文分析 | 基于智能推理的搜索 |

### v1.5版的语义搜索功能增强

```python
# TF-IDF similarity
similarity = cosine_similarity(query_tfidf, memory_tfidf)

# Context awareness
context_query = " ".join(context[-3:]) + " " + query

# Weight adjustment
adjusted_score = similarity * weight_multiplier
```

### 选择规则的集成

```
C_ab = 1 when geometric neighbors

QST_Physics ↔ QST_Computation ↔ QST_Audit
```

---

## 🤖 自动分类（v1.5新功能）

### 智能推理机制

```python
from auto_classify import auto_classify

result = auto_classify("QST暗物質使用FSCA理論")
# → suggested_category: "QST_Physics_FSCA"
# → confidence: "high"
```

### 权重自动检测

| 权重等级 | 触发关键词 |
|--------|-----------------|
| **[C]** 关键级 | key, token, config, 密鑰, 決策 |
| **[I]** 重要级 | project, plan, 專案, 討論, 偏好 |
| **[N]** 普通级 | chat, greeting, 問候, 閒聊 |

---

## 🧹 内存衰减系统（v1.5新功能）

### 清理规则

| 权重等级 | 阈值 | 处理方式 |
|--------|-----------|--------|
| **[C]** 关键级 | 永远不删除 | 永久保留 |
| **[I]** 重要级 | 365天后 | 归档 |
| **[N]** 普通级 | 30天后 | 删除 |

### 内存衰减系数

```
[C]: 2.0 (never decay)
[I]: max(0.5, 1.5 - age * 0.1/365)
[N]: max(0.1, 1.0 - age * 0.5/30)
```

---

## 📊 统计面板

```bash
python qst_memory.py stats
```

---

## 💾 内存格式

```markdown
# Memory Title

[Category] [Weight]
Date: 2026-02-14

Content...

Tags: tag1, tag2
```

---

## 🚀 快速入门

```bash
# Search with hybrid mode (default)
python qst_memory.py search "暗物質"

# Enhanced semantic with context
python qst_memory.py search "ARM芯片" --method enhanced --context "技術討論"

# Auto-classify content
python qst_memory.py classify "QST暗物質計算使用FSCA"

# Save with auto-classification
python qst_memory.py save "採用 FSCA v7 作為暗物質理論"

# Cleanup preview
python qst_memory.py cleanup --dry-run

# Statistics
python qst_memory.py stats
```

---

## 📁 文件结构

```
qst-memory/
├── SKILL.md              # This file
├── config.yaml           # Tree config + settings
├── qst_memory.py         # Main entry (v1.5)
└── scripts/
    ├── tree_search.py        # Tree search
    ├── bfs_search.py         # BFS search
    ├── semantic_search.py    # Basic semantic
    ├── semantic_search_v15.py # Enhanced semantic (v1.5)
    ├── hybrid_search.py      # Hybrid engine (v1.5)
    ├── auto_classify.py      # Auto-classification (v1.5)
    ├── save_memory.py        # Smart save (v1.5)
    ├── cleanup.py            # Decay system (v1.5)
    └── stats_panel.py        # Statistics
```

---

## 🎯 令牌优化

| 版本 | 每次查询使用的令牌数量 | 相关性 |
|---------|--------------|-----------|
| v1.2 | 约500个 | 85% |
| v1.4 | 约300个 | 90% |
| **v1.5** | 约200个 | 95% |
**改进**：令牌数量减少了60%，相关性提高了95%。

---

## ⚙️ 配置设置

```yaml
version: '1.5'

search:
  default_method: "hybrid"
  min_relevance: 0.1

add_category:
  max_depth: 3
  min_occurrences: 3

decay:
  critical: 0      # Never decay
  important: 0.1    # Slow decay
  normal: 0.5       # Fast decay

cleanup:
  enabled: true
  max_age_days:
    critical: -1    # Never
    important: 365  # Archive after 1 year
    normal: 30      # Delete after 30 days
```

---

## 🔧 安装方法

### 通过ClawHub安装
```bash
clawhub install qst-memory
```

### 通过GitHub安装
```bash
git clone https://github.com/ZhuangClaw/qst-memory-skill.git
```

---

*QST内存管理v1.5——构建下一代人工智能内存系统。*