---
name: notion-sync
description: >
  **Notion页面与数据库的双向同步与管理**  
  适用于需要使用Notion工作空间进行协作编辑、研究记录、项目管理，或者需要将Markdown文件同步到/从Notion页面中，以及监控Notion页面变更的场景。
homepage: https://github.com/robansuini/agent-skills
repository: https://github.com/robansuini/agent-skills/tree/main/productivity/notion-sync
license: MIT-0
metadata:
  clawdis:
    requires:
      env: [NOTION_API_KEY]
      bins: [node]
    stateDirs: [memory]
---
# Notion 同步工具

本工具支持 markdown 文件与 Notion 页面之间的双向同步，并提供数据库管理功能，适用于研究内容跟踪和项目管理。

## 升级说明

**从 v2.0 开始：**  
- 将 `--token "ntn_..."` 替换为 `--token-file`、`--token-stdin` 或环境变量 `NOTION_API_KEY`。单独使用 `--token` 已不再被支持（凭证信息不应出现在进程列表中）。  
- 有关从 v1.x 升级的详细信息，请参阅 v2.0 的变更日志。

## 系统要求

- **Node.js** v18 或更高版本  
- 需要一个 Notion 集成令牌（以 `ntn_` 或 `secret_` 开头）

## 设置步骤

1. 访问 [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)  
2. 创建一个新的集成（或使用现有的集成）  
3. 复制“内部集成令牌”  
4. 使用以下方法之一传递令牌（脚本优先级顺序如下）：  

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

   **默认设置：**  
   如果存在 `~/.notion-token` 文件，脚本会自动使用该令牌，无需指定 `--token-file`。  

5. 将你的 Notion 页面/数据库共享给该集成：  
   - 在 Notion 中打开相应的页面/数据库  
   - 点击“共享”→“邀请”  
   - 选择你的集成  

## JSON 输出模式  

所有脚本都支持 `--json` 标志：  
- 遮盖输出到标准错误流（stderr）的进度日志  
- 保持标准输出（stdout）便于自动化脚本读取  
- 错误信息以 JSON 格式输出：`{"error": "..."}`  

**示例：**  
```bash
node scripts/query-database.js <db-id> --limit 5 --json
```  

## 路径安全机制  

默认情况下，读取/写入本地文件的脚本仅限于当前工作目录：  
- 防止意外访问工作区外的文件  
- 适用于以下脚本：`md-to-notion.js`、`add-to-database.js`、`notion-to-md.js`、`watch-notion.js`  
- 可通过 `--allow-unsafe-paths` 选项手动覆盖此限制。  
**示例：**  
```bash
# Default (safe): path must be inside current workspace
node scripts/md-to-notion.js docs/draft.md <parent-id> "Draft"

# Intentional override (outside workspace)
node scripts/notion-to-md.js <page-id> ~/Downloads/export.md --allow-unsafe-paths
```  

## 核心功能  

### 1. 搜索页面和数据库  

- 可根据标题或内容在 Notion 工作区中搜索页面。  
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

### 2. 带过滤条件的数据库查询  

- 支持使用高级过滤条件和排序功能查询数据库内容。  
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
- 包含：`{"property": "Tags", "multi_select": {"contains": "AI"}}`  
- 日期晚于：`{"property": "Date", "date": {"after": "2024-01-01"}}`  
- 复选框状态为“已选中”：`{"property": "Published", "checkbox": {"equals": true}}`  
- 数字大于：`{"property": "Count", "number": {"greater_than": 100}}`  

### 3. 更新页面属性  

- 可更新数据库页面的属性（如状态、标签、日期等）。  
**示例：**  
```bash
node scripts/update-page-properties.js <page-id> <property-name> <value> [--type <type>] [--json]
```  
**支持的属性类型：** `select`、`multi_select`、`checkbox`、`number`、`url`、`email`、`date`、`rich_text`  

### 4. 批量更新  

- 可通过单个命令批量更新多个页面的属性。  
**模式 1：** 查询后更新：**  
```bash
node scripts/batch-update.js <database-id> <property-name> <value> --filter '<json>' [--type select] [--dry-run] [--limit 100]
```  
**示例：**  
```bash
node scripts/batch-update.js <db-id> Status Review \
  --filter '{"property":"Status","select":{"equals":"Draft"}}' \
  --type select
```  
**模式 2：** 从标准输入（stdin）获取页面 ID：**  
```bash
echo "page-id-1\npage-id-2\npage-id-3" | \
  node scripts/batch-update.js --stdin <property-name> <value> [--type select] [--dry-run]
```  
**功能：**  
- `--dry-run`：仅输出将要更新的页面（包含当前属性值），不实际执行更新  
- `--limit <n>`：限制处理的页面数量（默认为 100 页）  
- 查询模式下支持分页（`has_more`/`next_cursor`）  
- 遵循速率限制（每次更新间隔 300 毫秒）  
- 进度信息输出到标准错误流（stderr），结果以 JSON 数组形式输出到标准输出（stdout）  

### 5. Markdown → Notion 同步  

- 将 markdown 内容同步到 Notion，并保留所有格式。  
**示例：**  
```bash
node scripts/md-to-notion.js \
  "<markdown-file-path>" \
  "<notion-parent-page-id>" \
  "<page-title>" [--json] [--allow-unsafe-paths]
```  
**支持的格式：**  
- 标题（H1-H3）  
- 加粗/斜体文本  
- 链接  
- 列表  
- 带语法高亮的代码块  
- 水平分隔线  
- 段落  
**特点：**  
- 批量上传（每次请求最多 100 个代码块）  
- 自动控制上传频率（每次上传间隔 350 毫秒）  
- 自动将长文本分割成 Notion 的 2000 字符限制  
- 返回 Notion 页面的 URL 和 ID  

**示例：**  
```
Parsed 294 blocks from markdown
✓ Created page: https://www.notion.so/[title-and-id]
✓ Appended 100 blocks (100-200)
✓ Appended 94 blocks (200-294)

✅ Successfully created Notion page!
```  

### 6. Notion → Markdown 同步  

- 从 Notion 页面提取内容并转换为 markdown 格式。  
**示例：**  
```bash
node scripts/notion-to-md.js <page-id> [output-file] [--json] [--allow-unsafe-paths]
```  
**特点：**  
- 保留原始的格式（标题、列表、代码、引号等）  
- 可选择将结果输出到文件或标准输出（stdout）  

### 7. 变更检测与监控  

- 监控 Notion 页面的更改，并与本地 markdown 文件进行比较。  
**示例：**  
```bash
node scripts/watch-notion.js "<page-id>" "<local-markdown-path>" [--state-file <path>] [--json] [--allow-unsafe-paths]
```  
**状态跟踪：** 默认情况下，变更信息保存在 `memory/notion-watch-state.json` 文件中（位于当前工作目录）。可通过 `--state-file <path>` 选项自定义存储路径（支持通配符 `~`）。  
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
**输出结果：**  
```json
{
  "pageId": "<page-id>",
  "title": "Your Page Title",
  "lastEditedTime": "2026-01-30T08:57:00.000Z",
  "hasChanges": false,
  "localPath": "/path/to/your-draft.md",
  "actions": ["✓ No changes since last check"]
}
```  
**自动监控：** 可使用 cron、CI 流程或任务调度器定期执行检查；当 `hasChanges` 为 `true` 时，将结果发送到通知系统。  

### 8. 数据库管理  

#### 向数据库添加 Markdown 内容  

- 可将 markdown 文件作为新页面添加到 Notion 数据库中。  
**示例：**  
```bash
node scripts/add-to-database.js <database-id> "<page-title>" <markdown-file-path> [--json] [--allow-unsafe-paths]
```  
**特点：**  
- 为页面设置标题属性  
- 将 markdown 转换为 Notion 可用的格式（标题、段落等）  
- 支持批量上传大文件  
- 返回页面的 URL 以供立即访问  

**注意：** 创建页面后，需在 Notion 界面手动设置其他属性（如类型、标签、状态等）。  

#### 查看数据库结构  

- 可查看数据库的架构信息。  
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

- 可将页面标记为已归档（`archived: true`），但不会永久删除页面。  

## 常见工作流程  

### 协同编辑流程  

1. 将本地草稿推送到 Notion：  
   ```bash
   node scripts/md-to-notion.js draft.md <parent-id> "Draft Title"
   ```  
2. 用户在 Notion 中进行编辑（支持任何设备）  
3. 监控页面变化：  
   ```bash
   node scripts/watch-notion.js <page-id> <local-path>
   # Returns hasChanges: true when edited
   ```  
4. 将更新内容拉回本地：  
   ```bash
   node scripts/notion-to-md.js <page-id> draft-updated.md
   ```  
5. 根据需要重复上述步骤（更新同一页面，避免重复创建多个版本）。  

### 研究成果跟踪  

1. 在本地生成研究内容（例如通过子代理）。  
2. 将内容同步到 Notion 数据库：  
   ```bash
   node scripts/add-research-to-db.js
   ```  
3. 用户在 Notion 界面添加元数据（类型、标签、状态等）。  
4. 通过 Notion 的网页或移动应用访问结果。  

### 页面 ID 提取  

- 从 Notion URL `https://notion.so/Page-Title-abc123-example-page-id-456def` 中提取页面 ID：  
  - `abc123-example-page-id-456def`（位于标题后的部分）  
  - 或使用 32 个字符的格式：`abc123examplepageid456def`（ hyphens 可选）  

## 限制事项  

- **属性更新：** 数据库属性（类型、标签、状态）必须在创建页面后通过 Notion 界面手动设置。  
- **文件大小限制：** 非常大的 markdown 文件（超过 1000 个代码块）可能因速率限制而需要较长时间同步。  
- **格式问题：** 复杂的 markdown 结构（如嵌套列表超过 3 层）可能无法完美转换。  

## 故障排除  

- **“无法找到页面”错误：**  
  - 确保页面/数据库已共享给该集成工具  
  - 检查页面 ID 的格式（32 个字符，包含字母数字和 hyphens）  

- **“模块未找到”错误：**  
  - 该工具使用内置的 Node.js 模块（无需安装 npm）  
  - 确保在脚本所在目录中运行脚本  

- **速率限制：** Notion API 有速率限制（每秒最多 3 次请求）  
  - 脚本会自动控制上传频率（每次上传间隔 350 毫秒）  

## 资源说明  

### 脚本目录（scripts/）  

- **核心同步脚本：**  
  - `md-to-notion.js`：Markdown → Notion 同步（保留格式）  
  - `notion-to-md.js`：Notion → Markdown 转换  
  - `watch-notion.js`：变更检测与监控  

- **搜索与查询脚本：**  
  - `search-notion.js`：根据查询条件搜索页面和数据库  
  - `query-database.js`：带过滤条件和排序功能的数据库查询  
  - `update-page-properties.js`：更新数据库页面属性  
  - `batch-update.js`：批量更新多个页面的属性  

- **数据库管理脚本：**  
  - `add-to-database.js`：将 markdown 文件添加到数据库  
  - `get-database-schema.js`：查看数据库结构  
  - `delete-notion-page.js`：归档页面  

- **辅助工具：**  
  - `notion-utils.js`：提供通用功能（错误处理、属性格式化、API 请求处理）  

所有脚本仅使用内置的 Node.js 模块（`https`、`fs`），无需额外依赖。  

### 参考资料：**  
- **database-patterns.md**：常见的数据库结构和属性模式文档