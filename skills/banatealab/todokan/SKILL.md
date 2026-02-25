---
name: todokan
version: 1.0.0
description: "通过 MCP 在 Todokan 中管理任务、看板、想法和评审。"
homepage: https://todokan.com
user-invocable: true
metadata: {"category":"productivity","tags":["tasks","kanban","mcp","planning","review"],"requires":{"env":["TODOKAN_API_KEY","TODOKAN_MCP_URL"],"mcp":true},"openclaw":{"homepage":"https://todokan.com","requires":{"env":["TODOKAN_API_KEY","TODOKAN_MCP_URL"]}}}
---
# Todokan — 看板任务管理

Todokan 是一个基于看板风格的任务管理工具。您可以通过 MCP 工具来管理用户任务、看板和项目。

## 先决条件

`todokan` MCP 服务器必须在 `~/.openclaw/openclaw.json` 文件的 `mcpServers` 部分进行配置。请参阅 README 文件以获取设置说明。

---

## 触发条件 — 何时激活此技能

当用户有以下意图时，激活 Todokan 技能：

| 意图 | 例子 |
|---------|----------|
| 创建/修改/删除任务 | “创建一个任务：审核 PR” |
| 查看看板或任务 | “显示我的任务”，“开发看板上有什么？” |
| 更改任务状态 | “将任务 X 标记为已完成” |
| 保存搜索结果 | “将结果保存为 Todokan 中的任务/文档” |
| 获取任务概要 | “给我一个关于未完成任务的概要” |
| 为任务附加文档 | “为任务 X 写一条备注” |
| 在多个看板中查找信息 | “我为投资者会议记录了什么？” |
| 获取自上次检查以来的更改 | “从今天早上开始有什么新内容？”

**如果用户只是泛泛谈论任务，请勿激活此技能。**

---

## 工具使用顺序

为确保结果的一致性，请遵循以下顺序：

### 阅读（始终先进行信息收集）

```
1. list_habitats          → Welche Workspaces existieren?
2. list_boards          → Welche Boards gibt es? (IDs merken)
3. list_tasks           → Tasks auf einem Board (mit Filtern)
4. search_across_habitats → Volltext über mehrere Boards/Habitats
5. get_events_since       → Änderungen seit Zeitpunkt abrufen
6. list_board_labels      → Verfügbare Labels + Nutzung
7. list_task_documents    → Dokumente eines Tasks
8. read_document          → Inhalt eines Dokuments
```

### 编写（在收集信息并确认后进行）

```
9.  create_task / create_board / create_habitat
10. update_task / update_task_by_title
11. create_document / add_document_to_task
12. delete_task          → Nur nach expliziter Bestätigung
```

### 人工智能辅助（可选）

```
13. propose_task_variants → 2-3 Varianten generieren lassen
14. confirm_task_fields   → Felder vor Erstellung prüfen
```

**黄金法则：**切勿盲目编写。始终先调用 `list_boards` 来获取任务 ID — 切勿猜测 UUID。

---

## 必须询问的问题

在执行任何编写操作之前，请先确认以下内容：

### 在 `create_task` 之前
- [ ] **看板**：选择哪个看板？（如果不确定 → 显示 `list_boards` 并让用户选择）
- [ ] **标题**：简短、准确、具有指令性（最多 80 个字符）
- [ ] **优先级**：低 / 中 / 高 — 如果不确定，使用“normal”优先级
- [ ] **截止日期**：仅在用户提供时设置

### 在 `update_task` 之前
- [ ] **这是正确的任务吗？** 请确认任务标题和看板名称
- [ ] **需要修改哪些字段？** 只修改用户要求的字段

### 在 `delete_task` 之前
- [ ] **务必获得明确确认** — “我真的要删除看板 `[Board]' 上的任务 `[Title]' 吗？此操作不可撤销。”

### 在 `create_document` 之前
- [ ] **明确文档格式**：markdown、text 或 html
- [ ] **关联方式**：将其附加到哪个任务上（或独立保存？）

---

## 规范与注意事项

### 注意事项
- **使用真实数据**：仅使用 MCP 工具返回的 **真实数据**。不要自行生成任务 ID、看板名称或内容。
- 如果工具调用失败或返回空数据，请告知用户，切勿自行处理。
- 在不确定的情况下，显示实际结果并询问用户。

### 不要处理敏感数据
- 不要在任务标题或描述中传输密码、API 密钥、令牌或个人信息。
- 如果用户提供了敏感信息，请提醒他们：“这可能包含敏感数据 — 我真的需要将其保存在 Todokan 中吗？”

### 来源标注
- 如果您将外部来源（网站、文件、其他工具）的内容保存到 Todokan 中，请在任务描述或文档中标注来源：
  ```
  Quelle: [URL oder Dateiname]
  Erstellt von: Agent am [Datum]
  ```

### 权限范围
- **Worker 端点** (`/mcp-worker`）：仅支持读取和添加评论（`add_comment`）。不允许执行任务/看板的创建或删除操作，也不允许创建文档。
- **Planner 端点** (`/mcp`）：具有完整访问权限。但在执行破坏性操作前仍需询问用户。
- 如果权限范围不正确，请告知用户当前端点没有所需的权限。

### 重试机制
- 如果出现网络错误，请不要盲目重复操作。先使用 `list_tasks` 检查操作是否已经执行过。

## 输出格式

### 任务概要（显示现有任务）

```markdown
## Briefing: [Board-Name] — [Datum]

**Offen (todo):** X Tasks
**In Arbeit (doing):** Y Tasks
**Erledigt (done):** Z Tasks

### Dringend (high priority)
- [ ] [Task-Titel] — fällig [Datum]
- [ ] [Task-Titel] — fällig [Datum]

### In Arbeit
- [~] [Task-Titel] — seit [Datum]

### Nächste Schritte
[1-2 Sätze Empfehlung basierend auf den Daten]
```

### 任务创建前的草稿

```markdown
## Task-Entwurf

| Feld        | Wert                        |
|-------------|------------------------------|
| Board       | [Board-Name]                 |
| Titel       | [Titel, max 80 Zeichen]      |
| Beschreibung| [Beschreibung, max 500 Zeichen] |
| Status      | todo                         |
| Priorität   | [low / normal / high]        |
| Fällig      | [YYYY-MM-DD oder —]          |
| Labels      | [label1, label2]             |

Soll ich diesen Task so erstellen?
```

### 文档草稿

```markdown
## Dokument-Entwurf

**Titel:** [Titel]
**Format:** markdown
**Verknüpft mit:** [Task-Titel] auf [Board-Name]

---
[Inhalt des Dokuments]
---

Soll ich dieses Dokument so anlegen?
```

---

## 数据模型

- **Habitats**：用户可以拥有多个工作空间（看板组）。
- **Boards**：用于管理任务的看板。`task` 类型用于表示可执行的任务，`thought` 类型用于记录想法/备注。
- **Tasks**：存在于看板上，并会随着状态的变化而移动。
- **Documents**：是附加到任务上的富文本内容。

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
- `list_boards` — 列出所有看板（返回 id、名称、版本）
- `list_tasks` — 根据 `boardId`、`status`、`label`/`labels`、`limit`、`cursor` 筛选任务
- `search_across_habitats` — 一次性搜索所有工作空间/看板/任务
- `get_events_since` — 自指定时间戳以来的事件汇总（包括任务事件、评论和文档）
- `list_board_labels` — 获取看板上的唯一标签及其使用频率
- `list_task_documents` — 获取附加到任务上的文档
- `read_document` — 读取文档内容
- `list_task_comments` — 列出任务的评论

### 创建与修改（仅限 Planner 端点）
- `create_habitat` — 创建新的工作空间（提供名称）
- `create_board` — 创建新的看板（提供名称，可选 `habitatId`、`boardType`）
- `create_task` — 创建任务（提供标题、`boardId` 或 `boardName`，可选 `description`、`dueDate`、`priority`、`labels`）
- `update_task` — 根据 ID 更新任务（提供 `taskId` 及要修改的字段）
- `update_task_by_title` — 根据标题精确匹配更新任务（提供 `titleExact`、`boardId` 或 `boardName`）
- `delete_task` — 永久删除任务（提供 `taskId`）
- `create_document` — 创建文档（可选提供 `relatedTaskId` 以关联任务）
- `add_document_to_task` — 为任务添加文档
- `add_comment` — 为任务添加评论

### 人工智能辅助功能
- `propose_task_variants` — 根据粗略描述生成 2-3 个任务选项（简略/标准/详细）
- `confirm_task_fields` — 在创建前预览选项的字段内容

## OAuth 与身份验证

- **使用 PKCE 的 OAuth 2.1**（RS256 JWT）
- **令牌有效期**：30 天，不提供刷新令牌
- **Planner** (`/mcp`）：具有完整的 CRUD 操作权限（所有权限范围）
- **Worker** (`/mcp-worker`）：支持 `boards:read`、`tasks:read`、`labels:read`、`docs:read`、`comments:read`、`comments:write` 操作
- **尽管没有速率限制，但仍需谨慎使用 API 调用**
- **所有 API 调用都会被服务器记录**

## 常见工作流程

### 查看看板上的所有任务
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

### 在所有工作空间中搜索
```
search_across_habitats { "query": "investor meeting", "limit": 20 }
```

### 监听事件更新（代理循环）
```
get_events_since { "since": "2026-02-24T08:00:00Z", "limit": 200 }
```

## 提示
- 始终先调用 `list_boards` 以获取可用的看板 ID — 不要猜测 UUID。
- 当用户按名称查找看板时，使用 `boardName` 而不是 `boardId`。
- 截止日期应使用 `YYYY-MM-DD` 格式。
- 任务标题最多 80 个字符，描述最多 500 个字符。
- 标签可以是任意格式的字符串（每个任务最多 10 个标签）。
- `update_task` 功能需要任务的 UUID。可以使用 `list_tasks` 查找 UUID，或者仅知道标题时使用 `update_task_by_title`。