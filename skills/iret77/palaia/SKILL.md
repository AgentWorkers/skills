---
name: palaia
description: 专为 OpenClaw 代理设计的本地化、防崩溃的持久性存储解决方案。该方案通过语义搜索、项目管理和基于范围的访问控制机制，替代了原有的内置内存核心功能。
metadata:
  openclaw:
    emoji: 📦
    requires:
      bins: ["python3"]
    install:
      - id: pip
        kind: shell
        command: "pip install git+https://github.com/iret77/palaia.git"
        bins: ["palaia"]
        label: "Install Palaia"
---
# Palaia — 代理内存管理技能

## 设置过程中的沟通

- 在每个重要步骤完成后，向用户发送简短的状态消息。不要保持沉默。
- 如果某个步骤耗时超过约10秒，请说明你正在做什么：“正在安装sentence-transformers，这需要一点时间……”
- 如果发生意外情况（例如CUDA错误、提供者失败），请立即解释发生了什么以及你正在采取的措施。
- 不要批量处理所有步骤，而应在每个步骤完成后立即报告。

示例节奏：
1. “正在安装Palaia…” → [运行pip install] → “完成。正在初始化……”
2. “正在检查系统中可用的搜索提供者…” → [运行palaia doctor + detect] → “找到：[X]。有个小问题：”
3. [入职对话 — 最多3个问题]
4. “正在配置链……模型预热（这需要约15秒）…” → “准备就绪。”
5. “全部设置完成。以下是您的设置概况：[一句话总结]”

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

在继续之前，请仔细阅读**每个**警告信息。对于`palaia doctor`发现的每个警告，立即提出修复建议 — 不要等待用户询问：

**HEARTBEAT.md旧版模式：**
→ 告诉用户：“您的心跳系统仍然使用旧的内存模式。是否需要更新为使用Palaia？（这需要一点时间，数据不会丢失）”
- 如果用户同意：更新HEARTBEAT.md文件，将`memory_search`/`memory_get`/直接文件读取替换为`palaia query`/`palaia write`等对应功能
- 如果用户不同意：跳过此步骤，进入下一个警告

**检测到Smart-Memory技能：**
→ 告诉用户：“旧的Smart-Memory技能仍然已安装。是否需要将其移除？（仅在确认Palaia已接管您的内存后进行）”
- 如果用户同意：运行`palaia migrate <workspace-path>`，然后删除Smart-Memory技能文件夹
- 如果用户不同意：继续使用，但两个系统将并行运行（不推荐）

**OpenClaw插件仍使用旧的内存核心：**
→ 告诉用户：“Palaia尚未连接到OpenClaw的内存系统。是否需要切换？（需要快速重启OpenClaw）”
- 如果用户同意：更新OpenClaw配置（`plugins.slots.memory = "palaia"`），然后重启OpenClaw
- 如果用户不同意：Palaia将独立运行（不集成`memory_search`/`memory_get`工具）

**仅使用OpenAI的搜索链（没有本地备份）：**
→ 告诉用户：“您的搜索没有本地备份。是否需要安装fastembed作为备用方案？（下载量小，无需GPU）”
- 如果用户同意：`pip install fastembed`，然后运行`palaia warmup`，并将搜索链更新为包含fastembed的顺序：bm25
- 如果用户不同意：跳过此步骤（警告：“当OpenAI不可用时，搜索性能可能会下降”）

**规则：**
- 对于每个警告，每次只提出一个问题
- 不要批量处理问题 — 按顺序逐一处理
- 不要等待用户主动询问
- 用户回答“是”或“否”后，进入下一个警告
- 在所有警告都被解决或用户明确拒绝后，再继续下一步

**入职对话**

运行`palaia doctor`并查看警告信息后，与用户进行简短的对话。
对话时间控制在3个问题以内。除非用户询问，否则不要涉及技术细节。

**脚本：**

告诉用户：
“我已经为您配置好了Palaia — 现在您的内存既安全又可搜索。
快速设置：3个简单问题。”

**问题1 — 搜索质量：**

- 如果存在OpenAI API密钥，并且检测到本地模型（sentence-transformers/fastembed/ollama）：
  → 仅确认：“我将使用您的OpenAI密钥和本地模型。设置完成。”
  → 无需额外问题。

- 如果存在OpenAI API密钥，但没有安装本地模型：
  → 告诉用户：“您有OpenAI API密钥 — 对搜索质量很有帮助。但没有本地备份的话，当OpenAI不可用时，搜索质量会显著下降。我建议安装一个免费的本地模型（300MB，可离线运行）。是否需要安装？”
  → 如果用户同意：`pip install sentence-transformers`（如果遇到CUDA问题：改用`pip install fastembed` — 更轻量级，无需GPU），然后运行`palaia warmup`，并将搜索链设置为`openai → sentence-transformers → bm25`
  → 如果用户不同意：搜索链设置为`openai → bm25`（警告：“注意：如果没有本地备份，搜索可能会失败或性能下降。”）

- 如果没有OpenAI密钥且没有安装本地模型：
  → 告诉用户：“尚未找到搜索提供者。我建议安装一个免费的本地模型（300MB）。是否需要安装？”
  → 如果用户同意：`pip install sentence-transformers`（如果遇到CUDA问题：改用`pip install fastembed` — 更轻量级，无需GPU），然后运行`palaia warmup`，并将搜索链设置为`sentence-transformers → bm25`
  → 如果用户不同意：仅使用BM25（警告：“搜索将基于关键词进行 — 您以后可以使用palaia detect来改进。”）

- 如果没有OpenAI密钥但检测到本地模型：
  → 仅确认：“使用本地搜索模型 — 可离线使用，无需API费用。”
  → 无需额外问题。

**问题2 — 现有的内存（仅在存在旧版内存文件或检测到Smart-Memory时询问）：**
  询问：“您有现有的内存数据吗？是否需要将其导入到Palaia中？”
  → 如果用户同意：运行`palaia migrate <workspace-path>`
  → 如果用户不同意：从头开始设置（现有文件保持不变）

**问题3 — 项目（仅在检测到多个项目文件夹或存在多个代理时询问）：**
  询问：“您是否处理多个项目？我可以为每个项目单独管理内存数据。”
  → 如果用户同意：简要解释：“使用`palaia project create <名称>`为每个项目创建单独的存储空间。我会记录每个项目的内存数据。”
  → 如果用户不同意：跳过此步骤

**总结：**
向用户简要说明配置情况：
“完成。[搜索质量：使用OpenAI / 本地模型 / 仅基于关键词]。[迁移情况：导入X条记录 / 从头开始]。[项目状态：已配置 / 未使用]。”

除非用户特别询问，否则不要解释命令、WAL、BM25、嵌入模型或任何技术细节。

### 第3步：检查嵌入设置（由初始化自动完成）
```bash
palaia detect
```
查看检测到的提供者以及配置的搜索链。`palaia init`会自动检测可用的提供者并配置最佳的搜索链 — 通常无需进行任何更改。

如果搜索链配置有误或您希望更改：
```bash
palaia config set-chain <provider1> [provider2] bm25
```

- 如果仅显示BM25且您需要语义搜索：
```bash
pip install sentence-transformers   # Recommended for most systems
palaia warmup                       # pre-load model
```

- 如果`sentence-transformers`失败或需要CUDA支持：改用`fastembed`（`pip install fastembed`） — 更轻量级，无需GPU。

### 第4步：预热模型
```bash
palaia warmup
```
此步骤会预下载嵌入模型，以便首次搜索能够即时完成。请在完成链配置后运行此步骤。

### 第5步：可选 — 迁移额外的内存文件
```bash
palaia migrate <path> --dry-run   # Preview first
palaia migrate <path>             # Then import
```
注意：如果在第2步中已经处理了Smart-Memory的迁移，请跳过此步骤，除非还有其他需要导入的数据源。

### 第6步：将Palaia维护任务添加到您的心跳系统中（必选）

这是必需的操作。Palaia的内存管理功能（HOT → WARM → COLD）仅在触发时才会运行。
如果不定期进行维护，所有记录将永久保持在HOT状态，导致搜索质量逐渐下降。

检查工作空间中是否存在`HEARTBEAT.md`文件（路径：`~/.openclaw/workspace/HEARTBEAT.md`）。

**如果文件存在：** 在文件末尾添加以下内容：
```
# TASK: Palaia Maintenance (daily + weekly)
# [INSTRUCTION for LLM]:
# Daily: run `palaia gc` — moves entries between HOT/WARM/COLD based on age and access.
# Weekly (Sunday): run `palaia gc --aggressive` — also clears COLD tier.
# Fast operation, never blocks user queries. Only run if palaia is installed (check: which palaia).
```

**如果文件不存在：** 使用上述内容创建`HEARTBEAT.md`文件。

告诉用户：“我已经将Palaia的维护任务添加到了您的心跳系统调度中。这会自动整理您的内存数据 — 您无需任何操作。”

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

### 项目管理
项目用于分组相关记录。这些功能是可选的 — 即使没有它们，系统也能正常工作。
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

### 配置设置
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

### 诊断工具
```bash
# Check Palaia health and detect legacy systems
palaia doctor

# Show guided fix instructions for each warning
palaia doctor --fix

# Machine-readable output
palaia doctor --json
```

### 维护管理
```bash
# Tier rotation — moves old entries from HOT → WARM → COLD
palaia gc [--aggressive]

# Replay any interrupted writes from the write-ahead log
palaia recover
```

### 数据同步
```bash
# Export entries for sharing
palaia export [--project NAME] [--output DIR] [--remote GIT_URL]

# Import entries from an export
palaia import <path> [--dry-run]

# Import from other memory formats (smart-memory, flat-file, json-memory, generic-md)
palaia migrate <path> [--dry-run] [--format FORMAT] [--scope SCOPE]
```

### JSON输出
所有命令都支持`--json`选项，以生成机器可读的输出格式：
```bash
palaia status --json
palaia query "search" --json
palaia project list --json
```

## 数据可见性范围

每个记录都有一个可见性范围：
- **`private`** — 仅写入记录的代理可以读取
- **`team`** — 同一工作空间内的所有代理都可以读取（默认）
- **`public`** — 可以导出并在不同工作空间之间共享

**默认设置：**
```bash
# Global default
palaia config set default_scope <scope>

# Per-project default
palaia project set-scope <name> <scope>
```

**范围确定规则**（Palaia如何确定新记录的可见性范围）：
1. 显式的`--scope`参数优先
2. 如果记录属于某个项目，则使用该项目的默认范围
3. 从配置文件中读取全局`default_scope`
4. 如果以上方法都不适用，则默认使用`team`范围

## 项目管理

- 项目是可选的，且对系统功能没有影响 — 即使没有项目，Palaia也能正常工作
- 每个项目都有自己的默认可见性范围
- 使用`--project NAME`或`palaia project write NAME`命令可以为项目分配可见性
- 删除项目不会影响其中记录的内容（记录仅会失去项目标签）
- `palaia project show NAME`命令可以列出所有记录及其可见性范围

## 使用命令的推荐场景

| 情况 | 建议使用的命令 |
|-----------|---------|
| 记住一个简单的事实 | `palaia write "..."` |
| 为特定项目存储信息 | `palaia project write <名称> "..."` |
| 查找已存储的内容 | `palaia query "..."` |
| 在项目中查找内容 | `palaia project query <名称> "..."` |
| 检查活动内存中的内容 | `palaia list` |
| 检查归档内存中的内容 | `palaia list --tier cold` |
| 查看系统状态 | `palaia status` |
| 清理旧记录 | `palaia gc` |

## 错误处理

| 错误类型 | 处理方法 |
|---------|-----------|
| 嵌入提供者不可用 | 系统会自动切换到下一个可用提供者。请通过`palaia status`查看当前使用的提供者。 |
| 写入日志损坏 | 运行`palaia recover`以恢复中断的写入操作。 |
| 记录似乎丢失 | 运行`palaia recover`，然后运行`palaia list`。检查所有存储层（`--tier warm`、`--tier cold`）。 |
| 搜索无结果 | 尝试`palaia query "..." --all`以包含COLD层的记录。通过`palaia status`确认提供者是否正常运行。 |
| `.palaia`目录缺失 | 运行`palaia init`以创建新的存储目录。 |

## 数据分层机制

Palaia根据访问频率将记录分为三个层级：
- **HOT**（默认：7天） — 频繁访问，始终可搜索
- **WARM**（默认：30天） — 较少访问，但仍会默认被搜索
- **COLD** — 已归档，仅通过`--all`参数可搜索

定期运行`palaia gc`（或使用cron任务）来调整记录的层级。`palaia gc --aggressive`命令会强制将更多记录降级到较低层级。

## 配置参数

| 参数 | 默认值 | 说明 |
|-----|---------|-------------|
| `default_scope` | `team` | 新记录的默认可见性设置 |
| `embedding_chain` | *(自动)* | 搜索提供者的顺序列表 |
| `embedding_provider` | `auto` | 旧版的单个提供者设置 |
| `embedding_model` | — | 可根据提供者自定义模型 |
| `hot_threshold_days` | `7` | 从HOT层级降级到WARM层的时间 |
| `warm_threshold_days` | `30` | 从WARM层级降级到COLD层的时间 |
| `hot_max_entries` | `50` | HOT层中的最大记录数量 |
| `decay_lambda` | `0.1` | 记录得分的衰减率 |

---

© 2026 byte5 GmbH — MIT许可证