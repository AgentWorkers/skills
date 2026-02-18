---
name: org-memory
description: "使用 org-mode 文件构建结构化的知识库和任务管理系统。通过 `org` CLI 可以查询、修改、链接以及搜索 org 文件和 org-roam 数据库中的内容。"
metadata: {"openclaw":{"emoji":"🦄","requires":{"bins":["org"]},"install":[{"id":"github-release","kind":"manual","label":"Download from GitHub releases: https://github.com/dcprevere/org-cli/releases"}]}}
---
# org-memory

使用 `org` CLI 来维护结构化、链接化且易于人类阅读的知识内容，这些内容存储在 org-mode 文件中。org 文件是具有丰富结构的纯文本文件，包含标题、待办事项状态、标签、属性、时间戳和链接。结合 `org-roam`，它们可以形成一个由 SQLite 数据库支持的知识图谱。

## 快捷操作

当用户使用这些快捷操作时，系统会立即执行相应的动作：

| 操作模式 | 动作 |
|---------|--------|
| `Remember: <信息>` | 将信息保存到知识库中（`$ORG_MEMORY_AGENT_DIR`）。创建或更新一个节点，以便您日后查询。 |
| `Note: <任务或信息>` | 将该信息添加到用户的 org 文件中（`$ORG_MEMORY_HUMAN_DIR/inbox.org`），供用户后续处理。 |

示例：
- “Remember: Sarah prefers morning meetings” → 在您的仓库中为 Sarah 创建或更新一个节点。
- “Note: Buy groceries” → 在用户的收件箱中添加一个待办事项。
- “Remember: The API uses OAuth2, not API keys” → 在您的仓库中为该 API 创建或更新一个节点。
- “Note: Review PR #42 by Friday” → 在用户的收件箱中添加一个带有截止日期的待办事项。

不要询问确认，直接执行操作。每次执行操作后，都会以以下格式输出一条信息：

```
org-memory: <action> <file-path>
```

示例：`org-memory: added TODO to ~/org/human/inbox.org`, `org-memory: created node ~/org/agent/sarah.org`, `org-memory: updated ~/org/agent/sarah.org`.

## 输出格式

所有命令都支持 `-f json` 选项，以生成结构化的输出，格式为 `{"ok":true,"data":...}`。如果出现错误，会返回 `{"ok":false,"error":{"type":"...","message":"..."}`。请始终使用 `-f json`。

## 命令说明

运行 `org schema` 可以获取所有命令、参数和标志的机器可读描述。这样您就可以在不记住接口细节的情况下构建有效的命令。

## 配置

配置通过环境变量完成。请将配置设置到 `openclaw.json` 文件中，以便所有命令都能自动使用这些配置。

| 变量 | 默认值 | 作用 |
|---|---|---|
| `ORG_MEMORY_USE_FOR_AGENT` | `true` | 启用代理的知识库功能 |
| `ORG_MEMORY_AGENT_DIR` | `~/org/agent` | 代理的 org 文件目录 |
| `ORG_MEMORY_AGENT_DATABASE_LOCATION` | `~/.local/share/org-memory/agent/.org.db` | 代理的数据库文件路径 |
| `ORG_MEMORY_USE_FOR_HUMAN` | `true` | 启用用户 org 文件中的任务管理功能 |
| `ORG_MEMORY_HUMAN_DIR` | `~/org/human` | 用户的 org 文件目录 |
| `ORG_MEMORY_HUMAN_DATABASE_LOCATION` | `~/.local/share/org-memory/human/.org.db` | 用户的数据库文件路径 |

如果 `ORG_MEMORY_USE_FOR_AGENT` 未设置为 `true`，则跳过知识管理部分；如果 `ORG_MEMORY_USE_FOR_HUMAN` 未设置为 `true`，则跳过任务管理和批量操作部分。

请始终使用 `--db` 参数指定正确的数据库路径。CLI 会使用 `--db` 参数的值在每次修改后自动同步数据库。如果没有指定 `--db`，CLI 会默认使用 Emacs 的 org-roam 数据库（`~/.emacs.d/org-roam.db`），但这可能不是您想要的结果。

请为每个启用的目录创建一个初始节点：

```bash
org roam node create "Index" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
```

响应中会包含节点的 ID、文件路径、标题和标签。在后续命令中可以使用这些信息。

## 知识管理

当 `ORG_MEMORY_USE_FOR_AGENT` 为 `true` 时，以下规则适用：

### ⚠️ 创建前请务必搜索

在创建节点或链接之前，请先检查该实体是否已经存在：

```bash
org roam node find "Sarah" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
```

- 如果找到现有节点：使用该节点的 ID 和文件路径。
- 如果未找到（返回 `headline_not_found` 错误）：创建一个新的节点。

**切勿在未搜索的情况下创建节点**，否则会导致知识图谱出现重复。

### 记录实体

只有在确认没有现有节点的情况下，才能进行记录：

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

**注意：** `org note` 命令用于向标题添加备注，而不是直接向文件级别的节点添加备注。如果某个节点是文件级别的（尚未添加标题），请先使用 `org add` 命令创建一个标题，然后再添加备注。

### 链接两个节点

**请务必先搜索两个节点** 以获取它们的 ID：

```bash
# Find source node
org roam node find "Bob" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
# → Returns {"ok":true,"data":{"id":"e5f6a7b8-...","file":"/path/to/bob.org",...}}

# Find target node  
org roam node find "Alice" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
# → Returns {"ok":true,"data":{"id":"a1b2c3d4-...",...}}
```

如果其中一个节点不存在，请先创建该节点，然后使用返回的 ID 进行链接：

```bash
org roam link add <source-file> "<source-id>" "<target-id>" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" --description "manages" -f json
```

`--description` 参数是用于描述节点之间关系的可选元数据。

### 查询知识

```bash
org roam node find "Sarah" -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
org roam backlinks "a1b2c3d4-..." -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
org roam tag find person -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
org search "Sarah.*March" -d "$ORG_MEMORY_AGENT_DIR" -f json
```

### 添加别名和引用

别名可以让节点通过多个名称被查找；引用则用于关联 URL 或外部标识符：

```bash
org roam alias add <file> "a1b2c3d4-..." "Sarah Chen" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION"
org roam ref add <file> "a1b2c3d4-..." "https://github.com/sarahchen" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION"
```

## 任务管理

当 `ORG_MEMORY_USE_FOR_HUMAN` 为 `true` 时，以下规则适用：

### 查看用户的状态

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

使用 `--dry-run` 命令预览修改后的结果，而不会实际修改文件：

```bash
org todo tasks.org "Buy groceries" DONE --dry-run -f json
```

## 批量操作

当 `ORG_MEMORY_USE_FOR_HUMAN` 为 `true` 时，以下规则适用：

可以原子性地执行多个操作。命令会按顺序对内存中的状态进行操作，只有所有操作都成功后才会写入文件：

```bash
echo '{"commands":[
  {"command":"todo","file":"tasks.org","identifier":"Buy groceries","args":{"state":"DONE"}},
  {"command":"tag-add","file":"tasks.org","identifier":"Write report","args":{"tag":"urgent"}},
  {"command":"schedule","file":"tasks.org","identifier":"Write report","args":{"date":"2026-03-01"}}
]}' | org batch -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
```

## 何时记录知识

当同时启用代理和用户功能时，需要区分用户的请求和系统生成的背景信息：用户的请求应记录在 `$ORG_MEMORY_HUMAN_DIR` 中，系统生成的背景信息应记录在 `$ORG_MEMORY_AGENT_DIR` 中。

示例：
- “Cancel my Thursday meeting with Sarah and reschedule the API migration review to next week. Sarah is going to be out all of March.”（取消与 Sarah 的周四会议，并将 API 迁移审查安排到下周。Sarah 三月份都不在。）
  - 取消和重新安排会议属于用户请求，记录在 `$ORG_MEMORY_HUMAN_DIR` 中。
  - Sarah 三月份不在属于系统生成的背景信息，记录在 `$ORG_MEMORY_AGENT_DIR` 中。

如果只启用了代理的知识管理功能，所有相关内容都记录在 `$ORG_MEMORY_AGENT_DIR` 中；如果只启用了用户文件管理功能，只处理用户的明确请求。

在创建节点之前，请先检查该节点是否已经存在。请使用操作返回的数据，而不是再次进行查询。

**每次写入操作后都必须进行记录**。每次对任一目录进行修改后，都会输出 `org-memory: <操作> <文件路径>`。切勿默默地写入文件。

## 稳定的标识符

请始终使用 org-id 或完整的标题来引用节点，而不是使用文件中的位置编号。文件被编辑后，位置编号可能会发生变化。如果您将来需要引用某个标题，请为其设置一个唯一的 ID：

```bash
org property set file.org "My task" ID "$(uuidgen)" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
```

## 错误处理

根据 `ok` 字段的值来处理错误：
- `file_not_found`：路径错误或文件已被删除。
- `headline_not_found`：标识符不匹配；请重新查询以获取当前状态。
- `parse_error`：文件包含解析器无法处理的格式；请不要重试。
- `invalid_args`：请检查 `org schema` 或使用 `org <命令> --help` 获取帮助信息。

## 故障排除

### 创建了重复节点
在创建节点之前，请务必先执行 `node find` 操作。如果发现重复节点，请手动删除新文件并运行 `org roam sync`。

### 使用 `org note` 时出现 “headline_not_found” 错误
如果您尝试向文件级别的节点（即没有标题的节点）添加备注，请先使用 `org add` 命令创建一个标题，然后再使用 `org note` 命令添加备注。

### 链接显示的文本不正确
`--description` 参数用于设置关系元数据，而非显示文本。链接显示的是目标节点的标题，这是 org-roam 的正常行为。

### 数据库不同步
运行 `org roam sync -d <dir> --db <db-path>` 命令来重新构建数据库。