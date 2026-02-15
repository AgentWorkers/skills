---
name: clawvault
version: 1.12.1
description: 该代理内存系统具备检查点/恢复功能、结构化存储机制、观测性内存支持以及会话记录修复能力。它与 OpenClaw 的 qmd 内存后端集成，用于 BM25+vector+reranker 搜索算法。适用场景包括：存储/检索内存数据、防止数据丢失（即“上下文丢失”现象）、修复损坏的会话记录。不建议用于常规的文件读写操作。
author: Versatly
repository: https://github.com/Versatly/clawvault
homepage: https://clawvault.dev
metadata: {"openclaw":{"emoji":"🐘","requires":{"bins":["clawvault"]},"env":{"CLAWVAULT_PATH":{"required":false,"description":"Vault directory path (auto-discovered if not set)"},"GEMINI_API_KEY":{"required":false,"description":"Only used by observe --compress for LLM compression. No other command uses this."}},"hooks":{"clawvault":{"events":["gateway:startup","command:new"],"capabilities":["executes clawvault CLI via child_process","reads vault state files","injects recovery alerts into session on context death","runs clawvault checkpoint before /new","runs clawvault observe --compress on session transcript (if GEMINI_API_KEY set)"],"does_not":["modify session transcripts (only the repair-session CLI command does that, never the hook)","make network calls (the hook itself makes zero network calls; observe --compress may call Gemini API)","access files outside the vault directory and session transcript path"]}},"install":[{"id":"node","kind":"node","package":"clawvault","bins":["clawvault"],"label":"Install ClawVault CLI (npm)"}]}}
---

# ClawVault 🐘

“大象永远不会忘记。”专为 OpenClaw 代理设计的结构化存储解决方案。

> **专为 [OpenClaw](https://openclaw.ai) 设计** — 通过 `clawhub install clawvault` 进行安装

## 安全性与透明度

**该工具的功能说明：**

| 功能 | 范围 | 是否需要手动启用？ |
|---|---|---|
| 读写 markdown 文件 | 仅限于您的存储目录（`CLAWVAULT_PATH` 或自动检测到的目录） | 始终启用 |
| 在存储目录中搜索（关键词 + 语义搜索） | 通过 `qmd` CLI 进行只读查询 | 始终启用 |
| 创建检查点/恢复/唤醒/休眠 | 将状态文件写入存储目录内的 `.clawvault/` 目录 | 始终启用 |
| `repair-session` — 修复损坏的会话记录 | 读取并修改 `~/.openclaw/agents/` 目录中的 JSONL 文件。**写入前会自动创建备份文件 `.bak`**。可以使用 `--dry-run` 预览更改而不进行任何修改。 | 仅通过特定命令启用 |
| OpenClaw 钩子（`handler.js`） | 在 `gateway:startup` 和 `command:new` 事件期间运行。调用 `clawvault checkpoint` 和 `clawvault recover`。**不进行网络调用**。 | **需要手动启用** — 必须运行 `openclaw hooks enable clawvault` |
| `observe --compress` — LLM 压缩功能 | 将会话记录文本发送到 Gemini Flash API 以提取分析数据。**这是唯一一个会进行外部 API 调用的功能**。需要设置 `GEMINI_API_KEY`。如果没有设置该密钥，此功能将无法使用。 | 仅通过特定命令启用，并且需要 API 密钥 |

**网络调用：** 默认情况下为零。唯一会进行外部 API 调用的功能是 `observe --compress`，且只有在您使用有效的 `GEMINI_API_KEY` 启用该功能时才会执行。所有其他命令都是纯粹的本地文件系统操作。

**使用的环境变量：**
- `CLAWVAULT_PATH` — 存储目录的位置（可选，如果未设置则自动检测）
- `OPENCLAW_HOME` / `OPENCLAW_STATE_DIR` — 由 `repair-session` 用于定位会话记录文件 |
- `GEMINI_API_KEY` — 仅由 `observe --compress` 用于 LLM 压缩功能。如果未设置，`observe` 会使用基于规则的默认压缩方式。其他命令不会读取此密钥。
- `CLAWVAULT_NO_LLM=1` — 即使存在 API 密钥，也强制禁用所有 LLM 调用

**注意：** 该工具不支持云同步、遥测、数据分析或数据上报功能。所有数据都保存在您的本地机器上。

## 钩子行为（`hooks/clawvault/handler.js`）

捆绑提供的钩子是**可选**的——在您未运行 `openclaw hooks enable clawvault` 之前，它不会执行任何操作。

启用后，它会处理以下两个事件：

| 事件 | 执行的操作 | 是否进行网络调用？ |
|---|---|---|
| `gateway:startup` | 运行 `clawvault recover --clear` 以检查会话是否中断。如果检测到中断，会在会话中插入恢复提示。 | **不进行网络调用** |
| `command:new` | 在重置之前运行 `clawvault checkpoint` 以保存状态。如果存在会话记录文件，还会运行 `clawvault observe --compress`。 | **仅在设置了 `GEMINI_API_KEY` 时进行压缩**。如果没有设置密钥，`observe` 会使用基于规则的默认压缩方式，且不进行网络调用。 |

**该钩子不执行以下操作：**
- 不会修改会话记录（这些操作由单独的 `repair-session` CLI 命令完成）
- 不会读取或写入存储目录之外的文件
- 不会进行数据上报、收集分析数据，也不会联系任何服务器（除了用于 `observe` 功能的 Gemini API）

该钩子通过 `child_process.execSync` 执行 `clawvault` CLI 可执行文件。您需要单独安装该文件（使用 `npm install -g clawvault`）。钩子的源代码完整地保存在 `hooks/clawvault/handler.js` 中。

## 安装

```bash
npm install -g clawvault
```

## 设置

```bash
# Initialize vault (creates folder structure + templates)
clawvault init ~/my-vault

# Or set env var to use existing vault
export CLAWVAULT_PATH=/path/to/memory

# Optional: shell integration (aliases + CLAWVAULT_PATH)
clawvault shell-init >> ~/.bashrc
```

## 新代理的快速入门

```bash
# Start your session (recover + recap + summary)
clawvault wake

# Capture and checkpoint during work
clawvault capture "TODO: Review PR tomorrow"
clawvault checkpoint --working-on "PR review" --focus "type guards"

# End your session with a handoff
clawvault sleep "PR review + type guards" --next "respond to CI" --blocked "waiting for CI"

# Health check when something feels off
clawvault doctor
```

## 核心命令

### 唤醒/休眠（基本操作）

```bash
clawvault wake
clawvault sleep "what I was working on" --next "ship v1" --blocked "waiting for API key"
```

### 按类型存储数据

```bash
# Types: fact, feeling, decision, lesson, commitment, preference, relationship, project
clawvault remember decision "Use Postgres over SQLite" --content "Need concurrent writes for multi-agent setup"
clawvault remember lesson "Context death is survivable" --content "Checkpoint before heavy work"
clawvault remember relationship "Justin Dukes" --content "Client contact at Hale Pet Door"
```

### 快速将数据捕获到收件箱

```bash
clawvault capture "TODO: Review PR tomorrow"
```

### 搜索（需要安装 qmd）

```bash
# Keyword search (fast)
clawvault search "client contacts"

# Semantic search (slower, more accurate)
clawvault vsearch "what did we decide about the database"
```

## 会话中断的恢复机制

### 唤醒（会话开始）

```bash
clawvault wake
```

### 休眠（会话结束）

```bash
clawvault sleep "what I was working on" --next "finish docs" --blocked "waiting for review"
```

### 定期创建检查点（保存状态）

```bash
clawvault checkpoint --working-on "PR review" --focus "type guards" --blocked "waiting for CI"
```

### 手动恢复（手动检查）

```bash
clawvault recover --clear
# Shows: death time, last checkpoint, recent handoff
```

### 会话结束时的数据移交

```bash
clawvault handoff \
  --working-on "ClawVault improvements" \
  --blocked "npm token" \
  --next "publish to npm, create skill" \
  --feeling "productive"
```

### 会话重启（重新启动新会话）

```bash
clawvault recap
# Shows: recent handoffs, active projects, pending commitments, lessons
```

## 自动链接

在 markdown 文件中链接 Wiki 实体：

```bash
# Link all files
clawvault link --all

# Link single file
clawvault link memory/2024-01-15.md
```

## 文件夹结构

```
vault/
├── .clawvault/           # Internal state
│   ├── last-checkpoint.json
│   └── dirty-death.flag
├── decisions/            # Key choices with reasoning
├── lessons/              # Insights and patterns
├── people/               # One file per person
├── projects/             # Active work tracking
├── handoffs/             # Session continuity
├── inbox/                # Quick captures
└── templates/            # Document templates
```

## 最佳实践

1. **会话开始时唤醒** — 使用 `clawvault wake` 恢复会话上下文
2. **在高负载工作时每 10-15 分钟创建一个检查点**  
3. **会话结束时休眠** — 使用 `clawvault sleep` 保存后续操作  
4. **明确数据类型** — 了解要存储的数据类型有助于决定存储位置  
5. **广泛使用 Wiki 链接** — 使用 `[[person-name]]` 构建知识图谱  

## AGENTS.md 的检查清单

```markdown
## Memory Checklist
- [ ] Run `clawvault wake` at session start
- [ ] Checkpoint during heavy work
- [ ] Capture key decisions/lessons with `clawvault remember`
- [ ] Use wiki-links like `[[person-name]]`
- [ ] End with `clawvault sleep "..." --next "..." --blocked "..."`
- [ ] Run `clawvault doctor` when something feels off
```

## 会话记录修复（v1.5.0+）

当 Anthropic API 返回 “unexpected tool_use_id found in tool_result blocks” 错误时，请使用以下命令：

```bash
# See what's wrong (dry-run)
clawvault repair-session --dry-run

# Fix it
clawvault repair-session

# Repair a specific session
clawvault repair-session --session <id> --agent <agent-id>

# List available sessions
clawvault repair-session --list
```

**修复内容：**
- 修复引用不存在的 `tool_use` ID 的孤立 `tool_result` 块  
- 修复因工具调用失败而导致的部分 JSON 数据  
- 修复损坏的父级引用链  

系统会自动创建备份（使用 `--no-backup` 可跳过备份功能）。

## 故障排除

- **未安装 qmd** — 运行 `bun install -g github:tobi/qmd` 或 `npm install -g qmd`  
- **未找到 ClawVault** — 运行 `clawvault init` 或设置 `CLAWVAULT_PATH`  
- **CLAWVAULT_PATH 未设置** — 运行 `clawvault shell-init` 并将其添加到 shell 配置文件中  
- **存在过多孤立链接** — 运行 `clawvault link --orphans`  
- **收件箱积压警告** — 处理或归档收件箱中的项目  
- **出现 “unexpected tool_use_id” 错误** — 运行 `clawvault repair-session`  

## 与 qmd 的集成

ClawVault 使用 [qmd](https://github.com/tobi/qmd) 进行搜索：

```bash
# Install qmd
bun install -g github:tobi/qmd

# Add vault as collection
qmd collection add /path/to/vault --name my-memory --mask "**/*.md"

# Update index
qmd update && qmd embed
```

## 环境变量

- `CLAWVAULT_PATH` — 默认存储目录路径（未设置时自动检测）  
- `OPENCLAW_HOME` — OpenClaw 的主目录（由 `repair-session` 使用）  
- `OPENCLAW_STATE_DIR` — OpenClaw 的状态目录（由 `repair-session` 使用）  
- `GEMINI_API_KEY` — 由 `observe` 功能用于 LLM 压缩（可选）  

## 架构：ClawVault + qmd

ClawVault 和 qmd 的作用互补：

- **ClawVault** 负责存储、分类、路由观察数据、管理会话连续性（唤醒/休眠/创建检查点）以及实体链接。它按类别组织 markdown 文件。  
- **qmd** 负责搜索：提供 BM25 关键字搜索、向量嵌入以及用于提高搜索准确性的重新排序算法。它会索引 ClawVault 生成的 markdown 文件。  

**组合使用方式：** ClawVault 生成数据 → qmd 进行索引 → 您可以使用 `qmd query`（结合 BM25 算法、向量嵌入和神经重新排序算法）进行搜索，从而获得最准确的结果。

### OpenClaw 配置建议

```yaml
memory:
  backend: "qmd"
  vault: "${CLAWVAULT_PATH}"
```

默认的 `qmd query` 流程使用 BM25 关键字匹配、向量嵌入和神经重新排序算法来获得最准确的结果。

### 低内存环境

神经重新排序算法需要约 8GB 以上的 RAM。在内存有限的机器上（例如小型 VPS 或 WSL2 环境），`qmd query` 可能会因内存不足而崩溃。您可以在 OpenClaw 配置中设置 `qmd_command` 为指向 `qmd vsearch`（仅使用向量，不使用重新排序算法）的包装脚本。这是一种特定于操作系统的解决方案，并非推荐的最佳做法。

## 链接

- npm: https://www.npmjs.com/package/clawvault  
- GitHub: https://github.com/Versatly/clawvault  
- 问题报告：https://github.com/Versatly/clawvault/issues