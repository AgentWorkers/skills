---
name: vibe-notionbot
description: 使用官方 API 与 Notion 工作区进行交互——管理页面、数据库、区块、用户和评论
version: 0.8.0
allowed-tools: Bash(vibe-notionbot:*)
metadata:
  openclaw:
    requires:
      bins:
        - vibe-notionbot
    install:
      - kind: node
        package: vibe-notion
        bins: [vibe-notionbot]
---
# Vibe Notionbot

这是一个基于TypeScript的命令行工具（CLI），它允许AI代理和人类通过Notion的官方API与Notion工作区进行交互。该工具支持页面、数据库、区块、用户、评论以及搜索等功能。

## 应使用哪个CLI

该工具提供了两个CLI版本，请根据您的需求选择合适的版本：

| | `vibe-notion` | `vibe-notionbot`（当前推荐的CLI） |
|---|---|---|
| API | 非官方的私有API | 官方Notion API |
| 认证 | 从Notion桌面应用自动提取的`token_v2` | 环境变量`NOTION_TOKEN`（集成令牌） |
| 身份识别 | 以用户身份运行 | 以机器人身份运行 |
| 设置 | 无需任何设置——凭证自动提取 | 需要手动在[notion.so/my-integrations]创建集成 |
| 数据库操作 | `add-row`、`update-row` | 通过`page create --database`创建 |
| 视图管理 | `view-get`、`view-update`、`view-list`、`view-add`、`view-delete` | 不支持 |
| 工作区列表 | 支持 | 不支持 |
| 稳定性 | 私有API——可能会因Notion的更新而失效 | 官方API——稳定性更高 |

**决策流程：**

1. 如果安装了Notion桌面应用 → 使用`vibe-notion`
2. 如果设置了`NOTION_TOKEN`但没有安装桌面应用 → 使用`vibe-notionbot`（当前推荐的CLI）
3. 如果两者都可用 → 更推荐使用`vibe-notion`（功能更丰富，无需设置）
4. 如果两者都没有 → 请用户安装其中一个工具

## 重要提示：仅使用CLI

**切勿直接调用Notion API**。请始终使用`vibe-notionbot`提供的CLI命令。不要直接发送原始HTTP请求到Notion API，也不要直接使用`@notionhq/client`。直接调用API可能会导致凭证泄露，并可能触发Notion的滥用检测机制，从而导致用户账户被封禁。

如果您需要的功能未被`vibe-notionbot`支持，请告知用户，并代表他们向[devxoul/vibe-notion](https://github.com/devxoul/vibe-notion/issues)提交功能请求。在提交之前，请删除所有可能识别用户或工作区的信息（如ID、姓名、电子邮件、令牌、页面内容等），仅使用通用占位符来描述问题。

## 重要提示：禁止编写脚本

**禁止编写任何脚本（Python、TypeScript、Bash等）来自动化Notion操作**。`batch`命令已经可以处理任意规模的大量操作。编写脚本来循环调用API是错误的做法——请使用`batch`命令并配合`--file`参数。

以下情况同样适用：
- 需要创建100个以上的页面或区块
- 需要在新创建的项之间建立关联（请参考[批量操作策略](#bulk-operations-strategy)
- 操作规模过大，无法通过单个命令完成

如果您有这样的需求，请立即停止并使用`batch`命令。

## 快速入门

```bash
# Check authentication status
vibe-notionbot auth status

# Search for a page or database
vibe-notionbot search "Project Roadmap"

# List all databases
vibe-notionbot database list

# Create a new page
vibe-notionbot page create --parent <parent_id> --title "My New Page"
```

## 认证

### 集成令牌（官方API）

使用从[Notion开发者门户](https://www.notion.so/my-integrations)获取的集成令牌，设置`NOTION_TOKEN`环境变量。

```bash
export NOTION_TOKEN=secret_xxx
vibe-notionbot auth status
```

集成令牌允许您访问官方Notion API（`@notionhq/client`）。

## 命令

### 页面相关命令

```bash
# Retrieve a page
vibe-notionbot page get <page_id>

# Create a new page under a parent page or database
vibe-notionbot page create --parent <parent_id> --title "New Page Title"
vibe-notionbot page create --parent <database_id> --title "New Database Item" --database

# Create a page with markdown content
vibe-notionbot page create --parent <parent_id> --title "My Doc" --markdown '# Hello\n\nThis is **bold** text.'

# Create a page with markdown from a file
vibe-notionbot page create --parent <parent_id> --title "My Doc" --markdown-file ./content.md

# Create a page with markdown containing local images (auto-uploaded to Notion)
vibe-notionbot page create --parent <parent_id> --title "My Doc" --markdown-file ./doc-with-images.md

# Update page properties
vibe-notionbot page update <page_id> --set "Status=In Progress" --set "Priority=High"

# Replace all content on a page with new markdown
vibe-notionbot page update <page_id> --replace-content --markdown '# New Content'
vibe-notionbot page update <page_id> --replace-content --markdown-file ./updated.md

# Archive (delete) a page
vibe-notionbot page archive <page_id>

# Retrieve a specific page property
vibe-notionbot page property <page_id> <property_id>
```

### 数据库相关命令

```bash
# Retrieve a database schema
vibe-notionbot database get <database_id>

# Query a database with optional filters and sorts
vibe-notionbot database query <database_id> --filter '{"property": "Status", "select": {"equals": "In Progress"}}'
vibe-notionbot database query <database_id> --sort '[{"property": "Created time", "direction": "descending"}]'
vibe-notionbot database query <database_id> --page-size 10 --start-cursor <cursor>

# Create a database under a parent page
vibe-notionbot database create --parent <page_id> --title "My Database" --properties '{"Name": {"title": {}}}'

# Update a database schema or title
vibe-notionbot database update <database_id> --title "Updated Title"

# Delete a property from a database
vibe-notionbot database delete-property <database_id> --property "Status"

# List all databases accessible by the integration
vibe-notionbot database list
vibe-notionbot database list --page-size 10 --start-cursor <cursor>
```

### 区块相关命令

```bash
# Retrieve a block
vibe-notionbot block get <block_id>

# List direct children of a block (paginated)
vibe-notionbot block children <block_id>
vibe-notionbot block children <block_id> --page-size 50 --start-cursor <cursor>

# Append child blocks to a parent
vibe-notionbot block append <parent_id> --content '[{"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Hello World"}}]}}]'

# Append markdown content as blocks
vibe-notionbot block append <parent_id> --markdown '# Hello\n\nThis is **bold** text.'

# Append markdown from a file
vibe-notionbot block append <parent_id> --markdown-file ./content.md

# Append markdown with local images (auto-uploaded to Notion)
vibe-notionbot block append <parent_id> --markdown-file ./doc-with-images.md

# Append nested markdown (indented lists become nested children blocks)
vibe-notionbot block append <parent_id> --markdown '- Parent item\n  - Child item\n    - Grandchild item'

# Append blocks after a specific block (positional insertion)
vibe-notionbot block append <parent_id> --after <block_id> --markdown '# Inserted after specific block'
vibe-notionbot block append <parent_id> --after <block_id> --content '[{"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Inserted after"}}]}}]'

# Append blocks before a specific block
vibe-notionbot block append <parent_id> --before <block_id> --markdown '# Inserted before specific block'

# Update a block's content
vibe-notionbot block update <block_id> --content '{"paragraph": {"rich_text": [{"type": "text", "text": {"content": "Updated content"}}]}}'

# Delete (archive) a block
vibe-notionbot block delete <block_id>

# Upload a file as a block (image or file block)
vibe-notionbot block upload <parent_id> --file ./image.png --pretty
vibe-notionbot block upload <parent_id> --file ./document.pdf --pretty
vibe-notionbot block upload <parent_id> --file ./image.png --after <block_id> --pretty
vibe-notionbot block upload <parent_id> --file ./image.png --before <block_id> --pretty
```

### 用户相关命令

```bash
# List all users in the workspace
vibe-notionbot user list
vibe-notionbot user list --page-size 10 --start-cursor <cursor>

# Get info for a specific user
vibe-notionbot user get <user_id>

# Get info for the current bot/integration
vibe-notionbot user me
```

### 搜索相关命令

```bash
# Search across the entire workspace
vibe-notionbot search "query text"

# Filter search by object type
vibe-notionbot search "Project" --filter page
vibe-notionbot search "Tasks" --filter database

# Sort search results
vibe-notionbot search "Meeting" --sort desc

# Paginate search results
vibe-notionbot search "Notes" --page-size 10 --start-cursor <cursor>
```

### 评论相关命令

```bash
# List comments on a page
vibe-notionbot comment list --page <page_id>
vibe-notionbot comment list --page <page_id> --page-size 10 --start-cursor <cursor>

# List inline comments on a specific block
vibe-notionbot comment list --block <block_id>

# Create a comment on a page
vibe-notionbot comment create "This is a comment" --page <page_id>

# Reply to a comment thread (discussion)
vibe-notionbot comment create "Replying to thread" --discussion <discussion_id>

# Retrieve a specific comment
vibe-notionbot comment get <comment_id>
```

## 批量操作

您可以在一次CLI调用中执行多个写操作。当需要同时创建、更新或删除多个项目时，使用此方法可以节省令牌并减少网络请求次数。

```bash
# Inline JSON (no --workspace-id needed, uses NOTION_TOKEN)
vibe-notionbot batch '<operations_json>'

# From file (for large payloads)
vibe-notionbot batch --file ./operations.json '[]'
```

**支持的操作（共11项）：**

| 操作 | 描述 |
|--------|-------------|
| `page.create` | 创建页面 |
| `page.update` | 更新页面属性 |
| `page.archive` | 将页面归档 |
| `block.append` | 向父区块添加区块 |
| `block.update` | 更新区块 |
| `block.delete` | 删除区块 |
| `comment.create` | 创建评论 |
| `database.create` | 创建数据库 |
| `database.update` | 更新数据库标题或结构 |
| `database.delete-property` | 删除数据库属性 |
| `block.upload` | 上传文件作为图片或文件区块 |

**操作格式**：每个操作都是一个对象，包含`action`以及传递给相应命令的参数。示例（包含多种操作）：

```json
[
  {"action": "page.create", "parent": "<parent_id>", "title": "Meeting Notes"},
  {"action": "block.append", "parent_id": "<page_id>", "markdown": "# Agenda\n\n- Item 1\n- Item 2"},
  {"action": "comment.create", "content": "Page created via batch", "page": "<page_id>"}
]
```

**输出格式**：

```json
{
  "results": [
    {"index": 0, "action": "page.create", "success": true, "data": {"id": "page-uuid", "...": "..."}},
    {"index": 1, "action": "block.append", "success": true, "data": {"...": "..."}},
    {"index": 2, "action": "comment.create", "success": true, "data": {"id": "comment-uuid", "...": "..."}}
  ],
  "total": 3,
  "succeeded": 3,
  "failed": 0
}
```

**错误处理机制**：

操作按顺序执行。如果任何操作失败，整个过程会立即停止。输出将包含所有已完成操作的结果以及失败的操作信息。失败时程序的退出代码为1，成功时为0。

```json
{
  "results": [
    {"index": 0, "action": "page.create", "success": true, "data": {"...": "..."}},
    {"index": 1, "action": "block.append", "success": false, "error": "Block not found"}
  ],
  "total": 3,
  "succeeded": 1,
  "failed": 1
}
```

### 批量操作策略

对于大量操作（数十到数百个项目），请使用`--file`参数来避免超出Shell命令行的参数限制。

**步骤1**：将所有操作写入一个JSON文件，然后使用`--file`参数执行批量操作：

```bash
# Write operations to a file (using your Write tool), then:
vibe-notionbot batch --file ./operations.json '[]'
```

**多步骤处理方式**（当新创建的项目之间需要相互引用时，例如一个页面属性需要引用另一个新创建的页面）：

1. **第一步——创建所有项目**：编写一个包含所有创建操作的JSON文件，省略那些需要引用其他新项目的属性。执行该文件，收集返回的ID。
2. **第二步——设置引用关系**：编写另一个JSON文件，其中包含使用第一步获取的ID来更新相关属性的操作。再次执行该文件。

```
Pass 1: Create items A, B, C (no cross-refs) → get IDs for A, B, C
Pass 2: Update A.related=B, C.parent_ref=A (using real IDs from Pass 1)
```

这种方法与编写脚本的效果相同，但无需编写任何代码，只需执行两次批量操作即可。

### 速率限制

Notion对其API实施了速率限制。批量操作会依次执行，因此大量操作（超过30个）可能会触发“429 Too Many Requests”错误。为了避免这个问题：
- 将大量操作分成每批25-30个的操作
- 如果某批操作中途失败，请仅重新执行剩余的操作
- `batch`命令的输出会显示哪些操作成功了——使用`index`字段来确定从哪里继续执行

## 输出格式

### JSON格式（默认）

所有命令默认以JSON格式输出，便于AI程序处理：

```json
{
  "id": "...",
  "object": "page",
  "properties": { ... }
}
```

### 美化输出（便于人类阅读）

使用`--pretty`参数可以获取格式化的输出：

```bash
vibe-notionbot search "Project" --pretty
```

## 错误处理

Notion API可能返回的常见错误：
- `object_not_found`：ID错误或集成权限不足。
- `unauthorized`：`NOTION_TOKEN`无效。
- `rate_limited`：请求次数过多。

## 故障排除

### `vibe-notionbot: command not found`

说明`vibe-notion`包未安装。请使用包管理工具直接运行该工具。如果用户已经指定了喜欢的包管理工具，请直接使用该工具。

## 限制事项：
- 仅支持Notion API版本2022-06-28。
- 不支持OAuth认证（仅支持令牌认证）。
- **（注：v1.0版本不支持文件上传）** 现在可以通过`block upload`命令上传文件。
- 页面属性的更新仅支持简单的键值对格式，除非使用原始JSON格式。