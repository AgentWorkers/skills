---
name: reclaw
description: "在访问内存、记录信息、搜索之前的上下文或管理主题时使用。"
read_when:
  - You need to find something from a previous session
  - You want to record a decision, fact, task, or question
  - You're asked about what you remember or know
  - You need to check or update the subject registry
---
# Reclaw内存系统

Reclaw是一个只支持追加操作的日志系统，用于替代每日生成的内存文件。所有内存数据都以结构化条目的形式存储在`log.jsonl`文件中。数据提取会在会话结束时自动完成——用户无需直接写入日志。你的任务是在对话中清晰地表达信息，以便提取工具能够捕获这些数据。

## 内存工作原理

1. **MEMORY.md**文件会在每个会话开始时自动加载。其中包含手动输入的内容（如目标、偏好设置）以及每晚更新的一次Reclaw内存快照。
2. 每次会话结束后，会话的详细信息会被写入到`MEMORY.md`文件中。
3. `memory_search`功能可以根据关键词、类型、主题或状态来查找日志条目。
4. `memory_get`功能可以通过ID检索特定条目，也可以读取`MEMORY.md`文件或获取整个会话的记录。

请从已有的信息（步骤1-2）开始使用Reclaw系统。只有在需要特定功能时才使用相关工具。

## 条目类型

| 类型 | 捕获的内容 | 关键细节 |
|---|---|---|
| `task` | 需要执行的操作事项、后续任务 | 包含状态字段`status`（`open`或`done`） |
| `fact` | 与用户相关的信息（如偏好设置、事件、观察结果、里程碑） |
| `decision` | 带有原因的决策 | 使用`detail`字段记录决策的依据 |
| `question` | 未解决的疑问 | 通常会通过后续关于同一主题的条目得到解答 |
| `handoff` | 会话的结束状态 | 每个会话对应一条记录，总结当前正在进行的工作 |

## 主题

除了会话结束状态相关的条目外，所有条目都有一个`subject`字段，该字段采用Kebab-case格式（例如`auth-migration`或`reclaw`）。主题信息会被记录在一个注册表中，其类型可以是`project`、`person`、`system`或`topic`（默认值）。

在讨论新内容时，请使用明确的Kebab-case格式的标签。系统会自动创建尚未记录的主题。如需手动管理主题，可以参考以下代码示例：

```bash
# List all subjects
openclaw reclaw subjects list

# Add a subject with a type
openclaw reclaw subjects add auth-migration --type project
openclaw reclaw subjects add alice-chen --type person

# Rename a subject (updates registry and all log entries)
openclaw reclaw subjects rename old-slug new-slug
```

## 使用`memory_search`

`memory_search`功能结合了结构化的日志过滤规则和基于关键词的搜索机制。

```
# Keyword search
memory_search({"query": "webhook retries"})

# Structured filters
memory_search({"type": "decision", "subject": "auth-migration"})
memory_search({"type": "task", "status": "open"})
memory_search({"type": "question"})

# Combined
memory_search({"query": "backoff", "type": "fact", "subject": "auth-migration"})
```

使用`memory_search`时，至少需要提供`query`、`type`、`subject`或`status`中的一个参数。

## 使用`memory_get`

`memory_get`提供三种查找方式，具体取决于`path`参数的值：

```
# By entry ID (12-char nanoid from search results)
memory_get({"path": "r7Wp3nKx_mZe"})

# By session transcript (from an entry's session field)
memory_get({"path": "session:abc123def456"})

# By file path
memory_get({"path": "MEMORY.md"})
```

通过ID读取条目会使其使用频率增加，从而提高该条目在夜间生成的内存快照中的显示概率。

## 引用

在对话中引用之前的事件时，使用格式`[<12个字符的ID>]`（例如`[r7Wp3nKx_mZe]`）。这种引用格式会被用于统计条目的使用频率——被引用的条目更有可能出现在未来的内存快照中。

## 更正与更新

Reclaw日志系统仅支持追加操作。若需更正错误：
- 在对话中明确说明更正内容；提取工具会为同一主题创建新的条目。
- 若要将任务标记为已完成，请明确说明；提取工具会生成状态为`done`的新`task`条目。
- 若要回答问题，需详细说明解决方案；提取工具会将答案记录为`fact`或`decision`类型的条目。

旧条目永远不会被修改。当前的状态是通过按时间顺序读取某个主题的所有条目来重建的。

## 过滤规则

日志中仅应记录与用户相关的信息。请思考：“如果没有这个用户的背景信息，我还需要知道这些内容吗？”如果一个通用的大型语言模型（LLM）能够在没有用户上下文的情况下生成这些内容，那么这些信息就不应该被记录在日志中。日志中不应包含通用知识、依赖关系列表或重复性的内容。

## 命令行接口（CLI）命令

```bash
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

# Regenerate the MEMORY.md memory snapshot now
openclaw reclaw snapshot generate

# Force-refresh MEMORY.md session handoff block from log
openclaw reclaw handoff refresh

# Import historical conversations
openclaw reclaw import <chatgpt|claude|grok|openclaw> <file>
openclaw reclaw import status
openclaw reclaw import resume <jobId>

# Setup
openclaw reclaw init
openclaw reclaw verify
openclaw reclaw uninstall
```