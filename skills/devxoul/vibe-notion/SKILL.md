---
name: vibe-notion
description: 使用非官方的私有 API 与 Notion 进行交互：页面、数据库、区块、搜索、用户和评论
version: 0.8.1
allowed-tools: Bash(vibe-notion:*)
metadata:
  openclaw:
    requires:
      bins:
        - vibe-notion
    install:
      - kind: node
        package: vibe-notion
        bins: [vibe-notion]
---
# Vibe Notion

这是一个TypeScript命令行工具（CLI），它允许AI代理和人类通过Notion的非官方私有API与Notion工作区进行交互。该工具支持对页面、数据库、区块、搜索和用户管理进行完整的CRUD操作。

> **注意**：此工具使用的是Notion的内部/私有API（`/api/v3/`），这与官方的公共API是分开的。如需访问官方API，请使用`vibe-notionbot`。

## 使用哪个CLI

此包提供了两个CLI工具。根据您的需求选择合适的工具：

| | `vibe-notion` | `vibe-notionbot` |
|---|---|---|
| API | 非官方私有API | 官方Notion API |
| 认证 | 从Notion桌面应用自动提取`token_v2` | 环境变量`NOTION_TOKEN`（集成令牌） |
| 身份 | 以用户身份运行 | 以机器人身份运行 |
| 设置 | 无需设置——凭证自动提取 | 需要手动在notion.so/my-integrations创建集成 |
| 数据库操作 | `add-row`, `update-row` | 通过`page create --database`创建 |
| 视图管理 | `view-get`, `view-update`, `view-list`, `view-add`, `view-delete` | 不支持 |
| 工作区列表 | 支持 | 不支持 |
| 稳定性 | 私有API——Notion更新可能导致问题 | 官方API版本更稳定 |

**决策流程**：

1. 如果安装了Notion桌面应用 → 使用`vibe-notion`（此CLI）
2. 如果设置了`NOTION_TOKEN`但没有桌面应用 → 使用`vibe-notionbot`
3. 如果两者都可用 → 优先选择`vibe-notion`（功能更丰富，无需设置）
4. 如果两者都没有 → 请用户安装其中一个工具

## 重要提示：仅使用CLI

**切勿直接调用Notion的内部API。**始终使用本文档中描述的`vibe-notion` CLI命令。不要直接向`notion.so/api/v3/`发送原始HTTP请求，也不要使用任何Notion客户端库。直接调用API可能会导致凭证泄露，并可能触发Notion的滥用检测，从而导致用户账户被封禁。

如果您需要的功能未被`vibe-notion`支持，请告知用户，并代表他们向[devxoul/vibe-notion](https://github.com/devxoul/vibe-notion/issues)提交功能请求。在提交之前，请删除所有真实用户数据（ID、姓名、电子邮件、令牌、页面内容或其他可能识别用户或其工作区的信息），使用通用占位符，并专注于描述缺失的功能。

## 重要提示：切勿编写脚本

**切勿编写脚本（Python、TypeScript、Bash等）来自动化Notion操作。**`batch`命令已经可以处理任意规模的大量操作。编写脚本来循环调用API总是错误的——请使用`batch`和`--file`选项。

即使在以下情况下也适用：
- 需要创建100多行数据
- 需要在新创建的行之间建立关联（请使用多步骤批量操作——参见[批量操作策略](#bulk-operations-strategy)
- 操作规模“太大”，无法通过单个命令完成

如果您有这样的想法，请停止并使用`batch`。

## 快速入门

```bash
# 1. Find your workspace ID
vibe-notion workspace list --pretty

# 2. Search for a page
vibe-notion search "Roadmap" --workspace-id <workspace-id> --pretty

# 3. Get page content
vibe-notion page get <page-id> --workspace-id <workspace-id> --pretty

# 4. Query a database
vibe-notion database query <collection-id> --workspace-id <workspace-id> --pretty
```

首次使用时，凭证会从Notion桌面应用自动提取。无需手动设置。

> **重要提示**：所有在特定工作区内执行的命令都需要`--workspace-id`参数。使用`vibe-notion workspace list`来查找您的工作区ID。

## 认证

运行任何命令时，凭证（`token_v2`）会从Notion桌面应用自动提取。无需API密钥、OAuth或手动提取。

在macOS上，系统可能在首次使用时提示您访问Keychain——这是正常的，也是解密cookie所必需的。

提取的`token_v2`会存储在`~/.config/vibe-notion/credentials.json`文件中，文件权限设置为`0600`。

## 内存管理

代理会维护一个`~/.config/vibe-notion/MEMORY.md`文件作为会话间的持久内存。此文件由代理管理——CLI不会读取或写入该文件。使用`Read`和`Write`工具来管理这个内存文件。

### 读取内存

**在每个任务开始时**，使用`Read`工具读取`~/.config/vibe-notion/MEMORY.md`文件，以加载之前发现的工作区ID、页面ID、数据库ID和用户偏好设置。

- 如果文件尚不存在，可以忽略它，并在首次有需要存储的信息时创建该文件。
- 如果文件无法读取（权限问题或目录缺失），可以忽略内存信息——不要报错。

### 写入内存

在发现有用信息后，使用`Write`工具更新`~/.config/vibe-notion/MEMORY.md`文件。触发写入操作的场景包括：
- 发现工作区ID后
- 发现页面ID、数据库ID或集合ID后（来自`search`、`page list`、`page get`、`database list`等）
- 用户提供了别名或偏好设置后（例如，“将此称为任务数据库”或“我的主工作区是X”）
- 发现页面/数据库结构后（父子关系、哪些数据库属于哪些页面）

写入时，请包含**完整的文件内容**——`Write`工具会覆盖整个文件。

### 应存储的内容**

- 带有名称的工作区ID
- 带有标题和父级信息的页面ID
- 带有标题和父级信息的数据库/集合ID
- 用户指定的别名（如“任务数据库”、“主工作区”
- 常使用的视图ID
- 父子关系（哪些数据库属于哪些页面）
- 用户在交互过程中表达的任何偏好设置

### 不应存储的内容

切勿存储`token_v2`、凭证、API密钥或任何敏感数据。切勿存储完整的页面内容（仅存储ID和标题）。除非是持久引用（如数据库区块），否则不要存储区块级别的ID。

### 处理过时数据

如果存储的ID返回错误（页面未找到、访问被拒绝），请从`MEMORY.md`中删除该ID。不要盲目信任存储的数据——在数据似乎有问题时重新搜索。

### 格式/示例

以下是一个`MEMORY.md`文件的结构示例：

```markdown
# Vibe Notion Memory

## Workspaces

- `abc123-...` — Acme Corp (default)

## Pages (Acme Corp)

- `page-id-1` — Product Roadmap (top-level)
- `page-id-2` — Q1 Planning (under Product Roadmap)

## Databases (Acme Corp)

- `coll-id-1` — Tasks (under Product Roadmap, views: `view-1`)
- `coll-id-2` — Contacts (top-level)

## Aliases

- "roadmap" → `page-id-1` (Product Roadmap)
- "tasks" → `coll-id-1` (Tasks database)

## Notes

- User prefers --pretty output for search results
- Main workspace is "Acme Corp"
```

> 内存功能可以避免重复执行`search`和`workspace list`命令。如果您在之前的会话中已经知道某个ID，可以直接使用它。

## 命令

### 认证命令

```bash
vibe-notion auth status     # Check authentication status
vibe-notion auth logout     # Remove stored token_v2
vibe-notion auth extract    # Manually re-extract token_v2 (for troubleshooting)
```

### 页面命令

```bash
# List pages in a space (top-level only)
vibe-notion page list --workspace-id <workspace_id> --pretty
vibe-notion page list --workspace-id <workspace_id> --depth 2 --pretty

# Get a page and all its content blocks
vibe-notion page get <page_id> --workspace-id <workspace_id> --pretty
vibe-notion page get <page_id> --workspace-id <workspace_id> --limit 50
vibe-notion page get <page_id> --workspace-id <workspace_id> --backlinks --pretty

# Create a new page (--parent is optional; omit to create at workspace root)
vibe-notion page create --workspace-id <workspace_id> --parent <parent_id> --title "My Page" --pretty
vibe-notion page create --workspace-id <workspace_id> --title "New Root Page" --pretty


# Create a page with markdown content
vibe-notion page create --workspace-id <workspace_id> --parent <parent_id> --title "My Doc" --markdown '# Hello\n\nThis is **bold** text.'

# Create a page with markdown from a file
vibe-notion page create --workspace-id <workspace_id> --parent <parent_id> --title "My Doc" --markdown-file ./content.md

# Create a page with markdown containing local images (auto-uploaded to Notion)
vibe-notion page create --workspace-id <workspace_id> --parent <parent_id> --title "My Doc" --markdown-file ./doc-with-images.md

# Replace all content on a page with new markdown
vibe-notion page update <page_id> --workspace-id <workspace_id> --replace-content --markdown '# New Content'
vibe-notion page update <page_id> --workspace-id <workspace_id> --replace-content --markdown-file ./updated.md

# Update page title or icon
vibe-notion page update <page_id> --workspace-id <workspace_id> --title "New Title" --pretty
vibe-notion page update <page_id> --workspace-id <workspace_id> --icon "🚀" --pretty

# Archive a page
vibe-notion page archive <page_id> --workspace-id <workspace_id> --pretty
```

### 数据库命令

```bash
# Get database schema
vibe-notion database get <database_id> --workspace-id <workspace_id> --pretty

# Query a database (auto-resolves default view)
vibe-notion database query <database_id> --workspace-id <workspace_id> --pretty
vibe-notion database query <database_id> --workspace-id <workspace_id> --limit 10 --pretty
vibe-notion database query <database_id> --workspace-id <workspace_id> --view-id <view_id> --pretty
vibe-notion database query <database_id> --workspace-id <workspace_id> --search-query "keyword" --pretty
vibe-notion database query <database_id> --workspace-id <workspace_id> --timezone "America/New_York" --pretty

# Query with filter and sort (uses property IDs from database get schema)
vibe-notion database query <database_id> --workspace-id <workspace_id> --filter '<filter_json>' --pretty
vibe-notion database query <database_id> --workspace-id <workspace_id> --sort '<sort_json>' --pretty

# List all databases in workspace
vibe-notion database list --workspace-id <workspace_id> --pretty

# Create a database
vibe-notion database create --workspace-id <workspace_id> --parent <page_id> --title "Tasks" --pretty
vibe-notion database create --workspace-id <workspace_id> --parent <page_id> --title "Tasks" --properties '{"status":{"name":"Status","type":"select"}}' --pretty

# Update database title or schema
vibe-notion database update <database_id> --workspace-id <workspace_id> --title "New Name" --pretty

# Add a row to a database
vibe-notion database add-row <database_id> --workspace-id <workspace_id> --title "Row title" --pretty
vibe-notion database add-row <database_id> --workspace-id <workspace_id> --title "Row title" --properties '{"Status":"In Progress","Due":{"start":"2025-03-01"}}' --pretty

# Add row with date range
vibe-notion database add-row <database_id> --workspace-id <workspace_id> --title "Event" --properties '{"Due":{"start":"2026-01-01","end":"2026-01-15"}}' --pretty

# Update properties on an existing database row (row_id from database query)
vibe-notion database update-row <row_id> --workspace-id <workspace_id> --properties '{"Status":"Done"}' --pretty
vibe-notion database update-row <row_id> --workspace-id <workspace_id> --properties '{"Priority":"High","Tags":["backend","infra"]}' --pretty
vibe-notion database update-row <row_id> --workspace-id <workspace_id> --properties '{"Due":{"start":"2026-06-01"},"Status":"In Progress"}' --pretty
vibe-notion database update-row <row_id> --workspace-id <workspace_id> --properties '{"Due":{"start":"2026-01-01","end":"2026-01-15"}}' --pretty
vibe-notion database update-row <row_id> --workspace-id <workspace_id> --properties '{"Related":["<target_row_id>"]}' --pretty

# Delete a property from a database (cannot delete the title property)
vibe-notion database delete-property <database_id> --workspace-id <workspace_id> --property "Status" --pretty

# Get view configuration and property visibility
vibe-notion database view-get <view_id> --workspace-id <workspace_id> --pretty

# Show or hide properties on a view (comma-separated names)
vibe-notion database view-update <view_id> --workspace-id <workspace_id> --show "ID,Due" --pretty
vibe-notion database view-update <view_id> --workspace-id <workspace_id> --hide "Assignee" --pretty
vibe-notion database view-update <view_id> --workspace-id <workspace_id> --show "Status" --hide "Due" --pretty

# Reorder columns (comma-separated names in desired order; unmentioned columns appended)
vibe-notion database view-update <view_id> --workspace-id <workspace_id> --reorder "Name,Status,Priority,Date" --pretty
vibe-notion database view-update <view_id> --workspace-id <workspace_id> --reorder "Name,Status" --show "Status" --pretty

# Resize columns (JSON mapping property names to pixel widths)
vibe-notion database view-update <view_id> --workspace-id <workspace_id> --resize '{"Name":200,"Status":150}' --pretty

# List all views for a database
vibe-notion database view-list <database_id> --workspace-id <workspace_id> --pretty

# Add a new view to a database (default type: table)
vibe-notion database view-add <database_id> --workspace-id <workspace_id> --pretty
vibe-notion database view-add <database_id> --workspace-id <workspace_id> --type board --name "Board View" --pretty

# Delete a view from a database (cannot delete the last view)
vibe-notion database view-delete <view_id> --workspace-id <workspace_id> --pretty
```

### 区块命令

```bash
# Get a specific block
vibe-notion block get <block_id> --workspace-id <workspace_id> --pretty
vibe-notion block get <block_id> --workspace-id <workspace_id> --backlinks --pretty

# List child blocks
vibe-notion block children <block_id> --workspace-id <workspace_id> --pretty
vibe-notion block children <block_id> --workspace-id <workspace_id> --limit 50 --pretty
vibe-notion block children <block_id> --workspace-id <workspace_id> --start-cursor '<next_cursor_json>' --pretty

# Append child blocks
vibe-notion block append <parent_id> --workspace-id <workspace_id> --content '[{"type":"text","properties":{"title":[["Hello world"]]}}]' --pretty

# Append markdown content as blocks
vibe-notion block append <parent_id> --workspace-id <workspace_id> --markdown '# Hello\n\nThis is **bold** text.'

# Append markdown from a file
vibe-notion block append <parent_id> --workspace-id <workspace_id> --markdown-file ./content.md

# Append markdown with local images (auto-uploaded to Notion)
vibe-notion block append <parent_id> --workspace-id <workspace_id> --markdown-file ./doc-with-images.md

# Append nested markdown (indented lists become nested children blocks)
vibe-notion block append <parent_id> --workspace-id <workspace_id> --markdown '- Parent item\n  - Child item\n    - Grandchild item'

# Append blocks after a specific block (positional insertion)
vibe-notion block append <parent_id> --workspace-id <workspace_id> --after <block_id> --markdown '# Inserted after specific block'
vibe-notion block append <parent_id> --workspace-id <workspace_id> --after <block_id> --content '[{"type":"text","properties":{"title":[["Inserted after"]]}}]'

# Append blocks before a specific block
vibe-notion block append <parent_id> --workspace-id <workspace_id> --before <block_id> --markdown '# Inserted before specific block'

# Update a block
vibe-notion block update <block_id> --workspace-id <workspace_id> --content '{"properties":{"title":[["Updated text"]]}}' --pretty

# Delete a block
vibe-notion block delete <block_id> --workspace-id <workspace_id> --pretty

# Upload a file as a block (image or file block)
vibe-notion block upload <parent_id> --workspace-id <workspace_id> --file ./image.png --pretty
vibe-notion block upload <parent_id> --workspace-id <workspace_id> --file ./document.pdf --pretty
vibe-notion block upload <parent_id> --workspace-id <workspace_id> --file ./image.png --after <block_id> --pretty
vibe-notion block upload <parent_id> --workspace-id <workspace_id> --file ./image.png --before <block_id> --pretty

# Move a block to a new position
vibe-notion block move <block_id> --workspace-id <workspace_id> --parent <parent_id> --pretty
vibe-notion block move <block_id> --workspace-id <workspace_id> --parent <parent_id> --after <sibling_id> --pretty
vibe-notion block move <block_id> --workspace-id <workspace_id> --parent <parent_id> --before <sibling_id> --pretty
```

### 区块类型参考

内部API使用特定的区块格式。以下是所有支持的区块类型：

#### 标题

```json
{"type": "header", "properties": {"title": [["Heading 1"]]}}
{"type": "sub_header", "properties": {"title": [["Heading 2"]]}}
{"type": "sub_sub_header", "properties": {"title": [["Heading 3"]]}}
```

#### 文本

```json
{"type": "text", "properties": {"title": [["Plain text paragraph"]]}}
```

#### 列表

```json
{"type": "bulleted_list", "properties": {"title": [["Bullet item"]]}}
{"type": "numbered_list", "properties": {"title": [["Numbered item"]]}}
```

#### 嵌套子节点

列表区块支持通过`children`属性嵌套子节点：

```json
{"type": "bulleted_list", "properties": {"title": [["Parent"]]}, "children": [{"type": "bulleted_list", "properties": {"title": [["Child"]]}}]}
```

#### 待办事项/复选框

```json
{"type": "to_do", "properties": {"title": [["Task item"]], "checked": [["Yes"]]}}
{"type": "to_do", "properties": {"title": [["Unchecked task"]], "checked": [["No"]]}}
```

#### 代码区块

```json
{"type": "code", "properties": {"title": [["console.log('hello')"]], "language": [["javascript"]]}}
```

#### 引用

```json
{"type": "quote", "properties": {"title": [["Quoted text"]]}}
```

#### 分隔符

```json
{"type": "divider"}
```

### 富文本格式

富文本使用嵌套数组和格式代码：

| 格式 | 语法 | 示例 |
|--------|--------|---------|
| 普通文本 | `[["text"]]` | `[["Hello"]]` |
| 加粗 | `["text", [["b"]]]` | `["Hello", [["b"]]]` |
| 斜体 | `["text", ["i"]]]` | `["Hello", ["i"]]]` |
| 下划线 | `["text", ["s"]]]` | `["Hello", ["s"]]]` |
| 内联代码 | `["text", ["c"]]]` | `["Hello", ["c"]]]` |
| 链接 | `["text", ["a", "url"]]]` | `["Click", ["a", "https://example.com"]]]` |
| 加粗 + 斜体 | `["text", ["b"], ["i"]]]` | `["Hello", ["b"], ["i"]]]` |

多个段落：`[["plain "], ["bold", ["b"]]], [" more plain"]`

### 评论命令

```bash
# List comments on a page
vibe-notion comment list --page <page_id> --workspace-id <workspace_id> --pretty

# List inline comments on a specific block
vibe-notion comment list --page <page_id> --block <block_id> --workspace-id <workspace_id> --pretty

# Create a comment on a page (starts a new discussion)
vibe-notion comment create "This is a comment" --page <page_id> --workspace-id <workspace_id> --pretty

# Reply to an existing discussion thread
vibe-notion comment create "Replying to thread" --discussion <discussion_id> --workspace-id <workspace_id> --pretty

# Get a specific comment by ID
vibe-notion comment get <comment_id> --workspace-id <workspace_id> --pretty
```

## 批量操作

您可以在一次CLI调用中执行多个写入操作。当需要同时创建、更新或删除多个项目时，使用此方法。这样可以节省令牌并减少往返次数。

```bash
# Inline JSON
vibe-notion batch --workspace-id <workspace_id> '<operations_json>'

# From file (for large payloads)
vibe-notion batch --workspace-id <workspace_id> --file ./operations.json '[]'
```

**支持的操作**（共13个）：

| 操作 | 描述 |
|--------|-------------|
| `page.create` | 创建页面 |
| `page.update` | 更新页面标题、图标或内容 |
| `page.archive` | 将页面归档 |
| `block.append` | 向父区块添加区块 |
| `block.update` | 更新区块 |
| `block.delete` | 删除区块 |
| `comment.create` | 创建评论 |
| `database.create` | 创建数据库 |
| `database.update` | 更新数据库标题或模式 |
| `database.delete-property` | 删除数据库属性 |
| `database.add-row` | 向数据库添加行 |
| `database.update-row` | 更新数据库行的属性 |
| `block.upload` | 上传文件作为图片或文件区块 |

**操作格式**：每个操作都是一个对象，包含`action`以及传递给相应命令处理器的相同字段。以下是一个包含多种操作的示例：

```json
[
  {"action": "database.add-row", "database_id": "<db_id>", "title": "Task A", "properties": {"Status": "To Do"}},
  {"action": "database.add-row", "database_id": "<db_id>", "title": "Task B", "properties": {"Status": "In Progress"}},
  {"action": "page.update", "page_id": "<page_id>", "title": "Updated Summary"}
]
```

**输出格式**

```json
{
  "results": [
    {"index": 0, "action": "database.add-row", "success": true, "data": {"id": "row-uuid-1", "...": "..."}},
    {"index": 1, "action": "database.add-row", "success": true, "data": {"id": "row-uuid-2", "...": "..."}},
    {"index": 2, "action": "page.update", "success": true, "data": {"id": "page-uuid", "...": "..."}}
  ],
  "total": 3,
  "succeeded": 3,
  "failed": 0
}
```

**快速失败机制**：操作按顺序执行。如果任何操作失败，执行会立即停止。输出将包含所有已完成操作的结果以及失败的操作的结果。失败时进程以代码1退出，成功时以代码0退出。

```json
{
  "results": [
    {"index": 0, "action": "database.add-row", "success": true, "data": {"...": "..."}},
    {"index": 1, "action": "page.update", "success": false, "error": "Page not found"}
  ],
  "total": 3,
  "succeeded": 1,
  "failed": 1
}
```

### 批量操作策略

对于大量操作（数十个或数百个项目），使用`--file`参数以避免shell参数限制，使操作更易于管理。

**步骤1**：将操作信息写入文件，然后使用`--file`参数运行批量操作：

```bash
# Write operations to a file (using your Write tool), then:
vibe-notion batch --workspace-id <workspace_id> --file ./operations.json '[]'
```

**多步骤模式**——当新行之间需要建立关联时（例如，行A指向行B的关系属性）：

1. **第一步——创建所有行**（不包含关联属性）：编写一个包含所有`database.add-row`操作的批量JSON文件，省略指向其他新行的关联属性。运行该文件并收集返回的ID。
2. **第二步——设置关联**：编写第二个批量JSON文件，使用第一步中的ID来设置关联属性。运行该文件。

```
Pass 1: Create rows A, B, C (no cross-refs) → get IDs for A, B, C
Pass 2: Update A.predecessor=B, C.related=A (using real IDs from Pass 1)
```

这与编写脚本的效果相同，但无需编写任何代码。只需进行两次批量调用即可。

### 速率限制

Notion对其API实施了速率限制。批量操作是顺序执行的，因此大量操作（30个以上）可能会触发**429 Too Many Requests**错误。为了避免这种情况：

- 将大型批量操作分成每批25-30个操作
- 如果批量操作在中间失败，重新运行仅包含未处理操作的批次
- `batch`的输出会显示哪些操作成功了——使用`index`字段来确定从哪里继续

### 搜索命令

```bash
# Search across workspace (--workspace-id is required)
vibe-notion search "query" --workspace-id <workspace_id> --pretty
vibe-notion search "query" --workspace-id <workspace_id> --limit 10 --pretty
vibe-notion search "query" --workspace-id <workspace_id> --start-cursor <offset> --pretty
vibe-notion search "query" --workspace-id <workspace_id> --sort lastEdited --pretty
```

### 用户命令

```bash
# Get current user info
vibe-notion user me --pretty

# Get a specific user
vibe-notion user get <user_id> --workspace-id <workspace_id> --pretty
```

## 输出格式

### JSON（默认）

所有命令默认输出JSON格式，以便AI处理：

```bash
# Search results
vibe-notion search "Roadmap" --workspace-id <workspace_id>
```
```json
{
  "results": [
    {
      "id": "305c0fcf-90b3-807a-bc1a-dc7cc18e0022",
      "title": "Getting Started",
      "score": 76.58
    }
  ],
  "has_more": true,
  "next_cursor": "20",
  "total": 100
}
```

```bash
# Database query — properties use human-readable field names from the collection schema
vibe-notion database query <database_id> --workspace-id <workspace_id>
```
```json
{
  "results": [
    {
      "id": "row-uuid",
      "properties": {
        "Name": "Acme Corp",
        "Status": "Active",
        "Type": "Enterprise"
      }
    }
  ],
  "has_more": false,
  "next_cursor": null
}
```

### 模式提示（`$hints`）

当数据库模式出现问题时，`database get`和`database query`可能会包含`$hints`数组。这些是可操作的警告——请按照每个提示中的说明来解决问题。

```json
{
  "id": "collection-uuid",
  "name": "My Database",
  "schema": { "Name": "title", "Status": "select" },
  "$hints": [
    "Rollup 'Revenue Sum' depends on deleted relation 'Deals'. This rollup will return empty values. Fix: run `database delete-property --property \"Revenue Sum\"` to remove it."
  ]
}
```

**当 `$hints` 存在时**：仔细阅读每个提示并执行建议的修复命令。损坏的属性可能会导致Notion应用程序崩溃。常见的问题包括：
- **已删除但仍在模式中的属性**：通常无害，但表明过去存在问题。
- **损坏的关联**：引用的集合已删除或缺失。可能会导致返回空值，并可能使Notion崩溃。
- **损坏的关系**：目标集合缺失。可能会导致Notion崩溃。

如果 `$hints` 不存在，说明模式是正常的——无需采取任何操作。

```bash
# Page get — returns page metadata with content blocks
vibe-notion page get <page_id> --workspace-id <workspace_id>
```
```json
{
  "id": "page-uuid",
  "title": "My Page",
  "blocks": [
    { "id": "block-1", "type": "text", "text": "Hello world" },
    { "id": "block-2", "type": "to_do", "text": "Task item" }
  ]
}
```

```bash
# With --backlinks: includes pages that link to this page/block
vibe-notion page get <page_id> --workspace-id <workspace_id> --backlinks
vibe-notion block get <block_id> --workspace-id <workspace_id> --backlinks
```
```json
{
  "id": "page-uuid",
  "title": "My Page",
  "blocks": [...],
  "backlinks": [
    { "id": "linking-page-uuid", "title": "Page That Links Here" }
  ]
}
```

```bash
# Block get — collection_view blocks include collection_id and view_ids
vibe-notion block get <block_id> --workspace-id <workspace_id>
```

### 人类可读格式

使用`--pretty`标志可以获取格式化的输出：

```bash
vibe-notion search "Roadmap" --workspace-id <workspace_id> --pretty
```

## 何时使用 `--backlinks`

`--backlinks` 参数可以显示哪些页面/数据库链接到了给定的页面。这对于高效导航非常有用。

**在以下情况下使用 `--backlinks`**：
- **追踪关联**：搜索结果看起来像是一个选择选项、枚举值或关联目标（例如，计划名称或类别）。`--backlinks` 可以立即显示所有通过关联属性引用它的页面/行——无需手动查找父数据库。
- **查找引用**：您找到了一个页面，想知道其他页面是否提到了它或链接到了它。
- **反向查找**：不需要查询每个数据库来查找指向该页面的行，可以直接使用目标页面上的`--backlinks`。

**示例——查找使用特定计划的人**：
```bash
# BAD: 15 API calls — search, open empty pages, trace parents, find database, query
vibe-notion search "Enterprise Plan" ...
vibe-notion page get <plan-page-id> ...  # empty
vibe-notion block get <plan-page-id> ...  # find parent
# ... many more calls to discover the database

# GOOD: 2-3 API calls — search, then backlinks on the target
vibe-notion search "Enterprise Plan" ...
vibe-notion page get <plan-page-id> --backlinks --pretty
# → backlinks immediately show all people/rows linked to this plan
```

## 分页

返回列表的命令支持通过`has_more`和`next_cursor`字段进行分页：

- **`block children`**：基于游标。从前一个响应中传递`next_cursor`值作为`--start-cursor`。
- **`search`**：基于偏移量。传递`next_cursor`值（一个数字）作为`--start-cursor`。
- **`database query`**：使用`--limit`来控制页面大小。`has_more` 表示还有更多结果，但私有API不支持基于游标的分页——增加`--limit`来获取更多行。

## 故障排除

### 认证失败

如果自动提取失败（例如，未安装Notion桌面应用或未登录），请手动运行提取命令以获取调试信息：

```bash
vibe-notion auth extract --debug
```

这将显示Notion的目录路径和提取步骤，有助于诊断问题。

### `vibe-notion: command not found`

`vibe-notion`包未安装。请使用包管理器直接运行它。如果已知用户偏好的包管理器，请直接使用该工具。

## 限制

- 自动提取功能支持macOS和Linux系统。Windows的DPAPI解密功能尚未支持。
- `token_v2` 使用的是非官方的内部API，如果Notion对其进行更改，可能会导致功能失效。
- 这是一个私有/非官方API，Notion官方并不支持它。