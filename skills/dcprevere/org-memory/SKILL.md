---
name: org-memory
description: "使用 org-mode 文件构建结构化的知识库和任务管理系统。通过 `org` CLI 可以查询、修改、链接以及搜索 org 文件和 org-roam 数据库中的内容。"
metadata: {"openclaw":{"emoji":"🦄","requires":{"bins":["org"]},"install":[{"id":"github-release","kind":"manual","label":"Download from GitHub releases: https://github.com/dcprevere/org-cli/releases"}]}}
---

# org-memory

使用 `org` 命令行工具（CLI）来维护 `org-mode` 文件中结构化、相互关联且易于阅读的知识内容。`org-mode` 文件是具有丰富结构的纯文本文件，包含标题、待办事项状态、标签、属性、时间戳和链接等内容。结合 `org-roam` 工具，它们可以形成一个由 SQLite 数据库支持的知识图谱。

## 快捷操作

当用户使用这些快捷操作时，系统会立即执行相应的动作：

| 操作模式 | 动作 |
|---------|--------|
| `Remember: <信息>` | 将信息保存到代理的知识库（`$ORG_MEMORY_AGENT_DIR`）中。创建或更新一个节点，以便用户日后查阅。 |
| `Note: <任务或信息>` | 将该信息添加到用户的 `org-mode` 文件（`$ORG_MEMORY_HUMAN_DIR/inbox.org`）中，供用户执行相应的操作。 |

**示例：**
- “Remember: Sarah prefers morning meetings” → 在代理的知识库中为 Sarah 创建/更新一个节点。
- “Note: Buy groceries” → 在用户的待办事项列表中添加一条任务。
- “Remember: The API uses OAuth2, not API keys” → 在代理的知识库中为该 API 创建/更新一个节点。
- “Note: Review PR #42 by Friday” → 在用户的待办事项列表中添加一条带有截止日期的任务。

**注意：** 不需要用户确认快捷操作的执行结果——直接执行操作后，再确认信息是否已保存。

## 输出格式

所有命令都支持使用 `-f json` 选项来生成结构化的输出格式，输出格式为 `{"ok":true,"data":...}`。如果出现错误，输出格式为 `{"ok":false,"error":{"type":"...","message":"..."}`。请务必使用 `-f json` 选项。

## 命令说明

运行 `org schema` 可以获取所有命令、参数和标志的机器可读描述，从而无需记忆具体的接口信息。

## 配置

配置通过环境变量完成。将配置信息设置在 `openclaw.json` 文件中，这样每次执行命令时都会自动应用这些配置。

| 变量 | 默认值 | 作用 |
|---|---|---|
| `ORG_MEMORY_USE_FOR_AGENT` | `true` | 启用代理的知识库功能 |
| `ORG_MEMORY_AGENT_DIR` | `~/org/agent` | 代理的 `org-mode` 文件目录 |
| `ORG_MEMORY_AGENT_DATABASE_LOCATION` | `~/.local/share/org-memory/agent/.org.db` | 代理的数据库文件路径 |
| `ORG_MEMORY_USE_FOR_HUMAN` | `true` | 启用用户 `org-mode` 文件中的任务管理功能 |
| `ORG_MEMORY_HUMAN_DIR` | `~/org/human` | 用户的 `org-mode` 文件目录 |
| `ORG_MEMORY_HUMAN_DATABASE_LOCATION` | `~/.local/share/org-memory/human/.org.db` | 用户的数据库文件路径 |

如果 `ORG_MEMORY_USE_FOR_AGENT` 未设置为 `true`，则跳过知识管理相关内容；如果 `ORG_MEMORY_USE_FOR_HUMAN` 未设置为 `true`，则跳过任务管理和批量操作相关内容。

**注意：** 必须使用 `--db` 选项指定正确的数据库路径。`org` CLI 会在每次执行命令后自动使用 `--db` 指定的数据库进行同步。如果不使用 `--db`，它会默认使用 Emacs 的 `org-roam` 数据库（`~/.emacs.d/org-roam.db`），但这可能不是您想要的结果。

**初始化操作：** 在每个启用相关功能的目录中创建第一个节点：

```bash
org roam node create "Index" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
```

响应中会包含节点的 ID、文件路径、标题和标签。后续命令可以使用这些信息。

## 知识管理

当 `ORG_MEMORY_USE_FOR_AGENT` 为 `true` 时，以下规则适用：

### ⚠️ 创建前务必先搜索

在创建节点或链接之前，先检查该实体是否已经存在：

```bash
org roam node find "Sarah" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
```

- 如果找到该实体：使用现有的节点 ID 和文件路径。
- 如果未找到（返回 `headline_not_found` 错误）：创建一个新的节点。

**切勿在未搜索的情况下直接创建节点**，否则会导致知识图谱出现重复。

### 记录实体

只有在确认不存在现有节点的情况下，才能进行记录：

```bash
org roam node create "Sarah" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -t person -t work -f json
```

### 为节点添加结构

使用 `create` 或 `find` 命令返回的文件路径来为节点添加结构：

```bash
# Add a headline to the node
org add <file> "Unavailable March 2026" --tag scheduling --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json

# Add a note to an existing headline (NOT to file-level nodes)
org note <file> "Unavailable March 2026" "Out all of March per human." --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
```

**注意：** `org note` 命令用于向标题（而非文件级别的节点）添加注释。如果某个节点是文件级别的（尚未添加标题），请先使用 `org add` 命令创建一个标题，然后再添加注释。

### 链接两个节点

**务必先搜索两个节点** 以获取它们的 ID：

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

`--description` 参数用于设置节点之间的关联元数据（可选）。

### 查询知识

```bash
org roam node find "Sarah" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
org roam backlinks "a1b2c3d4-..." -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
org roam tag find person -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
org search "Sarah.*March" -d "$ORG_MEMORY_AGENT_DIR" -f json
```

### 添加别名和引用

别名可以让节点通过多个名称被访问；引用用于关联外部 URL 或标识符：

```bash
org roam alias add <file> "a1b2c3d4-..." "Sarah Chen" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION"
org roam ref add <file> "a1b2c3d4-..." "https://github.com/sarahchen" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION"
```

## 任务管理

当 `ORG_MEMORY_USE_FOR_HUMAN` 为 `true` 时，以下规则适用：

### 读取用户的待办事项状态

```bash
org agenda today -d "$ORG_MEMORY_HUMAN_DIR" -f json
org agenda week -d "$ORG_MEMORY_HUMAN_DIR" -f json
org agenda todo -d "$ORG_MEMORY_HUMAN_DIR" -f json
org agenda todo --tag work -d "$ORG_MEMORY_HUMAN_DIR" -f json
```

### 进行修改

```bash
org add $ORG_MEMORY_HUMAN_DIR/inbox.org "Review PR #42" --todo TODO --tag work --deadline 2026-02-10 --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION"
org todo $ORG_MEMORY_HUMAN_DIR/inbox.org "Review PR #42" DONE --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
org schedule $ORG_MEMORY_HUMAN_DIR/projects.org "Quarterly review" 2026-03-15 --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
org note $ORG_MEMORY_HUMAN_DIR/projects.org "Quarterly review" "Pushed back per manager request" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION"
org refile $ORG_MEMORY_HUMAN_DIR/inbox.org "Review PR #42" $ORG_MEMORY_HUMAN_DIR/work.org "Code reviews" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
```

### 写入前预览

使用 `--dry-run` 选项可以预览修改操作的效果，而不会实际修改文件内容：

```bash
org todo tasks.org "Buy groceries" DONE --dry-run -f json
```

## 批量操作

当 `ORG_MEMORY_USE_FOR_HUMAN` 为 `true` 时，以下规则适用：

可以原子性地执行多个修改操作。命令会按顺序处理内存中的数据，只有所有操作都成功后才会写入文件：

```bash
echo '{"commands":[
  {"command":"todo","file":"tasks.org","identifier":"Buy groceries","args":{"state":"DONE"}},
  {"command":"tag-add","file":"tasks.org","identifier":"Write report","args":{"tag":"urgent"}},
  {"command":"schedule","file":"tasks.org","identifier":"Write report","args":{"date":"2026-03-01"}}
]}' | org batch -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
```

## 何时记录知识

当代理和用户的功能都启用时，需要区分用户的请求和系统生成的背景信息：用户的请求应记录在 `$ORG_MEMORY_HUMAN_DIR` 中，系统生成的背景信息应记录在 `$ORG_MEMORY_AGENT_DIR` 中。

**示例：**
- “Cancel my Thursday meeting with Sarah and reschedule the API migration review to next week. Sarah is going to be out all of March.”  
  - 取消并重新安排会议：属于用户的请求，记录在 `$ORG_MEMORY_HUMAN_DIR` 中。
- “Sarah is going to be out all of March.”  
  - 这是系统生成的背景信息，记录在 `$ORG_MEMORY_AGENT_DIR` 中。

**注意：** 如果仅启用代理的知识管理功能，所有相关内容都会记录在 `$ORG_MEMORY_AGENT_DIR` 中；如果仅启用用户文件管理功能，只处理用户的明确请求。

在创建节点之前，请先检查该节点是否已经存在。请使用命令返回的数据，避免进行额外的查询。

## 稳定的标识符

始终使用节点的 `org-id` 或完整标题来引用节点，而不是使用其在文件中的位置编号（位置编号可能会在文件编辑后发生变化）。如果将来需要引用某个节点，请为其设置一个唯一的 ID：

```bash
org property set file.org "My task" ID "$(uuidgen)" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
```

## 错误处理

根据 `ok` 字段的值来处理错误：
- `file_not_found`：路径错误或文件已被删除。
- `headline_not_found`：标识符不匹配；重新查询以获取当前状态。
- `parse_error`：文件包含解析器无法处理的格式；不要重试。
- `invalid_args`：请检查 `org schema` 或使用 `org <command> --help` 获取帮助信息。

## 故障排除：

### 创建了重复节点
**原因：** 创建前未进行搜索。请先运行 `node find` 命令。如果发现重复节点，请手动删除新文件并运行 `org roam sync` 命令进行同步。

### 使用 `org note` 时出现 “headline_not_found” 错误
**原因：** 尝试向文件级别的节点（0 级节点）添加注释。请先使用 `org add` 命令创建一个标题，然后再使用 `org note` 命令添加注释。

### 链接显示的文本不正确
`--description` 参数用于设置节点之间的关联元数据，而不是显示文本。链接显示的是目标节点的标题，这是 `org-roam` 的正常行为。

### 数据库不同步
运行 `org roam sync -d <dir> --db <db-path>` 命令可以从文件中重建数据库。