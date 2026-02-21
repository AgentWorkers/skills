# SurrealDB知识图谱内存系统 v2.2

这是一个全面的知识图谱内存系统，具备语义搜索、情景记忆、工作记忆、自动上下文注入以及**代理隔离**功能——使每个代理都能成为不断自我提升的AI。

## 描述

使用此技能可：
- **语义记忆**：通过带有置信度权重的向量搜索来存储和检索事实
- **情景记忆**：记录任务历史并从中学习
- **工作记忆**：跟踪活跃任务状态并具备崩溃恢复功能
- **自动注入**：自动将相关上下文插入代理提示中
- **结果校准**：根据任务结果调整事实的置信度
- **自我提升**：定期提取数据并发现关系，使每个代理逐渐变得更智能

**触发语句**：`remember this`（记住这个）、`store fact`（存储事实）、`what do you know about`（你知道什么）、`memory search`（内存搜索）、`find similar tasks`（查找类似任务）、`learn from history`（从历史中学习）

> **安全性**：此技能会读取工作区内存文件并将其内容发送给OpenAI进行提取。它会注册两个后台定时任务，并（可选地）更新OpenClaw源文件。所有行为均为可选或已记录在文档中。有关详细信息，请参阅[SECURITY.md](SECURITY.md)。

> **所需条件**：`OPENAI_API_KEY`、`surreal`二进制文件、`python3` ≥3.10

---

## 🔄 自我提升代理循环

这是核心概念：**每个配备了此技能的代理都能自动提升自身**，无需人工干预。两个定时的定时任务——知识提取和关系关联——会按照固定时间表运行，不断扩展知识图谱。结合自动注入功能，代理在每次对话中都会变得越来越智能。

### 循环流程

```
[Agent Conversation]
       ↓  stores important facts via knowledge_store_sync
[Memory Files]  ← agent writes to MEMORY.md / daily memory/*.md files
       ↓  every 6 hours — extraction cron fires
[Entity + Fact Extraction]  ← LLM reads files, extracts structured facts + entities
       ↓  facts stored with embeddings + agent_id tag
[Knowledge Graph]  ← SurrealDB: facts, entities, mentions
       ↓  daily at 3 AM — relation discovery cron fires
[Relationship Correlation]  ← AI finds semantic links between facts
       ↓  relates_to edges created between connected facts
[Richer Knowledge Graph]  ← facts are no longer isolated; they form a web
       ↓  on every new message — auto-injection reads the graph
[Context Window]  ← relevant facts + relations + episodes injected automatically
       ↓
[Better Responses]  ← agent uses accumulated knowledge to respond more accurately
       ↑  new insights written back to memory files → cycle repeats
```

### 每个定时任务的功能

#### 任务1 — 知识提取（每6小时一次）
**脚本**：`scripts/extract-knowledge.py extract`

- 读取工作区中的`MEMORY.md`文件以及所有`memory/YYYY-MM-DD.md`文件
- 使用LLM（GPT-4）提取结构化的事实、实体和关键概念
- 对文件内容进行哈希处理，跳过未更改的文件——仅处理差异部分
- 以以下方式存储每个事实：
  - 一个向量嵌入（OpenAI `text-embedding-3-small`）用于语义搜索
  - 一个`置信度`分数（默认为0.9）
  - 一个`agent_id`标签，以确保事实仅属于相应的代理
  - `source`元数据，指向原始文件
- 结果：原始的对话知识变得可搜索，形成结构化的内存

#### 任务2 — 关系关联（每天凌晨3点）
**脚本**：`scripts/extract-knowledge.py discover-relations`

- 查询知识图谱中尚未建立关系的事实（“孤立事实”）
- 将它们分组，并请求LLM识别它们之间的语义联系
- 在SurrealDB中创建`relates_to`边，将相关事实连接起来
- 结果：孤立的事实变成了一个**相互关联的知识网络**——代理现在可以遍历这些关系，而不仅仅是关键词匹配
- 随着时间的推移，知识图谱从一个扁平列表演变成一个丰富的语义网络

### 为什么这能让代理自我提升

当启用自动注入功能后，每次新的对话都会基于最相关的知识图谱片段开始。代理：
1. 进行对话 → 将见解写入内存文件
2. 提取任务启动 → 将这些见解转换为结构化的事实
3. 关系任务启动 → 将这些事实与现有知识连接起来
4. 下一次对话 → 自动注入更丰富、更关联的上下文

...通过这个循环，代理实际上会变得越来越智能。它从自己的输出中学习，基于积累的历史来生成未来的响应，并通过情景记忆和结果校准避免重复错误。

### OpenClaw定时任务（已配置）

这些任务已在OpenClaw中注册并自动运行：

| 任务名称 | 定时ID | 时间表 | 执行内容 |
|----------|---------|----------|--------------|
| Memory Knowledge Extraction | `b9936b69-c652-4683-9eae-876cd02128c7` | 每6小时 (`0 */6 * * *`) | `python3 scripts/extract-knowledge.py extract` |
| Memory Relation Discovery | `2a3dd973-5d4d-46cf-848d-0cf31ab53fa1` | 每天凌晨3点 (`0 3 * * *`) | `python3 scripts/extract-knowledge.py discover-relations` |

这两个任务都使用`sessionTarget: "main"`，并通过`systemEvent`传递命令，因此主代理会接收并执行这些命令。

要随时检查任务状态：
```bash
# Via OpenClaw cron list (in Koda's chat)
# Or via CLI:
openclaw cron list
```

### 为新代理添加定时任务

在创建一个需要自我提升的新代理时，需要为其注册自己的提取任务：

```bash
# OpenClaw cron add (via Koda) — example for a 'scout-monitor' agent
# Schedule: every 6h, extract facts tagged to scout-monitor
python3 scripts/extract-knowledge.py extract --agent-id scout-monitor
```

`--agent-id`标志确保提取的事实仅属于该代理的池，不会污染主代理的知识。每个代理独立自我提升，同时仍然可以访问共享的`scope='global'`事实。

---

## 特性（v2.2）

| 特性 | 描述 |
|---------|-------------|
| **语义事实** | 带有置信度评分的向量索引事实 |
| **情景记忆** | 包含决策、问题和解决方案的任务历史 |
| **工作记忆** | 可在崩溃后恢复的基于YAML的任务状态 |
| **结果校准** | 成功任务中使用的事实会获得更高的置信度 |
| **自动注入** | 相关事实/情景会自动插入提示中 |
| **实体提取** | 自动进行实体链接和关系发现 |
| **置信度衰减** | 过时的事实会随时间自然衰减 |
| **代理隔离** | 每个代理都有自己的内存池；`scope='global'`的事实在所有代理之间共享 |
| **自我提升循环** | 定期提取 + 关系发现自动扩展知识图谱 |

---

## 代理隔离（v2.2）

OpenClaw中的每个代理都有自己的内存池。写入时，事实会被标记上`agent_id`；所有读取查询都会过滤为`(agent_id = $agent_id OR scope = 'global')`。

### 工作原理

```
Agent A (main)          Agent B (scout-monitor)
   ┌──────────┐              ┌──────────┐
   │ 391 facts│              │   0 facts│   ← isolated pools
   └──────────┘              └──────────┘
         ↑                         ↑
         └──── scope='global' ─────┘   ← shared facts visible to both
```

### 存储事实

所有的`knowledge_store` / `knowledge_store_sync`调用都接受`agent_id`参数：

```bash
# Stored to scout-monitor's pool only
mcporter call surrealdb-memory.knowledge_store \
    content="API is healthy at /ping" \
    agent_id='scout-monitor'

# Stored globally (visible to all agents)
mcporter call surrealdb-memory.knowledge_store \
    content="Project uses Python 3.12" \
    agent_id='main' scope='global'
```

### 自动注入（代理感知）

通过将`references/enhanced-loop-hook-agent-isolation.md`应用于`src/agents/enhanced-loop-hook.ts`，增强循环会自动从会话键中提取代理ID，并将其传递给`memory_inject`。无需手动配置——每个代理的自动注入都会自动限制在其自己的事实范围内。

### 提取（代理感知）

在`extract-knowledge.py`中传递`--agent-id`参数，以确保定时提取的事实被正确标记：

```bash
python3 scripts/extract-knowledge.py extract --agent-id scout-monitor
```

默认值为`"main"`。对于非主代理，请相应地更新定时任务。

### 向后兼容性

现有的事实如果没有明确的`agent_id`，则被视为属于`"main"`代理。升级到v2.2后，现有数据不会丢失。

---

## 仪表板UI

控制面板中的“Memory”标签页提供两列布局：

### 左列：仪表板
- **📊 统计** — 实时显示事实、实体、关系和存档项目的数量
- **置信度条形** — 平均置信度得分的可视化显示
- **来源分解** — 按来源文件分组的事实
- **🏥 系统健康** — SurrealDB、模式和Python依赖项的状态
- **🔗 DB Studio** — 快速链接到SurrealDB的Web界面

### 右列：操作
- **📥 知识提取**
  - *Extract Changes* — 从修改过的文件中逐步提取事实
  - *Find Relations* — 发现现有事实之间的语义关系
  - *Full Sync* — 完整提取 + 关系发现
  - 带有实时状态更新的进度条

- **🔧 维护**
  - *Apply Decay* — 降低过时事实的置信度
  - *Prune Stale* — 将置信度低于阈值的事实存档
  - *Full Sweep* — 完整维护周期

- **💡 提示** — 操作的快速参考

当系统需要设置时，会出现一个**安装**部分，其中包含手动控制选项。

---

## 先决条件

1. **SurrealDB**已安装并运行：
   ```bash
   # Install (one-time)
   ./scripts/install.sh
   
   # Start server
   surreal start --bind 127.0.0.1:8000 --user root --pass root file:~/.openclaw/memory/knowledge.db
   ```

2. **Python依赖项**（使用技能的虚拟环境）：
   ```bash
   cd /path/to/surrealdb-memory
   python3 -m venv .venv
   source .venv/bin/activate
   pip install surrealdb openai pyyaml
   ```

3. **OpenAI API密钥**（用于嵌入）（在OpenClaw配置或环境中设置）

4. **mcporter**已配置为使用此技能的MCP服务器

## MCP服务器设置

在`config/mcporter.json`中添加以下配置：

```json
{
  "servers": {
    "surrealdb-memory": {
      "command": ["python3", "/path/to/surrealdb-memory/scripts/mcp-server-v2.py"],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "SURREAL_URL": "http://localhost:8000",
        "SURREAL_USER": "root",
        "SURREAL_PASS": "root"
      }
    }
  }
}
```

---

## MCP工具（共11个）

### 核心工具
| 工具 | 描述 |
|------|-------------|
| `knowledge_search` | 用于事实的语义搜索 |
| `knowledge_recall` | 获取包含完整上下文（关系、实体）的事实 |
| `knowledge_store` | 存储新事实 |
| `knowledge_stats` | 获取数据库统计信息 |

### v2工具
| 工具 | 描述 |
|------|-------------|
| `knowledge_store_sync` | 带有重要性路由的存储（高重要性 = 立即写入） |
| `episode_search` | 查找类似的过去任务 |
| `episode_learnings` | 从历史中获取可操作的见解 |
| `episode_store` | 记录已完成的任务情节 |
| `working_memory_status` | 获取当前任务状态 |
| `context_aware_search` | 带有任务上下文增强的搜索 |
| `memory_inject` | **用于提示的智能上下文注入** |

### memory_inject工具

`memory_inject`工具返回格式化的上下文，准备插入提示中：

```bash
# Scoped to a specific agent (returns only that agent's facts + global facts)
mcporter call surrealdb-memory.memory_inject \
    query="user message" \
    max_facts:7 \
    max_episodes:3 \
    confidence_threshold:0.9 \
    include_relations:true \
    agent_id='scout-monitor'
```

**输出：**
```markdown
## Semantic Memory (Relevant Facts)
📌 [60% relevant, 100% confidence] Relevant fact here...

## Related Entities
• Entity Name (type)

## Episodic Memory (Past Experiences)
✅ Task: Previous task goal [similarity]
   → Key learning from that task
```

---

## 自动注入（增强循环集成）

启用后，内存会自动注入到每个代理的对话中：

1. **在模式界面中启用**：
   - 打开控制面板 → “Mode”标签页
   - 滚动到“🧠 Memory & Knowledge Graph”部分
   - 切换“Auto-Inject Context”选项
   - 配置限制（最大事实数量、最大情节数量、置信度阈值）

2. **工作原理**：
   - 在每次用户消息时，都会自动调用`memory_inject`
   - 根据用户的查询搜索相关事实
   - 如果平均事实置信度低于阈值，就会包含情景记忆
   - 格式化的上下文会被插入代理的系统提示中
   - **v2.2**：通过应用`references/enhanced-loop-hook-agent-isolation.md`，会从会话键中自动提取当前活跃代理的ID，并将其作为`agent_id`——每个代理的注入都会自动限制在其自己的事实范围内

3. **配置（在模式设置中）**：
   | 设置 | 默认值 | 描述 |
|---------|---------|-------------|
| Auto-Inject Context | Off | 主要开关 |
| Max Facts | 7 | 最大可注入的语义事实数量 |
| Max Episodes | 3 | 最大情景记忆数量 |
| Confidence Threshold | 90% | 低于此阈值的情节会被包含 |
| Include Relations | On | 包含实体关系 |

---

## 命令行接口（CLI）命令

```bash
# Activate venv
source .venv/bin/activate

# Store a fact
python scripts/memory-cli.py store "Important fact" --confidence 0.9

# Search
python scripts/memory-cli.py search "query"

# Get stats
python scripts/knowledge-tool.py stats

# Run maintenance
python scripts/memory-cli.py maintain

# Extract from files (incremental)
python scripts/extract-knowledge.py extract

# Extract for a specific agent
python scripts/extract-knowledge.py extract --agent-id scout-monitor

# Force full extraction (all files, not just changed)
python scripts/extract-knowledge.py extract --full

# Discover semantic relationships
python scripts/extract-knowledge.py discover-relations
```

---

## 数据库模式（v2）

### 表结构
- `fact` — 带有嵌入和置信度的语义事实
- `entity` — 提取的实体（人、地点、概念）
- `relates_to` — 事实之间的关系
- `mentions` — 事实到实体的链接
- `episode` — 包含结果的任务历史
- `working_memory` — 活跃任务快照

### 关键字段（事实）
- `content` — 事实文本
- `embedding` — 用于语义搜索的向量
- `confidence` — 基础置信度（0-1）
- `success_count` / `failure_count` — 结果跟踪
- `scope` — 全局、客户端或代理
- `agent_id` — 拥有此事实的代理（v2.2）

### 关键字段（情节）
- `goal` — 尝试的目标
- `outcome` — 成功、失败或放弃
- `decisions` — 做出的关键决策
- `problems` — 遇到的问题（结构化）
- `solutions` | 应用的解决方案（结构化）
- `key_learnings` | 提取的教训

---

## 置信度评分

有效置信度根据以下因素计算：
- **基础置信度**（0.0–1.0）
- **来自支持事实的增强置信度**
- **来自已建立实体的增强置信度**
- **基于成功/失败历史的调整**
- **来自矛盾事实的置信度降低**
- **时间衰减**（可配置，每月约5%）

---

## 维护

### 自动化 — 通过OpenClaw定时任务运行

自我提升循环通过两个注册的OpenClaw定时任务运行：

```
Every 6h  → python3 scripts/extract-knowledge.py extract
             (reads memory files, extracts facts into the graph)

Daily 3AM → python3 scripts/extract-knowledge.py discover-relations
             (finds semantic relationships between existing facts)
```

这些任务已在OpenClaw中预注册。要验证它们是否正在运行：
```bash
openclaw cron list
# or ask Koda: "list cron jobs"
```

要手动触发提取操作：
```bash
# From the Memory dashboard UI: click "Extract Changes" or "Find Relations"
# Or via CLI:
cd ~/openclaw/skills/surrealdb-memory && source .venv/bin/activate
python3 scripts/extract-knowledge.py extract
python3 scripts/extract-knowledge.py discover-relations
```

### 手动操作（通过UI）
使用“Memory”标签页中的**维护**部分：
- **Apply Decay** — 降低过时事实的置信度
- **Prune Stale** — 将置信度低于0.3的事实存档
- **Full Sweep** — 运行完整的维护周期

---

## 文件

### 脚本
| 文件 | 用途 |
|------|---------|
| `mcp-server-v2.py` | 包含所有11个工具的MCP服务器 |
| `mcp-server.py` | 旧版v1 MCP服务器 |
| `episodes.py` | 情景记忆模块 |
| `working_memory.py` | 工作记忆模块 |
| `memory-cli.py` | 用于手动操作的命令行接口 |
| `extract-knowledge.py` | 从文件批量提取事实（支持`--agent-id`参数） |
| `knowledge-tools.py` | 高级提取工具 |
| `schema-v2.sql` | v2数据库模式 |
| `migrate-v2.py` | 迁移脚本 |

### 集成
| 文件 | 用途 |
|------|---------|
| `openclaw-integration/gateway/memory.ts` | 网关服务器方法 |
| `openclaw-integration/ui/memory-view.ts` | 内存仪表板UI |
| `openclaw-integration/ui/memory-controller.ts` | UI控制器 |

---

## 故障排除

**“连接被拒绝”**
→ 启动SurrealDB：`surreal start --bind 127.0.0.1:8000 --user root --pass root file:~/.openclaw/memory/knowledge.db`

**“未配置MCP服务器”**
→ 确保mcporter从包含`config/mcporter.json`的目录中运行，并且定义了surrealdb-memory服务器

**内存注入返回空值**
→ 检查环境变量中是否设置了`OPENAI_API_KEY`
→ 确认SurrealDB正在运行且模式已初始化

**搜索结果为空**
→ 通过UI或CLI运行提取操作：`python3 scripts/extract-knowledge.py extract`

**在关系发现中“没有可分析的事实”**
→ 如果所有事实都已经相互关联，这是正常的——说明知识图谱已经连接良好。如果知识图谱为空，请先运行提取操作。

**进度条不更新**
→ 确保在UI更新后重新启动了网关
→ 检查浏览器控制台是否有polling错误

**错误代理的事实出现**
→ 检查是否正确地将`agent_id`传递给了所有存储/搜索调用
→ 确认已应用`references/enhanced-loop-hook-agent-isolation.md`以进行自动注入的上下文限制

---

## 从v1/v2.1升级**

### 向后兼容性

所有没有`agent_id`的现有事实都被视为属于`"main"`代理。

---

## 统计数据

可以通过UI（仪表板部分）或CLI查看知识图谱：
```bash
mcporter call surrealdb-memory.knowledge_stats
```

示例输出：
```json
{
  "facts": 379,
  "entities": 485,
  "relations": 106,
  "episodes": 3,
  "avg_confidence": 0.99
}
```

*v2.2 — 代理隔离、自我提升循环、基于定时任务的提取和关系关联*