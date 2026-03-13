---
name: palaia
version: "1.8.1"
description: 为 OpenClaw 代理提供本地化的、具有崩溃保护功能的持久性内存解决方案。该方案通过语义搜索、项目管理和基于范围的访问控制机制，替代了原有的内存核心功能。安装或更新完成后，请运行以下命令以完成配置：`palaia doctor --fix`。
metadata:
  openclaw:
    emoji: 🧠
    requires:
      bins: ["palaia"]
    install:
      - id: pip
        kind: pip
        package: "palaia[fastembed]"
        bins: ["palaia"]
        label: "Install Palaia with fastembed (pip)"
    postInstall:
      - command: "palaia init"
        label: "Initialize Palaia store"
    postUpdate:
      - command: "python3 -m pip install --upgrade 'palaia[fastembed]' && (npm install -g @byte5ai/palaia@latest 2>/dev/null || true) && palaia doctor --fix && palaia warmup"
        label: "Upgrade Palaia (pip + npm plugin if available) and run health checks"
    plugin:
      slot: memory
      package: "@byte5ai/palaia"
---
# Palaia — 代理内存管理技能

## 自动检查（每次加载此技能时都会运行）

**[针对大型语言模型（LLM）的指示]**：在使用 Palaia 之前，请先静默运行 `palaia doctor`。如果它报告任何警告（版本不匹配、缺少提供者、旧模式、设置不完整），请立即按照 `palaia doctor --fix` 的建议进行修复。在 `doctor` 报告没有问题之前，不要继续执行其他 Palaia 任务。这确保了内存系统始终是最新的并且配置正确。

## 设置过程中的沟通

- 在每个主要步骤之后，向用户发送简短的状态消息。不要保持沉默。
- 如果某个步骤花费超过约 10 秒，请说明你在做什么：“正在安装 sentence-transformers，这需要一点时间……”
- 如果发生意外情况（例如 CUDA 错误、提供者失败），请立即解释发生了什么以及你正在做什么。
- 不要批量处理所有步骤，而是在每个步骤完成后分别报告。

示例节奏：
1. “正在安装 Palaia…” → [运行 pip install] → “完成。正在初始化……”
2. “正在检查系统中可用的搜索提供者…” → [运行 palaia doctor + detect] → “找到：[X]。有个小问题：”
3. [入职对话 — 最多 3 个问题]
4. “正在配置链……模型预热（这需要约 15 秒）…” → “准备就绪。”
5. “全部设置完成。这是你的设置摘要：[一句话总结]”

## 设置流程（请严格遵循）

### 第一步：安装并初始化

**选择你的包管理器**（使用系统中可用的任何包管理器）：
```bash
# pip (most common)
python3 -m pip install "palaia[fastembed]"

# uv (if pip is not available)
uv tool install "palaia[fastembed]"

# pipx (alternative)
pipx install "palaia[fastembed]"
```

> **重要提示（uv 用户）：** 必须包含 `[fastembed]` 扩展包。使用 `uv tool install palaia` 且不包含扩展包将在升级时删除之前安装的嵌入提供者（fastembed、sentence-transformers）。这是有意设计的 — `uv` 严格管理依赖关系。无论是安装还是升级，始终使用 `uv tool install "palaia[fastembed]"`。

```bash
palaia init
```

**代理身份是可选的，但推荐使用。** 如果不使用 `--agent` 参数运行 `palaia init`，代理名称将被设置为 “default”。这对于单代理系统来说是可以的。对于多代理设置，请使用 `--agent` 参数：
```bash
palaia init --agent YOUR_AGENT_NAME
```

如果检测到使用单个代理的 OpenClaw 配置，代理名称会自动检测：
```
Auto-detected agent: HAL (from OpenClaw config)
```

代理名称存储在 `.palaia/config.json` 文件中，并自动附加到所有写入和备忘录操作中。不需要环境变量。

**从单代理迁移到多代理：**
当后来添加第二个代理时，现有条目的代理名称将保持不变（“default”）。要将旧的 “default” 条目与你的命名代理关联起来：
```bash
palaia config set-alias default YOUR_NAME
```
这样，查询 `YOUR_NAME` 时也会返回标记为 “default”的条目。条目不会被重写 — 别名仅在查询时生效。`palaia doctor` 会在需要时提醒你。

**可选：设置会话实例**（对于多实例代理）：
```bash
palaia instance set YOUR_INSTANCE_NAME
```
实例是会话级别的，并为条目添加可追溯性。备忘录可以针对特定实例。

### 第二步：检查现有的内存系统（必须执行 — 不可跳过）
```bash
palaia doctor
```

在继续之前，请查看 **每个** 警告。对于 `palaia doctor` 找到的每个警告，立即提出修复建议 — 不要等待用户询问：

**HEARTBEAT.md 旧模式：**
→ 告诉用户：“你的 heartbeat 仍然使用旧的内存模式。我应该将其更新为使用 Palaia 吗？（需要一点时间，不会丢失数据）”
- 如果用户同意：更新 HEARTBEAT.md，将 `memory_search`/`memory_get`/直接文件读取替换为 `palaia query`/`palaia write` 等等
- 如果用户不同意：跳过，进入下一个警告

**检测到 Smart-Memory 技能：**
→ 告诉用户：“旧的 smart-memory 技能仍然安装着。我应该删除它吗？（只有在确认 Palaia 已经处理了你的记忆后）”
- 如果用户同意：运行 `palaia migrate <workspace-path>`，然后删除 smart-memory 技能文件夹
- 如果用户不同意：继续，但两个系统将并行运行（不推荐）

**OpenClaw 插件仍然使用内存核心：**
→ 告诉用户：“Palaia 尚未连接到 OpenClaw 的内存系统。我应该切换它吗？（需要快速重启 OpenClaw）”
- 如果用户同意：更新 OpenClaw 配置（`plugins.slots.memory = "palaia"`），然后重启 OpenClaw
- 如果用户不同意：Palaia 将独立运行（不集成 `memory_search`/`memory_get` 工具）

**仅使用 OpenAI 的链（没有本地备份）：**
→ 告诉用户：“你的搜索没有本地备份。我应该安装 fastembed 作为备用方案吗？（下载量小，不需要 GPU）”
- 如果用户同意：`pip install fastembed`，然后运行 `palaia warmup`，在 bm25 之前更新链
- 如果用户不同意：跳过（警告：“当 OpenAI 不可用时，搜索可能会降级”）

规则：
- 对于每个警告：一次只问一个问题
- 不要批量处理所有问题 — 按顺序处理
- 不要等待用户注意到并询问
- 用户回答“是”或“否”后，进入下一个警告
- 在所有警告都得到解决或用户明确拒绝之前，不要继续

### 入职对话

运行 `palaia doctor` 并查看警告后，与用户进行简短的对话。
保持简短 — 最多 3 个问题。除非用户询问，否则不要涉及技术细节。

**脚本：**

告诉用户：
“我已经为你设置了 Palaia — 你的内存现在更安全且可搜索了。
快速设置：3 个简短的问题。”

**问题 1 — 搜索质量：**

如果存在 OpenAI API 密钥，并且也检测到本地模型（sentence-transformers/fastembed/ollama）：
  → 只需确认：“我将使用你的 OpenAI 密钥和本地备份模型。设置良好。”
  → 不需要提问。

如果存在 OpenAI API 密钥，但没有安装本地模型：
  → 告诉用户：“你有 OpenAI API 密钥 — 对搜索质量很有帮助。但是如果没有本地备份，当 OpenAI 不可用时，搜索质量会显著下降。我建议安装一个小的本地模型（300MB，免费，可离线运行）。我应该这样做吗？”
  → 如果用户同意：`pip install sentence-transformers`（如果遇到 CUDA 问题：改为 `pip install fastembed` — 更轻量级，不需要 GPU），然后运行 `palaia warmup`，链设置为 openai → sentence-transformers → bm25
  → 如果用户不同意：链设置为 openai → bm25（警告：“注意：如果没有本地备份，搜索可能会失败或降级。”）

如果不存在 OpenAI 密钥，也没有安装本地模型：
  → 告诉用户：“尚未找到搜索提供者。我建议安装一个免费的本地模型（300MB）。我应该这样做吗？”
  → 如果用户同意：`pip install sentence-transformers`（如果遇到 CUDA 问题：改为 `pip install fastembed` — 更轻量级，不需要 GPU），然后运行 `palaia warmup`，链设置为 sentence-transformers → bm25
  → 如果用户不同意：仅使用 BM25（警告：“搜索将基于关键词 — 你可以以后使用 palaia detect 来改进。”）

如果不存在 OpenAI 密钥，但检测到本地模型：
  → 只需确认：“使用本地搜索模型 — 可以离线使用，不需要 API 成本。”
  → 不需要提问。

**问题 2 — 现有内存（仅在存在旧内存文件或检测到 smart-memory 时询问）：**
  询问：“你有现有的内存吗？我应该将其导入到 Palaia 中吗？”
  → 如果用户同意：运行 `palaia migrate <workspace-path>`
  → 如果用户不同意：从头开始设置（现有文件保持不变）

**问题 3 — 项目（仅在检测到多个项目文件夹或存在多个代理时询问）：**
  询问：“你处理多个项目吗？我可以为每个项目分别管理它们的记忆。”
  → 如果用户同意：简要解释：“使用 ‘palaia project create <name>’ 为每个项目创建项目。我会记住每个项目的记忆属于哪里。”
  → 如果用户不同意：跳过

**总结：**
告诉用户配置了什么 — 用一句话概括：
“完成。[搜索质量：OpenAI / 本地模型 / 基于关键词]。[迁移：导入 X 条目 / 从头开始]。[项目：已配置 / 未使用]。”

除非用户明确询问，否则不要解释命令、WAL、BM25、嵌入模型或任何技术细节。

### 第三步：迁移现有条目（最佳实践 — 现在就执行）
如果有来自早期 Palaia 版本（或初始设置）的现有条目，请运行：
```bash
palaia migrate --suggest
```
这会检查没有类型分类的条目并提出改进建议。在存储量较小时尽早执行此操作 — 随着存储量的增加，这会变得更加困难。应用合理的建议。

### 第 4a 步：检查嵌入设置（由 init 自动配置）
```bash
palaia detect
```
查看检测到的提供者和配置的链。`palaia init` 会自动检测可用的提供者
并配置最佳的嵌入链 — 通常你不需要更改任何设置。

如果链看起来不正确，或者你想更改它：
```bash
palaia config set-chain <provider1> [provider2] bm25
```

如果只显示 BM25 并且你想要语义搜索：
```bash
# fastembed — lightweight, no GPU needed, recommended for most systems
python3 -m pip install fastembed    # or: uv pip install fastembed
palaia warmup                       # pre-load model + build index
```

如果 fastembed 不可用，`sentence-transformers` 也可以使用（`python3 -m pip install sentence-transformers`），但在仅使用 CPU 的系统上速度较慢。

### 第 4b 步：预热模型
```bash
palaia warmup
```
这会预先下载嵌入模型，以便第一次搜索可以立即完成。总是在链设置完成后运行此操作。

### 第 5 步：验证设置（必须执行 — 不可跳过）
运行一个测试查询以验证语义搜索是否端到端工作：
```bash
palaia query "important context and decisions"
```
**检查：**
- 结果必须出现（不可为空）
- 响应时间应在 5 秒以内
- 如果超时或没有返回结果：检查 `palaia status` 和 `palaia detect`，在继续之前修复任何问题

然后验证 `palaia status` 是否显示索引条目（Index: N/N，而不是 0/N）。
如果在预热后索引为 0/N，运行几个查询 — 索引是在第一次查询时懒加载的。

**在验证通过之前，不要告诉用户“设置完成”。** 这只是一个假设，并不是真正的验证。

### 第 6 步：可选 — 迁移额外的内存文件（如果在第 3 步中已经完成，则可以跳过）
```bash
palaia migrate <path> --dry-run   # Preview first
palaia migrate <path>             # Then import
```
注意：如果在第 2 步中已经处理了 smart-memory 的迁移，则可以跳过此步骤，除非还有其他需要导入的来源。

### 第 7 步：将 Palaia 维护任务添加到你的 heartbeat 中（必须执行）

这是必需的。Palaia 的分级（HOT → WARM → COLD）只有在触发时才会运行。
如果没有定期维护，所有条目将永远保持 HOT 状态，搜索质量会随时间下降。

检查工作空间中是否存在 `HEARTBEAT.md` 文件（`~/.openclaw/workspace/HEARTBEAT.md`）。

**如果存在：** 在文件末尾添加以下内容（在任何最终评论之前）：

```
# TASK: Palaia Maintenance (daily + weekly)
# [INSTRUCTION for LLM]:
# Daily: run `palaia gc` — moves entries between HOT/WARM/COLD based on age and access.
# Weekly (Sunday): run `palaia gc --aggressive` — also clears COLD tier.
# Fast operation, never blocks user queries. Only run if palaia is installed (check: which palaia).
```

**如果不存在：** 使用上述内容创建 `HEARTBEAT.md` 文件。

告诉用户：“我已经在你的 heartbeat 日程中添加了一个 Palaia 维护任务。这会自动组织你的内存——你无需执行任何操作。”

## 故障排除：找不到 pip**

在某些主机上，`pip` 不能作为独立命令使用。请按以下顺序使用备用方案：

```bash
# Option 1: python3 -m pip (most reliable)
python3 -m pip install --upgrade "palaia[fastembed]"

# Option 2: uv (modern Python package manager)
uv tool install "palaia[fastembed]"

# Option 3: pipx (if installed)
pipx install "palaia[fastembed]"

# Option 4: Bootstrap pip first
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade "palaia[fastembed]"

# Option 5: Install from git directly
python3 -m pip install "palaia[fastembed] @ git+https://github.com/iret77/palaia.git"
```

> **uv 用户：** 在使用 `uv tool install` 进行升级时，始终包含 `[fastembed]` — `uv` 会在升级时删除依赖项规范中未包含的包。使用 `uv tool install palaia` 且不包含扩展包会静默卸载 fastembed。

## 故障排除：Debian/Ubuntu（PEP 668）

在基于 Debian 的系统（Debian 12+，Ubuntu 23.04+）上，pip 可能会因为 PEP 668 而失败，该规则阻止 pip 修改系统 Python 包。

使用以下方法之一：

```bash
# Option 1: User install (recommended)
python3 -m pip install --user "palaia[fastembed]"

# Option 2: Break system packages (use if you know what you're doing)
python3 -m pip install --break-system-packages "palaia[fastembed]"

# Option 3: pipx (cleanest isolation)
pipx install "palaia[fastembed]"

# Option 4: Virtual environment
python3 -m venv ~/.palaia-venv
~/.palaia-venv/bin/pip install "palaia[fastembed]"
alias palaia=~/.palaia-venv/bin/palaia
```

升级后，始终运行 `palaia doctor --fix` 以验证提供者并更新存储。

**重要提示：** 如果在升级之前安装了 sentence-transformers 或 fastembed，
请在升级后验证它们是否仍然可用：
```bash
palaia detect
```

如果缺少提供者，请重新安装它：
```bash
python3 -m pip install "palaia[sentence-transformers]"
palaia warmup
```

## 插件激活（OpenClaw 内存后端）

安装 palaia 后，将其激活为你的内存后端：

### 1. 安装 OpenClaw 插件
```bash
npm install -g @byte5ai/palaia
```

### 2. 配置 OpenClaw

**配置路径：** 在你的 OpenClaw 配置文件（`openclaw.json`）中的 `plugins.entries.palaia.config`。

> **警告：** 不要使用 `plugins.config.palaia` — 该路径不存在。
> 正确的路径是 `plugins.entries.palaia.config`。

修改你的 OpenClaw 配置文件（`openclaw.json`）以加载和激活插件：

```json
{
  "plugins": {
    "load": {
      "paths": ["<path-to-npm-global>/node_modules/@byte5ai/palaia"]
    },
    "allow": ["..existing..", "palaia"],
    "slots": {
      "memory": "palaia"
    },
    "entries": {
      "palaia": {
        "enabled": true,
        "config": {
          "workspace": "/path/to/.openclaw/workspace"
        }
      }
    }
  }
}
```

使用 `npm root -g` 查找你的 npm 全局路径。

**插件配置键**（在 `plugins.entries.palaia.config` 下）：

| 键 | 描述 |
|-----|-------------|
| `workspace` | OpenClaw 工作空间的路径（`.palaia/` 所在的位置） |

### 3. 重启 OpenClaw Gateway
配置更改需要重启 Gateway 才能生效。

### 变更内容
- `memory_search` 和 `memory_get` 工具现在会搜索 Palaia 存储，而不是 MEMORY.md 文件
- MEMORY.md 和 workspace 文件将继续作为项目上下文加载（不变）
- 所有 Palaia 功能（项目、范围、分级、语义搜索）都可以通过标准的内存工具访问

## 命令参考

### 基本内存操作
```bash
# Write a memory entry (default type: memory)
palaia write "text" [--scope private|team|public] [--project NAME] [--tags a,b] [--title "Title"] [--type memory|process|task] [--instance NAME]

# Write a task with structured fields
palaia write "fix login bug" --type task --status open --priority high --assignee Elliot --due-date 2026-04-01

# Edit an existing entry (content, metadata, task fields)
palaia edit <id> ["new content"] [--status done] [--priority high] [--tags new,tags] [--title "New Title"] [--type task]

# Search memories (semantic + keyword) with structured filters
palaia query "search term" [--project NAME] [--limit N] [--all] [--type task] [--status open] [--priority high] [--assignee NAME] [--instance NAME]

# Read a specific entry by ID
palaia get <id> [--from LINE] [--lines N]

# List entries in a tier with filters
palaia list [--tier hot|warm|cold] [--project NAME] [--type task] [--status open] [--priority high] [--assignee NAME] [--instance NAME]

# System health, active providers, and entry class breakdown
palaia status

# Suggest type assignments for untyped entries
palaia migrate --suggest
```

### 项目
项目将相关条目分组。它们是可选的 — 没有它们也可以正常工作。

```bash
# Create a project
palaia project create <name> [--description "..."] [--default-scope team]

# List all projects
palaia project list

# Show project details + entries
palaia project show <name>

# Write an entry directly to a project
palaia project write <name> "text" [--scope X] [--tags a,b] [--title "Title"]

# Search within a project only
palaia project query <name> "search term" [--limit N]

# Change the project's default scope
palaia project set-scope <name> <scope>

# Delete a project (entries are preserved, just untagged)
palaia project delete <name>
```

### 配置
```bash
# Show all settings
palaia config list

# Get/set a single value
palaia config set <key> <value>

# Set the embedding fallback chain (ordered by priority)
palaia config set-chain <provider1> [provider2] [...] bm25

# Detect available embedding providers on this system
palaia detect

# Pre-download embedding models
palaia warmup
```

### 诊断
```bash
# Check Palaia health and detect legacy systems
palaia doctor

# Show guided fix instructions for each warning
palaia doctor --fix

# Machine-readable output
palaia doctor --json
```

### 维护
```bash
# Tier rotation — moves old entries from HOT → WARM → COLD
palaia gc [--aggressive]

# Replay any interrupted writes from the write-ahead log
palaia recover
```

### 文档导入（RAG）
```bash
# Index a file, URL, or directory into the knowledge base
palaia ingest <file-or-url> [--project X] [--scope X] [--tags a,b] [--chunk-size N] [--dry-run]

# Query with RAG-formatted context (ready for LLM injection)
palaia query "question" --project X --rag
```

### 同步
```bash
# Export entries for sharing
palaia export [--project NAME] [--output DIR] [--remote GIT_URL]

# Import entries from an export
palaia import <path> [--dry-run]

# Import from other memory formats (smart-memory, flat-file, json-memory, generic-md)
palaia migrate <path> [--dry-run] [--format FORMAT] [--scope SCOPE]
```

### JSON 输出
所有命令都支持 `--json` 选项，以生成机器可读的输出：
```bash
palaia status --json
palaia query "search" --json
palaia project list --json
```

## 范围系统

每个条目都有一个可见性范围：

- **`private`** — 只有写入它的代理才能读取
- **`team`** — 同一工作空间中的所有代理都可以读取（默认）
- **`public`** — 可以导出并在工作空间之间共享

**设置默认值：**
```bash
# Global default
palaia config set default_scope <scope>

# Per-project default
palaia project set-scope <name> <scope>
```

**范围级联**（Palaia 如何决定新条目的范围）：
1. 显式的 `--scope` 标志 → 总是优先
2. 项目的默认范围 → 如果条目属于某个项目
3. 配置中的全局 `default_scope`
4. 默认情况下回退到 `team`

## 项目
- 项目是可选的，而且是附加的 — 没有它们 Palaia 也可以正常工作
- 每个项目都有自己的默认范围
- 使用 `--project NAME` 或 `palaia project write NAME` 写入条目时，都会将其分配给该项目
- 删除项目会保留其条目（只是失去项目标签）
- `palaia project show NAME` 会列出所有条目及其层级和范围

## 何时使用什么命令

| 情况 | 命令 |
|-----------|---------|
| 记住一个简单的事实 | `palaia write "..."` |
| 为特定项目记住某件事 | `palaia project write <name> "..."` |
| 创建任务/待办事项 | `palaia write "fix bug" --type task --priority high` |
| 记录流程/SOP | `palaia write "deploy steps" --type process` |
| 标记任务已完成 | `palaia edit <id> --status done` |
| 查找存储的内容 | `palaia query "..."` |
| 查找未完成的任务 | `palaia query "tasks" --type task --status open` |
| 列出高优先级任务 | `palaia list --type task --priority high` |
| 在项目中查找某件事 | `palaia project query <name> "..."` |
| 查看活动内存中的内容 | `palaia list` |
| 查看归档内存中的内容 | `palaia list --tier cold` |
| 查看系统健康状况和分类 | `palaia status` |
| 清理旧条目 | `palaia gc` |
| 索引文档或网站 | `palaia ingest <file/url> --project <name>` |
| 为旧条目提供类型建议 | `palaia migrate --suggest` |
| 在 LLM 中搜索索引文档 | `palaia query "..." --project <name> --rag` |

## 文档知识库

使用 `palaia ingest` 对外部文档进行索引 — PDF、网站、文本文件、目录。
**使用场景：**
- 用户要求你“记住”一个文档、手册或网站
- 需要搜索大量文档
- 构建特定于项目的知识库

**使用方法：**
```bash
palaia ingest document.pdf --project my-project
palaia ingest https://docs.example.com --project api-docs --scope team
palaia ingest ./docs/ --project my-project --tags documentation

palaia query "How does X work?" --project my-project --rag
```

`--rag` 标志会返回一个格式化的上下文块，可以直接插入到你的 LLM 提示中。

**PDF 支持：** 需要安装 pdfplumber — 使用命令 `pip install pdfplumber`。

**来源归属：** 每个块都会自动跟踪其来源（文件、页面、URL）。

## 错误处理

| 问题 | 应采取的措施 |
|---------|-----------|
| 嵌入提供者不可用 | 链接会自动回退到下一个提供者。检查 `palaia status` 以查看哪个提供者是激活的。 |
| 写入前的日志损坏 | 运行 `palaia recover` — 重放任何中断的写入操作。 |
| 条目似乎丢失 | 运行 `palaia recover`，然后运行 `palaia list`。检查所有层级（`--tier warm`，`--tier cold`）。 |
| 搜索没有结果 | 尝试 `palaia query "..." --all` 以包含 COLD 层级。检查 `palaia status` 以确认提供者是否激活。 |
| `.palaia` 目录丢失 | 运行 `palaia init` 以创建一个新的存储。 |

## 分级
Palaia 根据访问频率将条目分为三个层级：

- **HOT**（默认：7 天）——频繁访问，始终被搜索
- **WARM**（默认：30 天）——访问较少，但仍默认被搜索
- **COLD**——已归档，只有使用 `--all` 标志时才会被搜索

定期运行 `palaia gc`（或者让 cron 任务处理）来在不同层级之间轮换条目。`palaia gc --aggressive` 会强制更多条目降级到较低层级。

## 信息来源的统一
这是避免信息重复的最重要部分。

**项目文件（CONTEXT.md, MEMORY.md 等）= 静态事实：**
- 仓库 URL、技术栈、架构概述、当前版本
- 该项目的 Palaia 使用信息：项目名称、常见标签、范围
- 指向 Palaia 的链接：“流程：`palaia query --type process --project <name>`”

**更改很少。**永远不要将流程、检查列表或决策日志存储在这里。

**Palaia = 所有动态信息：**
- 流程和检查列表（类型：process）——可重用、可搜索、具有范围意识
- 决策和行动记录（类型：memory，标签：adr）
- 学习成果和见解（类型：memory，标签：learning）
- 任务和计划（类型：task）
- 任何会演变、需要共享或应在适当时间展示的内容

**外部问题跟踪器（GitHub Issues, Jira 等）= 错误和工单：**
- 如果项目使用了这些工具：错误、功能请求和技术工单会存储在那里
- 不要在外部跟踪器和 Palaia 任务之间重复存储相同的内容

**最佳实践：**保存具体的工作状态，而不仅仅是项目名称。**
在保存活动上下文时，要写明具体的步骤、障碍和下一步行动 — 而不是简单地写 “正在处理项目 X”。错误的做法：`palaia write "Working on PT 2.0"`。正确的做法：`palaia write "PT 2.0: testing Railway MCP integration, blocked on /mcp command timeout, next step: check logs at /var/log/railway.log" --project pt --tag active-work`。这样可以确保在不同会话和上下文切换之间保持连贯性。

**常见错误避免：**
- 将发布检查列表保存到 CONTEXT.md 中，而不是使用 `palaia write --type process`
- 将决策日志保存在 markdown 文件中，而不是 Palaia 条目中
- 在文件和 Palaia 之间重复保存任务列表
- 保存模糊的状态（如 “正在处理 X”），而不是具体的步骤、障碍和下一步行动

## 与现有内存模式的协调
当用户安装 Palaia 时，他们实际上是在告诉你：“我希望有更好的内存管理。” 这就是你的目标。你的工作是让 Palaia 实现这一承诺 — 同时不破坏现有的工作方式。

**如果你的工作空间中已经有 CONTEXT.md、MEMORY.md 或 AGENTS.md 文件，并且这些文件中的内存规则早于 Palaia：**
1. **不要与之冲突。** 这些文件是工作空间的权威配置。你不能也不应该覆盖它们。
2. **识别出冲突之处。** 仔细阅读现有的内存规则，找出它们与 Palaia 的有效使用方式之间的冲突。常见的冲突模式包括：
   - “将所有项目知识都写入 CONTEXT.md” → 流程、决策和学习成果更适合存储在 Palaia 中（可搜索、具有范围意识）
   - “将检查列表保存在 MEMORY.md 中” → 这些应该存储在 Palaia 的流程条目中
   - “每次任务后更新 CONTEXT.md” → 静态事实可以保存在 MEMORY.md 中，但动态知识应该保存在 Palaia 中
3. **向用户提出修改建议。** 解释你发现了什么，为什么 Palaia 对动态知识更有帮助，并建议他们对工作空间文件进行具体修改。不要默默地进行更改。
4. **逐步迁移。** 一次只迁移一个类别（例如，先迁移流程，然后再迁移决策）。每次迁移后，在旧位置添加一个提示：“流程现在保存在 Palaia 中：`palaia query --type process`”
5. **保留有效的内容。** CONTEXT.md 适用于静态项目概要。MEMORY.md 适用于会话启动时的快速参考。这些文件与 Palaia 相辅相成——它们的目的是互补的，而不是替代彼此。

**良好的共存方式：**
- CONTEXT.md：项目 URL、技术栈、当前版本、Palaia 项目名称和常见标签
- MEMORY.md：路由规则、代理身份、快速参考链接
- Palaia：流程、决策、学习成果、任务、任何可搜索或可共享的内容

**用户选择了 Palaia。** 尊重这一选择，将其作为动态知识的主要存储方式。但要保持务实——一个有效的混合系统比强行替换现有系统更好。**

## 迁移最佳实践
在升级到 Palaia 1.7+ 时，将现有的规划数据迁移到结构化的 Palaia 条目中：

**需要迁移的内容：**
- 路径图项目、待办事项、来自 CONTEXT.md 或 MEMORY.md 的待办任务 → `palaia write --type task --status open --priority <level>`
- 检查列表、SOP、发布流程 → `palaia write --type process`
- 无类型的现有 Palaia 条目 → 运行 `palaia migrate --suggest` 以获取建议

**迁移后：**
- 从 CONTEXT.md、MEMORY.md 或之前的任何位置删除迁移后的条目
- 用提示替换它们：“任务保存在 Palaia 中：`palaia list --type task --project <name>`**
- 这可以避免信息来源的重复

**会话身份：**
- 在会话开始时运行 `palaia instance set YOUR_INSTANCE_NAME`（例如：“Claw-Main”，“Claw-Palaia”）
- 这可以区分同一代理的不同会话中的条目
- 在查询时使用 `--instance` 标志按会话来源过滤条目
- 或者，设置 `PALAIA_INSTANCE` 环境变量（配置文件具有优先级）

**备忘录提醒：**
- 在执行 `palaia query` 和 `palaia write` 之后，Palaia 会自动检查未读的备忘录
- 如果有未读的备忘录：显示 “你有 N 条未读的备忘录。运行：palaia memo inbox”
- 这个提醒是有限制的（每小时最多一次），并在 `--json` 模式下被抑制

**最佳实践：双层消息传递（多代理设置）**
在向其他代理发送备忘录时，使用双层消息传递方式以确保可靠传递：

1. **发送备忘录**（实际的消息，持久保存）：
   ```bash
   palaia memo send AgentName "Important update about project X"
   # or broadcast to all:
   palaia memo broadcast "New process available — check palaia query --type process"
   ```

2. **发送通知**（短暂的通知，仅对活跃的会话有效）：
   通知活跃的代理会话有新的备忘录等待。这取决于平台的具体实现 — Palaia 不处理这部分，但实际操作如下：

   *OpenClaw 的示例：*
   ```python
   sessions_send(sessionKey="agent:agentname:...", 
     message="New Palaia memos waiting. Please run: palaia memo inbox")
   ```

   *其他平台：* 使用任何可用的进程间或 Webhook 机制来通知代理。

   如果无法发送活跃通知，也没关系 — CLI 会在下一次 `palaia query` 或 `palaia write` 时通知代理。

**为什么需要双层消息传递？** 备忘录是持久的信息（与平台无关）。通知只是短暂的通知（与平台相关）。如果通知失败，备忘录仍然存在。永远不要将完整的信息内容放在通知中 — 避免重复。

## 更新 Palaia 后
Palaia 有三个独立的组件。需要同时更新所有组件：
```bash
# 1. Python CLI (the main tool)
python3 -m pip install --upgrade "palaia[fastembed]"
# or: uv tool install "palaia[fastembed]"  (always include [fastembed]!)

# 2. OpenClaw plugin (memory-slot integration)
npm install -g @byte5ai/palaia@latest

# 3. SKILL.md (agent instructions — if installed via ClawHub)
clawhub update palaia

# 4. Always run after updating:
palaia doctor --fix
palaia warmup
```

**为什么需要同时更新三个组件？** pip 包是 CLI。npm 包是将 Palaia 连接到内存插件的插件。SKILL.md（通过 ClawHub）告诉代理如何使用 Palaia。如果只更新其中一个组件，其他组件可能会过时。

`palaia doctor` 会检查你的存储是否兼容，建议新功能，并处理版本更新。如果安装的版本与存储中的版本不同，Palaia 会在每次调用 CLI 时提醒你。

## 代理操作指南 — 来自生产环境的经验教训
这些是在生产环境中使用 Palaia 的代理们总结的经验。在首次查询之前，请阅读这些内容。

### 性能：预热是必需的
安装或更新后，务必运行 `palaia warmup`。如果不运行预热，**每次查询都会重新计算所有条目的嵌入信息** — 在 CPU 系统上这需要 14 秒以上的时间。预热之后，相同的查询只需不到 2 秒。预热会构建一个持久的嵌入缓存，即使在重启后也能保留。

如果查询速度慢，请检查：
1. 你是否运行了 `palaia warmup`？（如果未运行，`palaia status` 会显示 “X 条目未索引”）
2. 哪个提供者是激活的？（`palaia detect`）——在仅使用 CPU 的系统上，fastembed 的速度比 sentence-transformers 快 50 倍
3. 嵌入链是否正确配置？（`palaia config show`）——链应该首先列出你首选的提供者

### 在 CPU 系统上选择提供者很重要
- **fastembed**：每个嵌入大约需要 0.3 秒，轻量级，不需要 GPU — **推荐用于大多数系统**
- **sentence-transformers**：每个嵌入大约需要 16 秒（需要加载 PyTorch）——仅在有 GPU 的系统上使用
- 如果同时安装了这两个提供者，请明确设置链：`palaia config set-chain fastembed bm25`
- 更换提供者会使嵌入缓存失效 — 在更改链后运行 `palaia warmup`

### 分阶段写入，而不是在会话结束时一次性写入
不要将所有的学习成果一次性写入。在每个有意义的步骤之后再写入：
```bash
# After a decision
palaia write "Decided to use FastAPI over Flask — async support needed for webhook handlers" --project myproject --tag decision

# After hitting a blocker
palaia write "Redis connection pool exhausted under load — need to configure max_connections" --project myproject --tag blocker,active-work

# After resolving something
palaia write "Fixed Redis pool: set max_connections=50, added connection timeout=5s" --project myproject --tag learning
```
如果会话崩溃，知识仍然可以保留。如果在会话结束时才写入，知识就会丢失。

### 对于可重复的操作使用流程
发布检查列表、部署步骤、审查流程等，使用 `--type process` 来写入。当你写入或查询相关主题时，Palaia 会自动显示相关的流程（流程提示）。这只有在流程存在于 Palaia 中时才有效，如果流程存在于 markdown 文件中则无效。

### 标签是未来自己搜索的关键词
选择你的未来自己（或其他代理）会搜索的标签。好的标签示例：`decision`、`learning`、`blocker`、`adr`、`release`、`config`。不好的标签示例：`important`、`note`、`misc`。始终使用 `--project` 标签 — 这是跨项目设置的主要过滤方式。

### doctor 是处理问题的第一选择
遇到问题时，首先运行 `palaia doctor --fix`。它会检查版本、修复链、重建索引，并自动处理大多数问题。在任何更新后、任何配置更改后、任何错误发生后，先使用 doctor，再使用调试工具。

### 会话连续性检查
在每个会话开始时：
1. 运行 `palaia doctor` — 发现任何问题
2. 运行 `palaia query "active work"` — 从上次停止的地方继续
3. 运行 `palaia memo inbox` — 查看来自其他代理的消息

在会话结束时：
1. 写下当前的状态：具体的步骤、任何障碍、下一步行动
2. 关闭任何未完成的任务：`palaia edit <id> --status done`

## 配置键
| 键 | 默认值 | 描述 |
|-----|---------|-------------|
| `default_scope` | `team` | 新条目的默认可见性 |
| `embedding_chain` | *(自动)* | 搜索提供者的有序列表 |
| `embedding_provider` | `auto` | 旧的单一提供者设置 |
| `embedding_model` | — | 按提供者指定的模型 |
| `hot_threshold_days` | `7` | 从 HOT 级别变为 WARM 级别的天数 |
| `warm_threshold_days` | `30` | 从 WARM 级别变为 COLD 级别的天数 |
| `hot_max_entries` | `50` | HOT 级别的最大条目数量 |
| `decay_lambda` | `0.1` | 内存得分的衰减率 |

---

© 2026 byte5 GmbH — MIT 许可证