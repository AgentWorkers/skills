---
name: notion-sync
description: **Notion页面与数据库的双向同步与管理功能**  
适用于需要使用Notion工作空间进行协作编辑、研究记录、项目管理的场景，或者当您需要将Markdown文件同步到/从Notion页面中，或监控Notion页面的变更时。
homepage: https://github.com/robansuini/agent-skills
repository: https://github.com/robansuini/agent-skills/tree/main/productivity/notion-sync
license: MIT
---

# Notion 同步工具

本工具支持 markdown 文件与 Notion 页面之间的双向同步，并提供数据库管理功能，可用于研究内容跟踪和项目管理。

## 升级说明

**从 v2.0 开始：**
- 将 `--token "ntn_..."` 替换为 `--token-file`、`--token-stdin` 或环境变量 `NOTION_API_KEY`。单独使用 `--token` 的方式已不再被支持（凭证信息不应出现在进程列表中）。
- 有关从 v1.x 升级的详细信息，请参阅 v2.0 的变更日志。

## 系统要求

- **Node.js** v18 或更高版本
- 需要一个 Notion 集成令牌（以 `ntn_` 或 `secret_` 开头）

## 设置步骤

1. 访问 [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)。
2. 创建一个新的集成（或使用现有的集成）。
3. 复制“内部集成令牌”（Internal Integration Token）。
4. 使用以下方法之一传递令牌（按安全性优先级排序）：

   - **选项 A — 令牌文件（推荐）：**
     ```bash
   echo "ntn_your_token" > ~/.notion-token && chmod 600 ~/.notion-token
   node scripts/search-notion.js "query" --token-file ~/.notion-token
   ```

   - **选项 B — 标准输入（stdin）：**
     ```bash
   echo "$NOTION_API_KEY" | node scripts/search-notion.js "query" --token-stdin
   ```

   - **选项 C — 环境变量：**
     ```bash
   export NOTION_API_KEY="ntn_your_token"
   node scripts/search-notion.js "query"
   ```

5. 将你的 Notion 页面/数据库共享给该集成：
   - 在 Notion 中打开相应的页面/数据库。
   - 点击“共享”（Share）→“邀请”（Invite）。
   - 选择你的集成。

## 核心功能

### 1. 搜索页面和数据库

可以通过标题或内容在 Notion 工作区中进行搜索。

```bash
node scripts/search-notion.js "<query>" [--filter page|database] [--limit 10]
```

**示例：**
```bash
# Search for newsletter-related pages
node scripts/search-notion.js "newsletter"

# Find only databases
node scripts/search-notion.js "research" --filter database

# Limit results
node scripts/search-notion.js "AI" --limit 5
```

**输出结果：**
```json
[
  {
    "id": "page-id-here",
    "object": "page",
    "title": "Newsletter Draft",
    "url": "https://notion.so/...",
    "lastEdited": "2026-02-01T09:00:00.000Z"
  }
]
```

### 2. 带有过滤条件的数据库查询

可以使用高级过滤条件和排序功能查询数据库内容。

```bash
node scripts/query-database.js <database-id> [--filter <json>] [--sort <json>] [--limit 10]
```

**示例：**
```bash
# Get all items
node scripts/query-database.js xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Filter by Status = "Complete"
node scripts/query-database.js <db-id> \
  --filter '{"property": "Status", "select": {"equals": "Complete"}}'

# Filter by Tags containing "AI"
node scripts/query-database.js <db-id> \
  --filter '{"property": "Tags", "multi_select": {"contains": "AI"}}'

# Sort by Date descending
node scripts/query-database.js <db-id> \
  --sort '[{"property": "Date", "direction": "descending"}]'

# Combine filter + sort
node scripts/query-database.js <db-id> \
  --filter '{"property": "Status", "select": {"equals": "Complete"}}' \
  --sort '[{"property": "Date", "direction": "descending"}]'
```

**常见过滤模式：**
- 等于：`{"property": "Status", "select": {"equals": "Done"}}`
- 多选包含：`{"property": "Tags", "multi_select": {"contains": "AI"}}`
- 日期在之后：`{"property": "Date", "date": {"after": "2024-01-01"}}`
- 复选框为真：`{"property": "Published", "checkbox": {"equals": true}}`
- 数字大于：`{"property": "Count", "number": {"greater_than": 100}}`

### 3. 更新页面属性

可以更新数据库页面的属性（如状态、标签、日期等）。

```bash
node scripts/update-page-properties.js <page-id> <property-name> <value> [--type <type>]
```

**支持的属性类型：** select, multi_select, checkbox, number, url, email, date, rich_text

**示例：**
```bash
# Set status
node scripts/update-page-properties.js <page-id> Status "Complete" --type select

# Add multiple tags
node scripts/update-page-properties.js <page-id> Tags "AI,Leadership,Research" --type multi_select

# Set checkbox
node scripts/update-page-properties.js <page-id> Published true --type checkbox

# Set date
node scripts/update-page-properties.js <page-id> "Publish Date" "2024-02-01" --type date

# Set URL
node scripts/update-page-properties.js <page-id> "Source URL" "https://example.com" --type url

# Set number
node scripts/update-page-properties.js <page-id> "Word Count" 1200 --type number
```

### 4. 将 Markdown 内容同步到 Notion

可以将 markdown 内容推送至 Notion，并保留所有格式。

```bash
node scripts/md-to-notion.js \
  "<markdown-file-path>" \
  "<notion-parent-page-id>" \
  "<page-title>"
```

**示例：**
```bash
node scripts/md-to-notion.js \
  "projects/newsletter-draft.md" \
  "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" \
  "Newsletter Draft - Feb 2026"
```

**支持的格式：**
- 标题（H1-H3）
- 加粗/斜体文本
- 链接
- 列表
- 带有语法高亮的代码块
- 水平分隔线
- 段落

**特性：**
- 批量上传（每次请求最多 100 个代码块）
- 自动限速（每次批量上传之间间隔 350 毫秒）
- 返回 Notion 页面的 URL 和 ID

**输出结果：**
```
Parsed 294 blocks from markdown
✓ Created page: https://www.notion.so/[title-and-id]
✓ Appended 100 blocks (100-200)
✓ Appended 94 blocks (200-294)

✅ Successfully created Notion page!
```

### 5. 将 Notion 页面内容同步到 Markdown

可以从 Notion 获取页面内容并将其转换为 markdown 格式。

```bash
node scripts/notion-to-md.js <page-id> [output-file]
```

**示例：**
```bash
node scripts/notion-to-md.js \
  "abc123-example-page-id-456def" \
  "newsletter-updated.md"
```

**特性：**
- 将 Notion 的内容转换为 markdown 格式
- 保留格式（标题、列表、代码、引号等）
- 可选择将结果写入文件或标准输出（stdout）

### 6. 变更检测与监控

监控 Notion 页面的更改，并与本地 markdown 文件进行比较。

```bash
node scripts/watch-notion.js --token-file ~/.notion-token "<page-id>" "<local-markdown-path>"
```

**示例：**
```bash
node scripts/watch-notion.js --token-file ~/.notion-token \
  "abc123-example-page-id-456def" \
  "projects/newsletter-draft.md"
```

**状态跟踪：** 变更信息存储在 `memory/notion-watch-state.json` 文件中：
```json
{
  "pages": {
    "<page-id>": {
      "lastEditedTime": "2026-01-30T08:57:00.000Z",
      "lastChecked": "2026-01-31T19:41:54.000Z",
      "title": "Your Page Title"
    }
  }
}
```

**自动监控：** 可使用 cron、CI 流程或任何任务调度器定期检查：
```bash
# Example: cron job every 2 hours during work hours
0 9-21/2 * * * cd /path/to/workspace && node scripts/watch-notion.js "<page-id>" "<local-path>"
```

当 `hasChanges` 为 `true` 时，脚本会将结果输出为 JSON 格式，可通过任何通知系统接收。

### 7. 数据库管理

#### 向数据库添加 Markdown 内容

可以将 markdown 文件作为新页面添加到 Notion 数据库中。

```bash
node scripts/add-to-database.js <database-id> "<page-title>" <markdown-file-path>
```

**示例：**
```bash
# Add research output
node scripts/add-to-database.js \
  xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx \
  "Research Report - Feb 2026" \
  projects/research-insights.md

# Add project notes
node scripts/add-to-database.js \
  <project-db-id> \
  "Sprint Retrospective" \
  docs/retro-2026-02.md

# Add meeting notes
node scripts/add-to-database.js \
  <notes-db-id> \
  "Weekly Team Sync" \
  notes/sync-2026-02-06.md
```

**特性：**
- 创建带有标题属性的数据库页面
- 将 markdown 转换为 Notion 的格式（标题、段落、分隔线等）
- 支持批量上传大文件
- 返回页面的 URL 以便立即访问

**注意：** 创建后需在 Notion 界面手动设置额外的属性（如类型、标签、状态等）。

#### 检查数据库架构

```bash
node scripts/get-database-schema.js <database-id>
```

**示例输出：**
```json
{
  "object": "database",
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "title": [{"plain_text": "Ax Resources"}],
  "properties": {
    "Name": {"type": "title"},
    "Type": {"type": "select"},
    "Tags": {"type": "multi_select"}
  }
}
```

**使用场景：**
- 设置新的数据库集成
- 调试属性名称/类型
- 了解数据库结构

#### 归档页面

```bash
node scripts/delete-notion-page.js <page-id>
```

**注意：** 这只是将页面标记为已归档（设置 `archived: true`），并非永久删除。

## 常见工作流程

### 协作编辑流程

1. 将本地草稿推送到 Notion：
   ```bash
   node scripts/md-to-notion.js draft.md <parent-id> "Draft Title"
   ```

2. 用户在 Notion 中进行编辑（支持任何设备）。

3. 监控更改：
   ```bash
   node scripts/watch-notion.js
   # Returns hasChanges: true when edited
   ```

4. 将更新内容拉取回来：
   ```bash
   node scripts/notion-to-md.js <page-id> draft-updated.md
   ```

5. 根据需要重复上述步骤（更新同一页面，避免生成重复版本）。

### 研究成果跟踪

1. 在本地生成研究内容（例如通过子代理）。
2. 将内容同步到 Notion 数据库：
   ```bash
   node scripts/add-research-to-db.js
   ```

3. 用户在 Notion 界面添加元数据（类型、标签、状态等）。
4. 通过 Notion 的网页或移动应用随时访问这些内容。

### 页面 ID 提取

从 Notion URL `https://notion.so/Page-Title-abc123-example-page-id-456def` 中提取页面 ID：
- 提取格式：`abc123-example-page-id-456def`（位于标题之后的部分）
- 或使用 32 个字符的格式：`abc123examplepageid456def`（ hyphens 可选）

## 限制事项

- **属性更新：** 数据库属性（类型、标签、状态）必须在创建页面后通过 Notion 界面手动设置。对于内联数据库，API 的属性更新可能不稳定。
- **代码块数量限制：** 非常大的 markdown 文件（超过 1000 个代码块）可能因限速机制而需要较长时间才能完成同步。
- **格式问题：** 某些复杂的 markdown 结构（如嵌套列表超过 3 层）可能无法完美转换。

## 故障排除

- **“找不到页面”错误：** 确保页面/数据库已共享给该集成。
- 检查页面 ID 的格式（32 个字符，包含字母数字和 hyphens）。
- **“模块未找到”错误：** 脚本使用内置的 Node.js 模块（无需安装 npm）。
- 确保在脚本所在的目录中运行脚本。

**限速机制：**
- Notion API 有每秒 3 次请求的限速限制。
- 脚本会自动在每次批量上传之间间隔 350 毫秒。

## 资源

### 脚本文件

- **md-to-notion.js**：将 markdown 内容同步到 Notion 并保留所有格式。
- **notion-to-md.js**：将 Notion 内容转换为 markdown 格式。
- **watch-notion.js**：负责变更检测和监控。

- **搜索与查询：**
  - **search-notion.js**：根据查询条件搜索页面和数据库。
  - **query-database.js**：使用过滤条件和排序功能查询数据库。
  - **update-page-properties.js**：更新数据库页面的属性。

- **数据库管理：**
  - **add-to-database.js**：将 markdown 文件添加到数据库中。
  - **get-database-schema.js**：检查数据库结构。
  - **delete-notion-page.js**：将页面归档。

- **辅助工具：**
  - **notion-utils.js**：提供通用辅助功能（错误处理、属性格式化、API 请求处理）。

所有脚本仅使用内置的 Node.js 模块（https, fs），无需外部依赖。

### 参考资料

- **database-patterns.md**：常见的数据库架构和属性模式文档。