---
name: notion
description: Notion API：通过 `notioncli` 命令行工具（CLI）来创建和管理页面、数据库、区块（blocks）、关系（relations）、汇总数据（rollups）以及多工作空间（multi-workspace）配置文件。
homepage: https://github.com/JordanCoin/notioncli
metadata:
  openclaw:
    emoji: "📝"
    requires:
      env: ["NOTION_API_KEY"]
    primaryEnv: NOTION_API_KEY
    install: "npm install -g @jordancoin/notioncli"
---

# notioncli — Notion API 工具

这是一个强大的命令行工具（CLI），用于操作 Notion API。它支持查询数据库、管理页面、添加注释，并通过终端自动化管理工作区。该工具既适用于 AI 代理，也适用于人类用户。

## 设置

```bash
npm install -g notioncli
notion init --key $NOTION_API_KEY
```

`init` 命令会保存您的 API 密钥，并**自动检测**所有与您的集成服务共享的数据库。每个数据库都会被赋予一个别名（一个由数据库名称派生的简短字符串），因此您无需输入原始的 UUID。

> **提示：** 在 Notion 中，您需要先与集成服务共享每个数据库：打开数据库 → 菜单 → “连接” → 添加您的集成服务。

## 自动别名生成

当您运行 `notion init` 时，每个共享的数据库都会自动被分配一个别名：

```
Found 3 databases:

  ✅ projects                   → Projects
  ✅ tasks                      → Tasks  
  ✅ reading-list               → Reading List
```

之后，您可以在所有地方使用 `projects` 代替 `a1b2c3d4-e5f6-...` 等原始 UUID。您也可以手动管理别名：

```bash
notion alias list                  # Show all aliases
notion alias add mydb <db-id>     # Add a custom alias
notion alias rename old new        # Rename an alias
notion alias remove mydb           # Remove an alias
```

## 命令参考

### 数据库检测

```bash
notion dbs                         # List all databases shared with your integration
notion alias list                  # Show configured aliases with IDs
```

### 数据查询

```bash
notion query tasks                                     # Query all rows
notion query tasks --filter Status=Active              # Filter by property
notion query tasks --sort Date:desc                    # Sort results
notion query tasks --filter Status=Active --limit 10   # Combine options
notion query tasks --output csv                        # CSV output
notion query tasks --output yaml                       # YAML output
notion query tasks --output json                       # JSON output
notion --json query tasks                              # JSON (shorthand)
```

**输出格式：**
- `table` — 格式化的 ASCII 表格（默认格式）
- `csv` — 带有标题行的逗号分隔值
- `json` — 完整的 API 响应（以 JSON 格式）
- `yaml` — 简单的键/值对（JSON 格式）

### 创建页面

```bash
notion add tasks --prop "Name=Buy groceries" --prop "Status=Todo"
notion add projects --prop "Name=New Feature" --prop "Priority=High" --prop "Due=2026-03-01"
```

可以使用多个 `--prop` 标志来指定多个属性。属性名称不区分大小写，并会与数据库模式进行匹配。

### 更新页面

- **按页面 ID 更新：**
```bash
notion update <page-id> --prop "Status=Done"
notion update <page-id> --prop "Priority=Low" --prop "Notes=Updated by CLI"
```

- **按别名 + 过滤条件更新：**
```bash
notion update tasks --filter "Name=Ship feature" --prop "Status=Done"
notion update workouts --filter "Name=LEGS #5" --prop "Notes=Great session"
```

### 读取页面及内容

- **按页面 ID 读取：**
```bash
notion get <page-id>               # Page properties
notion blocks <page-id>            # Page content (headings, text, lists, etc.)
```

- **按别名 + 过滤条件读取：**
```bash
notion get tasks --filter "Name=Ship feature"
notion blocks tasks --filter "Name=Ship feature"
```

### 删除（归档）页面

```bash
notion delete <page-id>                              # By page ID
notion delete tasks --filter "Name=Old task"         # By alias + filter
notion delete workouts --filter "Date=2026-02-09"    # By alias + filter
```

### 关系与汇总数据

```bash
notion relations tasks --filter "Name=Ship feature"           # See linked pages with titles
notion relations projects --filter "Name=Launch CLI"          # Explore connections
```

在查询结果中，关系会自动转换为页面标题；汇总数据会被解析为数字、日期或数组，而不是原始的 JSON 格式。

### 块的操作（CRUD）

```bash
notion blocks tasks --filter "Name=Ship feature"              # View page content
notion blocks tasks --filter "Name=Ship feature" --ids        # View with block IDs
notion append tasks "New paragraph" --filter "Name=Ship feature"  # Append block
notion block-edit <block-id> "Updated text"                   # Edit a block
notion block-delete <block-id>                                # Delete a block
```

使用 `--ids` 参数可以获取块 ID，然后使用 `block-edit` 或 `block-delete` 命令来操作特定块。

### 添加内容

```bash
notion append <page-id> "Meeting notes: discussed Q2 roadmap"
notion append tasks "Status update: phase 1 complete" --filter "Name=Ship feature"
```

可以在页面中添加段落块。

### 用户管理

```bash
notion users                       # List all workspace users
notion user <user-id>              # Get details for a specific user
```

### 添加注释

```bash
notion comments <page-id>                                      # By page ID
notion comments tasks --filter "Name=Ship feature"             # By alias + filter
notion comment <page-id> "Looks good, shipping this!"          # By page ID
notion comment tasks "AI review complete ✅" --filter "Name=Ship feature"  # By alias + filter
```

### 页面检查器

```bash
notion props tasks --filter "Name=Ship feature"    # Quick property dump
notion me                                          # Show bot identity and owner
```

### 数据库管理

```bash
notion db-create <parent-page-id> "New DB" --prop "Name:title" --prop "Status:select"
notion db-update tasks --add-prop "Rating:number"      # Add a column
notion db-update tasks --remove-prop "Old Column"      # Remove a column
notion db-update tasks --title "Renamed DB"            # Rename database
notion templates tasks                                 # List page templates
```

### 移动页面

```bash
notion move tasks --filter "Name=Done task" --to archive     # Move by alias
notion move tasks --filter "Name=Done task" --to <page-id>   # Move to page
```

### 上传文件

```bash
notion upload tasks --filter "Name=Ship feature" ./report.pdf
notion upload <page-id> ./screenshot.png
```

支持上传图片、PDF、文本文件和文档。MIME 类型会根据文件扩展名自动识别。

### 搜索

```bash
notion search "quarterly report"   # Search across all pages and databases
```

### JSON 输出

在命令前添加 `--json` 选项，即可获取原始的 Notion API 响应：

```bash
notion --json query tasks
notion --json get <page-id>
notion --json users
notion --json comments <page-id>
```

## AI 代理的常用操作模式

### 1. 检测可用的数据库

```bash
notion dbs
notion alias list
```

### 2. 查询和过滤数据

```bash
notion query tasks --filter Status=Active --sort Date:desc
notion --json query tasks --filter Status=Active    # Parse JSON programmatically
notion query tasks --output csv                     # CSV for spreadsheet tools
```

### 3. 创建新条目

```bash
notion add tasks --prop "Name=Review PR #42" --prop "Status=Todo" --prop "Priority=High"
```

### 4. 更新现有条目（无需提供 UUID）

```bash
# By alias + filter — no page ID needed
notion update tasks --filter "Name=Review PR #42" --prop "Status=Done"

# Or by page ID if you already have it
notion update <page-id> --prop "Status=Done"
```

### 5. 读取页面内容（无需提供 UUID）

```bash
# By alias + filter
notion get tasks --filter "Name=Review PR #42"
notion blocks tasks --filter "Name=Review PR #42"

# Or by page ID
notion get <page-id>
notion blocks <page-id>
```

### 6. 向页面添加注释

```bash
notion append tasks "Status update: completed phase 1" --filter "Name=Review PR #42"
notion append <page-id> "Status update: completed phase 1"
```

### 7. 通过注释进行协作

```bash
notion comments tasks --filter "Name=Review PR #42"              # Check existing
notion comment tasks "AI review complete ✅" --filter "Name=Review PR #42"  # Add comment

# Or by page ID
notion comments <page-id>
notion comment <page-id> "AI review complete ✅"
```

### 8. 根据别名 + 过滤条件删除页面

```bash
notion delete tasks --filter "Name=Old task"
notion delete workouts --filter "Date=2026-02-09"
```

### 9. 管理数据库模式

```bash
notion db-update tasks --add-prop "Priority:select"    # Add column
notion db-update tasks --remove-prop "Old Field"       # Remove column
notion db-create <parent-page-id> "New DB" --prop "Name:title" --prop "Status:select"
```

### 10. 移动页面和上传文件

```bash
notion move tasks --filter "Name=Done" --to archive
notion upload tasks --filter "Name=Ship feature" ./report.pdf
```

### 11. 检查和调试

```bash
notion me                                       # Check integration identity
notion props tasks --filter "Name=Ship feature" # Quick property dump
notion templates tasks                          # List available templates
```

## 属性类型参考

当使用 `--prop key=value` 时，CLI 会自动从数据库模式中检测属性类型：

| 类型 | 示例值 | 备注 |
|------|-------------|-------|
| `title` | `Name=Hello World` | 主标题属性 |
| `rich_text` | `Notes=Some text` | 普通文本内容 |
| `number` | `Amount=42.5` | 数值类型 |
| `select` | `Status=Active` | 单选选项 |
| `multi_select` | `Tags=bug,urgent` | 逗号分隔的多选选项 |
| `date` | `Due=2026-03-01` | ISO 8601 格式的日期字符串 |
| `checkbox` | `Done=true` | `true`、`1` 或 `yes` |
| `url` | `Link=https://example.com` | 完整的 URL |
| `email` | `Contact=user@example.com` | 电子邮件地址 |
| `phone_number` | `Phone=+1234567890` | 电话号码字符串 |
| `status` | `Status=In Progress` | 状态属性 |

## 多个工作区管理

可以通过一个 CLI 工具管理多个 Notion 账户：

```bash
notion workspace add work --key ntn_work_key       # Add workspace
notion workspace add personal --key ntn_personal    # Add another
notion workspace list                               # Show all
notion workspace use work                           # Switch active
notion workspace remove old                         # Remove one

# Per-command override
notion query tasks --workspace personal
notion -w work add projects --prop "Name=Q2 Plan"

# Init with workspace
notion init --workspace work --key ntn_work_key
```

别名是针对每个工作区进行设置的。旧的单一密钥配置会自动迁移到“默认”工作区。

## Notion API 2025 — 双重 ID

Notion API（2025-09-03 版本）使用双重 ID 来标识数据库：`database_id` 和 `data_source_id`。`notioncli` 会自动处理这两个 ID——当您运行 `notion init` 或 `notion alias add` 时，这两个 ID 会被同时检测并存储。您无需手动处理这些细节。

## 故障排除

- **“未找到 Notion API 密钥”** — 运行 `notion init --key ntn_...` 或 `export NOTION_API_KEY=ntn_...`
- **“未知的数据库别名”** — 运行 `notion alias list` 查看可用的别名，或运行 `notion init` 重新检测别名 |
- **“未找到相关数据”** — 确保数据库/页面已与您的集成服务共享 |
- **某些属性无法查询/排序** — 属性名称不区分大小写；运行 `notion --json query <alias> --limit 1` 可查看可用的属性列表