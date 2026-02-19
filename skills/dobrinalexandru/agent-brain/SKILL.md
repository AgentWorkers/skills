---
name: agent-brain
description: "专为AI代理设计的本地优先持久化存储方案，采用SQLite进行数据存储；支持数据检索/提取流程的自动化管理、混合式数据检索机制、矛盾检测功能、错误修正学习机制，并提供可选的SuperMemory镜像备份功能。"
homepage: https://github.com/alexdobri/agent-brain
metadata:
  openclaw:
    emoji: 🧠
    disable-model-invocation: false
    user-invocable: true
---
# Agent Brain 🧠

**只需教人工智能一次，它就会永远记住。随着时间的推移，它会变得越来越聪明。**

Agent Brain 是一个用于人工智能代理的模块化记忆系统，具备持续学习的能力。它能够存储事实信息、识别矛盾之处、了解用户习惯、吸收外部知识、追踪有效的方法、从错误中学习，并根据用户的语气进行调整——所有这些功能都通过一个本地 SQLite 数据库来实现，该数据库支持持久化存储、全文搜索以及可插拔的存储后端。

### 为什么需要这样的系统

每次与人工智能的对话都像是从零开始。用户可能需要重复说明同样的内容，而人工智能也可能会忘记你之前教给它的内容。Agent Brain 通过一个可靠的持久化层（`scripts/memory.sh`）以及六个认知模块来解决这个问题，这些模块会根据任务的实际需求被选择性地调用。

### 它的独特之处

- **生产级存储**：使用支持 WAL 模式的 SQLite 和索引查询功能，可以轻松处理 10,000 条以上的条目；同时提供 JSON 后端作为备用选项。
- **可插拔的后端**：存储抽象层允许你将 SQLite 替换为 Postgres、Supabase 或其他后端，而命令接口保持不变。
- **持续学习**：系统会记录错误和正确的操作及其原因，成功的经验会强化有效的方法；重复的错误会帮助识别不良的做事方式。
- **选择性处理**：调度器会根据任务的需要选择 1-3 个相关的模块来执行任务。存储信息时不需要额外的处理流程，读取用户语气时也不需要额外的模块。
- **主动提取信息**：代理会自动扫描用户消息中的可存储内容（如身份信息、技术栈、偏好设置、工作流程等）。
- **真实的信心评估**：不会给出虚假的 0.0-1.0 分数；信心评估基于元数据（如信息来源类型、访问次数、信息更新时间）分为四个等级：**确定**（SURE）、**可能**（LIKELY）、**不确定**（UNCERTAIN）、**未知**（UNKNOWN）。
- **混合式检索**：结果会根据词汇和语义进行排序（通过参数 `--policy fast|balanced|deep`），并提供可选的分数解释功能（`--explain`）。
- **替换而非删除**：旧的信息不会被删除，而是会被标记为 `superseded_by` 并附上替换信息的指针，从而保留完整的历史记录。
- **自动衰减机制**：条目的衰减速度会根据访问次数进行调整：使用频繁的知识会保留得更久，不常用的知识则会逐渐消失。

## 架构

六个模块，一个调度器，以及可插拔的存储系统。

```
          ┌──────────────────────────────┐
          │       🧠 ORCHESTRATOR        │
          │   Dispatches by task type    │
          └──────────┬───────────────────┘
                     │
        ┌────────────┼────────────────────┐
        │ Which modules does this need?   │
        └────────────┼────────────────────┘
                     │
   ┌─────────┬───────┼───────┬──────────┬──────────┐
   ▼         ▼       ▼       ▼          ▼          ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ARCHIVE│ │GAUGE │ │INGEST│ │SIGNAL│ │RITUAL│ │ VIBE │
│  📦  │ │  📊  │ │  📥  │ │  ⚡  │ │  🔄  │ │  🎭  │
│Store │ │Conf. │ │Learn │ │Check │ │Habits│ │ Tone │
└──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘
   └─────────┴───────┴────┬───┴────────┴─────────┘
                          ▼
                ┌──────────────────┐
                │  💾 memory.db    │
                │  SQLite (default)│
                │  or memory.json  │
                └──────────────────┘
```

## 工作原理

### 每条消息的处理流程

对于用户的每条消息，代理会执行以下步骤：

**步骤 1：检索（RETRIEVE）** — 在执行任何操作之前，先在内存中查找与这条消息相关的信息。

从用户消息中提取 2-4 个关键词，然后进行搜索：

```bash
./scripts/memory.sh get "<topic words>" --policy balanced
```

如何选择搜索词：

| 用户输入 | 搜索查询 | 原因 |
|-----------|-------------|-----|
| “帮我设置 API 端点” | `"api endpoint setup"` | 核心任务相关的名词 |
| “你能重构认证模块吗？” | `"auth refactor code"` | 任务 + 领域相关 |
| “我们的服务器运行在哪个端口？” | `"server port config"` | 问题主题 |
| “修复 checkout 中的 TypeScript 错误” | `"typescript checkout error"` | 技术 + 组件相关 |
| “为支付流程编写测试用例” | `"payment testing workflow"` | 领域 + 动作相关 |

如果搜索到结果，就将其用于生成响应；永远不要使用 “我记得...” 或 “根据我的记忆...” 这样的表述，而是自然地应用这些知识。

如果没有找到结果，就按正常流程继续处理。

### 步骤 2：提取（EXTRACT）** — 扫描用户消息，提取可存储的信息、偏好设置或操作步骤。

具体细节请参考 **Archive 模块**（`modules/archive/SKILL.md`）中的信号模式、分类和示例。在存储之前，务必检查是否存在冲突：

```bash
./scripts/memory.sh conflicts "<content to store>"
# If NO_CONFLICTS → proceed with add
# If POTENTIAL_CONFLICTS → ask user to clarify, or supersede old entry
./scripts/memory.sh add <type> "<content>" <source> "<tags>"
```

提取过程是静默进行的，不会发出任何提示信息。

**步骤 3：响应（RESPOND）** — 根据检索到的信息来回答用户的问题。

**步骤 4：学习（LEARN）** — 如果用户纠正了你的回答或确认某些操作是正确的，就将其记录下来：

```bash
# User says "that's wrong, it's actually X"
./scripts/memory.sh correct <wrong_id> "<right content>" "<reason>"

# User says "that worked great"
./scripts/memory.sh success <id>
```

### 完整示例

**用户输入**：“你能更新数据库迁移吗？我们使用的是 Prisma 和 PostgreSQL。”

代理的处理流程如下：

1. **检索（RETRIEVE）**：搜索相关信息
   ```bash
   ./scripts/memory.sh get "database migration prisma"
   ```
   结果：`[sure] （事实）项目使用 Prisma ORM 和 PostgreSQL` — 确认后，按照已知设置进行操作。

2. **提取（EXTRACT）**：用户提供了技术栈信息。检查是否已经存储在内存中：
   - “我们使用的是 Prisma 和 PostgreSQL” — 如果已经存储在内存中，则跳过此步骤。

3. **响应（RESPOND）**：利用关于 Prisma 和 PostgreSQL 的知识来帮助用户完成迁移。

4. **学习（LEARN）**：此时没有需要纠正或确认的内容。

**用户输入**：“实际上我们上个月改用了 Drizzle。”

代理的处理流程如下：

1. **检索（RETRIEVE）**：`./scripts/memory.sh get "database orm drizzle"` — 没有找到关于 Drizzle 的信息。

2. **提取（EXTRACT）**：这是一个需要纠正的错误。找到旧的记录并进行修正：
   ```bash
   ./scripts/memory.sh correct <prisma_entry_id> "Project uses Drizzle ORM with PostgreSQL" "Switched from Prisma to Drizzle"
   ```

3. **响应（RESPOND）**：确认用户已经改用了 Drizzle，并调整建议以使用 Drizzle。

### 选择性处理

并非每个任务都需要使用所有模块。调度器会根据任务类型选择性地调用相关模块：

| 任务类型 | 使用的模块 |
|-----------|-------------|
| 任何消息（提取信息） | Archive（提取 + 存储）+ Signal（检查冲突） |
| 回答问题 | Gauge（信心评估）+ Archive（检索） |
| 用户显得沮丧 | Vibe（检测用户情绪）+ Archive（调整回答风格） |
| 吸收 URL | Ingest（获取 URL）+ Archive（存储提取的信息） |
| 重复的工作流程 | Ritual（检测重复行为）+ Archive（存储） |
| 检查一致性 | Signal（检测冲突）+ Archive（存储结果） |
| 用户纠正了你的回答 | Archive（记录纠正内容）+ Gauge（更新信心评估） |
| 记录有效的操作 | Archive（记录成功案例） |
| 检查内存状态 | Archive（记录操作历史） |

### 持久化

记忆信息存储在 `memory/memory.db`（默认为 SQLite）或 `memory/memory.json`（旧版本）中。
所有操作都通过 `scripts/memory.sh` 和 `scripts/brain.py` 来执行，其中存储后端是可插拔的。

```
AGENT_BRAIN_BACKEND=sqlite  (default) → memory/memory.db
AGENT_BRAIN_BACKEND=json    (legacy)  → memory/memory.json
```

**可选的 SuperMemory 功能**（在写入操作时生效，如 `add`、`correct`）：

```
AGENT_BRAIN_SUPERMEMORY_SYNC=auto  (default)
AGENT_BRAIN_SUPERMEMORY_SYNC=on    (force sync attempt)
AGENT_BRAIN_SUPERMEMORY_SYNC=off   (disable sync)
SUPERMEMORY_API_KEY=...            (required for auto/on)
SUPERMEMORY_API_URL=...            (optional; default https://api.supermemory.ai/v3/documents)
AGENT_BRAIN_SUPERMEMORY_TIMEOUT=8  (optional timeout seconds)
AGENT_BRAIN_SUPERMEMORY_DEBUG=1    (optional sync warnings to stderr)
```

默认情况下（`auto`），只有当 `SUPERMEMORY_API_KEY` 可用时（可以从环境变量中获取，或者从 `AGENT_BRAIN_ENV_FILE` 文件中加载，该文件位于 `scripts/memory.sh` 中，默认路径为 `../.env`），Agent Brain 才会尝试与云端同步；因此本地持久化仍然是默认行为。

SQLite 后端支持 WAL 模式，支持并发读取，并对数据类型/信心/标签/记忆类别进行索引处理，处理速度低于 100 毫秒。现有的 `memory.json` 文件会在首次运行时自动迁移到 SQLite 中（原始文件会被备份为 `memory.json.bak`）。

### 信心评估

不会给出虚假的数字分数。信心评估基于元数据分为四个等级：
- **确定**（SURE）：多次被提及或成功应用超过 3 次的事实。
- **可能**（LIKELY）：仅被提及一次且没有矛盾的信息。
- **不确定**（UNCERTAIN）：根据元数据推断出来的信息。
- **未知**（UNKNOWN）：没有相关记忆记录的信息。

### 检索结果排序

结果会根据以下混合公式进行排序：
- 关键词匹配（40%）：考虑有意义的词汇和过滤后的停用词。
- 标签重叠（25%）：支持命名空间化的标签（例如 `code.python`）。
- 信心程度（15%）：信心程度较高的条目排名更高。
- 最新访问时间（10%）：最近被访问的条目会获得优先显示。
- 访问频率（10%）：频繁使用的知识会获得更高的排名。
- 语义相似性（取决于配置）：默认使用本地语义向量；如果启用 `AGENT_BRAIN_REMOTE_EMBEDDINGS=on` 并设置 `AGENT_BRAIN_EMBEDDING_URL`，则会使用远程嵌入算法。

检索到的条目会自动标记为已被访问（无需手动操作）。

### 持续学习

学习过程包括三个信号机制：
- **纠正（correct）**：当你回答错误时，系统会记录错误的内容、正确的答案及其原因。如果同一标签被纠正超过 3 次，系统会识别出不良的做事方式。
- **成功（success）**：当某个记忆被成功应用时，系统会将其记录下来。如果成功应用超过 3 次，信心等级会自动提升到 **确定**。
- **模式识别（similar）**：代理可以手动检查是否存在 3 次以上的相似条目，并创建相应的模式记录。如果同一标签被纠正超过 3 次，系统会自动识别出不良的做事方式。

## 存储方式

默认存储方式：`memory/memory.db`（SQLite）。旧版本使用 `memory/memory.json`。

### 条目结构

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `id` | UUID | 唯一标识符 |
| `type` | 字符串 | 类型（如事实、偏好设置、操作步骤、模式、吸收的信息、纠正内容、不良模式、策略） |
| `memory_class` | 字符串 | 记忆信息的分类（如事件性、语义性、程序性、偏好设置、策略） |
| `content` | 字符串 | 记忆内容 |
| `source` | 字符串 | 信息来源（用户输入、推断或外部获取） |
| `source_url` | 字符串？ | 来源 URL |
| `tags` | 列表 | 带有命名空间的标签（例如 `code.python`） |
| `context` | 字符串？ | 信息适用的场景（例如 “日常对话”） |
| `session_id` | 整数？ | 信息创建的会话 ID |
| `created` | ISO 8601 格式的创建时间 |
| `last_accessed` | ISO 8601 格式的最后访问时间 |
| `access_count` | 整数 | 访问次数（从 1 开始计数） |
| `confidence` | 字符串 | 信心等级（确定、可能、不确定） |
| `superseded_by` | UUID？ | 替换条目的指针 |
| `success_count` | 整数 | 成功应用的次数 |
| `correction_meta` | 对于纠正操作，包含错误条目的 ID、错误的说法、正确的答案、原因等 |

### 元数据字段

| 字段 | 描述 |
|-----|-------------|
| `version` | 数据库版本（4） |
| `last_decay` | 上次衰减操作的时间戳 |
| `session_counter` | 自动递增的会话 ID |
| `current_session` | 当前活跃会话（ID、上下文、开始时间） |

### 衰减机制

条目的衰减速度会根据访问次数进行调整：访问次数越多，衰减速度越快：
- 访问一次的条目在 60 天后开始衰减。
- 访问 5 次的条目在 180 天后开始衰减。
- 高频使用的知识会保留得更久。

衰减机制会在 `get` 和 `add` 操作中自动执行（有 24 小时的冷却时间）。

### 标签

标签支持命名空间化的表示法（例如 `code.python`、`style.tone`、`workflow.git`）。
搜索时，`code` 既匹配 `code.python` 也匹配 `code.typescript`。
可以使用 `./scripts/memory.sh tags` 来查看标签的层级结构。

## 自然语言 → 命令

以下是一些用户可能说的话以及代理应该执行的命令示例：

### 核心功能（Core）```
"Remember: <fact>"              → add fact "<content>" user "<tags>"
"What do you know about X?"     → get "<topic>" --policy balanced
"Process this full message"     → loop "<message>"
"Update that info"              → supersede <old_id> <new_id>
"Show all memories"             → export
```

### 学习功能（Learning）```
"That's wrong, it's actually Y" → correct <wrong_id> "<right>" "<reason>"
"That worked well"               → success <id>
"What patterns do you see?"      → similar "<topic>" (agent creates pattern if 3+ found)
"Any anti-patterns?"             → list anti-pattern
```

### 元数据管理（Meta）```
"Check for conflicts"           → conflicts "<content>"
"Memory health?"                → reflect
"What needs consolidation?"     → consolidate
"What happened recently?"       → log
```

### 会话管理（Sessions）```
"Start session: Frontend work"  → session "Frontend work"
```

## 模块结构

每个模块都有对应的 `SKILL.md` 文件，位于 `modules/` 目录下：

| 模块 | 类型 | 功能 | 适用场景 |
|--------|------|-------------|-----------------|
| **Archive** 📦 | 存储和检索记忆信息 | 所有的存储/检索操作 |
| **Gauge** 📊 | 评估信心等级 | 在返回基于记忆的答案时使用 |
| **Ingest** 📥 | 获取 URL 并提取信息 | 用户输入 “Ingest: URL”（默认禁用） |
| **Signal** ⚡ | 检测信息中的矛盾 | 在存储前调用 `conflicts` 函数 |
| **Ritual** 🔄 | 识别重复行为 | 存储后调用 `similar` 函数 |
| **Vibe** 🎭 | 分析用户语气 | 每条消息都会分析用户的语气 |

**代码**（Code）：实现于 `scripts/brain.py` 中，包含具体的命令逻辑。
**指南**（Guideline）：代理的行为指令——没有专门的代码，代理通过 `add`、`get`、`conflicts`、`similar` 等命令来执行这些功能。

## 安全性

- **优先使用本地存储**：所有数据首先写入 `memory/memory.db`。
- **可选的云端同步**：SuperMemory 同步是可选的，可以通过 `AGENT_BRAIN_SUPERMEMORYSYNC=off` 来禁用。
- **保护用户隐私**：敏感信息会被拒绝存储（默认设置为 `AGENT_BRAIN_PII_MODE=strict`）。
- **禁止自动获取 URL**：需要用户明确同意才能获取 URL（防止 SSRF 风险）。
- **可导出**：可以使用 `export` 命令将所有记忆信息导出为 JSON 格式，或者直接打开 SQLite 文件查看。
- **WAL 模式**：SQLite 的 Write-Ahead Logging 功能可以防止数据损坏。
- **自动迁移**：v2/v3 格式的 JSON 或 SQLite 数据会自动迁移到新版本（包括备份）。