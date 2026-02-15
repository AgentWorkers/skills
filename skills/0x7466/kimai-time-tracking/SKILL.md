---
name: kimai-time-tracking
description: 完成 Kimai 时间跟踪 API 的集成。通过 REST API 管理时间表、客户、项目、活动、团队、发票以及数据导出功能。支持时间跟踪工作流程、报告生成及行政操作。关键词：kimai、zeiterfassung（时间跟踪）、时间表、跟踪、项目、客户、活动、发票、导出、计时器。
---

# Kimai 时间跟踪技能

该技能实现了与 [Kimai](https://www.kimai.org/) 时间跟踪软件的完整 API 集成，提供了对时间表、项目、客户、活动、团队、发票和系统配置的全面控制。

## 使用场景

**在用户请求以下操作时激活此技能：**
- 开始/停止/重新开始时间跟踪
- 列出、筛选或导出时间表
- 管理客户、项目或活动
- 创建发票或导出数据
- 执行管理任务（如用户管理、团队设置、费率调整）
- 查询系统状态（版本信息、插件列表、配置设置）

**激活触发词：**
- “kimai”、“zeiterfassung”、“timesheet”、“timer”、“stunden”、“erfasse Zeit”、“starte Tracking”、“Projekt anlegen”、“Rechnung erstellen”
- “为项目 X 开始跟踪”
- “显示我上周的时间表”
- “在 Kimai 中创建新客户”
- “将时间表导出为 CSV 格式”
- “列出所有活跃的时间跟踪记录”
- “停止当前的时间跟踪”

**不适用的场景：**
- 一般性的时间查询（例如：“现在几点了？”）
- 其他时间跟踪工具（如 Toggl、Clockify 等）
- 与 Kimai 无关的日历/调度任务

## 环境设置

**所需环境变量：**
- `KIMAI_BASE_URL`：Kimai 服务器的完整 URL（例如：`https://kimai.example.com`）
- `KIMAI_API_TOKEN`：用于身份验证的令牌

**可选设置：**
- `KIMAI_WORKSPACE`：导出文件的存储路径（默认为 `~/.openclaw/workspace/kimai`）

**根据操作类型所需的 API 权限：**
- `view_own_timesheet`：查看/创建/编辑/删除自己的时间表
- `view_other_timesheet`：查看其他用户的时间表
- `view_customer`：查看/编辑/删除客户信息
- `view_project`：查看/编辑/删除项目信息
- `view_activity`：查看/编辑/删除活动信息
- `view_team`：查看/编辑/创建/删除团队信息
- `viewinvoice`：查看/管理发票信息
- `view_user`：查看用户信息

**兼容性：** 需要 Kimai 2.x 版本，并且启用了 REST API。需要互联网连接。支持 Linux 和 macOS 系统。

## 工作流程

### 1. 快速时间跟踪

```bash
# List recent activities (to find project/activity IDs)
./scripts/kimai_cli.py timesheets recent

# Start tracking
./scripts/kimai_cli.py timesheets start --project 1 --activity 5 --description "Implementing API"

# Check active timers
./scripts/kimai_cli.py timesheets active

# Stop tracking
./scripts/kimai_cli.py timesheets stop --id 123
```

### 2. 数据管理工作流程

```bash
# Create customer → Project → Activity hierarchy
./scripts/kimai_cli.py customers create --name "Acme Corp" --country DE --currency EUR --timezone Europe/Berlin
./scripts/kimai_cli.py projects create --name "Website Redesign" --customer 1
./scripts/kimai_cli.py activities create --name "Development" --project 1

# List with filters
./scripts/kimai_cli.py timesheets list --customer 1 --begin "2024-01-01T00:00:00" --exported 0
```

### 3. 导出/发票管理工作流程

```bash
# Mark timesheets as exported (locks them)
./scripts/kimai_cli.py timesheets export --id 123

# List invoices
./scripts/kimai_cli.py invoices list --status pending --begin 2024-01-01T00:00:00
```

## CLI 工具参考

使用 `scripts/kimai_cli.py` 执行所有操作。该工具的命令结构遵循 API 接口的规范：

### 时间表 (`timesheets`)
- `list`：列出时间表条目（支持分页和筛选：用户、客户、项目、活动、标签、日期范围、导出状态）
- `get <id>`：获取单个时间表条目
- `create`：创建新的时间表条目或启动时间跟踪
- `update <id>`：更新现有时间表条目
- `delete <id>`：删除时间表条目（操作具有破坏性，需要确认）
- `stop <id>`：停止正在运行的时间跟踪
- `restart <id>`：重新启动已完成的时间跟踪
- `duplicate <id>`：复制时间表条目（会重置导出状态）
- `active`：列出当前正在运行的时间跟踪记录
- `recent`：列出最近的活动记录
- `export <id>`：切换导出状态（启用/禁用导出）

### 客户 (`customers`)
- `list`：列出所有客户（可筛选显示的客户）
- `get <id>`：获取客户详细信息
- `create`：创建新客户
- `update <id>`：更新客户信息
- `delete <id>`：删除客户信息（操作具有破坏性，会影响到关联的项目和活动）
- `meta <id>`：更新客户的自定义字段
- `rates <id>`：管理客户的费率信息

### 项目 (`projects)`
- `list`：列出所有项目（可筛选客户和日期范围）
- `get <id>`：获取项目详细信息
- `create`：创建新项目（需要指定客户 ID）
- `update <id>`：更新项目信息
- `delete <id>`：删除项目信息（操作具有破坏性，会影响到关联的活动和时间表）
- `rates <id>`：管理项目的费率信息

### 活动 (`activities`)
- `list`：列出所有活动（可筛选项目）
- `get <id>`：获取活动详细信息
- `create`：创建新活动（可以是全局的或特定于项目的）
- `update <id>`：更新活动信息
- `delete <id>`：删除活动信息（操作具有破坏性，会影响到关联的时间表）
- `rates <id>`：管理活动的费率信息

### 团队 (`teams`)
- `list`、`get`、`create`、`update`、`delete`：基本团队管理操作
- `member-add <team-id> <user-id>`：添加团队成员
- `member-remove <team-id> <user-id>`：移除团队成员
- `grant-customer <team-id> <customer-id>`：授予客户团队访问权限
- `grant-project <team-id> <project-id>`：授予项目团队访问权限
- `grant-activity <team-id> <activity-id>`：授予活动团队访问权限

### 用户 (`users`)
- `list`：列出所有用户（需要 `view_user` 权限）
- `me`：显示当前用户信息
- `get <id>`：获取用户详细信息
- `create`：创建新用户（仅限管理员）
- `update <id>`：更新用户信息

### 发票 (`invoices)`
- `list`：列出所有发票（可筛选日期范围和客户）
- `get <id>`：获取发票详细信息

### 系统 (`system`)
- `ping`：测试系统连接
- `version`：显示 Kimai 的版本信息
- `plugins`：列出已安装的插件
- `config`：配置时间表显示样式
- `colors`：设置时间表的颜色代码

## 安全性与注意事项

**⚠️ 破坏性操作：**
- 对客户、项目、活动、时间表或标签的删除操作 **必须得到用户的明确确认**。
- 删除客户会影响到所有关联的项目、活动和时间表。
- 删除项目会影响到关联的活动和时间表。
- CLI 会显示受影响数据的预览，并要求用户确认是否执行删除操作。

**API 安全性：**
- API 令牌通过 `Authorization: Bearer` 头部传递。
- 令牌不会被记录或存储在 CLI 输出中。
- 可使用 `--dry-run` 标志进行测试（模拟 API 调用，不会实际执行操作）。

**速率限制与分页：**
- API 返回分页结果（默认每页 50 条记录）。
- CLI 会自动处理 `list` 命令的分页（可以获取所有页面或根据 `--limit` 参数进行分页）。
- 可使用 `--page` 和 `--size` 参数手动控制分页。

**数据隐私：**
- 时间表数据可能包含敏感信息。
- 导出文件会保存在具有受限权限的工作空间文件夹中（默认为 `KIMAI_WORKSPACE` 或 `~/.openclaw/workspace/kimai`）。
- 分享调试输出时，会隐藏个人数据（如电子邮件和姓名）。

## 输入/输出规范

**输入：**
- 实体 ID（整数）
- ISO 8601 格式的日期时间字符串（格式：YYYY-MM-DDTHH:mm:ss）
- 用于创建/更新操作的 JSON 数据（通过 `--json` 文件或 CLI 参数传递）
- 筛选参数（客户 ID、项目 ID、活动 ID、日期范围、可见性设置）

**输出：**
- JSON 格式（默认格式，便于管道传输）
- 表格格式（使用 `--format table` 参数）
- CSV 格式（使用 `--format csv` 参数）
- 输出代码：0（成功）、1（API 错误）、2（验证错误）、3（用户取消操作）

**成功标准：**
- HTTP 响应码 200/201 表示操作成功
- 输出的 JSON 数据符合 API 的结构规范
- 导出文件会保存在工作空间中，并包含正确的记录数量

## 示例

### 开始时间跟踪并添加描述

```bash
./scripts/kimai_cli.py timesheets create \
  --project 5 \
  --activity 12 \
  --description "Client meeting - requirements analysis" \
  --tags "meeting,urgent"
```

### 列出未导出的时间记录并导出

```bash
# Find billable hours not yet exported
./scripts/kimai_cli.py timesheets list \
  --exported 0 \
  --billable 1 \
  --begin "2024-01-01T00:00:00" \
  --end "2024-01-31T23:59:59" \
  --format csv > january_hours.csv
```

### 更新自定义字段（元数据）

```bash
./scripts/kimai_cli.py customers meta 42 \
  --name "order_number" \
  --value "PO-2024-001"
```

### 创建团队并分配资源

```bash
./scripts/kimai_cli.py teams create --name "Development Team" --members '[{"user": 1, "teamlead": true}]'
./scripts/kimai_cli.py teams grant-project 1 5
```

## 错误处理

**常见的 HTTP 状态码：**
- 200：操作成功
- 201：创建成功
- 204：无内容（删除成功）
- 400：请求错误（参数不完整）
- 401：未经授权（令牌无效或过期）
- 403：权限不足
- 404：找不到资源（ID 错误）
- 409：冲突（配置不允许的情况下时间表重复）

**CLI 行为：**
- 在调用 API 之前会验证必要的参数。
- 会以友好的方式显示验证错误信息，并提示用户如何修复问题（例如：“您是想使用 `PATCH` 而不是 `DELETE` 吗？可以尝试将 `visible` 设置为 `false` 来隐藏记录”）

## 验证

使用 Openclaw 的技能验证工具来验证此技能的功能：

```bash
skills-ref validate ./kimai-time-tracking
```

**测试 API 连接：**

```bash
export KIMAI_BASE_URL="https://your-kimai.example.com"
export KIMAI_API_TOKEN="your-api-token"
./kimai-time-tracking/scripts/kimai_cli.py system ping
```

## 参考资料**
- Kimai REST API 文档：https://www.kimai.org/documentation/rest-api.html
- 分页指南：https://www.kimai.org/documentation/api-pagination.html
- API 规范：`references/api-reference.json`（完整的 OpenAPI 架构）