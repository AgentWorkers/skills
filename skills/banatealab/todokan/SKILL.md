---
name: todokan
version: 1.3.2
description: "通过MCP在Todokan中管理任务、看板、想法和评审记录。"
homepage: https://todokan.com
metadata: {"category":"productivity","tags":["tasks","kanban","mcp","planning","review"],"requires":{"env":["TODOKAN_API_KEY","TODOKAN_MCP_URL"],"mcp":true},"openclaw":{"homepage":"https://todokan.com","requires":{"env":["TODOKAN_API_KEY","TODOKAN_MCP_URL"]}}}
---
# Todokan — 看板任务管理工具

Todokan 是一款基于看板模式的任务管理工具。您可以通过 MCP 工具来管理用户任务、看板和项目。

## 先决条件

- 必须有可用的 Todokan MCP 服务器（请参阅 README 文件以了解设置方法）
- 需要的环境变量：`TODOKAN_API_KEY`、`TODOKAN_MCP_URL`（在技能元数据中声明）

---

## 触发条件 — 何时激活此技能

当用户有以下意图时，激活 Todokan 技能：

| 意图 | 例子 |
|--------|---------|
| 创建/编辑/删除任务 | “创建一个任务：审核 PR” |
| 显示看板或任务 | “显示我的任务”，“开发看板上有什么？” |
| 更改任务状态 | “将任务 X 标记为已完成” |
| 保存研究结果 | “将此内容保存为 Todokan 中的任务/文档” |
| 任务概要 | “给我讲讲我未完成的任务” |
| 为任务附加文档 | “在任务 X 上写个备注” |
| 在多个看板中搜索内容 | “我关于投资者会议做了哪些记录？” |
| 获取自上次检查以来的变化 | “从今天早上起有什么新内容？”

**注意**：当用户只是泛泛讨论任务而不提及 Todokan 时，不要激活此技能。

---

## 工具使用顺序

为确保操作的一致性，请按照以下顺序使用这些工具：

### 阅读（始终先进行阅读）

```
1. list_habitats            → Which workspaces exist?
2. list_boards              → Which boards exist? (note the IDs)
3. list_tasks               → Tasks on a board (with filters)
4. search_across_habitats   → Full-text search across boards/habitats
5. get_events_since         → Retrieve changes since a timestamp
6. list_board_labels        → Available labels + usage counts
7. list_task_documents      → Documents attached to a task
8. read_document            → Content of a document
```

### 编写（仅在阅读和确认后进行）

```
9.  create_task / create_board / create_habitat
10. update_task / update_task_by_title
11. create_document / add_document_to_task
12. delete_task              → Only after explicit confirmation
```

### 人工智能辅助（可选）

```
13. propose_task_variants    → Generate 2-3 variants
14. confirm_task_fields      → Review fields before creation
```

**黄金法则**：切勿盲目编写代码。始终先调用 `list_boards` 来获取任务 ID — 切勿猜测 UUID。

---

## 必须执行的检查

在执行写入操作之前，请确认以下内容：

### 在 `create_task` 之前
- [ ] **看板**：选择哪个看板？（如果不确定 → 显示 `list_boards`，让用户选择）
- [ ] **标题**：简洁、准确、具有指示性（最多 80 个字符）
- [ ] **优先级**：低/普通/高 — 如果不确定，默认为“普通”
- [ ] **截止日期**：仅当用户提供时才设置

### 在 `update_task` 之前
- [ ] **任务正确吗？** 请确认任务标题和看板信息
- [ ] **需要修改哪些字段？** 仅修改用户请求修改的字段

### 在 `delete_task` 之前
- [ ] **务必获得明确确认** — “我是否要永久删除看板 `[Board]' 上的任务 '[Title]'？此操作不可撤销。”

### 在 `create_document` 之前
- [ ] **明确文档格式**：markdown、文本或 html
- [ ] **链接**：文档要关联到哪个任务（或单独保存）？

---

## 规范要求

### 禁止虚构数据
- **仅使用 MCP 工具返回的真实数据**。切勿伪造任务 ID、看板名称或内容。
- 如果工具调用失败或返回空数据，请通知用户，切勿自行处理。
- 如有疑问，请显示实际结果并询问用户。

### 禁止存储敏感信息
- 不要在任务标题或描述中存储密码、API 密钥、令牌或个人数据。
- 如果用户提到敏感信息，请提醒他们：“这可能包含敏感数据 — 我真的应该将其存储在 Todokan 中吗？”

### 来源标注
- 当将外部研究内容（网页、文件、其他工具）存储到 Todokan 中时，请在任务描述或文档中注明来源：
  ```
  Source: [URL or filename]
  Created by: Agent on [date]
  ```

### 权限范围
- **工作者端点** (`/mcp-worker`）：仅支持读取和添加评论。不允许修改任务/看板信息或创建文档。
- **规划者端点** (`/mcp`)：具有完整访问权限。但在执行破坏性操作前仍需询问用户。
- 如果遇到权限问题，请向用户说明当前端点没有所需的权限。

### idempotency（幂等性）
- 在网络错误发生时，不要盲目重试相同操作。首先检查该操作是否已经执行过（使用 `list_tasks`）。

---

## 输出格式

### 任务概要

```markdown
## Briefing: [Board Name] — [Date]

**Open (todo):** X tasks
**In progress (doing):** Y tasks
**Completed (done):** Z tasks

### Urgent (high priority)
- [ ] [Task Title] — due [Date]
- [ ] [Task Title] — due [Date]

### In Progress
- [~] [Task Title] — since [Date]

### Next Steps
[1-2 sentences recommendation based on the data]
```

### 任务创建前的预览

```markdown
## Task Draft

| Field       | Value                         |
|-------------|-------------------------------|
| Board       | [Board Name]                  |
| Title       | [Title, max 80 chars]         |
| Description | [Description, max 500 chars]  |
| Status      | todo                          |
| Priority    | [low / normal / high]         |
| Due         | [YYYY-MM-DD or —]             |
| Labels      | [label1, label2]              |

Should I create this task?
```

### 文档草稿

```markdown
## Document Draft

**Title:** [Title]
**Format:** markdown
**Linked to:** [Task Title] on [Board Name]

---
[Document content]
---

Should I create this document?
```

---

## 数据模型

```
Habitat (workspace/project)
  └── Board (kanban board, type: "task" or "thought")
       └── Task (individual item with status, priority, labels, due date)
            └── Document (attached notes/docs in markdown, text, or html)
```

- **Habitats**：用于分组看板。用户可以拥有多个 habitats。
- **Boards**：表示看板。类型为 `task` 的条目表示可执行的任务，类型为 `thought` 的条目表示想法/备注。
- **Tasks**：存在于看板上，并会随着状态的变化而移动。
- **Documents**：附加到任务上的富文本内容。

## 状态说明

| 状态 | 含义 |
|--------|---------|
| `todo` | 未开始 |
| `doing` | 进行中 |
| `done` | 已完成 |

## 优先级说明

| 优先级 | 含义 |
|----------|---------|
| `low` | 低优先级 |
| `normal` | 默认优先级 |
| `high` | 高/紧急优先级 |

## 可用的 MCP 工具

### 数据读取
- `list_habitats` — 列出所有工作空间
- `list_boards` — 列出所有看板（返回 ID、名称、版本）
- `list_tasks` — 根据 `boardId`、`status`、`label`/`labels`、`limit`、`cursor` 筛选任务
- `search_across_habitats` — 一次性搜索多个工作空间/看板/任务
- `get_events_since` — 自指定时间戳以来的事件汇总（包括任务事件、评论和文档）
- `list_board_labels` — 获取看板上的唯一标签及其使用频率
- `list_task_documents` — 获取附加到任务上的文档
- `read_document` — 读取文档内容
- `list_task_comments` — 列出任务的评论

### 创建和修改（仅限规划者端点）
- `create_habitat` — 创建新的工作空间（提供名称）
- `create_board` — 创建新的看板（提供名称，可选 `habitatId`、`boardType`）
- `create_task` — 创建任务（提供标题、`boardId` 或 `boardName`，可选 `description`、`dueDate`、`priority`、`labels`）
- `update_task` — 根据 ID 更新任务（提供 `taskId` 及需要修改的字段）
- `update_task_by_title` — 根据标题精确匹配更新任务（提供 `titleExact`、`boardId` 或 `boardName`）
- `delete_task` — 永久删除任务（提供 `taskId`）
- `create_document` — 创建文档（可选提供 `relatedTaskId` 以关联任务）
- `add_document_to_task` — 为任务附加新文档
- `add_comment` — 为任务添加评论

### 人工智能辅助创建
- `propose_task_variants` — 根据粗略描述生成 2-3 个任务变体（简短/标准/详细）
- `confirm_task_fields` — 在创建前预览变体的字段内容

## 人工智能可见性控制

默认情况下，MCP 服务器仅返回 `aiEnabled: true` 的任务。`aiEnabled: false` 的任务对 MCP 代理是不可见的 — 它们不会出现在 `list_tasks`、`search_across_habitats`、`get_events_since` 或 `get_task` 中。

用户可以通过每个任务卡片上的 “Send to AI” 按钮来控制这一设置。点击后，系统会设置 `aiEnabled: true`、`assignee: 'ai'` 和 `status: 'doing'。

- 要查看仅由 AI 分配的任务：`list_tasks { "assignee": "ai" }`
- 要查看所有由 AI 分配的任务：`list_tasks {}`（默认情况下仅返回由 AI 分配的任务）
- 要明确包含非 AI 分配的任务：`list_tasks { "aiEnabled": false }`（用于报告）

## OAuth 与认证

- **使用 PKCE 的 OAuth 2.1**（RS256 JWT）
- **令牌有效期**：30 天，不支持刷新令牌
- **规划者端点** (`/mcp`)：具有完整的 CRUD 访问权限
- **工作者端点** (`/mcp-worker`)：具有 `boards:read`、`tasks:read`、`labels:read`、`docs:read`、`comments:read`、`comments:write` 权限
- **无速率限制** — 但仍需谨慎使用 API 调用
- **活动日志记录**：所有 API 调用都会在服务器端被记录

## 常见工作流程

### 列出看板上的所有任务
1. 使用 `list_boards` 查找看板 ID
2. 使用 `list_tasks` 和 `boardId` 获取任务列表

### 创建任务
```
create_task { "title": "Review PR #42", "boardName": "Development", "priority": "high", "dueDate": "2026-03-01" }
```

### 将任务标记为已完成
```
update_task { "taskId": "<uuid>", "status": "done" }
```

### 为任务添加标签
```
update_task { "taskId": "<uuid>", "labels": ["bug", "frontend"] }
```

### 根据标签查找任务
```
list_tasks { "boardId": "<uuid>", "labels": ["bug"] }
```

### 在多个工作空间中搜索
```
search_across_habitats { "query": "investor meeting", "limit": 20 }
```

### 监控事件流（代理循环）
```
get_events_since { "since": "2026-02-24T08:00:00Z", "limit": 200 }
```

## 提示

- 始终先调用 `list_boards` 以获取可用的看板 ID — 切勿猜测 UUID。
- 当用户按名称查找看板时，使用 `boardName` 而不是 `boardId`。
- 截止日期使用 `YYYY-MM-DD` 格式。
- 任务标题最多 80 个字符，描述最多 500 个字符。
- 标签为自由格式的字符串（每个任务最多 10 个）。
- `update_task` 操作需要任务的 UUID。可以使用 `list_tasks` 来获取 UUID，或者仅知道标题时使用 `update_task_by_title`。