---
name: palaia
description: 用于 OpenClaw 代理的本地化、防崩溃的持久性内存。它通过语义搜索、项目管理和基于范围的访问控制机制，替代了内置的内存核心功能。
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

## 设置流程（请严格遵循以下步骤）

### 第1步：安装并初始化
```bash
pip install git+https://github.com/iret77/palaia.git
palaia init
```

### 第2步：检查现有的内存系统（必选步骤 — 请勿跳过）
```bash
palaia doctor
```

在继续之前，请仔细阅读所有警告信息。对于每个警告，需明确询问用户：

**检测到智能内存系统：**
告知用户：“我发现了一个现有的智能内存系统。Palaia将替换它。是否需要将您现有的数据迁移到Palaia中，然后停用智能内存系统？”
- 如果用户同意：运行 `palaia migrate <workspace-path>`，然后删除智能内存系统的文件夹。
- 如果用户不同意：继续使用现有系统，但两个系统将并行运行（不推荐）。

**OpenClaw内存插件仍设置为 memory-core：**
告知用户：“是否需要将OpenClaw的内存系统切换为Palaia？”
- 如果用户同意：更新OpenClaw的配置（`plugins.slots.memory = "palaia"`），然后重启OpenClaw。
- 如果用户不同意：Palaia将独立运行（不集成 `memory_search`/`memory_get` 工具）。

**HEARTBEAT.md 文件中的旧格式：**
告知用户：“您的心跳文件（HEARTBEAT.md）使用的是旧的内存命令。是否需要将其更新为使用Palaia的命令？”
- 如果用户同意：更新 HEARTBEAT.md 文件，将其中的 `memory_search`/`memory_get`/直接文件读取操作替换为 `palaia query`/`palaia write`。

**在所有警告得到解决或用户明确表示忽略之前，请勿继续下一步。**

### 上线引导对话

运行 `palaia doctor` 并查看警告信息后，与用户进行简短的交流。
对话内容尽量简洁 — 最多提3个问题。除非用户询问，否则不要涉及技术细节。

**脚本：**
告知用户：
“我已经为您配置好了Palaia — 现在您的内存数据既安全又可搜索。
快速设置：3个简单问题。”

**问题1 — 搜索质量：**
如果系统中存在OpenAI API密钥：
  询问：“是否应该使用您的OpenAI密钥来提高搜索质量？这样可以获得更好的结果？”
  → 如果用户同意：在搜索链中优先使用OpenAI。
  → 如果用户不同意：可以使用 `sentence-transformers`（如有需要可安装）或 `BM25`。

如果没有OpenAI密钥：
  询问：“是否需要安装一个本地搜索模型来提高搜索效果？它是免费的，可以离线使用，占用约300MB的空间？”
  → 如果用户同意：使用 `pip install sentence-transformers`，然后运行 `palaia warmup`。
  → 如果用户不同意：仅使用 `BM25`（告知用户：“搜索将基于关键词进行——您可以稍后自行改进”。）

**问题2 — 现有的内存数据（仅在检测到旧内存文件或智能内存系统时询问）：**
  询问：“您有现有的内存数据吗？是否需要将其导入到Palaia中？”
  → 如果用户同意：运行 `palaia migrate <workspace-path>`。
  → 如果用户不同意：保持现有数据不变。

**问题3 — 项目（仅在检测到多个项目文件夹或存在多个代理时询问）：**
  询问：“您是否处理多个项目？我可以为每个项目单独管理内存数据？”
  → 如果用户同意：简要解释：“可以使用 `palaia project create <name>` 为每个项目创建单独的存储空间。我会记录每个项目的数据存储位置。”
  → 如果用户不同意：跳过此步骤。

**总结：**
用一句话告知用户配置结果：
“已完成配置。[搜索方式：使用OpenAI / 本地模型 / 基于关键词]。[数据迁移情况：X条数据已导入 / 从头开始]。[项目情况：已配置 / 未使用]。”

除非用户询问，否则不要解释相关命令、WAL、BM25、嵌入模型或任何技术细节。

### 第3步：检查嵌入设置（由初始化自动完成）
```bash
palaia detect
```
查看检测到的提供者及配置的搜索链。`palaia init` 会自动检测可用的提供者并配置最佳的搜索链——通常无需进行任何修改。

如果搜索链配置有误或您希望更改配置：
```bash
palaia config set-chain <provider1> [provider2] bm25
```

如果仅显示了BM25且您需要语义搜索：
```bash
pip install sentence-transformers   # fast local option
palaia warmup                       # pre-load model
```

### 第4步：预热模型
```bash
palaia warmup
```
此步骤会预下载嵌入模型，以确保首次搜索时响应迅速。请在完成配置后运行此步骤。

### 第5步：可选步骤 — 迁移额外的内存文件
```bash
palaia migrate <path> --dry-run   # Preview first
palaia migrate <path>             # Then import
```
注意：如果第2步中已经处理了智能内存的迁移，请跳过此步骤，除非还有其他需要导入的数据源。

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
项目用于对相关数据进行分组。这些功能是可选的 — 即使不使用它们，系统也能正常运行。
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

### 维护工具
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
所有命令都支持 `--json` 选项，以生成机器可读的输出格式：
```bash
palaia status --json
palaia query "search" --json
palaia project list --json
```

## 数据可见性范围

每个数据条目都有相应的可见性范围：
- **`private`** — 仅写入该数据的代理可以访问
- **`team`** — 同一工作空间内的所有代理都可以访问（默认设置）
- **`public`** — 可以导出并在不同工作空间之间共享

**默认设置：**
```bash
# Global default
palaia config set default_scope <scope>

# Per-project default
palaia project set-scope <name> <scope>
```

**数据可见性的确定规则**：
1. 显式指定的 `--scope` 标志具有最高优先级。
2. 如果数据条目属于某个项目，则使用该项目的默认可见性设置。
3. 使用配置文件中的全局 `default_scope`。
4. 如果以上选项都未指定，则使用 `team` 可见性。

## 项目管理
- 项目是可选的，且对系统功能没有影响 — 即使不使用项目，Palaia也能正常工作。
- 每个项目都有其默认的可见性设置。
- 使用 `--project NAME` 或 `palaia project write NAME` 命令可以指定数据条目的项目归属。
- 删除项目时，数据条目本身不会被删除，只会失去项目标签。
- 使用 `palaia project show NAME` 可以查看该项目下的所有数据条目及其可见性级别。

## 使用建议

| 情况 | 命令 |
|---------|---------|
| 记住一个简单的事实 | `palaia write "..."` |
| 为特定项目存储数据 | `palaia project write <name> "..."` |
| 查找已存储的内容 | `palaia query "..."` |
| 在项目中查找内容 | `palaia project query <name> "..."` |
| 查看活动内存中的内容 | `palaia list` |
| 查看存档内存中的内容 | `palaia list --tier cold` |
| 检查系统状态 | `palaia status` |
| 清理旧数据条目 | `palaia gc` |

## 错误处理

| 错误类型 | 处理方法 |
|---------|-----------|
| 嵌入提供者不可用 | 系统会自动切换到下一个可用提供者。请通过 `palaia status` 查看当前激活的提供者。 |
| 写入日志损坏 | 运行 `palaia recover` 以恢复未完成的写入操作。 |
| 数据条目丢失 | 运行 `palaia recover`，然后使用 `palaia list` 检查所有数据条目（使用 `--tier warm`/`--tier cold`）。 |
| 搜索无结果 | 尝试使用 `palaia query "..." --all` 来搜索所有数据层。请通过 `palaia status` 确认提供者是否正常工作。 |
| `.palaia` 目录缺失 | 运行 `palaia init` 以创建新的数据存储目录。 |

## 数据分层机制

Palaia根据数据访问频率将数据条目分为三个层级：
- **HOT**（默认：7天）—— 高频访问的数据，始终会被搜索
- **WARM**（默认：30天）—— 较少访问的数据，但仍会被默认搜索
- **COLD** — 被归档的数据，仅在使用 `--all` 标志时才会被搜索

建议定期运行 `palaia gc`（或通过cron任务）来调整数据条目的层级。`palaia gc --aggressive` 可强制将更多数据条目降级到较低层级。

## 配置参数

| 参数 | 默认值 | 说明 |
|-----|---------|-------------|
| `default_scope` | `team` | 新数据条目的默认可见性设置 |
| `embedding_chain` | *(自动配置)* | 搜索提供者的顺序列表 |
| `embedding_provider` | `auto` | 使用传统的单一提供者 |
| `embedding_model` | — | 可根据提供者自定义模型 |
| `hot_threshold_days` | `7` | 数据从HOT层级转移到WARM层级的天数 |
| `warm_threshold_days` | `30` | 数据从WARM层级转移到COLD层级的天数 |
| `hot_max_entries` | `50` | HOT层级的最大条目数量 |
| `decay_lambda` | `0.1` | 数据条目得分的衰减率 |

---

© 2026 byte5 GmbH — MIT许可证