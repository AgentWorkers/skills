---
name: org-memory
version: 0.5.0
description: "使用 org-mode 文件构建结构化的知识库和任务管理系统。可以通过 `org` CLI 对 org 文件及 org-roam 数据库进行查询、修改、链接和搜索操作。"
metadata: {"openclaw":{"emoji":"🦄","homepage":"https://github.com/dcprevere/org-cli","requires":{"bins":["org"],"env":["ORG_MEMORY_AGENT_DIR","ORG_MEMORY_HUMAN_DIR","ORG_MEMORY_AGENT_DATABASE_LOCATION","ORG_MEMORY_HUMAN_DATABASE_LOCATION","ORG_MEMORY_AGENT_ROAM_DIR","ORG_MEMORY_HUMAN_ROAM_DIR"]},"install":[{"kind":"download","label":"Download from GitHub releases: https://github.com/dcprevere/org-cli/releases"}],"scope":{"reads":["$ORG_MEMORY_AGENT_DIR","$ORG_MEMORY_HUMAN_DIR"],"writes":["$ORG_MEMORY_AGENT_DIR","$ORG_MEMORY_HUMAN_DIR"],"migrationReads":["~/.openclaw/workspace/MEMORY.md","~/.openclaw/workspace/memory/"],"migrationWrites":["~/.openclaw/openclaw.json"]}}}
---
# org-memory

使用 `org` 命令行工具（CLI）来维护 `org-mode` 文件中的结构化、链接化且易于人类阅读的知识内容。`org` 文件是具有丰富结构的纯文本文件，包含标题、待办事项（TODO）、标签、属性、时间戳和链接等内容。结合 `org-roam` 工具，它们可以形成一个由 SQLite 数据库支持的知识图谱。

## 快捷键

当人类用户使用这些快捷键时，系统会直接执行相应的操作。

### Org 命令操作

| 前缀 | 别名 | 功能 |
|---|---|---|
| `t:` | `Todo:` | 在用户的 `org` 文件中创建待办事项（会提取日期） |
| `d:` | `Done:` / `Finished:` | 将待办事项标记为已完成 |
| `s:` | | 重新安排待办事项的日程 |
| `r:` | `Note:` | 将内容保存到用户的 `roam` 文件中（作为知识或信息） |
| `k:` | `Know:` / `Remember:` | 将内容存储到代理的知识库中 |

### 行为修饰符

这些前缀会改变系统的响应方式，但不会改变存储的内容。

| 前缀 | 功能 |
|---|---|
| `v:` | 语音回复（TTS） |
| `?` | 进行搜索（网络 + 文件） |
| `@` | 在 `roam` 中查找信息 |
| `w:` | 设置工作上下文（Remundo） |
| `!` | 紧急——立即执行 |
| `q:` | 快速回答，不使用工具 |

### 创建待办事项

`t: <文本>` 或 `Todo: <文本>` 表示“创建一个待办事项”。从文本中提取日期或时间范围，并安排其执行时间。如果文本中包含相对日期（如“3周后”、“到周五”、“下个月”），系统会计算实际日期，并添加 `--scheduled <日期>` 或 `--deadline <日期>`。

**执行命令：** `org add "$ORG_MEMORY_HUMAN_DIR/inbox.org" '<标题>' --todo TODO --scheduled <日期> --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json`

当文本中明确指定了截止日期（如“到周五”、“3月1日截止”）时，使用 `--deadline`；对于较宽松的时间安排（如“3周后”、“下个月”、“明天”），使用 `--scheduled`。

**示例：**
- “t: 3周后提交税款” → `org add .../inbox.org '提交税款' --todo TODO --scheduled 2026-03-18`
- “Todo: 6月前更新护照” → `org add .../inbox.org '更新护照' --todo TODO --deadline 2026-06-01`
- “t: 明天看牙医” → `org add .../inbox.org '看牙医' --todo TODO --scheduled 2026-02-26`
- “Todo: 预订航班” → `org add .../inbox.org '预订航班' --todo TODO`（未提及日期）

### 备注 — 用于人类用户

`r: <文本>` 或 `Note: <文本>` 表示“将此内容添加到用户的 `org` 文件中”。这始终是针对人类的任务或提醒，而不是代理的。

**执行命令：** `org add "$ORG_MEMORY_HUMAN_DIR/inbox.org" '<文本>' --todo TODO -f json`

如果备注中包含日期或截止日期，添加 `--scheduled <日期>` 或 `--deadline <日期>`；如果没有日期，则不添加。

**示例：**
- “r: 购买食品杂货” → `org add .../inbox.org '购买食品杂货' --todo TODO`
- “Note: 在周五前审阅 PR #42” → `org add .../inbox.org '审阅 PR #42' --todo TODO --deadline 2026-02-28`
- “r: 我们可以在应用程序中添加功能 X” → `org add .../inbox.org '在应用程序中添加功能 X' --todo TODO`
- “Note: 向 Donna 发送关于安全措施的邮件” → `org add .../inbox.org '向 Donna 发送关于安全措施的邮件' --todo TODO`

**注意与待办事项的区别：** 两者都会创建待办事项标题。区别在于用途：`t:` / `Todo:` 表示具体的任务（总是尝试提取日期），而 `r:` / `Note:` 表示更广泛的内容（想法、提醒、观察记录）。如果没有日期，则不添加日期。

**特殊情况 — 想法与观察记录：** 如果用户输入 “r: 我们可以尝试 X” 或 “Note: 关于 Y 的想法”，这仍然属于备注。应将其作为待办事项记录下来，不要将其添加到代理的知识库中。

### 重新安排任务

`s: <文本>` 表示“重新安排这个任务”。系统会搜索匹配的待办事项并更新其日程。

**执行步骤：**
1. 搜索：`org todo list --state TODO --search '<文本>' -d "$ORG_MEMORY_HUMAN_DIR" -f json`
2. 如果只找到一个匹配项：`org schedule <自定义ID> <日期> -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json`
3. 如果找到多个匹配项：显示给用户并询问具体是哪个任务
4. 如果没有找到匹配项：告诉用户无法找到该任务

**示例：**
- “s: 将税款安排到下周五” → 查找 “税款” 待办事项，并将其重新安排到下周五
- “s: 2026-04-01 看牙医” → 查找 “牙医” 待办事项，并将其重新安排到 2026-04-01

### 标记完成

`d: <文本>`、`Done: <文本>` 或 `Finished: <文本>` 表示“将此任务标记为已完成”。系统会搜索匹配的待办事项并更新其状态。

**执行步骤：**
1. 搜索：`org todo list --state TODO --search '<文本>' -d "$ORG_MEMORY_HUMAN_DIR" -f json`
2. 如果只找到一个匹配项：`org todo set <自定义ID> DONE -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json`
3. 如果找到多个匹配项：显示给用户并询问具体是哪个任务
4. 如果没有找到匹配项：告诉用户无法找到该任务

**示例：**
- “d: 支付 Nigel Kerry” → 查找并标记为已完成
- “Finished: 完成了 PR 审阅” → 查找并标记为已完成
- “Done: 购买食品杂货” → 查找 “食品杂货” 待办事项，并将其标记为已完成

### 存储到代理的知识库中

`k: <信息>`、`Know: <信息>` 或 `Remember: <信息>` 表示“将此信息存储到代理的知识库中以供将来使用”。这些信息会在会话之间保留。

**执行步骤：**
1. 首先搜索现有的节点（`org roam node find`），然后创建或更新节点。

**示例：**
- “k: Sarah 更喜欢上午开会” → 在 `$ORG_MEMORY_AGENT_DIR` 中创建/更新 Sarah 的节点
- “Remember: API 使用 OAuth2，而不是 API 密钥” → 在 `$ORG_MEMORY_AGENT_DIR` 中创建/更新关于 API 的节点

### 每次写入后确认

在对任一目录进行任何修改后，都需要以以下格式输出一条信息：

```
org-memory: <action> <file-path>
```

**示例：** `org-memory: 向 ~/org/human/inbox.org 添加了待办事项`，`org-memory: 在 ~/org/agent/sarah.org 中创建了节点`，`org-memory: 更新了 ~/org/agent/sarah.org`。

**这是强制性的。** 绝不要默默地对任一目录进行写入操作。用户应始终能够看到你的操作内容及其位置。

## 输出格式

所有命令都支持 `-f json` 选项，以生成结构化的输出（格式为 `{"ok":true,"data":...}`）。错误会返回 `{"ok":false,"error":{"type":"...","message":"..."}`。始终使用 `-f json`。

## 命令安全性

用户提供的文本（任务标题、备注内容、搜索词）必须用单引号括起来，以防止 shell 解释。双引号可以包含 `$()`, 反引号和变量插值，但单引号无法实现这些功能。

```bash
# Correct
org add "$ORG_MEMORY_HUMAN_DIR/inbox.org" 'User provided text' --todo TODO -f json

# Wrong — double quotes allow shell injection
org add "$ORG_MEMORY_HUMAN_DIR/inbox.org" "User provided text" --todo TODO -f json
```

如果文本中包含字面意义上的单引号，需要使用 `'\''` 进行转义：

```bash
org add "$ORG_MEMORY_HUMAN_DIR/inbox.org" 'Don'\''t forget' --todo TODO -f json
```

对于多行内容，应通过标准输入（stdin）传递，而不是使用变量插值：

```bash
printf '%s' 'Long text here' | org append k4t --stdin -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
```

环境变量路径（如 `$ORG_MEMORY_HUMAN_DIR` 等）必须始终用双引号括起来，以避免包含空格；但用户提供的文本不能放在双引号内。

## 命令说明

运行 `org schema` 一次，可以获取所有命令、参数和标志的机器可读描述。这样你就可以在不记住接口细节的情况下构建有效的命令。

## 设置

配置通过环境变量完成。将它们设置到 `openclaw.json` 文件中，以便在每个命令中自动应用这些配置。

**必填项：** 设置以下变量以匹配你的目录结构：

| 变量 | 默认值 | 用途 |
|---|---|---|
| `ORG_MEMORY_AGENT_DIR` | `~/org/alcuin` | 代理的 `org` 工作区目录 |
| `ORG_MEMORY_AGENT_ROAM_DIR` | `~/org/alcuin/roam` | 代理的 `roam` 节点目录 |
| `ORG_MEMORY_AGENT_DATABASE_LOCATION` | `~/org/alcuin/roam/.org.db` | 代理的数据库 |
| `ORG_MEMORY_HUMAN_DIR` | `~/org/human` | 用户的 `org` 工作区目录 |
| `ORG_MEMORY_HUMAN_ROAM_DIR` | `~/org/human/roam` | 用户的 `roam` 节点目录 |
| `ORG_MEMORY_HUMAN_DATABASE_LOCATION` | `~/org/human/roam/.org.db` | 用户的数据库 |

**可选项：** 这些变量有默认值：

| 变量 | 默认值 | 用途 |
|---|---|---|
| `ORG_MEMORY_USE_FOR_AGENT` | `true` | 启用代理自己的知识库 |
| `ORG_MEMORY_USE_FOR_HUMAN` | `true` | 启用用户 `org` 文件中的任务管理功能 |
| `ORG_MEMORY_ORG_BIN` | `org` | `org` 命令行工具的路径 |
| `ORG_MEMORY_INBOX_FILE` | `inbox.org` | 新任务的文件名（相对于 `humanDir`） |

工作区目录（`*_DIR`）存储任务、收件箱和日常文件；`roam` 目录（`*_ROAM_DIR`）存储知识图谱节点。数据库默认与 `roam` 目录位于同一位置。`roam` 目录的默认路径为 `<workspace>/roam`——`roam` 节点不会被创建在工作区根目录下。

如果 `ORG_MEMORY_USE_FOR_AGENT` 未设置为 `true`，则跳过知识管理部分；如果 `ORG_MEMORY_USE_FOR_HUMAN` 未设置为 `true`，则跳过任务管理和批量操作部分。

始终使用 `--db` 参数指定正确的数据库路径。`org` 命令行工具会在每次修改后自动同步 `roam` 数据库。如果没有指定 `--db`，则使用默认的 `<directory>/.org.db`。

初始化所有已启用的目录。如果目录中已经存在 `org` 文件，需要先进行同步：

```bash
# Sync existing files into the roam database (skip if starting fresh)
org roam sync -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION"
org roam sync -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION"

# Create a seed node for the agent's knowledge base (skip if files already exist)
org roam node create 'Index' -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json

# Build the headline index (enables CUSTOM_ID auto-assignment and file-less commands)
org index -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION"
org index -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION"
```

`roam` 响应会包含节点的 ID、文件路径、标题和标签。

## 稳定的标识符（CUSTOM_ID）

使用 `org add` 创建的每个标题都会自动分配一个简短的 `CUSTOM_ID`（例如 `k4t`），前提是存在索引数据库。这个 ID 会出现在所有 JSON 响应的 `custom_id` 字段中，并作为文本输出中的列。

在后续命令中可以使用 `CUSTOM_ID` 来引用标题——它们在编辑过程中是稳定的，不需要提供文件路径：

```bash
org todo set k4t DONE -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
org schedule k4t 2026-03-15 -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
org note k4t 'Pushed back per manager request' -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
org append k4t 'Updated scope per review.' -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
```

**为没有 `CUSTOM_ID` 的现有标题补全 `CUSTOM_ID`：**

```bash
org custom-id assign -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION"
```

**切勿通过位置编号（`pos`）来引用标题。** 文件被编辑后，标题的位置会发生变化——对一个标题的修改会改变其后所有内容的字节位置。

**推荐的稳定标识符顺序：**
1. **CUSTOM_ID**（例如 `k4t`）——稳定、简短、唯一
2. **org-id**（UUID）——稳定、唯一
3. **确切的标题**——只要标题不变，就是稳定的

如果你需要在同一个文件中修改多个标题，可以：
- 使用 `org batch` 进行原子级的多步操作（推荐）
- 使用 `CUSTOM_ID` 或标题，切勿使用 `pos`
- 如果必须使用 `pos`，则在每次修改后重新查询以获取最新的位置

## 错误处理

根据 `ok` 字段的值来处理错误：
- `file_not_found`：路径错误或文件已删除
- `headline_not_found`：标识符不匹配；重新查询以获取当前状态
- `parse_error`：文件包含解析器无法处理的语法错误；不要重试
- `invalid_args`：检查 `org schema` 或 `org <command> --help`

## 参考资料

在需要时阅读以下文档：
- **知识管理**（`{baseDir}/references/knowledge-management.md`）：当 `ORG_MEMORY_USE_FOR_AGENT=true` 且需要创建/查询/链接代理知识库中的节点时阅读。
- **任务管理**（`{baseDir}/references/task-management.md`）：当 `ORG_MEMORY_USE_FOR_HUMAN=true` 且需要查询或修改用户的任务、使用批量操作或将自然语言查询映射为命令时阅读。
- **内存架构**（`{baseDir}/references/memory-architecture.md`）：在会话开始时阅读（文件结构、会话流程、环境捕获指南）。其中还包含可选的内存迁移说明——只有在用户明确要求从 `MEMORY.md` 迁移到 `org-mode` 时才需要执行迁移。迁移操作会读取/写入指定目录之外的文件（详情请参阅相关文档）。