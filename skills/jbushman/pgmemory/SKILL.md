---
name: pgmemory
version: 1.2.0
description: OpenClaw代理的持久性语义记忆存储方案：PostgreSQL + pgvector
author: jbushman
tags: [memory, postgresql, pgvector, embeddings, agents]
---
# pgmemory

pgmemory 为 OpenClaw 代理提供了持久化的语义记忆功能，该功能基于 PostgreSQL 和 pgvector 实现。

每次会话开始时，代理都会被重置为初始状态。pgmemory 解决了这个问题——代理的决策、约束条件、基础设施信息以及各种发现结果会在会话之间保持持久性，并在需要时自动显示出来。

## 设置

安装完成后，请运行以下命令一次：

```bash
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py
```

向导会处理所有相关设置：Docker/PostgreSQL 的配置、数据迁移、嵌入提供者的选择、`AGENTS.md` 文件的生成，以及记忆数据的定期清理（通过 cron 任务）。

## 何时使用此功能

在以下情况下，请阅读本文档：
- 首次设置 pgmemory 时
- 添加新的 OpenClaw 代理并希望其具备持久化记忆功能时
- 诊断内存问题时（运行 `--doctor` 命令）
- 更换嵌入提供者时
- 了解记忆数据的衰减机制或归档流程时

## 核心命令

### 创建记忆记录

```bash
python3 ~/.openclaw/skills/pgmemory/scripts/write_memory.py \
  --key "unique.descriptive.key" \
  --content "What to remember" \
  --category decision \
  --importance 3
```

**记录类别：** `decision`（决策）、`constraint`（约束条件）、`infrastructure`（基础设施信息）、`vision`（长远规划）、`preference`（偏好设置）、`context`（上下文信息）、`task`（任务相关内容）

**重要性等级：**
- `3`：至关重要——决策、约束条件、基础设施信息。这些记录永远不会过期，始终会被加载。
- `2`：重要——上下文信息、偏好设置。如果未被使用，将在 180 天后过期。
- `1`：临时性记录——低价值的信息。将在 30 天后过期。

### 搜索记忆记录

```bash
# Semantic search
python3 ~/.openclaw/skills/pgmemory/scripts/query_memory.py "database connection"

# Load all critical memories (importance 3)
python3 ~/.openclaw/skills/pgmemory/scripts/query_memory.py --importance 3 --limit 20

# Stats
python3 ~/.openclaw/skills/pgmemory/scripts/query_memory.py --stats

# List all keys
python3 ~/.openclaw/skills/pgmemory/scripts/query_memory.py --list
```

### 维护

```bash
# Full health check
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --doctor

# Validate config
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --validate

# Run pending migrations
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --migrate

# Sync pgmemory into all OpenClaw agent workspaces
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --sync-agents

# Run decay cycle manually
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --decay
```

## 何时需要创建记忆记录

在以下情况下，请立即创建记忆记录：
- 当您对架构、工具或方法做出决策时
- 当您发现可能对后续工作产生影响的约束条件时
- 当您完成基础设施相关的操作（如数据迁移、部署或配置更改）时
- 当您确定了一些应指导未来工作的偏好设置或长远规划时
- 当子代理完成任务后，需要收集其重要的发现结果时

**无需创建记忆记录的情况：**
- 用于日常的非正式交流
- 已经记录在 `MEMORY.md` 或其他工作区文件中的内容
- 除非内容确实有用，否则不需要创建重要性等级为 1 的记录

## 多代理设置

每个 OpenClaw 代理都有自己的命名空间（即代理 ID）。在添加新代理后，运行 `--sync-agents` 命令，pgmemory 会自动完成相应的配置：

```bash
openclaw agents add code-writer
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --sync-agents
```

或者，您也可以在 `HEARTBEAT.md` 文件中添加 `--sync-agents` 选项，以便系统在 30 分钟内自动完成配置。

### 从子代理处收集数据

当子代理完成任务后，需要将其重要的发现结果同步到主命名空间中：

```bash
python3 ~/.openclaw/skills/pgmemory/scripts/query_memory.py \
  --harvest shopwalk:subagent:task-label
```

## 记忆数据的衰减机制

记忆记录会根据其创建时间和类别进行衰减。频繁访问的记忆记录会保持最新状态；已衰减的记忆记录会被移至归档区（但不会被删除）。如果在未来的搜索中再次需要这些记录，系统会自动将其恢复。

记忆数据的衰减过程通过 cron 任务每天自动执行（具体配置在设置阶段完成）。您也可以随时手动执行该任务：

```bash
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --decay
```

## 更换嵌入提供者

在设置完成后更换嵌入提供者需要重新生成所有记忆记录——因为不同的数据维度不能存储在同一数据库中。请先运行 `--doctor` 命令检查是否存在数据不一致的情况。

⚠️ 提供者迁移功能（`--re-embed`）计划在 v1.1 版本中实现。目前，如果需要更换提供者，请重新创建一个新的数据库。

## 配置参考

所需配置非常简单（仅包含最低限度的设置）：

```json
{
  "db":         { "uri": "postgresql://openclaw@localhost:5432/openclaw" },
  "embeddings": { "provider": "voyage", "api_key_env": "VOYAGE_API_KEY" },
  "agent":      { "name": "main" }
}
```

默认配置文件位于 `~/.openclaw/pgmemory.json`。您可以使用 `--config <path>` 命令进行自定义配置。

完整的配置信息请参阅 `references/schema.sql` 和 `CHANGELOG.md`。

## 系统要求

- Python 3.9 或更高版本
- PostgreSQL 14 或更高版本，且已安装 pgvector 0.5 或更高版本
- `psycopg2-binary` 和 `numpy` 库（通过 `pip install -r requirements.txt` 安装）
- 嵌入提供者的 API 密钥（或使用 Ollama 作为本地嵌入解决方案）