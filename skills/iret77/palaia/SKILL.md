---
name: palaia
description: OpenClaw代理的本地、防崩溃的持久化存储机制。该机制用语义搜索、项目管理和基于范围的访问控制功能替换了内置的内存核心（memory-core）功能。
metadata:
  openclaw:
    emoji: 🧠
    requires:
      bins: ["palaia"]
    install:
      - id: pip
        kind: pip
        package: palaia
        bins: ["palaia"]
        label: "Install Palaia (pip)"
    postInstall:
      - command: "palaia init"
        label: "Initialize Palaia store"
    plugin:
      slot: memory
      package: "@byte5ai/palaia"
---
# Palaia — 代理内存管理技能

## 设置过程中的沟通

- 在每个重要步骤完成后，向用户发送简短的状态消息。不要保持沉默。
- 如果某个步骤花费的时间超过约10秒，请说明你正在做什么：“正在安装sentence-transformers，这需要一点时间……”
- 如果发生意外情况（例如CUDA错误、提供者失败），立即解释发生了什么以及你正在采取什么措施。
- 不要批量处理所有步骤，而应在每个步骤完成后立即报告。

示例节奏：
1. “正在安装Palaia…” → [运行pip install] → “完成。正在初始化……”
2. “正在检查您的系统是否有可用的搜索提供者…” → [运行palaia doctor + detect] → “找到：[X]。有个小问题：”
3. [入职对话 — 最多3个问题]
4. “配置链…模型预热（这需要约15秒）…” → “准备就绪。”
5. “所有设置完成。这是您的设置摘要：[一句话总结]”

## 设置流程（请严格遵循）

### 第1步：安装并初始化
```bash
pip install git+https://github.com/iret77/palaia.git
palaia init
```

### 第2步：检查现有的内存系统（必选 — 不可跳过）
```bash
palaia doctor
```

在继续之前，请仔细阅读**每个**警告。对于`palaia doctor`发现的每个警告，立即提出修复建议 — 不要等待用户询问：

**HEARTBEAT.md旧模式：**
→ 告诉用户：“您的心跳系统仍然使用旧的内存模式。我应该将其更新为使用Palaia吗？（这需要一点时间，不会丢失数据）”
- 如果用户同意：更新HEARTBEAT.md，将`memory_search`/`memory_get`/直接文件读取替换为`palaia query`/`palaia write`等效命令
- 如果用户不同意：跳过此步骤，进入下一个警告

**检测到Smart-Memory技能：**
→ 告诉用户：“旧的智能内存技能仍然已安装。我应该删除它吗？（仅在确认Palaia已获取您的内存数据后进行）”
- 如果用户同意：运行`palaia migrate <workspace-path>`，然后删除smart-memory技能文件夹
- 如果用户不同意：继续操作，但两种系统将并行运行（不推荐）

**OpenClaw插件仍使用内存核心：**
→ 告诉用户：“Palaia尚未连接到OpenClaw的内存系统。我应该切换吗？（需要快速重启OpenClaw）”
- 如果用户同意：更新OpenClaw配置（`plugins.slots.memory = "palaia"`），然后重启OpenClaw
- 如果用户不同意：Palaia将独立运行（不集成`memory_search`/`memory_get`工具）

**仅使用OpenAI的链（没有本地备份）：**
→ 告诉用户：“您的搜索没有本地备份。我应该安装fastembed作为备用吗？（下载量小，不需要GPU）”
- 如果用户同意：`pip install fastembed`，然后运行`palaia warmup`，并将链配置为`openai → bm25`
- 如果用户不同意：跳过此步骤（警告：“当OpenAI不可用时，搜索性能可能会下降”）

规则：
- 对于每个警告：每次只提出一个问题
- 不要批量处理问题 — 按顺序处理
- 不要等待用户注意到并询问
- 用户回答“是”或“否”后，进入下一个警告
- 在所有警告都得到解决或被用户明确拒绝后，再继续进行下一步

**在所有警告得到解决或被用户明确拒绝之前，不要继续进行设置。**

### 入职对话

运行`palaia doctor`并查看警告后，与用户进行简短的对话。
保持对话简短 — 最多3个问题。除非用户询问，否则不要涉及技术细节。

**脚本：**

告诉用户：
“我已经为您设置了Palaia — 现在您的内存数据既安全又可搜索。
快速设置：3个简短的问题。”

**问题1 — 搜索质量：**

如果存在OpenAI API密钥，并且也检测到了本地模型（sentence-transformers/fastembed/ollama）：
  → 仅确认：“我将使用您的OpenAI密钥和本地备份模型。设置完成。”
  → 无需提问。

如果存在OpenAI API密钥，但没有安装本地模型：
  → 告诉用户：“您有OpenAI API密钥 — 对搜索质量很有帮助。但是如果没有本地备份，当OpenAI不可用时，搜索质量会显著下降。我建议安装一个小的本地模型（300MB，免费，可离线运行）。您想这样做吗？”
  → 如果用户同意：`pip install sentence-transformers`（如果遇到CUDA问题：改用`pip install fastembed` — 更轻量级，不需要GPU），然后运行`palaia warmup`，并将链配置为`openai → bm25`
  → 如果用户不同意：将链配置为`openai → bm25`（警告：“注意：如果没有本地备份，搜索可能会失败或性能下降。”）

如果既没有OpenAI密钥也没有本地模型：
  → 告诉用户：“尚未找到搜索提供者。我建议安装一个免费的本地模型（300MB）。您想这样做吗？”
  → 如果用户同意：`pip install sentence-transformers`（如果遇到CUDA问题：改用`pip install fastembed` — 更轻量级，不需要GPU），然后运行`palaia warmup`，并将链配置为`sentence-transformers → bm25`
  → 如果用户不同意：仅使用BM25（警告：“搜索将基于关键词进行 — 您以后可以使用palaia detect来改进。”）

如果不存在OpenAI密钥，但检测到了本地模型：
  → 仅确认：“使用本地搜索模型 — 可以离线使用，无需API费用。”
  → 无需提问。

**问题2 — 现有的内存（仅在存在旧内存文件或检测到智能内存时提出）：**
  询问：“您有现有的内存数据吗？我应该将其导入到Palaia中吗？”
  → 如果用户同意：运行`palaia migrate <workspace-path>`
  → 如果用户不同意：从头开始设置（现有文件保持不变）

**问题3 — 项目（仅在检测到多个项目文件夹或存在多个代理时提出）：**
  询问：“您是否处理多个项目？我可以分别为它们管理内存数据。”
  → 如果用户同意：简要解释：“使用`palaia project create <name>`为每个项目创建单独的内存空间。我会记住每个内存数据属于哪个项目。”
  → 如果用户不同意：跳过此步骤

**总结：**
告诉用户配置了哪些内容 — 用一句话概括：
“完成。[搜索质量：使用OpenAI / 本地模型 / 仅基于关键词]。[迁移：导入X条记录 / 从头开始]。[项目：已配置 / 未使用]。”

除非用户明确询问，否则不要解释命令、WAL、BM25、嵌入模型或任何技术细节。

### 第3步：检查嵌入设置（由初始化自动配置）
```bash
palaia detect
```
查看检测到的提供者和配置的链。`palaia init`会自动检测可用的提供者
并配置最佳的嵌入链 — 通常您不需要进行任何更改。

如果链的配置看起来不正确，或者您希望更改它：
```bash
palaia config set-chain <provider1> [provider2] bm25
```

如果仅显示BM25并且您需要语义搜索：
```bash
pip install sentence-transformers   # Recommended for most systems
palaia warmup                       # pre-load model
```

如果`sentence-transformers`失败或需要CUDA：改用`fastembed`（`pip install fastembed`） — 更轻量级，不需要GPU。

### 第4步：预热模型
```bash
palaia warmup
```
此步骤会预下载嵌入模型，以便首次搜索时能够立即响应。总是在链设置完成后运行此步骤。

### 第5步：可选 — 迁移额外的内存文件
```bash
palaia migrate <path> --dry-run   # Preview first
palaia migrate <path>             # Then import
```
注意：如果在第2步中已经处理了智能内存的迁移，请跳过此步骤，除非还有其他需要导入的数据源。

### 第6步：将Palaia维护任务添加到您的心跳系统中（强制要求）

这是必需的。Palaia的分层系统（HOT → WARM → COLD）只有在被触发时才会运行。
如果不定期进行维护，所有条目将永久保持为HOT状态，搜索质量会随时间下降。

检查工作空间中是否存在`HEARTBEAT.md`文件（路径：`~/.openclaw/workspace/HEARTBEAT.md`）。

**如果存在：**在文件末尾添加以下内容：
```
# TASK: Palaia Maintenance (daily + weekly)
# [INSTRUCTION for LLM]:
# Daily: run `palaia gc` — moves entries between HOT/WARM/COLD based on age and access.
# Weekly (Sunday): run `palaia gc --aggressive` — also clears COLD tier.
# Fast operation, never blocks user queries. Only run if palaia is installed (check: which palaia).
```

**如果不存在：**使用上述内容创建`HEARTBEAT.md`文件。

告诉用户：“我已经将Palaia的维护任务添加到了您的心跳系统调度中。这会自动整理您的内存数据 — 您无需执行任何操作。”

## 插件激活（OpenClaw内存后端）

安装palaia后，将其激活为您的内存后端：

### 1. 安装OpenClaw插件
```bash
npm install -g @byte5ai/palaia
```

### 2. 配置OpenClaw
修改OpenClaw的配置文件（`openclaw.json`）以加载并激活插件：
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
      "palaia": { "enabled": true }
    }
  }
}
```

使用以下命令查找npm全局路径：`npm root -g`

### 3. 重启OpenClaw Gateway
配置更改需要重启Gateway才能生效。

**更改内容：**
- `memory_search`和`memory_get`工具现在会从Palaia存储中搜索数据，而不是从MEMORY.md文件中搜索
- MEMORY.md和工作空间文件仍会作为项目上下文被加载（保持不变）
- 所有Palaia功能（项目、范围、分层、语义搜索）都可以通过标准的内存工具访问

## 命令参考

### 基本内存操作
```bash
# Write a memory entry
palaia write "text" [--scope private|team|public] [--project NAME] [--tags a,b] [--title "Title"]

# Search memories (semantic + keyword)
palaia query "search term" [--project NAME] [--limit N] [--all]

# Read a specific entry by ID
palaia get <id> [--from LINE] [--lines N]

# List entries in a tier
palaia list [--tier hot|warm|cold] [--project NAME]

# System health and active providers
palaia status
```

### 项目
项目用于分组相关条目。这些功能是可选的 — 没有它们也可以正常使用。

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

### JSON输出
所有命令都支持`--json`选项，以生成机器可读的输出：
```bash
palaia status --json
palaia query "search" --json
palaia project list --json
```

## 范围系统

每个条目都有一个可见性范围：
- **`private`** — 仅写入该条目的代理可以读取
- **`team`** — 同一工作空间中的所有代理都可以读取（默认）
- **`public`** — 可以导出并在不同工作空间之间共享

**默认设置：**
```bash
# Global default
palaia config set default_scope <scope>

# Per-project default
palaia project set-scope <name> <scope>
```

**范围级联**（Palaia如何确定新条目的范围）：
1. 显式的`--scope`标志优先
2. 项目的默认范围
3. 配置中的全局`default_scope`
4. 如果没有指定，则使用`team`范围

## 项目
- 项目是可选的，且纯追加性质 — 没有项目也可以正常使用Palaia
- 每个项目都有自己的默认范围
- 使用`--project NAME`或`palaia project write NAME`命令可以为项目分配范围
- 删除项目不会删除其中的条目，只是会移除项目的标签
- `palaia project show NAME`可以列出所有条目及其范围和层级

## 使用场景及对应命令

| 情况 | 命令 |
|---------|---------|
| 记住一个简单的事实 | `palaia write "..."` |
| 为特定项目记住某件事 | `palaia project write <name> "..."` |
| 查找存储的内容 | `palaia query "..."` |
| 在项目中查找内容 | `palaia project query <name> "..."` |
| 查看活动内存中的内容 | `palaia list` |
| 查看归档内存中的内容 | `palaia list --tier cold` |
| 检查系统状态 | `palaia status` |
| 清理旧条目 | `palaia gc` |
| 索引文档或网站 | `palaia ingest <file/url> --project <name>` |
| 在LLM上下文中搜索索引文档 | `palaia query "..." --project <name> --rag` |

## 文档知识库

使用`palaia ingest`来索引外部文档 — PDF、网站、文本文件、目录。
索引后的内容会被分块处理、嵌入并作为常规条目存储（可以像内存数据一样进行搜索）。

**使用场景：**
- 用户请求您“记住”某个文档、手动输入的内容或网站
- 需要搜索大量文档
- 构建特定项目的知识库

**使用方法：**
```bash
palaia ingest document.pdf --project my-project
palaia ingest https://docs.example.com --project api-docs --scope team
palaia ingest ./docs/ --project my-project --tags documentation

palaia query "How does X work?" --project my-project --rag
```

`--rag`标志返回一个格式化的上下文块，可以直接插入到您的LLM提示中。

**PDF支持：**需要安装`pdfplumber`插件：`pip install pdfplumber`

**来源归属：**每个数据块都会自动记录其来源（文件、页面、URL）。

## 错误处理

| 问题 | 处理方法 |
|---------|-----------|
| 嵌入提供者不可用 | 系统会自动切换到下一个可用提供者。查看`palaia status`以确定当前使用的提供者。 |
| 写入日志损坏 | 运行`palaia recover`以恢复中断的写入操作。 |
| 条目似乎丢失 | 运行`palaia recover`，然后运行`palaia list`。检查所有层级（`--tier warm`、`--tier cold`）。 |
| 搜索没有结果 | 尝试`palaia query "..." --all`以包含COLD层级的条目。查看`palaia status`以确认提供者是否正常运行。 |
| `.palaia`目录缺失 | 运行`palaia init`以创建一个新的存储目录。 |

## 分层系统

Palaia根据访问频率将条目分为三个层级：
- **HOT**（默认：7天） — 频繁访问，始终可搜索
- **WARM**（默认：30天） — 较少访问，但仍会默认被搜索
- **COLD** — 已归档，仅在使用`--all`标志时才会被搜索

定期运行`palaia gc`（或让cron任务自动执行）来轮换条目的层级。`palaia gc --aggressive`会强制将更多条目降级到较低层级。

## 更新Palaia后

更新后务必运行`palaia doctor`。它会检查您的存储系统是否兼容，推荐新功能（如项目或嵌入链的改进），并处理版本更新。如果安装的版本与存储系统版本不同，Palaia会在每次通过CLI调用时自动发出警告，直到您运行`palaia doctor`为止。
```bash
pip install --upgrade palaia
palaia doctor --fix
```

## 配置键

| 键 | 默认值 | 描述 |
|-----|---------|-------------|
| `default_scope` | `team` | 新条目的默认可见范围 |
| `embedding_chain` | *(自动设置)* | 可用的搜索提供者列表 |
| `embedding_provider` | `auto` | 传统的单一提供者设置 |
| `embedding_model` | — | 可根据提供者自定义模型 |
| `hot_threshold_days` | `7` | 条目从HOT层级转移到WARM层级的天数 |
| `warm_threshold_days` | `30` | 条目从WARM层级转移到COLD层级的天数 |
| `hot_max_entries` | `50` | HOT层级的最大条目数量 |
| `decay_lambda` | `0.1` | 条目评分的衰减率 |

---

© 2026 byte5 GmbH — MIT许可证