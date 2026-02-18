# SurrealDB知识图谱内存系统 v2.0

这是一个基于SurrealDB构建的知识图谱内存系统，支持向量化语义搜索、置信度评分、图谱感知的事实关系处理、**情景记忆**、**工作记忆**以及**基于结果的学习**功能。

## 描述

该系统可用于：
- 以相互关联的事实形式存储和检索知识
- 进行带有置信度权重的语义搜索
- 管理事实之间的关系（支持支持、矛盾、更新等操作）
- 从内存文件中提取由大型语言模型（LLM）生成的知识
- 通过人工智能发现事实之间的关联
- **新功能 v2.0**：支持情景记忆，用于记录任务历史和学习过程
- **新功能 v2.0**：引入工作记忆功能，以提高任务处理的稳定性
- **新功能 v2.0**：基于结果进行置信度调整（有助于成功的事实会获得更高的置信度）
- **新功能 v2.0**：实现上下文感知的搜索功能（根据任务内容优化搜索结果）
- **新功能 v2.0**：对重要事实进行同步写入

**触发命令**：
- `remember this`：记住某个内容
- `store fact`：存储一个事实
- `what do you know about`：查询相关知识
- `memory search`：执行内存搜索
- `similar tasks`：查找类似的任务
- `past episodes`：查看过去的任务记录
- `working memory`：查询工作记忆中的信息
- `knowledge graph`：查询知识图谱

## ⚠️ 安全性与安装说明

该系统执行系统级操作，请在安装前仔细阅读以下说明：

| 操作        | 执行位置    | 说明                          |
|--------------|------------|---------------------------------------------|
| **网络安装**    | `install.sh`     | 运行 `curl https://install.surrealdb.com \| sh`                |
| **源代码修补**    | `integrate-clawdbot.sh` | 使用 `sed -i` 修复 Clawdbot 的源代码文件            |
| **服务管理**    | `memory.ts`     | 启动 SurrealDB 服务器并导入数据库模式             |
| **Python 包安装**   | `install.sh`     | 通过 pip 安装 surrealdb、openai 和 pyyaml                |
| **文件访问**    | `extract-knowledge.py` | 读取 `MEMORY.md` 及相关 md 文件以提取数据             |

**默认凭据**：示例中使用 `root/root`；在生产环境中请更换凭据，并确保仅允许本地访问。

**API 密钥**：需要设置 `OPENAI_API_KEY`，用于文本嵌入（`text-embedding-3-small`）和大型语言模型提取（`GPT-4o-mini`）功能。

## v2.0 新特性

### 1. 情景记忆（Episodic Memory）
- 从过去的任务尝试中学习：  
  ```bash
# Find similar past tasks
mcporter call surrealdb-memory.episode_search query="deploy API" limit:5

# Get actionable learnings
mcporter call surrealdb-memory.episode_learnings task_goal="Build REST API"
# Returns: ["Always validate OAuth tokens first", "⚠️ Past failure: Token expired mid-deploy"]
```

### 2. 工作记忆（Working Memory）
- 能够在系统崩溃后仍保留当前任务的状态：  
  ```bash
# Check active task status
mcporter call surrealdb-memory.working_memory_status
```

工作记忆通过 Python 进行管理：  
  ```python
from working_memory import WorkingMemory

wm = WorkingMemory()
wm.start_task("Deploy marketing pipeline", plan=[...])
wm.update_step(1, status="complete", result_summary="Audited 12 templates")
episode = wm.complete_task(outcome="success")
```

### 3. 同步写入（Synchronous Writes）
- 重要事实会立即被存储（而非批量处理）：  
  ```bash
mcporter call surrealdb-memory.knowledge_store_sync \
    content="Client X uses OAuth2 not API keys" \
    importance:0.85
```

### 4. 上下文感知搜索（Context-Aware Search）
- 根据当前任务内容优化搜索结果：  
  ```bash
mcporter call surrealdb-memory.context_aware_search \
    query="API authentication" \
    task_context="Deploy marketing automation for ClientX"
```

### 5. 结果驱动的置信度调整（Outcome-Based Confidence Calibration）
- 有助于成功的事实会获得更高的置信度；与失败相关的事实则会降低置信度。这一过程是自动完成的。

## MCP 工具（MCP Tools, v2.0）

| 工具        | 功能描述                          |
|-------------|---------------------------------------------|
| `knowledge_search` | 通过查询进行语义搜索                      |
| `knowledge_recall` | 带有完整上下文（包括关系和实体）的事实检索            |
| `knowledge_store` | 带有置信度和标签的新事实存储                    |
| `knowledge_stats` | 提供知识图谱的统计信息（包含任务记录）             |
| `knowledge_store_sync` | **新功能 v2.0**：基于重要性决定数据写入策略（>0.7 时立即写入） |
| `episode_search` | **新功能 v2.0**：查找相似的过去任务/事件           |
| `episode_learnings` | **新功能 v2.0**：从历史记录中获取可操作的洞察           |
| `episode_store` | **新功能 v2.0**：存储已完成的任务记录             |
| `working_memory_status` | **新功能 v2.0**：查询当前任务进度                   |
| `context_aware_search` | **新功能 v2.0**：根据任务上下文优化搜索结果           |

## 先决条件

- 确保已安装并运行 SurrealDB：  
  ```bash
   # Install (one-time)
   ./scripts/install.sh
   
   # Start server
   surreal start --bind 127.0.0.1:8000 --user root --pass root file:~/.clawdbot/memory/knowledge.db
   ```

- 安装必要的 Python 依赖项：  
  ```bash
   cd /path/to/surrealdb-memory
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r scripts/requirements.txt
   ```

- 设置 OpenAI API 密钥以使用嵌入和提取功能：  
  ```bash
   export OPENAI_API_KEY="sk-..."
   ```

## 快速入门

```bash
# Initialize the database schema (includes v2 tables)
./scripts/init-db.sh

# OR apply v2 schema to existing database
python3 scripts/migrate-v2.py

# Run initial knowledge extraction
source .venv/bin/activate
python3 scripts/extract-knowledge.py extract --full

# Check status
mcporter call surrealdb-memory.knowledge_stats
```

## MCP 服务器配置

请将以下配置添加到您的 mcporter 配置文件中：  
```json
{
  "surrealdb-memory": {
    "command": "/path/to/.venv/bin/python3 /path/to/scripts/mcp-server-v2.py"
  }
}
```

## 命令行接口（CLI）命令

### `knowledge-tool.py`（简单 CLI 工具）

```bash
python3 scripts/knowledge-tool.py search "query" --limit 10
python3 scripts/knowledge-tool.py recall "query"
python3 scripts/knowledge-tool.py store "Fact content" --confidence 0.9
python3 scripts/knowledge-tool.py stats
```

### `extract-knowledge.py`

| 命令          | 功能描述                        |
|----------------|--------------------------------------------|
| `extract`       | 仅从已更改的文件中提取数据                   |
| `extract --full`    | 提取所有文件中的数据                     |
| `status`       | 显示提取进度和统计信息                   |
| `reconcile`      | 进行数据整合（删除冗余、过时或孤立的数据）             |
| `discover-relations` | 通过人工智能发现事实之间的关系             |
| `dedupe`       | 删除重复的事实                         |

### `migrate-v2.py`  

```bash
# Apply v2 schema (safe to run multiple times)
python3 scripts/migrate-v2.py

# Force recreate v2 tables
python3 scripts/migrate-v2.py --force
```

## 架构（Architecture, v2.0）

```
Tier 1: Context Window (conversation)
    ↕ (continuous read/write during loop iterations)
Tier 1.5: Working Memory (~/.working-memory/current-task.yaml)  ← NEW
    ↕ (persisted every N iterations)
Tier 2: File-Based Memory (daily logs, MEMORY.md)
    ↕ (cron extraction + sync writes for important facts)
Tier 3: Knowledge Graph (facts, entities, relations, episodes)  ← ENHANCED
```

## 置信度评分（Confidence Scoring）

每个事实的置信度由以下因素综合计算得出：
- **基础置信度**（0.0–1.0）
- **来自高置信度支持事实的增强**  
- **来自被提及的知名实体的增强**  
- **基于任务结果的调整**  
- **来自矛盾事实的负面影响**  
- **时间衰减**（每月降低 5%）

## 控制界面集成（Control UI Integration）

该系统为 Clawdbot 仪表板提供了一个名为 “Memory” 的标签页，具备以下功能：
- 查看统计信息（事实、实体、关系、任务记录）
- 监控系统健康状态
- 一键自动修复功能
- 运行维护操作
- 查看数据提取进度

## 相关文件

```
surrealdb-memory/
├── SKILL.md                      # This file
├── INSTRUCTIONS.md               # Setup and usage guide
├── UPGRADE-V2.md                 # V2 upgrade guide
├── CHANGELOG.md                  # Version history
├── package.json                  # Skill metadata
├── scripts/
│   ├── mcp-server-v2.py          # MCP server with 10 tools (v2)
│   ├── mcp-server.py             # Legacy MCP server (v1)
│   ├── working_memory.py         # Working memory module (v2)
│   ├── episodes.py               # Episodic memory module (v2)
│   ├── migrate-v2.py             # V2 schema migration
│   ├── schema-v2.sql             # V2 database schema
│   ├── schema-v2-additive.sql    # Additive v2 schema
│   ├── knowledge-tool.py         # Simple CLI wrapper
│   ├── extract-knowledge.py      # LLM extraction from memory files
│   ├── memory-cli.py             # Full CLI for CRUD operations
│   ├── schema.sql                # Original schema
│   ├── init-db.sh                # Initialize database
│   ├── install.sh                # Install SurrealDB binary
│   └── requirements.txt          # Python dependencies
├── clawdbot-integration/
│   ├── gateway/
│   │   └── memory.ts             # Gateway RPC handlers
│   └── ui/
│       ├── memory-view.ts        # Memory tab view (Lit)
│       └── memory-controller.ts  # Memory tab controller
└── references/
    ├── surql-examples.md         # SurrealQL query patterns
    └── conflict-patterns.md      # Contradiction detection rules
```

## 故障排除

- 如果出现 “连接被拒绝” 的错误，请尝试启动 SurrealDB 服务：  
  ```bash
surreal start --user root --pass root file:~/.clawdbot/memory/knowledge.db
```

- 如果提示 “surrealdb 包未安装”，请先安装 Python 依赖项：  
  ```bash
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

- 如果找不到 “episode table”，请运行 v2.0 版本的迁移脚本：  
  ```bash
python3 scripts/migrate-v2.py
```

- 如果未设置 `OPENAI_API_KEY`，请先导出该密钥：  
  ```bash
export OPENAI_API_KEY="sk-..."
```

## 版本历史

- **v2.0.0**（2026-02-17）：新增情景记忆、工作记忆功能及基于结果的学习机制  
- **v1.2.0**（2026-02-09）：添加 MCP 服务器及四项新工具  
- **v1.1.0**（2026-02-09）：集成 Gateway 系统、实现关系发现功能及控制界面  
- **v1.0.0**（2026-01-31）：初始版本，包含数据提取和命令行接口