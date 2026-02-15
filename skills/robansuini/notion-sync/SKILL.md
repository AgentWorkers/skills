---
name: notion-sync
description: **Notion页面与数据库的双向同步与管理**  
适用于需要使用Notion工作空间进行协作编辑、研究跟踪、项目管理的场景，或者当您需要将Markdown文件同步到/从Notion页面中，或者监控Notion页面的变更时。
homepage: https://github.com/robansuini/agent-skills
repository: https://github.com/robansuini/agent-skills/tree/main/productivity/notion-sync
license: MIT
metadata:
  clawdis:
    requires:
      env: [NOTION_API_KEY]
      bins: [node]
---

# Notion 同步工具

本工具支持 markdown 文件与 Notion 页面之间的双向同步，并提供数据库管理功能，适用于研究内容跟踪和项目管理。

## 升级说明

**从 v2.0 开始：**
- 将 `--token "ntn_..."` 替换为 `--token-file`、`--token-stdin` 或环境变量 `NOTION_API_KEY`。单独使用 `--token` 的方式不再被支持（凭证信息不应出现在进程列表中）。
- 有关从 v1.x 升级的详细信息，请参阅 v2.0 的变更日志。

## 系统要求

- **Node.js** 版本：v18 或更高
- 需要一个 Notion 集成令牌（以 `ntn_` 或 `secret_` 开头）

## 设置步骤

1. 访问 [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)  
2. 创建一个新的集成（或使用现有的集成）  
3. 复制“内部集成令牌”（Internal Integration Token）  
4. 通过以下方式之一传递令牌（脚本优先使用以下顺序）：  

   **选项 A — 令牌文件（推荐）：**  
   ```bash
   echo "ntn_your_token" > ~/.notion-token && chmod 600 ~/.notion-token
   node scripts/search-notion.js "query" --token-file ~/.notion-token
   ```  

   **选项 B — 标准输入（stdin）：**  
   ```bash
   echo "$NOTION_API_KEY" | node scripts/search-notion.js "query" --token-stdin
   ```  

   **选项 C — 环境变量：**  
   ```bash
   export NOTION_API_KEY="ntn_your_token"
   node scripts/search-notion.js "query"
   ```  

   **自动默认设置：**  
   如果存在 `~/.notion-token` 文件，脚本会自动使用该令牌，无需指定 `--token-file`。  

5. 将你的 Notion 页面/数据库共享给该集成：  
   - 在 Notion 中打开相应的页面/数据库  
   - 点击“共享”→“邀请”  
   - 选择你的集成  

## 核心功能  

### 1. 搜索页面和数据库  

- 可根据标题或内容在整个 Notion 工作区中进行搜索。  
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

### 2. 使用过滤器查询数据库  

- 可使用高级过滤器对数据库内容进行查询和排序。  
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

**常用过滤模式：**  
- 等于：`{"property": "Status", "select": {"equals": "Done"}}`  
- 多选：包含：`{"property": "Tags", "multi_select": {"contains": "AI"}}`  
- 日期晚于：`{"property": "Date", "date": {"after": "2024-01-01"}}`  
- 复选框状态为“已选中”：`{"property": "Published", "checkbox": {"equals": true}}`  
- 数值大于：`{"property": "Count", "number": {"greater_than": 100}}`  

### 3. 更新页面属性  

- 可更新数据库页面的属性（如状态、标签、日期等）。  
   ```bash
node scripts/update-page-properties.js <page-id> <property-name> <value> [--type <type>]
```  

**支持的属性类型：** `select`、`multi_select`、`checkbox`、`number`、`url`、`email`、`date`、`rich_text`  

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

- 可将 markdown 内容推送至 Notion，并保留所有格式。  
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
- 带语法高亮的代码块  
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

- 可将 Notion 页面内容提取并转换为 markdown 格式。  
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
- 可选择将结果输出到文件或标准输出（stdout）  

### 6. 监控页面变更  

- 可监控 Notion 页面的更改，并与本地 markdown 文件进行对比。  
   ```bash
node scripts/watch-notion.js "<page-id>" "<local-markdown-path>" [--state-file <path>]
```  

**示例：**  
```bash
node scripts/watch-notion.js \
  "abc123-example-page-id-456def" \
  "projects/newsletter-draft.md"
```  

**状态跟踪：**  
默认情况下，变更信息会保存在 `memory/notion-watch-state.json` 文件中（相对于当前工作目录）。你也可以使用 `--state-file <path>` 来指定存储路径（支持使用 `~` 进行路径扩展）。  
**默认状态结构：**  
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

**自动监控：**  
可以通过 cron 任务、CI 流程或任何任务调度器定期执行监控：  
```bash
# Example: cron job every 2 hours during work hours
0 9-21/2 * * * cd /path/to/workspace && node scripts/watch-notion.js "<page-id>" "<local-path>"
```  
当 `hasChanges` 为 `true` 时，脚本会将结果输出到指定的通知系统。  

### 7. 数据库管理  

#### 向数据库添加 Markdown 内容  

- 可将 markdown 文件作为新页面添加到 Notion 数据库中。  
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
- 为页面创建一个包含标题属性的新数据库页面  
- 将 markdown 内容转换为 Notion 的格式（标题、段落、分隔线等）  
- 支持批量上传大文件  
- 返回页面的 URL 以便立即访问  

**注意：** 创建页面后，必须手动在 Notion 界面设置额外的属性（如类型、标签、状态等）。  

#### 检查数据库结构  

- 可查看数据库的当前结构。  
   ```bash
node scripts/get-database-schema.js <database-id>
```  

**使用场景：**  
- 设置新的数据库集成  
- 调试属性名称和类型  
- 了解数据库结构  

#### 归档页面  

- 可将页面标记为已归档（`archived: true`），但不会永久删除页面。  

## 常见工作流程  

### 协作编辑流程  

1. 将本地草稿推送到 Notion：  
   ```bash
   node scripts/md-to-notion.js draft.md <parent-id> "Draft Title"
   ```  

2. 用户在 Notion 中进行编辑（支持任何设备）。  
3. 监控页面是否发生变更：  
   ```bash
   node scripts/watch-notion.js <page-id> <local-path>
   # Returns hasChanges: true when edited
   ```  

4. 将更新内容拉取回本地：  
   ```bash
   node scripts/notion-to-md.js <page-id> draft-updated.md
   ```  

5. 根据需要重复上述步骤（更新同一页面，避免重复创建多个版本）。  

### 研究成果跟踪  

1. 在本地生成研究成果（例如通过子代理）。  
2. 将结果同步到 Notion 数据库：  
   ```bash
   node scripts/add-research-to-db.js
   ```  

3. 用户在 Notion 界面添加元数据（类型、标签、状态等）。  
4. 通过 Notion 的网页或移动应用访问结果。  

### 提取页面 ID  

- 从 Notion 页面 URL `https://notion.so/Page-Title-abc123-example-page-id-456def` 中提取：`abc123-example-page-id-456def`（位于标题之后的部分）  
- 或使用 32 个字符的格式：`abc123examplepageid456def`（ hyphens 可选）  

## 限制事项  

- **属性更新：**  
  数据库属性（类型、标签、状态等）必须在创建页面后手动在 Notion 界面设置。对于某些数据库类型，API 可能无法自动更新这些属性。  
- **文件大小限制：** 非常大的 markdown 文件（超过 1000 个代码块）可能因限速机制而需要较长时间才能同步完成。  
- **格式问题：** 某些复杂的 markdown 格式（如嵌套列表超过 3 层）可能无法完美转换。  

## 故障排除  

- **“无法找到页面”错误：**  
  确保页面/数据库已共享给该集成工具。  
  检查页面 ID 的格式（32 个字符，包含字母数字和 hyphens）。  

- **“模块未找到”错误：**  
  该工具使用内置的 Node.js 模块（无需安装 npm）。  
  确保在脚本所在的目录中运行脚本。  

- **限速问题：**  
  Notion API 有请求速率限制（每秒约 3 次请求）。  
  脚本会自动在每次批量上传之间等待 350 毫秒。  

## 资源文件  

### 脚本文件  

- **md-to-notion.js**：将 markdown 内容同步到 Notion 并保留所有格式。  
- **notion-to-md.js**：将 Notion 内容转换为 markdown 格式。  
- **watch-notion.js**：监控页面变更。  

- **搜索与查询功能：**  
  - **search-notion.js**：根据查询条件搜索页面和数据库。  
  - **query-database.js**：使用过滤器查询数据库内容并进行排序。  
  - **update-page-properties.js**：更新数据库页面的属性。  

- **数据库管理功能：**  
  - **add-to-database.js**：将 markdown 文件添加到数据库中。  
  - **get-database-schema.js**：查看数据库结构。  
  - **delete-notion-page.js**：将页面标记为已归档。  

- **辅助工具：**  
  - **notion-utils.js**：提供通用辅助功能（错误处理、属性格式化、API 请求处理）。  

所有脚本仅使用内置的 Node.js 模块（`https`、`fs`），无需额外依赖。  

### 参考资料  

- **database-patterns.md**：常见的数据库结构和属性模式文档。