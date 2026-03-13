---
name: reclaw
description: "在访问内存、记录信息、搜索之前的上下文或管理主题时使用。"
read_when:
  - You need to find something from a previous session
  - You want to record a decision, fact, task, or question
  - You're asked about what you remember or know
  - You need to check or update the subject registry
metadata:
  openclaw:
    homepage: https://github.com/maxpetretta/reclaw
    requires:
      bins:
        - openclaw
---
# Reclaw内存系统

Reclaw是一个仅支持追加操作的日志系统，用于替换每日生成的内存文件。它假设当前的OpenClaw环境已经安装了Reclaw插件。所有内存数据都以结构化条目的形式存储在`log.jsonl`文件中。数据提取会在会话结束时自动完成——用户无需直接写入日志。你的任务是在对话中清晰地表达信息，以便提取机制能够捕获这些数据。

## 内存工作原理

1. **MEMORY.md**文件会在每个会话开始时自动加载。其中包含手动输入的内容（如目标、偏好设置）以及每晚自动生成的Reclaw内存快照。
2. 每次会话数据提取完成后，会话摘要会被写入`MEMORY.md`文件中。
3. 与主题相关的Markdown文件会被生成并存储在`~/.openclaw/reclaw/memory/`目录下，这样OpenClaw就可以通过其内置的Markdown索引功能来语义化地搜索日志内容。
4. 当Reclaw插件在当前OpenClaw环境中被注册后，`memory_search`功能可以根据关键词、类型、主题或状态来查找日志条目；它可以从`MEMORY.md`文件以及生成的主题相关文件中获取所需信息。
5. 当Reclaw插件被注册后，`memory_get`功能可以通过ID检索特定条目、读取`MEMORY.md`文件，或者在需要时获取整个会话的记录。

请从现有的基础功能（步骤1-3）开始使用Reclaw。只有在需要特定信息时才使用相关工具。

## 条目类型

| 类型 | 捕获的内容 | 关键细节 |
|---|---|---|
| `task` | 需要执行的操作事项 | 包含状态信息（`open`或`done`） |
| `fact` | 与用户相关的具体信息 | 偏好设置、事件记录、观察结果、里程碑 |
| `decision` | 带有原因的决策 | 使用`detail`字段来说明决策的依据 |
| `question` | 未解决的问题 | 通常会通过后续关于同一主题的条目来解决 |
| `session_summary` | 会话的结束状态 | 每个会话对应一个摘要，总结当前正在进行的工作 |

## 主题

除了`session_summary`类型的条目外，所有条目都有一个`subject`字段（采用kebab-case格式，例如`auth-migration`或`reclaw`）。这些主题会被记录在一个注册表中，并根据类型分为`project`、`person`、`system`或`topic`（默认值）。

在讨论新内容时，请使用明确的kebab-case格式的名称。如果系统尚未记录某个主题，提取机制会自动创建该主题。

### 使用`memory_search`

`memory_search`功能结合了结构化的日志过滤规则、关键词搜索以及对`MEMORY.md`文件和生成的主题相关文件的语义搜索。

### 使用`memory_get`

`memory_get`功能提供了三种查找方式，具体取决于`path`参数的值：

### Markdown投影文件

Reclaw为每个主题在`~/.openclaw/reclaw/memory/`目录下生成一个Markdown文件。这些文件是从`log.jsonl`中提取的，目的是为了让OpenClaw的内置Markdown索引器能够语义化地搜索日志内容：
- 这些文件属于生成后的输出结果，切勿手动修改。
- 成功的实时数据提取会自动更新相关主题的投影文件。
- 成功的非测试性数据导入也会自动更新所有投影文件。
- 如果索引内容过时，可以使用`openclaw reclaw projection refresh`命令重新生成索引。

### 使用`memory_get`的三种查找模式

通过`path`参数的不同值，`memory_get`提供了三种不同的查找方式：

### 记录的使用频率

每次通过ID读取条目时，该条目的使用频率会增加，这有助于它在每晚生成的内存快照中持续被保留。

### 引用

在对话中引用之前的事件时，使用`[<12个字符的ID>]`的格式（例如`[r7Wp3nKx_mZe]`）。这种引用格式会被用于统计条目的使用频率——被引用的条目更有可能出现在未来的内存快照中。

### 更正与更新

日志系统仅支持追加操作。要更正错误：
- 在对话中明确说明更正内容，系统会为该主题生成新的条目。
- 要标记任务已完成，需要明确说明；系统会生成一个状态为`done`的新`task`条目。
- 要回答问题，需要讨论问题的解决方式；系统会将解决方案记录为`fact`或`decision`类型的条目。

旧条目永远不会被修改。当前的状态是通过按时间顺序读取相关主题的条目来重建的。

### 数据筛选规则

只有与用户直接相关的内容才会被记录在日志中。请问自己：“了解这个人是否真的需要知道这些信息？”如果一个通用的AI模型能够在没有用户上下文的情况下生成这些内容，那么这些信息就不应该被记录在日志中。日志中不应包含通用知识、依赖关系列表或重复性的内容。

### CLI命令

（具体CLI命令内容请参见````bash
# Recent log entries
openclaw reclaw log
openclaw reclaw log --type decision --subject auth-migration --limit 10

# Search with filters
openclaw reclaw search "webhook"
openclaw reclaw search --type task --status open
openclaw reclaw search --subject auth-migration --from 2026-02-01 --to 2026-03-01

# Trace a subject's chronological history
openclaw reclaw trace
openclaw reclaw trace --subject auth-migration
openclaw reclaw trace <entry-id>

# Subject management
openclaw reclaw subjects list
openclaw reclaw subjects add <slug> --type <project|person|system|topic>
openclaw reclaw subjects rename <old-slug> <new-slug>

# Refresh generated subject markdown projections
openclaw reclaw projection refresh
openclaw reclaw projection list

# Regenerate the MEMORY.md memory snapshot now
openclaw reclaw snapshot refresh

# Force-refresh MEMORY.md session summary block from log
openclaw reclaw summary refresh

# Import historical conversations
openclaw reclaw import <chatgpt|claude|grok|openclaw> <file>
openclaw reclaw import status
openclaw reclaw import resume <jobId>

# Setup
openclaw reclaw init
openclaw reclaw verify
openclaw reclaw uninstall
````）