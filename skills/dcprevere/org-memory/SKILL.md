---
name: org-memory
description: "使用 `org-mode` 文件构建结构化的知识库和任务管理系统。可以通过 `org` CLI 对 `org` 文件及 `org-roam` 数据库进行查询、修改、链接和搜索操作。"
metadata: {"openclaw":{"emoji":"🦄","requires":{"bins":["org"]},"install":[{"id":"github-release","kind":"manual","label":"Download from GitHub releases: https://github.com/dcprevere/org-cli/releases"}]}}
---
# org-memory

使用 `org` CLI 来维护结构化、链接化且易于阅读的知识内容，这些内容存储在 org-mode 文件中。org 文件是具有丰富结构的纯文本文件，包含标题、待办事项状态、标签、属性、时间戳和链接。结合 `org-roam`，它们可以形成一个由 SQLite 数据库支持的知识图谱。

## 快捷操作

当用户使用这些快捷操作时，系统会立即执行相应的动作：

| 操作模式 | 动作 |
|---------|--------|
| `Remember: <信息>` | 将信息保存到知识库中（`$ORG_MEMORY_AGENT_DIR`）。创建或更新一个节点，以便用户日后查阅。 |
| `Note: <任务或信息>` | 将信息添加到用户的 org 文件中（`$ORG_MEMORY_HUMAN_DIR/inbox.org`）。这些信息供用户后续处理。 |

示例：
- “Remember: Sarah prefers morning meetings” → 在你的仓库中为 Sarah 创建/更新一个节点
- “Note: Buy groceries” → 在用户的收件箱中添加一个待办事项
- “Remember: The API uses OAuth2, not API keys” → 在你的仓库中为该 API 创建/更新一个节点
- “Note: Review PR #42 by Friday” → 在用户的收件箱中添加一个带有截止日期的待办事项

不要请求确认，直接执行操作。每次执行操作后，都会以以下格式打印一条信息：

```
org-memory: <action> <file-path>
```

示例：`org-memory: added TODO to ~/org/human/inbox.org`, `org-memory: created node ~/org/agent/sarah.org`, `org-memory: updated ~/org/agent/sarah.org`.

## 输出格式

所有命令都支持 `-f json` 选项，用于生成结构化的输出，格式为 `{"ok":true,"data":...}`。如果出现错误，会返回 `{"ok":false,"error":{"type":"...","message":"..."}`。请始终使用 `-f json` 选项。

## 命令说明

运行 `org schema` 可以获取所有命令、参数和标志的机器可读描述。这样你就可以在不记住接口细节的情况下构建有效的命令。

## 配置

配置通过环境变量完成。将配置信息设置在 `openclaw.json` 文件中，以便在每个命令执行时自动应用这些设置。

| 变量 | 默认值 | 作用 |
|---|---|---|
| `ORG_MEMORY_USE_FOR_AGENT` | `true` | 启用代理自身的知识库 |
| `ORG_MEMORY_AGENT_DIR` | `~/org/agent` | 代理的 org 文件目录 |
| `ORG_MEMORY_AGENT_DATABASE_LOCATION` | `~/.local/share/org-memory/agent/.org.db` | 代理的数据库 |
| `ORG_MEMORY_USE_FOR_HUMAN` | `true` | 启用用户 org 文件中的任务管理功能 |
| `ORG_MEMORY_HUMAN_DIR` | `~/org/human` | 用户的 org 文件目录 |
| `ORG_MEMORY_HUMAN_DATABASE_LOCATION` | `~/.local/share/org-memory/human/.org.db` | 用户的数据库 |

如果 `ORG_MEMORY_USE_FOR_AGENT` 未设置为 `true`，则跳过知识管理部分；如果 `ORG_MEMORY_USE_FOR_HUMAN` 未设置为 `true`，则跳过任务管理和批量操作部分。

在执行任何操作时，务必使用 `--db` 选项指定正确的数据库。CLI 会使用 `--db` 指定的数据库自动同步数据。如果不使用 `--db`，CLI 会默认使用 Emacs 的 org-roam 数据库（`~/.emacs.d/org-roam.db`），但这可能不是你想要的结果。

对于已启用的目录，需要先创建一个节点并构建标题索引：

```bash
org roam node create "Index" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
org index -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION"
org index -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION"
```

`org-roam` 的响应会包含节点的 ID、文件路径、标题和标签。索引功能支持自定义 ID 的自动分配，以及无需文件即可执行的操作。

## 知识管理

当 `ORG_MEMORY_USE_FOR_AGENT` 为 `true` 时，以下规则适用：

### ⚠️ 创建前请务必搜索

在创建节点或链接之前，先检查该实体是否已经存在：

```bash
org roam node find "Sarah" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
```

- 如果找到：使用现有的节点 ID 和文件路径
- 如果未找到（返回 `headline_not_found` 错误）：创建一个新的节点

**切勿在未搜索的情况下创建节点**，否则会导致知识图谱出现重复。

### 记录实体

只有在确认不存在现有节点的情况下，才能进行记录：

```bash
org roam node create "Sarah" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -t person -t work -f json
```

### 为节点添加结构

使用 `create` 或 `find` 命令返回的文件路径来添加内容：

```bash
# Add a headline to the node (response includes auto-assigned custom_id)
org add <file> "Unavailable March 2026" --tag scheduling --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
# → {"ok":true,"data":{"custom_id":"k4t","title":"Unavailable March 2026",...}}

# Use the custom_id for follow-up commands
org note k4t "Out all of March per human." -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json

# Append body text to an existing headline
org append k4t "Confirmed by email on 2026-02-20." -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json

# Append multi-line text via stdin
echo "First paragraph.\n\nSecond paragraph." | org append k4t --stdin -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
```

**`org note` 与 `org append` 的区别：** `note` 会在日志簿（metadata）中添加带时间戳的条目；`append` 会在标题正文（可见内容）中添加文本。`note` 用于记录审计轨迹，`append` 用于逐步构建内容。

**注意：** 这两个命令都是针对标题（headlines）执行的，而不是针对文件级别的节点。如果一个节点是文件级别的（尚未添加标题），请先使用 `org add` 创建一个标题，然后再使用 `note` 或 `append`。

### 链接两个节点

**请务必先搜索两个节点以获取它们的 ID**：

```bash
# Find source node
org roam node find "Bob" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
# → Returns {"ok":true,"data":{"id":"e5f6a7b8-...","file":"/path/to/bob.org",...}}

# Find target node  
org roam node find "Alice" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
# → Returns {"ok":true,"data":{"id":"a1b2c3d4-...",...}}
```

如果任一节点不存在，请先创建该节点，然后使用返回的 ID 进行链接：

```bash
org roam link add <source-file> "<source-id>" "<target-id>" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" --description "manages" -f json
```

`--description` 参数用于设置关系相关的元数据。

### 查询知识

```bash
org roam node find "Sarah" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
org roam backlinks "a1b2c3d4-..." -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
org roam tag find person -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
org search "Sarah.*March" -d "$ORG_MEMORY_AGENT_DIR" -f json
```

### 添加别名和引用

别名可以让节点通过多个名称被访问。引用用于关联 URL 或外部标识符：

```bash
org roam alias add <file> "a1b2c3d4-..." "Sarah Chen" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION"
org roam ref add <file> "a1b2c3d4-..." "https://github.com/sarahchen" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION"
```

## 任务管理

当 `ORG_MEMORY_USE_FOR_HUMAN` 为 `true` 时，以下规则适用：

### 查看用户的状态

**从这里开始查询。** `org today` 是最有用的查询命令，它会返回所有今天安排或已过期的未完成待办事项：

```bash
org today -d "$ORG_MEMORY_HUMAN_DIR" -f json
```

为了获取更全面的视图：

```bash
org agenda today -d "$ORG_MEMORY_HUMAN_DIR" -f json   # all scheduled + deadlines for today
org agenda week -d "$ORG_MEMORY_HUMAN_DIR" -f json    # next 7 days
org agenda todo -d "$ORG_MEMORY_HUMAN_DIR" -f json    # all TODOs
org agenda todo --tag work -d "$ORG_MEMORY_HUMAN_DIR" -f json
```

### 进行修改

```bash
# Add a headline (response includes the auto-assigned custom_id)
org add $ORG_MEMORY_HUMAN_DIR/inbox.org "Review PR #42" --todo TODO --tag work --deadline 2026-02-10 --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json

# Subsequent commands use the custom_id — no file path needed
org todo k4t DONE -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
org schedule a1b 2026-03-15 -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
org note a1b "Pushed back per manager request" -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION"
org append a1b "Meeting notes from standup." -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json

# Refile still requires explicit file paths
org refile $ORG_MEMORY_HUMAN_DIR/inbox.org "Review PR #42" $ORG_MEMORY_HUMAN_DIR/work.org "Code reviews" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
```

### 写入前预览

使用 `--dry-run` 命令查看修改后的结果，而不会实际修改文件：

```bash
org todo tasks.org "Buy groceries" DONE --dry-run -f json
```

## 批量操作

当 `ORG_MEMORY_USE_FOR_HUMAN` 为 `true` 时，以下规则适用：

可以原子性地执行多个操作。命令会按顺序处理内存中的数据，只有所有操作都成功后才会写入文件：

```bash
echo '{"commands":[
  {"command":"todo","file":"tasks.org","identifier":"Buy groceries","args":{"state":"DONE"}},
  {"command":"tag-add","file":"tasks.org","identifier":"Write report","args":{"tag":"urgent"}},
  {"command":"schedule","file":"tasks.org","identifier":"Write report","args":{"date":"2026-03-01"}},
  {"command":"append","file":"tasks.org","identifier":"Write report","args":{"text":"Include Q1 metrics."}}
]}' | org batch -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
```

## 何时记录知识

当同时启用知识管理和任务管理功能，并且用户提供了具体请求时，需要区分用户的请求和环境中的信息：将用户的请求记录在 `$ORG_MEMORY_HUMAN_DIR` 中；将你学到的信息记录在 `$ORG_MEMORY_AGENT_DIR` 中。

示例： “Cancel my Thursday meeting with Sarah and reschedule the API migration review to next week. Sarah is going to be out all of March.”  
- 取消并重新安排会议：属于用户的明确请求，记录在 `$ORG_MEMORY_HUMAN_DIR` 中  
- Sarah 三月不在：属于环境信息，记录在 `$ORG_MEMORY_AGENT_DIR` 中  

如果仅启用了代理的知识管理功能，所有相关信息都记录在 `$ORG_MEMORY_AGENT_DIR` 中；如果仅启用了用户文件管理功能，则只处理用户的明确请求。

在创建节点之前，请先检查该节点是否已经存在。使用操作返回的数据，避免进行额外的查询。

**每次写入操作后都必须记录。** 在对任一目录进行修改后，都要打印 `org-memory: <操作> <文件路径>`。切勿默默地写入文件。

## 稳定的标识符（CUSTOM_ID）

当存在索引数据库时，使用 `org add` 创建的每个标题都会自动分配一个简短的 CUSTOM_ID（例如 `k4t`）。这个 ID 会出现在所有 JSON 响应的 `custom_id` 字段中，并作为文本输出的一部分。

在后续命令中，可以使用 CUSTOM_ID 来引用标题——这些 ID 在编辑过程中是稳定的，不需要依赖文件路径：

```bash
org todo k4t DONE -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
org schedule k4t 2026-03-15 -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
org note k4t "Pushed back per manager request" -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
org append k4t "Updated scope per review." -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
```

对于没有 CUSTOM_ID 的现有标题，需要手动为其分配：

```bash
org custom-id assign -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION"
```

切勿通过位置编号来引用标题。文件被编辑后，位置可能会发生变化。请使用 CUSTOM_ID、org-id 或完整的标题来引用标题。

## 错误处理

根据 `ok` 字段的值来处理错误：

- `file_not_found`：路径错误或文件已被删除  
- `headline_not_found`：标识符不匹配；重新查询以获取当前状态  
- `parse_error`：文件包含解析器无法处理的格式；不要重试  
- `invalid_args`：检查 `org schema` 或 `org <命令> --help` 的使用方式  

## 故障排除

### 创建了重复的节点
在创建节点之前，请务必先执行 `node find` 操作。如果发现重复节点，请手动删除新文件并运行 `org roam sync`。

### 使用 `org note` 时出现 “headline_not_found” 错误
如果你尝试向文件级别的节点（级别为 0）添加内容，请先使用 `org add` 创建一个标题，然后再使用 `org note`。

### 链接显示错误的文本
`--description` 参数用于设置关系元数据，而不是显示文本。链接显示的是目标节点的标题。这是 `org-roam` 的正常行为。

### 数据库不同步
运行 `org roam sync -d <dir> --db <db-path>` 以从文件中重建数据库。