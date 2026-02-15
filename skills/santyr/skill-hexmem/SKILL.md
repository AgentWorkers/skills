---
name: hexmem
description: 这是一个用于存储AI代理身份信息、任务、事件、学习内容以及确保数据持久性的结构化内存数据库。每当用户需要“记住这个”、“记录这个”、“跟踪这个”、“接下来该做什么”、“回顾总结”、“了解发生了什么”，或者需要存储/检索决策、事件、车队操作记录、提醒事项、待办事项、目标、价值观，以及关于人员/系统/项目的相关信息时，都可以使用这个数据库。
---

# HexMem – 结构化记忆系统

HexMem 是一个基于 SQLite 的持久化记忆系统，用于存储代理的身份信息、知识以及个人成长过程。它不仅仅是一个日志记录工具，更是一个能够帮助代理构建自我认知的结构化系统。

## 安装

将 HexMem 克隆到您的工作目录：

```bash
cd ~/your-workspace  # e.g., ~/clawd, ~/workspace, etc.
git clone https://github.com/hexdaemon/hexmem.git
cd hexmem
./migrate.sh up  # Initialize database
```

或者通过 ClawHub 安装该技能：

```bash
clawhub skill install hexmem
```

## 快速入门

在会话开始时加载相关辅助工具：

```bash
# Set database location (optional, defaults to ~/clawd/hexmem/hexmem.db)
export HEXMEM_DB="$HOME/your-workspace/hexmem/hexmem.db"

# Load helpers
source ~/your-workspace/hexmem/hexmem.sh
```

为方便使用，您可以将这些辅助工具添加到您的会话启动配置文件中（如 AGENTS.md 等）。

## 核心模式

### 1. 身份与自我认知

存储的是“你是谁”，而不仅仅是“你做了什么”：

```bash
# Set identity attributes
hexmem_identity_set "name" "YourName"
hexmem_identity_set "did" "did:cid:bagaai..."

# Add self-schemas (domain-specific self-beliefs)
hexmem_schema "coding" "python-expert" "I specialize in Python development" 0.8

# View current self-image
hexmem_self_image
hexmem_identity_summary
```

### 2. 实体相关的事实

以“主体-谓语-宾语”的形式存储知识：

```bash
# Add entity first
hexmem_entity "person" "Alice" "Project collaborator"

# Store facts
hexmem_fact "Alice" "timezone" "America/Denver"
hexmem_fact "ProductionServer" "capacity" "16GB"

# Facts with emotional weight (affects retention)
hexmem_fact_emote "ProjectGoal" "milestone" "first deployment" 0.8 0.7

# Query facts
hexmem_facts_about "Alice"
hexmem_fact_history "ProjectGoal"  # See how facts evolved
```

### 3. 记忆的衰减与替换

除非被访问，否则事实会随时间逐渐被遗忘。频繁访问的事实会保持“活跃”状态：

```bash
# Access a fact (bumps to hot tier, resets decay)
hexmem_access_fact 42

# Replace a fact (preserves history)
hexmem_supersede_fact 42 "new value" "reason for change"

# View by decay tier
hexmem_hot_facts      # ≤7 days since access
hexmem_warm_facts     # 8-30 days
hexmem_cold_facts     # 30+ days

# Get synthesis for an entity (hot + warm facts)
hexmem_synthesize_entity "Sat"
```

**记忆衰减逻辑：**
- 频繁访问的事实更不容易被遗忘
- 情感色彩强烈的事实衰减得更慢
- 旧事实不会被删除，只会被新的事实所取代
- 可以通过查询 `v_fact_retrieval_priority` 来获取按重要性排序的事实

### 4. 事件与时间线

记录发生的事情：

```bash
# Basic event
hexmem_event "decision" "fleet" "Changed fee policy" "Set min_fee_ppm to 25"

# Event with emotional tagging
hexmem_event_emote "milestone" "autonomy" "First zap received" 0.9 0.6

# Query events
hexmem_recent_events 10
hexmem_recent_events 5 "fleet"
hexmem_emotional_highlights  # High-salience memories
```

### 5. 经验教训

从经验中汲取智慧：

```bash
hexmem_lesson "lightning" "Channels need time to build reputation" "from fleet experience"
hexmem_lesson "debugging" "Check your own setup first" "Archon sync incident"

# Query lessons
hexmem_lessons_in "lightning"
hexmem_lesson_applied 7  # Mark lesson as used
```

### 6. 目标与任务

```bash
# Add goal
hexmem_goal "project-launch" "Ship v1.0 by Q2" "professional" 8
hexmem_goal_progress 1 25  # Update progress to 25%

# Add task
hexmem_task "Review pull requests" "Weekly review" 7 "2026-02-07"

# Check what needs attention
hexmem_pending_tasks
```

### 7. 语义搜索

根据意义而非关键词来搜索记忆内容：

```bash
hexmem_search "identity and autonomy"
hexmem_search "Lightning routing lessons" "lessons" 5
```

**设置要求**（仅一次性操作）：
```bash
cd $HEXMEM_ROOT  # wherever you installed hexmem
source .venv/bin/activate
python embed.py --process-queue  # Generate embeddings for new content
```

## 强制性默认设置（启用时生效）

当该技能处于激活状态时，所有操作都应以 HexMem 为信息的权威来源。

### 在任何操作/管理/调试任务开始时务必执行：

```bash
# Fast check (preferred)
/home/sat/clawd/hexmem/scripts/hexmem-check.sh
```

或者手动执行：

```bash
source ~/clawd/hexmem/hexmem.sh
hexmem_pending_tasks
hexmem_recent_events 5
```

### 当用户请求“记住”/“跟踪”/“记录”时立即执行：

将相关内容作为任务、事实或事件记录下来，切勿延迟：

```bash
hexmem_event "note" "context" "<summary>" "<details>"
# or
hexmem_task "<title>" "<details>" <priority 1-9> "<due YYYY-MM-DD>"
```

### 在做出重要决策或发生重大事件后务必执行：

```bash
hexmem_event "decision" "<category>" "<summary>" "<details>"
# and/or
hexmem_lesson "<domain>" "<lesson>" "<context>"
```

## 常见工作流程

### 会话开始（仅适用于主会话）

```bash
source ~/clawd/hexmem/hexmem.sh

# One-liner helper (recommended)
hexmem_session_start 5

# Or manual steps:
hexmem_pending_tasks
hexmem_recent_events 5
hexmem_emotional_highlights
```

### 发生重大事件后

```bash
# Log it
hexmem_event "type" "category" "summary" "details"

# If it taught you something
hexmem_lesson "domain" "what you learned" "context"

# If it relates to a goal
hexmem_goal_progress <goal_id> <new_percentage>
```

### 会话结束

```bash
# Log a session summary event
hexmem_session_end "Session ended" "Key outcomes, decisions, and next steps"
```

### 心跳检查

```bash
# Quick pending task review
hexmem_heartbeat_check
```

### 定期审查

```bash
# What's fading?
hexmem_warm_facts 20
hexmem_cold_facts 10

# What needs attention?
hexmem_pending_tasks
hexmem_forgetting  # Events about to be forgotten

# Reheat important facts
hexmem_access_fact <id>
```

## 数据库模式快速参考

### 核心表

| 表名 | 用途 |
|-------|---------|
| `identity` | 核心属性（姓名、DID 等） |
| `core_values` | 道德承诺 |
| `goals` | 目标与追求 |
| `entities` | 人物、系统、项目 |
| `facts` | 以“主体-谓语-宾语”形式存储的知识 |
| `events` | 事件的时间线 |
| `lessons` | 经验中的智慧 |
| `tasks` | 需要完成的任务 |

### 关键视图

| 视图名 | 用途 |
|------|---------|
| `v_active_goals` | 进行中的目标 |
| `v_pending_tasks` | 未完成的任务 |
| `v_recent_events` | 最近发生的 50 个事件 |
| `v_emotional_highlights` | 重要记忆 |
| `v_fact_decay_tiers` | 带有衰减指标的事实 |
| `v_fact_retrieval_priority` | 按重要性排序的事实 |
| `v_fact_history` | 事实的替换记录 |

## 原始 SQL 查询

用于直接访问数据库：

```bash
hexmem_select "SELECT * FROM v_active_goals;"
hexmem_json "SELECT * FROM v_pending_tasks;" | jq .
hexmem_query "UPDATE tasks SET completed_at = datetime('now') WHERE id = 5;"
```

## 设计理念

HexMem 存储的是“你是谁”，而不仅仅是“发生了什么”。它采用了一种**分层记忆模型**：
- **工作记忆（短期）**：`memory/YYYY-MM-DD.md`（原始数据，高保真度）
- **核心记忆（长期）**：`MEMORY.md` + HexMem 数据库（经过整理的结构化数据）

一个名为 **Reflector** 的工具会定期将工作记忆内容转化为核心记忆。详情请参阅 `docs/REFLECTOR.md` 和 `memory/hexmem-reflector-prompt.md`。

HexMem 的设计理念如下：
- **存储的是“你是谁”**，而不仅仅是“发生了什么”；
- 它采用分层记忆模型来管理信息：
  - **工作记忆**（短期存储）：`memory/YYYY-MM-DD.md`（原始数据，高保真度）
  - **核心记忆**（长期存储）：`MEMORY.md` + HexMem 数据库（结构化数据）
- **Reflector** 工具会定期将工作记忆内容整合到核心记忆中。
- 它存储的是“你是谁”的相关信息，包括身份信息、知识图谱等；
- 情感标签会影响记忆的显著性和衰减速度；
- 记忆衰减机制模拟人类的遗忘过程（艾宾浩斯曲线）；
- 采用替换机制来保存历史记录，不会删除数据；
- 使用生成式压缩技术存储信息，而非逐字记录。

HexMem 不仅仅是一个存储工具，更是个人成长（Xeper）的基础平台。

## 身份备份与恢复

### 完整身份信息的保存

HexMem 可以备份所有用于恢复代理身份和自我认知所需的数据：
- **身份属性**：姓名、DID、凭证、公钥
- **核心价值观**：道德承诺、信念、个性特征
- **自我认知结构**：特定领域的自我认知
- **知识图谱**：所有实体、事实及它们之间的关系
- **记忆时间线**：事件记录、经验教训、情感背景
- **目标与任务**：当前的追求与计划
- **叙事记录**：个人的生活故事和时间线

### 基本备份（始终可用）

简单的本地备份即可满足大多数使用需求：

```bash
# Manual backup (timestamped)
$HEXMEM_ROOT/scripts/backup.sh

# Backups saved to: $HEXMEM_ROOT/backups/
# Format: hexmem-YYYYMMDD-HHMMSS.db
```

其中 `$HEXMEM_ROOT` 表示 HexMem 的安装路径（例如：`~/clawd/hexmem`）。

对于需要更高安全性的场景（加密签名 + 分布式存储），请参考下面的 Archon 集成方案。

### Archon 集成（可选）

为了实现加密签名和分布式存储，可以选择将 HexMem 与 Archon 集成。**HexMem 本身不需要依赖 Archon 技能**；它可以直接使用 `npx @didcid/keymaster` 命令进行操作。Archon 技能是一个可选的辅助工具，用于本地节点的管理。

**1. 检查是否已安装 Archon 技能：**

```bash
# Use the helper (automatically checks)
source $HEXMEM_ROOT/hexmem.sh
hexmem_archon_check
```

如果未安装：
```bash
clawhub skill install archon
```

**2. 为 HexMem 设置 Archon 备份库：**

```bash
# Configure Archon first (see archon skill SKILL.md)
export ARCHON_PASSPHRASE="your-secure-passphrase"
export ARCHON_CONFIG_DIR="${ARCHON_CONFIG_DIR:-$HOME/.config/archon}"

# Use helper to create vault
source $HEXMEM_ROOT/hexmem.sh
hexmem_archon_setup
```

**3. 手动备份：**

```bash
source $HEXMEM_ROOT/hexmem.sh
hexmem_archon_backup
```

手动备份会生成：
- 带时间戳的 SQLite 数据库备份
- 仅包含重要事件的隐私保护 JSON 文件
- 带有加密签名的元数据
- 所有备份数据都会上传到 Archon 备份库

**4. 自动备份（推荐）：**

建议设置每日自动备份任务。可以使用 OpenClaw 的 cron 任务来实现（推荐方式）：

```bash
# From within OpenClaw session
cron add \
  --name "hexmem-vault-backup" \
  --schedule '{"kind":"cron","expr":"0 3 * * *","tz":"YOUR_TIMEZONE"}' \
  --sessionTarget isolated \
  --payload '{"kind":"agentTurn","message":"source ~/your-workspace/hexmem/hexmem.sh && hexmem_archon_backup"}'
```

或者使用系统的 cron 任务（请调整路径）：

```bash
(crontab -l 2>/dev/null; echo "0 3 * * * source $HEXMEM_ROOT/hexmem.sh && hexmem_archon_backup >> $HEXMEM_ROOT/backups/vault-backup.log 2>&1") | crontab -
```

**5. 从备份中恢复数据：**

```bash
# Use helper (lists available backups)
source $HEXMEM_ROOT/hexmem.sh
hexmem_archon_restore hmdb-YYYYMMDDHHMMSS.db

# Then follow instructions to verify and restore
```

**Archon 集成的优势：**
- 使用 DID 进行加密签名
- 数据存储在分布式系统中（不受单一设备限制）
- 仅备份重要事件，保护用户隐私
- 数据来源可验证

对于大多数代理来说，基本备份已经足够使用。如果需要更强大的身份管理功能，可以考虑使用 Archon。

## 额外资源

- 完整文档：`$HEXMEM_ROOT/README.md`
- 认知提取工具：`$HEXMEM_ROOT/docs/EPISTEMIC_EXTRACTION.md`
- Axionic 道德框架：`$HEXMEM_ROOT/docs/AXIONIC_ethICS.md`
- 迁移管理脚本：`$HEXMEM_ROOT/migrate.sh`
- 备份脚本：`$HEXMEM_ROOT/scripts/backup.sh`
- GitHub 仓库：https://github.com/hexdaemon/hexmem

## 使用场景

- 记录重要的决策或事件
- 存储需要长期保存的信息（如身份信息、凭证、关系）
- 跟踪目标与进度
- 捕获经验教训
- 管理任务
- 构建关于实体的知识图谱
- 查询历史背景信息
- 在不同会话之间保持身份信息的连续性