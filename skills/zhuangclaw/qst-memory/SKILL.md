---
name: qst-memory
description: >
  **OpenClaw代理的通用内存管理系统 v1.7.1**  
  该系统为OpenClaw代理提供以下功能：  
  1. **多代理支持**（qst、mengtian、lisi、自定义代理类型）  
  2. **代理状态管理系统**（“正在执行”/空闲/等待/暂停/已完成/失败）  
  3. **心跳信号集成**——基于代理状态的智能检查机制  
  4. **基于树的分类结构**（三级层次结构）  
  5. **三种搜索方式**：树状搜索、语义搜索、混合搜索  
  6. **人工智能辅助的自动分类功能**  
  7. **技术文档的附录索引系统**  
  8. **敏感数据的加密机制**（AES-128-CBC + HMAC）  
  9. **带有时间线的事件历史记录功能**  
  **适用场景**：  
  当代理需要具备智能内存管理功能以及状态感知能力时。  
  **目标效果**：  
  - 减少令牌消耗量70-90%  
  - 提高数据相关性20%  
  - 增强数据的上下文感知能力（即数据与使用场景的关联性）
---
# Universal Memory Management v1.7.1

## 🌳 基于树的分类结构

**核心创新**：采用三层分层分类机制，并具备自动关键词匹配功能。

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

该系统结合了三种搜索方法：

| 搜索方法 | 优势 | 使用场景 |
|--------|----------|----------|
| **树搜索** | 精确匹配 | 确切知道所属类别时使用 |
| **选择规则** | 几何邻域搜索 | 当 C_ab = 1 时使用 |
| **语义搜索（v1.5）** | TF-IDF + 上下文分析 | 基于智能推理的搜索 |

### v1.5 版本中的语义搜索功能增强

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

## 🤖 自动分类功能（v1.5 新功能）

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
| **[C]** 重要 | 关键词、令牌、配置信息、密钥、决策 |
| **[I]** 中等重要 | 项目、计划、讨论、偏好 |
| **[N]** 一般 | 聊天内容、问候语、闲聊信息 |

---

## 🧹 内存衰减系统（v1.5 新功能）

### 数据清理规则

| 权重等级 | 清理阈值 | 处理方式 |
|--------|-----------|--------|
| **[C]** 重要数据 | 永久保留 | 不进行清理 |
| **[I]** 中等重要数据 | 365天后归档 | |
| **[N]** 一般数据 | 30天后删除 | |

### 内存数据衰减系数

```
[C]: 2.0 (never decay)
[I]: max(0.5, 1.5 - age * 0.1/365)
[N]: max(0.1, 1.0 - age * 0.5/30)
```

---

## 🤖 代理状态系统（v1.7 新功能）

### 状态机机制

代理状态系统能够根据代理的当前状态智能调整心跳检测的频率：

| 状态 | 描述 | 心跳检测行为 |
|-------|-------------|-------------------|
| **空闲（IDLE）** | 代理处于空闲状态 | 进行全面检查（包括@提及、回复和投票） |
| **工作中（DOING）** | 代理正在执行任务 | 仅进行关键检查（包括@提及和回复，不参与投票） |
| **等待中（WAITING）** | 代理正在等待条件满足 | 进行快速检查（仅检查@提及） |
| **暂停（PAUSED）** | 代理处于暂停状态 | 跳过检查 |
| **已完成（COMPLETED）** | 任务已完成 | 进行全面检查 |
| **失败（FAILED）** | 任务失败 | 进行全面检查 |

### 如何使用代理状态系统

```bash
# Start a task (switches to DOING mode)
python universal_memory.py --agent qst doing start \
  --task "QST FSCA simulation #42" \
  --type Research

# Update progress
python universal_memory.py --agent qst doing update --progress 50

# Pause task
python universal_memory.py --agent qst doing pause --reason "Waiting for resources"

# Resume task
python universal_memory.py --agent qst doing resume

# Complete task
python universal_memory.py --agent qst doing complete --result "Simulation successful: ρ=0.08"

# View current status
python universal_memory.py --agent qst doing status

# View event history
python universal_memory.py --agent qst doing events
```

### 事件日志记录

所有状态变化都会自动记录，并附带时间戳：

```json
{
  "events": [
    {
      "timestamp": "2026-02-15T09:01:22.206211",
      "event_type": "TASK_START",
      "description": "开始: QST simulation #42",
      "progress": 0
    },
    {
      "timestamp": "2026-02-15T09:15:40.754321",
      "event_type": "PROGRESS_UPDATE",
      "description": "进度: QST simulation #42 (50%)",
      "progress": 50
    },
    {
      "timestamp": "2026-02-15T09:25:52.121518",
      "event_type": "TASK_COMPLETED",
      "description": "完成: QST simulation #42",
      "result": "Simulation successful"
    }
  ]
}
```

---

## 💓 心跳检测功能（v1.7.1 新功能）

### 基于状态的自适应检测策略

系统会根据代理的状态智能调整心跳检测的频率：

```python
# When agent is DOING: Only check critical notifications
# - ✅ Check: @mentions, replies
# - ❌ Skip: Voting (to avoid interrupting work)

# When agent is IDLE: Full checking
# - ✅ Check: @mentions, replies, voting
```

### 如何配置心跳检测功能

```bash
# Copy integration script to workspace
cp scripts/heartbeat_integration.py /home/node/.openclaw/workspace/heartbeat.py
chmod +x /home/node/.openclaw/workspace/heartbeat.py

# Set up cron task (every 20 minutes)
crontab -e
# Add: */20 * * * * python3 /home/node/.openclaw/workspace/heartbeat.py
```

### 心跳检测结果输出

```
============================================================
❤️  Heartbeat Started: 2026-02-15 09:15:26 UTC
============================================================

🤖 Agent: qst | 狀態: DOING
   任務: QST simulation #42
   類型: Research
   進度: 50%

🔄 狀態: DOING - 執行 HKGBook 檢查 (策略: 簡化)
   📢 通知: 0 提及, 0 回覆
   ⚠️  DOING/WAITING - 跳過投票
   ✅ HKGBook 檢查完成

============================================================
✅ Heartbeat Completed: 2026-02-15 09:15:28 UTC
============================================================
```

### 多代理支持

每个代理都维护自己的独立状态：

```bash
# qst agent
/data/qst_doing-state.json

# mengtian agent
/data/mengtian_doing-state.json

# lisi agent
/data/lisi_doing-state.json
```

---

## 🔐 内存加密（v1.7 新功能）

### 使用 AES-128-CBC + HMAC 加密算法

系统支持使用工业级加密技术来保护敏感数据（如 API 密钥、密码、令牌）：

```python
from crypto import MemoryCrypto

crypto = MemoryCrypto()
encrypted = crypto.encrypt("GitHubPAT: ghp_xxx...")
# Output: ENC::gAAAAABgF7qj... (encrypted string)

decrypted = crypto.decrypt(encrypted)
# Output: "GitHubPAT: ghp_xxx..."
```

### 密钥管理

- **密钥存储位置**：`~/.qst_memory.key`（权限设置为 600）
- **密钥生成方式**：PBKDF2HMAC（SHA256，480,000 次迭代）
- **加密算法**：Fernet（AES-128-CBC + HMAC）

---

## 📊 统计面板

```bash
python qst_memory.py stats
```

### 统计结果输出

```
📊 QST Memory v1.5 統計面板
├── 分類結構: 34 分類
├── 記憶總數: 156 條
├── Token 估算: ~8,500
└── 衰減狀態: 3 條高衰減
```

---

## 💾 内存数据格式

```markdown
# Memory Title

[Category] [Weight]
Date: 2026-02-14

Content...

Tags: tag1, tag2
```

---

## 🚀 快速入门指南

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

## 📁 文件结构说明

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

| 版本 | 每次查询使用的令牌数量 | 相关性评分 |
|---------|--------------|-----------|
| v1.2 | 约 500 个令牌 | 85% 的相关性 |
| v1.4 | 约 300 个令牌 | 90% 的相关性 |
| **v1.5** | 约 200 个令牌 | 95% 的相关性 |
| **改进**：令牌使用量减少了 60%，相关性提高了 95% |

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

## 🔧 安装指南

### 从 ClawHub 安装

```bash
clawhub install qst-memory
```

### 从 GitHub 安装

```bash
git clone https://github.com/ZhuangClaw/qst-memory-skill.git
```

*QST Memory v1.5——构建下一代人工智能内存管理系统。*