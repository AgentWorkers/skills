---
name: coda
description: 通用型 Coda 文档管理器（通过 REST API v1 提供支持）：支持列出/创建/更新/删除文档，管理表格/行/页面，触发自动化操作，以及浏览文档结构。使用 `CODA_API_TOKEN` 环境变量进行身份验证。删除操作需要用户明确确认；发布文档或更改权限也需要用户的明确指令。
---

# Coda API 技能

该技能用于与 Coda REST API v1 进行交互，以管理文档、表格、数据行、页面以及自动化任务。

## 使用场景

当用户需要执行以下操作时，请使用此技能：
- 列出、搜索、创建或删除 Coda 文档
- 读取或写入表格数据（插入、更新、删除数据行）
- 探索文档结构（页面、表格、列、公式、控件）
- 触发自动化任务（例如按钮操作）
- 导出文档内容或分析数据

## 不适用场景

- **请勿** 用于与 API 无关的常规文档编辑建议
- **请勿** 用于 Pack 开发（此技能仅涵盖文档管理，不涉及 Pack 的创建）
- **请勿** 在未确认用户具有相应权限的情况下执行需要 Doc Maker 权限的操作

## 先决条件

1. **API Token**：将环境变量 `CODA_API_TOKEN` 设置为您的 Coda API 令牌
   - 从以下链接获取令牌：https://coda.io/account -> API Settings
2. 安装了 `requests` 库的 Python 3.7 或更高版本
3. **权限要求**：某些操作（创建文档、更新文档标题、创建页面）需要用户具有 Doc Maker 角色

## CLI 工具使用

该技能包含一个名为 `scripts/coda_cli.py` 的 Python CLI 工具：

```bash
# Setup
export CODA_API_TOKEN="your_token_here"

# List docs
python scripts/coda_cli.py docs list --query "Project"

# Get doc info
python scripts/coda_cli.py docs get <doc-id>

# Create doc
python scripts/coda_cli.py docs create --title "My New Doc"

# List tables in doc
python scripts/coda_cli.py tables list <doc-id>

# List rows in table
python scripts/coda_cli.py rows list <doc-id> <table-id>

# Insert row
python scripts/coda_cli.py rows insert <doc-id> <table-id> --data '{"Name": "Task 1", "Status": "Done"}'

# Update row
python scripts/coda_cli.py rows update <doc-id> <table-id> <row-id> --data '{"Status": "In Progress"}'

# Delete row (requires confirmation)
python scripts/coda_cli.py rows delete <doc-id> <table-id> <row-id>

# List pages
python scripts/coda_cli.py pages list <doc-id>

# Trigger automation (push button)
python scripts/coda_cli.py automations trigger <doc-id> <button-id>

# Force delete without confirmation (use with caution)
python scripts/coda_cli.py docs delete <doc-id> --force
```

## 工作流程指南

### 1. 文档 ID 提取

Coda 文档 ID 可以从浏览器 URL 中提取：
- URL 示例：`https://coda.io/d/_dAbCDeFGH/Project-Tracker`
- 文档 ID：`AbCDeFGH`（去掉前缀 `_d`）

CLI 工具支持完整的 URL 和原始 ID。

### 2. 速率限制处理

API 有严格的速率限制：
- **读取操作**：每 6 秒 100 次请求
- **写入操作（POST/PUT/PATCH）**：每 6 秒 10 次请求
- **写入文档内容**：每 10 秒 5 次请求
- **列出文档**：每 6 秒 4 次请求

CLI 工具会自动对 429 错误响应实施指数级退避策略。

### 3. 异步操作

写入操作会返回 HTTP 202 状态码，并附带一个 `requestId`。CLI 工具可以通过 `--wait` 标志选择性地等待操作完成。

### 4. 安全防护措施

**删除操作**（删除数据行、文档、页面或文件夹）：
- 必须在交互模式下获得用户的明确确认
- 仅在自动化脚本中使用 `--force` 标志
- 会显示即将被删除的内容的预览

**发布操作**（`docs publish`）：
- 必须使用 `--confirm-publish` 标志
- 不能与 `--force` 标志同时使用

**权限操作**（`acl` 命令）：
- 对任何更改操作，都必须使用 `--confirm-permissions` 标志
- 读取操作（列出权限）始终被允许

**自动化触发**：
- 可以在没有特殊标志的情况下执行，但会生成日志记录
- 用户应注意自动化操作可能会触发通知或外部动作

### 5. 分页

列表命令支持以下参数：
- `--limit`：最大结果数量（默认为 25，具体数量取决于端点）
- `--page-token`：用于获取后续页面
- 使用 `--all` 标志时，CLI 会自动遍历所有页面

## 常见用法模式

### 批量操作数据行
```bash
# Insert multiple rows from JSON file
python scripts/coda_cli.py rows insert-batch <doc-id> <table-id> --file rows.json

# Upsert rows (update if exists, insert if not) using key columns
python scripts/coda_cli.py rows upsert <doc-id> <table-id> --file rows.json --keys "Email"
```

### 在文档之间同步数据
```bash
# Export from source
python scripts/coda_cli.py rows list <source-doc> <table-id> --format json > export.json

# Import to destination
python scripts/coda_cli.py rows insert-batch <dest-doc> <table-id> --file export.json
```

### 探索文档结构
```bash
# Get full doc structure
python scripts/coda_cli.py docs structure <doc-id>

# List all formulas
python scripts/coda_cli.py formulas list <doc-id>

# List all controls
python scripts/coda_cli.py controls list <doc-id>
```

## 错误处理

常见的 HTTP 状态码：
- `400`：请求错误（参数无效）
- `401`：API 令牌无效或已过期
- `403`：权限不足（需要 Doc Maker 角色）
- `404`：资源未找到
- `429`：达到速率限制（需实施退避策略）
- `202`：请求已接受，但尚未处理（异步操作）

## 安全注意事项

1. **令牌存储**：切勿将 `CODA_API_TOKEN` 存储在版本控制系统中
2. **令牌权限**：该令牌允许用户访问其有权访问的所有文档
3. **工作空间限制**：创建文档需要目标工作空间中的 Doc Maker 角色
4. **数据安全**：数据行可能包含敏感信息，请谨慎处理导出操作

## 示例

- **列出并过滤文档**
```bash
python scripts/coda_cli.py docs list --is-owner --query "Project"
```

- **根据模板创建文档**
```bash
python scripts/coda_cli.py docs create --title "Q4 Planning" --source-doc "template-doc-id"
```

- **更新数据行状态**
```bash
python scripts/coda_cli.py rows update AbCDeFGH grid-xyz row-123 \
  --data '{"Status": "Complete", "Completed Date": "2024-01-15"}'
```

- **确认后删除多行数据**
```bash
python scripts/coda_cli.py rows delete-batch AbCDeFGH grid-xyz \
  --filter '{"Status": "Archived"}' \
  --confirm "Delete all archived rows?"
```

- **将表格数据导出为 CSV 文件**
```bash
python scripts/coda_cli.py rows list AbCDeFGH grid-xyz --format csv > export.csv
```

## 参考资料

- API 文档：https://coda.io/developers/apis/v1
- OpenAPI 规范：https://coda.io/apis/v1/openapi.yaml
- 速率限制：https://coda.io/developers/apis/v1#section/Rate-Limiting