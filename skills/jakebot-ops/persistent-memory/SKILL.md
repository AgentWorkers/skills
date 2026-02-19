---
name: persistent-memory
description: 三层持久化存储系统（Markdown格式数据 + ChromaDB向量存储 + NetworkX知识图谱）：用于实现跨会话的长期信息存储与检索。当智能体需要在不同会话之间记住决策、事实、上下文或机构知识时，该系统可发挥重要作用。该系统支持数据存储、索引管理、历史上下文的搜索功能，同时也能帮助智能体识别自己是否忘记了之前的对话内容。
---
# 持久化内存（Persistent Memory）

该功能为任何 OpenClaw 工作空间添加了持久化的三层内存系统。通过该系统，代理能够在不同会话之间保持对决策、事实、经验教训以及机构知识的有效访问（即这些信息在系统重启后仍然可用）。

## 架构（Architecture）

| 层次 | 技术栈 | 功能                |
|-------|-----------|-------------------|
| L1：Markdown | MEMORY.md + 日志文件 | 人类可读的、经过整理的知识库 |
| L2：向量存储 | ChromaDB + MiniLM-L6-v2 | 实现跨所有知识库的语义搜索 |
| L3：图谱结构 | NetworkX       | 用于表示概念之间的关联关系 |

这三个层次会实时同步。索引器会自动从 L1 更新 L2 和 L3 的数据。

## 设置（Setup）

在 workspace 的根目录下运行以下命令：

```bash
bash skills/persistent-memory/scripts/setup.sh
```

此命令会创建一个名为 `vector_memory/` 的目录，其中包含一个 Python 虚拟环境（venv）、ChromaDB 数据库以及知识图谱。如果存在 `MEMORY.md` 文件，该脚本还会对其进行索引处理。

## 日常使用（Daily Usage）

### 编写知识内容

- **MEMORY.md**：用于存储经过整理的长期知识（如决策、项目架构、经验教训等），在重要事件发生后进行更新。
- **memory/YYYY-MM-DD.md**：记录每日发生的事件，包含原始的文字记录。
- **reference/*.md**：存储机构层面的基本信息（如人员、代码仓库、基础设施、业务规则等），可作为代理的“百科全书”。

### 索引更新（编辑任何知识文件后）

```bash
vector_memory/venv/bin/python vector_memory/indexer.py
```

索引器会解析 `MEMORY.md`、`reference/*.md` 和 `memory/*.md` 文件中的内容，将其转换为向量表示形式，并重新构建知识图谱。每次编辑后都需要运行此命令以确保各层次数据的一致性。

### 搜索功能

```bash
vector_memory/venv/bin/python vector_memory/search.py "your query"
```

该功能会返回与查询内容语义最相似的前三条信息，并同时显示原始文件及其所属章节。

### 同步状态检查

```bash
vector_memory/venv/bin/python vector_memory/auto_retrieve.py --status
```

该命令用于检查数据同步情况：比较 `MEMORY.md` 的文件哈希值与索引状态、数据条目数量以及知识图谱的大小。可以通过定期执行此命令来检测数据是否发生不一致。

## 代理行为规则（Agent Behavior Rules）

请将这些规则添加到 `AGENTS.md` 或 `SOUL.md` 文件中：

### 回答问题前的操作（强制要求）
在回答关于以往工作、决策、日期、人员或偏好设置的问题之前，必须先搜索知识库。可以使用 `memory_search` 命令或 `auto_retrieve.py` 脚本进行查询。未经查询就直接回答“我不记得了”是禁止的。

### 执行操作前的操作（强制要求）
在执行任何涉及外部标识符（如 URL、处理程序、电子邮件地址、代码仓库名称等）的操作之前，必须先在 `reference/` 文件中查询对应的准确信息。如果查询不到，则再查询向量存储中的数据；如果仍然找不到，则询问用户。**严禁伪造这些标识符**。

### 编辑文件后的操作（强制要求）
在编辑 `MEMORY.md` 或 `reference/`、`memory/` 目录下的任何文件后，需要重新执行索引操作：
```bash
vector_memory/venv/bin/python vector_memory/indexer.py
```

### 集成心跳检测（Heartbeat Integration）
请将以下代码添加到 `HEARTBEAT.md` 文件中：
```
## Memory Sync Check
Run `vector_memory/venv/bin/python vector_memory/auto_retrieve.py --status` and if status is OUT_OF_SYNC, re-index with `vector_memory/venv/bin/python vector_memory/indexer.py`.
```

## 参考目录（可选但推荐）
在 workspace 的根目录下创建 `reference/` 目录，作为代理的机构知识库：

```
reference/
├── people.md          — Contacts, roles, communication details
├── repos.md           — GitHub repositories, URLs, status
├── infrastructure.md  — Hosts, IPs, ports, services
├── business.md        — Company info, strategies, rules
└── properties.md      — Domain-specific entities (deals, products, etc.)
```

这些文件会与 `MEMORY.md` 一起被索引。代理在处理任何涉及外部标识符的操作前都会先查询这些文件。随着时间的推移，这些知识会被不断积累，从而实现“永不遗忘”的功能。

## 设置完成后的文件结构（File Structure After Setup）

```
workspace/
├── MEMORY.md              — Curated long-term memory (L1)
├── memory/
│   ├── 2026-02-17.md      — Daily log
│   └── heartbeat-state.json — Sync tracking
├── reference/             — Institutional knowledge (optional)
│   ├── people.md
│   └── ...
└── vector_memory/
    ├── indexer.py          — Index all markdown into vectors + graph
    ├── search.py           — Semantic search CLI
    ├── graph.py            — NetworkX knowledge graph
    ├── auto_retrieve.py    — Status checker + auto-retrieval
    ├── chroma_db/          — Vector database (gitignored)
    ├── memory_graph.json   — Knowledge graph (auto-generated)
    └── venv/               — Python venv (gitignored)
```

## 常见问题解决方法（Troubleshooting）

- **“找不到 chromadb 模块”**：重新运行 `setup.sh` 命令，或激活虚拟环境：`source vector_memory/venv/bin/activate`
- **同步状态异常**：运行索引器程序：`vector_memory/venv/bin/python vector_memory/indexer.py`
- **搜索结果为空**：确认 `MEMORY.md` 文件中包含有效内容，并且索引器至少已经执行过一次
- **索引过程中出现 SIGSEGV 错误**：通常是由于使用的机器学习库版本不兼容导致的。设置脚本会使用已知稳定的版本进行配置。