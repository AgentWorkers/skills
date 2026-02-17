---
name: q-memory
description: >
  **Universal Memory Management System v1.8.2** 专为 OpenClaw 代理设计，提供以下功能：  
  1. **多代理支持**（qst、mengtian、lisi、自定义代理类型）  
  2. **代理状态管理系统**（“我正在执行”：IDLE/DOING/WAITING/PAUSED/COMPLETED/FAILED/BLOCKED）  
  3. **心跳机制集成**——基于代理状态的智能检查策略  
  4. **新功能 v1.8.2**：循环保护机制与用户优先级功能——自动检测并处理卡住的任务  
  5. **基于树的分类结构**（三级层次结构）  
  6. **三种搜索方式**：树形搜索、语义搜索、混合搜索  
  7. **人工智能辅助的分类功能**  
  8. **技术文档的附录索引**  
  9. **敏感数据加密**（使用 AES-128-CBC + HMAC 算法）  
  10. **事件历史记录**（支持时间线显示）  
  **适用场景**：当代理需要具备智能内存管理功能及状态感知能力时。  
  **目标**：  
  - 将令牌消耗量降低 70-90%  
  - 提高数据的相关性 20%  
  - 增强系统的上下文感知能力  
  **v1.8.2 的循环保护机制**：通过心跳机制、超时检测及自动恢复功能，有效防止任务陷入无限循环。
---
# Universal Memory Management v1.8.2

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

| 方法 | 优点 | 使用场景 |
|--------|----------|----------|
| **树搜索** | 精确匹配 | 确切知道所需类别时使用 |
| **选择规则** | 几何邻居算法 | 当 C_ab = 1 时，查找相邻元素 |
| **语义搜索（v1.5）** | TF-IDF + 上下文分析 | 智能推理 |

### v1.5 版本的语义搜索功能增强

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

| 权重 | 触发关键词 |
|--------|-----------------|
| **[C]** 关键词 | key, token, config, 密鑰, 決策 |
| **[I]** 重要词汇 | project, plan, 專案, 討論, 偏好 |
| **[N]** 常见词汇 | chat, greeting, 問候, 閒聊 |

---

## 🧹 内存衰减系统（v1.5 新功能）

### 数据清理规则

| 权重 | 阈值 | 处理方式 |
|--------|-----------|--------|
| **[C]** 关键数据 | 永久保存 | 从不删除 |
| **[I]** 重要数据 | 365天后 | 归档 |
| **[N]** 常见数据 | 30天后 | 删除 |

### 内存衰减系数

```
[C]: 2.0 (never decay)
[I]: max(0.5, 1.5 - age * 0.1/365)
[N]: max(0.1, 1.0 - age * 0.5/30)
```

---

## 🤖 代理状态系统（v1.7 新功能）

### 状态机

代理状态系统能够根据代理的当前状态来智能地调整心跳检测频率：

| 状态 | 描述 | 心跳检测行为 |
|-------|-------------|-------------------|
| **IDLE** | 代理处于空闲状态 | 进行全面检查（@提及、回复、投票） |
| **DOING** | 代理正在执行任务 | 仅进行关键检查（@提及、回复，不参与投票） |
| **WAITING** | 代理正在等待条件触发 | 进行快速检查（仅检查@提及） |
| **PAUSED** | 代理处于暂停状态 | 跳过检查 |
| **COMPLETED** | 任务已完成 | 进行全面检查 |
| **FAILED** | 任务失败 | 进行全面检查 |

### 代理状态的使用方法

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

### 事件记录

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

## 🛡️ 循环保护系统（v1.8.2 新功能）

### 防止无限循环机制

v1.8.2 版本引入了全面的保护机制，以防止任务陷入无限循环或系统资源耗尽。

#### 保护层次

```
Layer 1: Heartbeat Throttling
  - Minimum 30-second interval between checks
  - Prevents rapid-fire heartbeat calls

Layer 2: Stagnation Detection
  - Detects tasks with no progress for 15+ minutes
  - Tracks progress history automatically

Layer 3: Timeout Detection
  - Priority-based timeouts:
    * Critical: 30 minutes
    * High: 45 minutes
    * Normal: 60 minutes
    * Low: 120 minutes

Layer 4: Auto-Recovery
  - Automatic priority downgrade (critical → high → normal)
  - Auto-BLOCK for extreme timeout (2x threshold)
  - Requires human intervention for resolved blocked tasks
```

#### 配置设置

```json
{
  "loop_protection": {
    "critical_timeout_minutes": 30,
    "high_timeout_minutes": 45,
    "normal_timeout_minutes": 60,
    "low_timeout_minutes": 120,
    "heartbeat_min_interval_seconds": 30,
    "stagnation_threshold_minutes": 15,
    "auto_downgrade_on_stagnation": true,
    "max_stagnant_checks": 10
  }
}
```

#### API 接口

```python
# Check if task is stuck
is_stagnant, reason = state_mgr.is_stagnant()

# Check if task has timed out
is_timeout, reason, minutes = state_mgr.is_timeout()

# Auto-handle stuck tasks
result = state_mgr.auto_handle_stagnation()
# Returns: {"action": "downgrade" | "block" | "none", ...}

# Check if heartbeat should be throttled
should_throttle, reason, wait_seconds = state_mgr.should_throttle_heartbeat()
```

#### 自动恢复机制

| 情况 | 处理方式 | 触发条件 |
|-----------|--------|---------|
| **关键任务停滞** | 将系统降级为高级模式 | 任务30分钟以上无进展 |
| **关键任务超时** | 将系统降级为高级模式 | 任务超时30分钟以上 |
| **高级任务停滞** | 将系统降级为普通模式 | 任务15分钟以上无进展 |
| **高级任务截止日期（超时2倍）** | 自动锁定系统 | 任务截止日期超时90分钟以上 |
| **普通任务截止日期（超时2倍）** | 自动锁定系统 | 任务截止日期超时120分钟以上 |

#### 带有循环保护功能的心跳检测输出

```
============================================================
❤️  Heartbeat Started: 2026-02-15 16:05:00 UTC
============================================================

🤖 Agent: lisi | 狀態: DOING | 優先級: CRITICAL
   任務: 測試防死循環保護
   進度: 42%

🛡️  Loop Protection:
   ✅ 心跳頻率正常 (上次檢查: 32 秒前)
   ✅ 任務未停滯 (上次更新: 5 分鐘前)
   ✅ 未超時 (運行時間: 25 分鐘 < 閾值: 30 分鐘)

🔄 狀態: DOING [CRITICAL] - 最小化干擾
   📢 通知: 0 提及, 0 回覆
   ❌ 跳過: HKGBook 巡邏, 投票檢查

============================================================
✅ Heartbeat Completed: 2026-02-15 16:05:01 UTC
============================================================
```

#### 心跳检测的节流机制

```
[lisi] ⏸️ 心跳頻率限制：Too frequent (3s < 30s)（等待 27 秒）

Check Result:
  - 來源: lisi_doing-state.json
  - 邏輯: 當前時間 - 上次檢查時間 < 最小間隔
  - 行動: 跳過本次檢查
  - 原因: 避免死循環，保護系統資源
```

### 解决无限循环问题

**问题**（v1.8初始版本）：
```json
{
  "status": "doing",
  "task": "Q Memory v1.8 實施",
  "progress": 0,
  "priority": "critical",
  "start_time": "14:08:59"
}
```
任务在0%的状态下停滞了1.77小时，导致无限循环。

**解决方案**（v1.8.2版本）：
```
Heartbeat Check 1 (16:00):
  - Check interval: 0 seconds (OK)
  - Task timeout: 51+ minutes > 30m threshold
  - Auto-action: DOWNGRADE priority (critical → high)

Heartbeat Check 2 (16:05):
  - Check interval: 300 seconds (OK, >30s min)
  - Task timeout: 56+ minutes > 45m threshold
  - Stagnation detected (0% for 15+ min)
  - Auto-action: BLOCK task (requires human intervention)

Result:
  - Priority: high
  - Status: BLOCKED
  - Reason: "任務停滯過久: 執行時間 56 分鐘超限（閾值：45 分鐘）"
  - Heartbeat: Only check @mentions and alerts
  - Loop eliminated ✅
```

---

## 👤 用户优先级响应机制（v1.8.2 新功能）

v1.8.2版本引入了**用户优先级窗口**，确保系统的心跳检测不会干扰用户的实时对话。

### 工作原理：

1. **检测**：记录用户最后一次交互的时间戳。
2. **优先级窗口**：定义一个优先窗口（默认30分钟），在此期间用户的操作具有最高优先级。
3. **跳过检测**：如果系统心跳检测发生在优先窗口内，将自动跳过检测。
4. **安全阀**：允许系统最多跳过指定次数的检测（默认3次），之后才会强制进行检查，以确保系统正常运行。

### 配置设置

### 用户优先级模式下的心跳检测输出

---

## 💓 心跳检测功能的集成（v1.7.1 新功能）

### 基于状态的检测策略

系统会根据代理的状态智能调整心跳检测的频率：

```python
# When agent is DOING: Only check critical notifications
# - ✅ Check: @mentions, replies
# - ❌ Skip: Voting (to avoid interrupting work)

# When agent is IDLE: Full checking
# - ✅ Check: @mentions, replies, voting
```

### 心跳检测功能的配置方法

```bash
# Copy integration script to workspace
cp scripts/heartbeat_integration.py /home/node/.openclaw/workspace/heartbeat.py
chmod +x /home/node/.openclaw/workspace/heartbeat.py

# Set up cron task (every 20 minutes)
crontab -e
# Add: */20 * * * * python3 /home/node/.openclaw/workspace/heartbeat.py
```

### 心跳检测的输出结果

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

系统支持使用工业级加密技术来保护敏感数据（如API密钥、密码、令牌）：

```python
from crypto import MemoryCrypto

crypto = MemoryCrypto()
encrypted = crypto.encrypt("GitHubPAT: ghp_xxx...")
# Output: ENC::gAAAAABgF7qj... (encrypted string)

decrypted = crypto.decrypt(encrypted)
# Output: "GitHubPAT: ghp_xxx..."
```

### 密钥管理

- **密钥存储位置**：`~/.qst_memory.key`（权限设置为600）
- **密钥生成方式**：PBKDF2HMAC（SHA256，480,000次迭代）
- **加密算法**：Fernet（AES-128-CBC + HMAC）

---

## 📊 统计面板

```bash
python qst_memory.py stats
```

### 输出结果展示

```
📊 Q Memory v1.5 統計面板
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
q-memory/
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

| 版本 | 令牌数量/查询次数 | 相关性 |
|---------|--------------|-----------|
| v1.2 | 约500个 | 85% |
| v1.4 | 约300个 | 90% |
| **v1.5** | 约200个 | 95% |
| **改进**：令牌数量减少60%，相关性提升95% |

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
clawhub install q-memory
```

### 从 GitHub 安装

```bash
git clone https://github.com/ZhuangClaw/q-memory-skill.git
```

*Q Memory v1.5——构建下一代人工智能内存管理系统。*