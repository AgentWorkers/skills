---
name: tiered-memory
description: "EvoClaw 分层内存架构 v2.2.0——一个基于 LLM（大型语言模型）的三层内存系统，具备自动每日数据摄取、结构化元数据提取、URL 保留、数据验证以及优先采用云同步的功能。"
version: "2.2.0"
---

# 分层记忆系统 v2.2.0

> “一个记住一切的头脑和一个什么都不记得的头脑一样无用。真正的艺术在于知道该记住什么。” 🧠

这款与EvoClaw兼容的三层记忆系统借鉴了人类的认知方式和PageIndex树的检索机制。

## v2.2.0的新功能

🔄 **自动每日笔记导入**
- `daily`/`monthly`/`full`模式现在会自动运行`ingest-daily`命令
- 将`memory/YYYY-MM-DD.md`文件整合到分层记忆系统中
- 无需手动导入——信息会自动流动
- 修复了“两条数据路径分离”的问题

## v2.1.0的新功能

🎯 **结构化元数据提取**
- 从笔记中自动提取URL、shell命令和文件路径
- 在信息提炼和整合过程中保留这些元数据
- 可通过URL片段进行搜索

✅ **记忆完整性验证**
- 每日检查笔记中是否缺少URL、命令或后续步骤
- 对不完整的信息发出主动警告
- 提出可操作的改进建议

🔍 **增强搜索功能**
- 可通过URL片段搜索笔记内容
- 从“热记忆”中获取所有存储的URL
- 元数据被用于存储笔记内容

🛡️ **URL保存**
- 在LLM信息提炼过程中明确保存URL
- 如果LLM无法获取URL，则使用备用元数据
- 提供命令行接口用于手动添加元数据

## 架构

```
┌─────────────────────────────────────────────────────┐
│              AGENT CONTEXT (~8-15KB)                │
│                                                     │
│  ┌──────────┐  ┌────────────────────────────────┐  │
│  │  Tree    │  │  Retrieved Memory Nodes         │  │
│  │  Index   │  │  (on-demand, 1-3KB)            │  │
│  │  (~2KB)  │  │                                │  │
│  │          │  │  Fetched per conversation      │  │
│  │  Always  │  │  based on tree reasoning       │  │
│  │  loaded  │  │                                │  │
│  └────┬─────┘  └────────────────────────────────┘  │
│       │                                             │
└───────┼─────────────────────────────────────────────┘
        │
        │ LLM-powered tree search
        │
┌───────▼─────────────────────────────────────────────┐
│              MEMORY TIERS                           │
│                                                     │
│  🔴 HOT (5KB)      🟡 WARM (50KB)     🟢 COLD (∞)  │
│                                                     │
│  Core memory       Scored facts      Full archive  │
│  - Identity        - 30-day         - Turso DB     │
│  - Owner profile   - Decaying       - Queryable    │
│  - Active context  - On-device      - 10-year      │
│  - Lessons (20 max)                                │
│                                                     │
│  Always in         Retrieved via     Retrieved via │
│  context           tree search       tree search   │
└─────────────────────────────────────────────────────┘
```

## 设计原则

### 基于人类记忆的机制
- **整合**：在整合周期内将短期记忆转化为长期记忆
- **相关性衰减**：未使用的记忆会逐渐消失；被访问的记忆会变得更加牢固
- **战略性遗忘**：不记住一切是一种能力
- **分层组织**：按类别导航，而非线性扫描

### 基于PageIndex的机制
- **无向量检索**：使用LLM进行推理，而非基于相似度
- **树状索引**：O(log n)级别的导航效率，而非O(n)级别的线性扫描
- **可解释的结果**：每次检索都会显示一条路径
- **基于推理的搜索**：询问“为什么相关？”而非“有多相似？”

### 以云为先（EvoClaw）
- **设备可更换**：信息存储在云端（Turso）
- **关键数据同步**：每次对话后都会同步热数据和树状索引
- **灾难恢复**：可在2分钟内完全恢复数据
- **多设备支持**：手机/桌面/嵌入式设备均可使用同一系统

## 记忆层次

### 🔴 热记忆（最大5KB）

**用途：**存储核心身份和当前上下文信息，始终显示在代理的界面中。

**结构：**
```json
{
  "identity": {
    "agent_name": "Agent",
    "owner_name": "User",
    "owner_preferred_name": "User",
    "relationship_start": "2026-01-15",
    "trust_level": 0.95
  },
  "owner_profile": {
    "personality": "technical, direct communication",
    "family": ["Sarah (wife)", "Luna (daughter, 3yo)"],
    "topics_loved": ["AI architecture", "blockchain", "system design"],
    "topics_avoid": ["small talk about weather"],
    "timezone": "Australia/Sydney",
    "work_hours": "9am-6pm"
  },
  "active_context": {
    "projects": [
      {
        "name": "EvoClaw",
        "description": "Self-evolving agent framework",
        "status": "Active - BSC integration for hackathon"
      }
    ],
    "events": [
      {"text": "Hackathon deadline Feb 15", "timestamp": 1707350400}
    ],
    "tasks": [
      {"text": "Deploy to BSC testnet", "status": "pending", "timestamp": 1707350400}
    ]
  },
  "critical_lessons": [
    {
      "text": "Always test on testnet before mainnet",
      "category": "blockchain",
      "importance": 0.9,
      "timestamp": 1707350400
    }
  ]
}
```

**自动修剪：**
- 课程：最多20条，满时删除优先级最低的课程
- 事件：仅保留最近发生的10个事件
- 任务：最多保留10个待办任务
- 总大小：严格限制在5KB以内，超出限制时会自动修剪

**生成文件：** `MEMORY.md` — 从结构化的热记忆状态自动生成

### 🟡 温暖记忆（最大50KB，保留30天）

**用途：** 存储最近提炼的信息，并对其进行相关性评分。

**条目格式：**
```json
{
  "id": "abc123def456",
  "text": "Decided to use zero go-ethereum deps for EvoClaw to keep binary small",
  "category": "projects/evoclaw/architecture",
  "importance": 0.8,
  "created_at": 1707350400,
  "access_count": 3,
  "score": 0.742,
  "tier": "warm"
}
```

**评分机制：**
```
score = importance × recency_decay(age) × reinforcement(access_count)

recency_decay(age) = exp(-age_days / 30)
reinforcement(access) = 1 + 0.1 × access_count
```

**层次分类：**
- `score >= 0.7` → 转入热记忆
- `score >= 0.3` → 保留在温暖记忆中
- `score >= 0.05` → 移至冷记忆
- `score < 0.05` → 被冻结并删除（超过保留期限后）

**驱逐规则：**
1. 存储时间超过30天且评分低于0.3
2. 温暖记忆总大小超过50KB（删除评分最低的条目）
3. 手动整合操作

### 🟢 冷记忆（无限容量，存储在Turso中）

**用途：** 长期存档，可查询但不可批量加载。

**数据结构：**
```sql
CREATE TABLE cold_memories (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  text TEXT NOT NULL,
  category TEXT NOT NULL,
  importance REAL DEFAULT 0.5,
  created_at INTEGER NOT NULL,
  access_count INTEGER DEFAULT 0
);

CREATE TABLE critical_state (
  agent_id TEXT PRIMARY KEY,
  data TEXT NOT NULL,  -- {hot_state, tree_nodes, timestamp}
  updated_at INTEGER NOT NULL
);
```

**保留期限：** 10年（可配置）
**清理机制：** 每月自动清理超过保留期限的条目

## 树状索引

**用途：** 提供O(log n)级别的分层类别导航。

**限制：**
- 最多50个节点
- 最大深度为4层
- 每个节点最多包含2KB的数据
- 每个节点最多有10个子节点

**示例：**
```
Memory Tree Index
==================================================
📂 Root (warm:15, cold:234)
  📁 owner — Owner profile and preferences
     Memories: warm=5, cold=89
  📁 projects — Active projects
     Memories: warm=8, cold=67
    📁 projects/evoclaw — EvoClaw framework
       Memories: warm=6, cold=45
      📁 projects/evoclaw/bsc — BSC integration
         Memories: warm=3, cold=12
  📁 technical — Technical setup and config
     Memories: warm=2, cold=34
  📁 lessons — Learned lessons and rules
     Memories: warm=0, cold=44

Nodes: 7/50
Size: 1842 / 2048 bytes
```

**操作命令：**
- `--add PATH DESC` — 添加类别节点
- `--remove PATH` — 删除节点（仅当该节点没有数据时）
- `--prune` — 删除60天内无活动的节点
- `--show` — 以美观的方式显示树状结构

## 提炼引擎

**用途：** 对对话内容进行三阶段压缩。

**处理流程：**
```
Raw conversation (500B)
  ↓ Stage 1→2: Extract structured info
Distilled fact (80B)
  ↓ Stage 2→3: Generate one-line summary
Core summary (20B)
```

### 第1阶段→第2阶段：原始数据 → 提炼后的结构化数据

**输入：** 原始对话文本
**输出：** 结构化的JSON数据

```json
{
  "fact": "User decided to use raw JSON-RPC for BSC to avoid go-ethereum dependency",
  "emotion": "determined",
  "people": ["User"],
  "topics": ["blockchain", "architecture", "dependencies"],
  "actions": ["decided to use raw JSON-RPC", "avoid go-ethereum"],
  "outcome": "positive"
}
```

**操作模式：**
- `rule`：基于正则表达式/启发式方法提取信息（快速，无需LLM）
- `llm`：利用LLM进行提取（准确，但需要API端点）

**使用方法：**
```bash
# Rule-based (default)
distiller.py --text "Had a productive chat about the BSC integration..." --mode rule

# LLM-powered
distiller.py --text "..." --mode llm --llm-endpoint http://localhost:8080/complete

# With core summary
distiller.py --text "..." --mode rule --core-summary
```

### 第2阶段→第3阶段：提炼后的数据 → 核心摘要

**用途：** 生成树状索引的简短摘要

**示例：**
```
Distilled: {
  "fact": "User decided raw JSON-RPC for BSC, no go-ethereum",
  "outcome": "positive"
}

Core summary: "BSC integration: raw JSON-RPC (no deps)"
```

**目标：** 输出长度小于30字节

## 基于LLM的树状搜索

**工作原理：**
1. 使用树状结构和查询构建提示
2. LLM判断哪些类别相关
3. 返回相关类别的路径及它们的评分
4. 从这些类别中检索相关信息

**示例：**

查询：“我们关于黑客马拉松的截止日期做出了什么决定？”

**关键词搜索** 返回：
- `projects/evoclaw`（0.8分）
- `technical/deployment`（0.4分）

**LLM搜索** 结果：
- `projects/evoclaw/bsc`（0.95分）—— “黑客马拉松的BSC集成”
- `active_context/events`（0.85分）—— “此处提到了截止日期”

**LLM提示模板：**
```
You are a memory retrieval system. Given a memory tree index and a query, 
identify which categories are relevant.

Memory Tree Index:
  projects/evoclaw — EvoClaw framework (warm:6, cold:45)
  projects/evoclaw/bsc — BSC integration (warm:3, cold:12)
  ...

User Query: What did we decide about the hackathon deadline?

Output (JSON):
[
  {"path": "projects/evoclaw/bsc", "relevance": 0.95, "reason": "BSC work for hackathon"},
  {"path": "active_context/events", "relevance": 0.85, "reason": "deadline tracking"}
]
```

**使用方法：**
```bash
# Keyword search (fast)
tree_search.py --query "BSC integration" --tree-file memory-tree.json --mode keyword

# LLM search (accurate)
tree_search.py --query "what did we decide about hackathon?" \
  --tree-file memory-tree.json --mode llm --llm-endpoint http://localhost:8080/complete

# Generate prompt for external LLM
tree_search.py --query "..." --tree-file memory-tree.json \
  --mode llm --llm-prompt-file prompt.txt
```

## 多代理支持**

**代理ID限定**：所有操作都支持`--agent-id`参数。

**文件布局：**
```
memory/
  default/
    warm-memory.json
    memory-tree.json
    hot-memory-state.json
    metrics.json
  agent-2/
    warm-memory.json
    memory-tree.json
    ...
MEMORY.md              # default agent
MEMORY-agent-2.md      # agent-2
```

**冷存储：** 通过`agent_id`字段进行代理级查询

**使用方法：**
```bash
# Store for agent-2
memory_cli.py store --text "..." --category "..." --agent-id agent-2

# Retrieve for agent-2
memory_cli.py retrieve --query "..." --agent-id agent-2

# Consolidate agent-2
memory_cli.py consolidate --mode daily --agent-id agent-2
```

## 整合机制

**用途：** 定期维护和优化记忆系统。

### 快速模式（每小时执行一次）
- 根据评分驱逐冷记忆中的条目
- 将过期条目归档到冷记忆
- 重新计算所有条目的评分
- 重建`MEMORY.md`文件

### 每日模式**
- 执行快速模式的全部操作
- 修剪树状结构中的无活动节点（60天内无操作的条目）

### 每月模式**
- 执行快速模式的全部操作
- 重建树状结构
- 清理冷记忆中的条目

### 完整模式**
- 执行每日和快速模式的全部操作
- 全面重新计算所有条目的评分
- 深度分析树状结构
- 生成整合报告

**推荐使用计划：**
- 快速模式：每2-4小时执行一次
- 每日模式：午夜通过cron任务执行
- 每月模式：每月1日通过cron任务执行

## 关键数据同步（以云为先）

**用途：** 每次对话后，将热记忆状态和树状索引同步到云端。

**同步内容：**
- 热记忆状态（身份信息、所有者资料、当前上下文、课程内容）
- 树状索引（结构及条目数量）
- 时间戳

**恢复机制：** 如果设备丢失，可在2分钟内从云端恢复数据

**失败处理策略：** 如果无法访问云端，采用指数级重试机制（5秒、10秒、20秒、40秒）

## 监控指标与可观测性**

**跟踪的指标：**
```json
{
  "tree_index_size_bytes": 1842,
  "tree_node_count": 37,
  "hot_memory_size_bytes": 4200,
  "warm_memory_count": 145,
  "warm_memory_size_kb": 38.2,
  "retrieval_count": 234,
  "evictions_today": 12,
  "reinforcements_today": 67,
  "consolidation_count": 8,
  "last_consolidation": 1707350400,
  "context_tokens_saved": 47800,
  "timestamp": "2026-02-10T14:30:00"
}
```

**使用方法：**
```bash
memory_cli.py metrics --agent-id default
```

**关键指标：**
- **context_tokens_saved** — 与原始`MEMORY.md`相比节省的令牌数量
- **retrieval_count** — 记忆内容的访问频率
- **evictions_today** — 记忆系统的压力指标
- **warm_memory_size_kb** — 存储使用情况

## 命令参考

### 存储操作

```bash
memory_cli.py store --text "Fact text" --category "path/to/category" [--importance 0.8] [--agent-id default]
```

**重要性分级：**
- `0.9-1.0` — 关键决策、凭证、核心身份信息
- `0.7-0.8` — 项目决策、架构信息、个人偏好
- `0.5-0.6` — 一般性事实、日常事件
- `0.3-0.4` — 非常次要的提及内容

**示例：**
```bash
memory_cli.py store \
  --text "Decided to deploy EvoClaw on BSC testnet before mainnet" \
  --category "projects/evoclaw/deployment" \
  --importance 0.85 \
  --db-url "$TURSO_URL" --auth-token "$TURSO_TOKEN"

# Store with explicit metadata (v2.1.0+)
memory_cli.py store \
  --text "Z-Image ComfyUI model for photorealistic images" \
  --category "tools/image-generation" \
  --importance 0.8 \
  --url "https://docs.comfy.org/tutorials/image/z-image/z-image" \
  --command "huggingface-cli download Tongyi-MAI/Z-Image" \
  --path "/home/user/models/"
```

### 验证功能（v2.1.0）

```bash
memory_cli.py validate [--file PATH] [--agent-id default]
```

**用途：** 每日检查笔记中是否存在不完整的信息（如缺失的URL、命令或后续步骤）。

**示例：**
```bash
# Validate today's daily notes
memory_cli.py validate

# Validate specific file
memory_cli.py validate --file memory/2026-02-13.md
```

**输出结果：**
```json
{
  "status": "warning",
  "warnings_count": 2,
  "warnings": [
    "Tool 'Z-Image' mentioned without URL/documentation link",
    "Action 'install' mentioned without command example"
  ],
  "suggestions": [
    "Add URLs for mentioned tools/services",
    "Include command examples for setup/installation steps",
    "Document next steps after decisions"
  ]
}
```

### 提取元数据（v2.1.0）

```bash
memory_cli.py extract-metadata --file PATH
```

**用途：** 从文件中提取结构化元数据（URL、命令、路径等信息）。

**示例：**
```bash
memory_cli.py extract-metadata --file memory/2026-02-13.md
```

**输出结果：**
```json
{
  "file": "memory/2026-02-13.md",
  "metadata": {
    "urls": [
      "https://docs.comfy.org/tutorials/image/z-image/z-image",
      "https://github.com/Lightricks/LTX-Video"
    ],
    "commands": [
      "huggingface-cli download Tongyi-MAI/Z-Image",
      "git clone https://github.com/Lightricks/LTX-Video.git"
    ],
    "paths": [
      "/home/peter/ai-stack/comfyui/models",
      "./configs/ltx-video-2-config.yaml"
    ]
  },
  "summary": {
    "urls_count": 2,
    "commands_count": 2,
    "paths_count": 2
  }
}
```

### 按URL搜索（v2.1.0）

```bash
memory_cli.py search-url --url FRAGMENT [--limit 5] [--agent-id default]
```

**用途：** 根据URL片段搜索笔记内容。

**示例：**
```bash
# Find all facts with comfy.org URLs
memory_cli.py search-url --url "comfy.org"

# Find GitHub repos
memory_cli.py search-url --url "github.com" --limit 10
```

**输出结果：**
```json
{
  "query": "comfy.org",
  "results_count": 1,
  "results": [
    {
      "id": "abc123",
      "text": "Z-Image ComfyUI model for photorealistic images",
      "category": "tools/image-generation",
      "metadata": {
        "urls": ["https://docs.comfy.org/tutorials/image/z-image/z-image"],
        "commands": ["huggingface-cli download Tongyi-MAI/Z-Image"],
        "paths": []
      }
    }
  ]
}
```

### 检索功能**

```bash
memory_cli.py retrieve --query "search query" [--limit 5] [--llm] [--llm-endpoint URL] [--agent-id default]
```

**操作模式：**
- 默认模式：基于关键词的树状搜索，结合温暖记忆和冷记忆
- `--llm`：使用LLM进行语义搜索

**示例：**
```bash
# Keyword search
memory_cli.py retrieve --query "BSC deployment decision" --limit 5

# LLM search (more accurate)
memory_cli.py retrieve \
  --query "what did we decide about blockchain integration?" \
  --llm --llm-endpoint http://localhost:8080/complete \
  --db-url "$TURSO_URL" --auth-token "$TURSO_TOKEN"
```

### 提炼功能**

```bash
memory_cli.py distill --text "raw conversation" [--llm] [--llm-endpoint URL]
```

**示例：**
```bash
# Rule-based distillation
memory_cli.py distill --text "User: Let's deploy to testnet first. Agent: Good idea, safer that way."

# LLM distillation
memory_cli.py distill \
  --text "Long conversation with nuance..." \
  --llm --llm-endpoint http://localhost:8080/complete
```

**输出结果：**
```json
{
  "distilled": {
    "fact": "Decided to deploy to testnet before mainnet",
    "emotion": "cautious",
    "people": [],
    "topics": ["deployment", "testnet", "safety"],
    "actions": ["deploy to testnet"],
    "outcome": "positive"
  },
  "mode": "rule",
  "original_size": 87,
  "distilled_size": 156
}
```

### 热记忆操作**

```bash
# Update hot state
memory_cli.py hot --update KEY JSON [--agent-id default]

# Rebuild MEMORY.md
memory_cli.py hot --rebuild [--agent-id default]

# Show current hot state
memory_cli.py hot [--agent-id default]
```

**可设置的字段：**
- `identity` — 代理/所有者的身份信息
- `owner_profile` — 所有者的偏好和个性特征
- `lesson` — 添加关键课程内容
- `event` — 将事件添加到当前上下文中
- `task` — 将任务添加到当前上下文中
- `project` — 添加或更新项目信息

**示例：**
```bash
# Update owner profile
memory_cli.py hot --update owner_profile '{"timezone": "Australia/Sydney", "work_hours": "9am-6pm"}'

# Add lesson
memory_cli.py hot --update lesson '{"text": "Always test on testnet first", "category": "blockchain", "importance": 0.9}'

# Add project
memory_cli.py hot --update project '{"name": "EvoClaw", "status": "Active", "description": "Self-evolving agent framework"}'

# Rebuild MEMORY.md
memory_cli.py hot --rebuild
```

### 树状索引操作**

```bash
# Show tree
memory_cli.py tree --show [--agent-id default]

# Add node
memory_cli.py tree --add "path/to/category" "Description" [--agent-id default]

# Remove node
memory_cli.py tree --remove "path/to/category" [--agent-id default]

# Prune dead nodes
memory_cli.py tree --prune [--agent-id default]
```

**示例：**
```bash
# Add category
memory_cli.py tree --add "projects/evoclaw/bsc" "BSC blockchain integration"

# Remove empty category
memory_cli.py tree --remove "old/unused/path"

# Prune dead nodes (60+ days no activity)
memory_cli.py tree --prune
```

### 冷存储操作**

```bash
# Initialize Turso tables
memory_cli.py cold --init --db-url URL --auth-token TOKEN

# Query cold storage
memory_cli.py cold --query "search term" [--limit 10] [--agent-id default] --db-url URL --auth-token TOKEN
```

**示例：**
```bash
# Init tables (once)
memory_cli.py cold --init --db-url "https://your-db.turso.io" --auth-token "your-token"

# Query cold archive
memory_cli.py cold --query "blockchain decision" --limit 10 --db-url "$TURSO_URL" --auth-token "$TURSO_TOKEN"
```

## 配置设置**

**配置文件：** `config.json`（可选，如未配置则使用默认值）

```json
{
  "agent_id": "default",
  "hot": {
    "max_bytes": 5120,
    "max_lessons": 20,
    "max_events": 10,
    "max_tasks": 10
  },
  "warm": {
    "max_kb": 50,
    "retention_days": 30,
    "eviction_threshold": 0.3
  },
  "cold": {
    "backend": "turso",
    "retention_years": 10
  },
  "scoring": {
    "half_life_days": 30,
    "reinforcement_boost": 0.1
  },
  "tree": {
    "max_nodes": 50,
    "max_depth": 4,
    "max_size_bytes": 2048
  },
  "distillation": {
    "aggression": 0.7,
    "max_distilled_bytes": 100,
    "mode": "rule"
  },
  "consolidation": {
    "warm_eviction": "hourly",
    "tree_prune": "daily",
    "tree_rebuild": "monthly"
  }
}
```

## 与OpenClaw代理的集成

### 对话后的处理**

```python
import subprocess
import json

def process_conversation(user_message, agent_response, category="conversations"):
    # 1. Distill conversation
    text = f"User: {user_message}\nAgent: {agent_response}"
    result = subprocess.run(
        ["python3", "skills/tiered-memory/scripts/memory_cli.py", "distill", "--text", text],
        capture_output=True, text=True
    )
    distilled = json.loads(result.stdout)
    
    # 2. Determine importance
    importance = 0.7 if "decision" in distilled["distilled"]["outcome"] else 0.5
    
    # 3. Store
    subprocess.run([
        "python3", "skills/tiered-memory/scripts/memory_cli.py", "store",
        "--text", distilled["distilled"]["fact"],
        "--category", category,
        "--importance", str(importance),
        "--db-url", os.getenv("TURSO_URL"),
        "--auth-token", os.getenv("TURSO_TOKEN")
    ])
    
    # 4. Critical sync
    subprocess.run([
        "python3", "skills/tiered-memory/scripts/memory_cli.py", "sync-critical",
        "--db-url", os.getenv("TURSO_URL"),
        "--auth-token", os.getenv("TURSO_TOKEN")
    ])
```

### 回答前的准备（数据检索）

```python
def get_relevant_context(query):
    result = subprocess.run(
        [
            "python3", "skills/tiered-memory/scripts/memory_cli.py", "retrieve",
            "--query", query,
            "--limit", "5",
            "--llm",
            "--llm-endpoint", "http://localhost:8080/complete",
            "--db-url", os.getenv("TURSO_URL"),
            "--auth-token", os.getenv("TURSO_TOKEN")
        ],
        capture_output=True, text=True
    )
    
    memories = json.loads(result.stdout)
    return "\n".join([f"- {m['text']}" for m in memories])
```

### 定期整合操作**

```python
import schedule

# Hourly quick consolidation
schedule.every(2).hours.do(lambda: subprocess.run([
    "python3", "skills/tiered-memory/scripts/memory_cli.py", "consolidate",
    "--mode", "quick",
    "--db-url", os.getenv("TURSO_URL"),
    "--auth-token", os.getenv("TURSO_TOKEN")
]))

# Daily tree prune
schedule.every().day.at("00:00").do(lambda: subprocess.run([
    "python3", "skills/tiered-memory/scripts/memory_cli.py", "consolidate",
    "--mode", "daily",
    "--db-url", os.getenv("TURSO_URL"),
    "--auth-token", os.getenv("TURSO_TOKEN")
]))

# Monthly full consolidation
schedule.every().month.do(lambda: subprocess.run([
    "python3", "skills/tiered-memory/scripts/memory_cli.py", "consolidate",
    "--mode", "monthly",
    "--db-url", os.getenv("TURSO_URL"),
    "--auth-token", os.getenv("TURSO_TOKEN")
]))
```

## LLM集成

**推荐模型：**

**用于数据提炼和树状搜索：**
- Claude 3 Haiku（速度快、成本低、结构良好）
- GPT-4o-mini（平衡性较好）
- Gemini 1.5 Flash（速度非常快）

**用于重建树状索引：**
- Claude 3.5 Sonnet（推理能力更强）
- GPT-4o（规划能力更强）

**成本优化建议：**
1. 对于频繁的操作（数据提炼、搜索），使用成本较低的模型
2. 批量处理对话内容以减少计算量
3. 缓存树状索引的提示信息（因为结构变化不大）
4. 对于简单的对话，可以省略LLM的使用，直接使用规则进行搜索

**示例LLM端点：**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/complete", methods=["POST"])
def complete():
    data = request.json
    prompt = data["prompt"]
    
    # Call your LLM (OpenAI, Anthropic, local model, etc.)
    response = llm_client.complete(prompt)
    
    return jsonify({"text": response})

if __name__ == "__main__":
    app.run(port=8080)
```

## 性能特点**

**内存占用：**
- 热记忆：约5KB（始终加载）
- 树状索引：约2KB（始终加载）
- 每次查询所需的数据量：约1-3KB
**总内存占用：** 约8-15KB（与代理的使用时间无关）

**检索速度：**
- 关键词搜索：10-20毫秒
- 基于LLM的树状搜索：300-600毫秒
- 冷记忆查询：50-100毫秒

**五年使用情况：**
- 热记忆：始终占用5KB
- 温暖记忆：最近30天的数据（约50KB）
- 冷记忆：在Turso中压缩后的数据量约为50MB
- 树状索引：仍然占用2KB（节点不同，但数据量不变）
**每次会话的上下文信息量：** 与初始状态相同

## 与其他系统的比较**

| 系统 | 记忆模型 | 扩展性 | 精确度 | 成本 |
|--------|-------------|---------|----------|------|
| **原始的MEMORY.md** | 线性文本 | 不支持扩展 | 易退化 | 成本较高 |
| **基于向量的RAG** | 基于嵌入的模型 | 可扩展多年 | 相似度而非相关性作为判断标准 | 效率一般 |
| **EvoClaw的分层记忆系统** | 结合树状结构和分层存储 | 可扩展数十年 | 基于推理的检索机制 | 更高效 |

**为什么选择树状存储而非向量存储：**
- **精确度：** 高达98%以上，而传统模型仅为70-80% |
- **可解释性：** 结果易于理解（例如：“项目 → EvoClaw → BSC” vs. “基于余弦相似度的判断” |
- **多步推理：** 更自然且更有效 |
- **误报率：** 更低 |

## 常见问题及解决方法**

### 树状索引大小超出限制

```bash
# Prune dead nodes
memory_cli.py tree --prune

# Check which nodes are largest
memory_cli.py tree --show | grep "Memories:"

# Manually remove unused categories
memory_cli.py tree --remove "unused/category"
```

### 温暖记忆空间不足

```bash
# Run consolidation
memory_cli.py consolidate --mode daily --db-url "$TURSO_URL" --auth-token "$TURSO_TOKEN"

# Check stats
memory_cli.py metrics

# Lower eviction threshold (keeps less in warm)
# Edit config.json: "eviction_threshold": 0.4
```

### 热记忆占用超过5KB

```bash
# Hot auto-prunes, but check structure
memory_cli.py hot

# Remove old projects/tasks manually
memory_cli.py hot --update project '{"name": "OldProject", "status": "Completed"}'

# Rebuild to force pruning
memory_cli.py hot --rebuild
```

### LLM搜索失败

```bash
# Fallback to keyword search (automatic)
memory_cli.py retrieve --query "..." --limit 5

# Test LLM endpoint
curl -X POST http://localhost:8080/complete -d '{"prompt": "test"}'

# Generate prompt for external testing
tree_search.py --query "..." --tree-file memory/memory-tree.json --mode llm --llm-prompt-file test.txt
```

## 从v1.x版本升级到v2.2的步骤**

**兼容性：**
- 现有的`warm-memory.json`和`memory-tree.json`文件可以继续使用
**新文件：**
- `config.json`（可选，使用默认配置）
- `hot-memory-state.json`（系统自动生成）
- `metrics.json`（系统自动生成）

**升级步骤：**
1. 更新技能配置：`clawhub update tiered-memory`
2. 运行整合命令重建热记忆状态：`memory_cli.py consolidate`
3. （可选）初始化冷存储：`memory_cli.py cold --init --db-url ... --auth-token ...`
4. 配置代理以使用新的命令（详见集成部分）

## 从v2.0版本升级到v2.1版本的步骤**

**完全兼容：** 现有的记忆文件无需修改即可使用新功能

**新功能：**
- 现在可以从笔记中自动提取元数据
- 新增命令：`validate`、`extract-metadata`、`search-url`
- `store`命令现在支持`--url`、`--command`、`--path`参数
- 提炼过程会保留URL和技术细节
- 升级后无需额外操作，只需更新设置即可使用新功能

**升级测试方法：**
```bash
# Update skill
clawhub update tiered-memory

# Test metadata extraction
memory_cli.py extract-metadata --file memory/2026-02-13.md

# Validate your recent notes
memory_cli.py validate

# Search by URL
memory_cli.py search-url --url "github.com"
```

## 参考资料**

- **设计文档：** `/docs/TIERED-MEMORY.md`（EvoClaw官方文档）
- **云同步指南：** `/docs/CLOUD-SYNC.md`（EvoClaw官方文档）
- **灵感来源：** [PageIndex](https://github.com/VectifyAI/PageIndex)（基于树状结构的检索技术）

---

*v2.1.0版本更新说明：** “一个记住一切的头脑和一个什么都不记得的头脑一样无用。真正的艺术在于知道该记住什么。现在系统增加了结构化元数据，帮助你记住信息的内容和获取方式。” 🧠🌲🔗