---
name: "google-workspace-cli"
description: "通过 gws CLI 进行 Google Workspace 的管理。可以安装、验证并自动化使用 Gmail、Drive、Sheets、Calendar、Docs、Chat 和 Tasks 等服务。执行安全审计，运行 43 个内置的自动化脚本（recipes），并使用 10 个预设的配置包（persona bundles）。适用于 Google Workspace 的管理、gws CLI 的配置、Gmail 的自动化操作、Drive 的管理以及 Calendar 的日程安排等场景。"
---
# Google Workspace CLI

这是一个基于开源工具 `gws` 的命令行界面（CLI），专为 Google Workspace 的管理提供专家级指导和自动化功能。涵盖了安装、身份验证、18 多项服务 API、43 个内置工作流程模板以及 10 个基于角色的工作流程包。

---

## 快速入门

### 检查安装情况

```bash
# Verify gws is installed and authenticated
python3 scripts/gws_doctor.py
```

### 发送邮件

```bash
gws gmail users.messages send me --to "team@company.com" \
  --subject "Weekly Update" --body "Here's this week's summary..."
```

### 列出 Drive 文件

```bash
gws drive files list --json --limit 20 | python3 scripts/output_analyzer.py --select "name,mimeType,modifiedTime" --format table
```

---

## 安装

### 推荐使用 npm

```bash
npm install -g @anthropic/gws
gws --version
```

### 从源代码安装（使用 Cargo）

```bash
cargo install gws-cli
gws --version
```

### 预编译的二进制文件

可以从 [github.com/googleworkspace/cli/releases](https://github.com/googleworkspace/cli/releases) 下载适用于 macOS、Linux 或 Windows 的预编译二进制文件。

### 验证安装

```bash
python3 scripts/gws_doctor.py
# Checks: PATH, version, auth status, service connectivity
```

---

## 身份验证

### OAuth 设置（交互式）

```bash
# Step 1: Create Google Cloud project and OAuth credentials
python3 scripts/auth_setup_guide.py --guide oauth

# Step 2: Run auth setup
gws auth setup

# Step 3: Validate
gws auth status --json
```

### 服务账户（无界面/持续集成环境）

```bash
# Generate setup instructions
python3 scripts/auth_setup_guide.py --guide service-account

# Configure with key file
export GWS_SERVICE_ACCOUNT_KEY=/path/to/key.json
export GWS_DELEGATED_USER=admin@company.com
gws auth status
```

### 环境变量

```bash
# Generate .env template
python3 scripts/auth_setup_guide.py --generate-env
```

| 变量 | 用途 |
|----------|---------|
| `GWS_CLIENT_ID` | OAuth 客户端 ID |
| `GWS_CLIENT_SECRET` | OAuth 客户端密钥 |
| `GWS_TOKEN_PATH` | 自定义令牌存储路径 |
| `GWS_SERVICE_ACCOUNT_KEY` | 服务账户 JSON 密钥路径 |
| `GWS_DELEGATED_USER` | 代理操作的用户（服务账户） |
| `GWS_DEFAULT_FORMAT` | 默认输出格式（json/ndjson/table） |

### 验证身份验证

```bash
python3 scripts/auth_setup_guide.py --validate --json
# Tests each service endpoint
```

---

## 工作流程 1：Gmail 自动化

**目标：** 自动化邮件操作——发送、搜索、标记和筛选邮件。

### 发送和回复邮件

```bash
# Send a new email
gws gmail users.messages send me --to "client@example.com" \
  --subject "Proposal" --body "Please find attached..." \
  --attachment proposal.pdf

# Reply to a thread
gws gmail users.messages reply me --thread-id <THREAD_ID> \
  --body "Thanks for your feedback..."

# Forward a message
gws gmail users.messages forward me --message-id <MSG_ID> \
  --to "manager@company.com"
```

### 搜索和筛选邮件

```bash
# Search emails
gws gmail users.messages list me --query "from:client@example.com after:2025/01/01" --json \
  | python3 scripts/output_analyzer.py --count

# List labels
gws gmail users.labels list me --json

# Create a filter
gws gmail users.settings.filters create me \
  --criteria '{"from":"notifications@service.com"}' \
  --action '{"addLabelIds":["Label_123"],"removeLabelIds":["INBOX"]}'
```

### 批量操作

```bash
# Archive all read emails older than 30 days
gws gmail users.messages list me --query "is:read older_than:30d" --json \
  | python3 scripts/output_analyzer.py --select "id" --format json \
  | xargs -I {} gws gmail users.messages modify me {} --removeLabelIds INBOX
```

---

## 工作流程 2：Drive 和 Sheets

**目标：** 管理文件、创建电子表格、配置共享权限以及导出数据。

### 文件操作

```bash
# List files
gws drive files list --json --limit 50 \
  | python3 scripts/output_analyzer.py --select "name,mimeType,size" --format table

# Upload a file
gws drive files create --name "Q1 Report" --upload report.pdf \
  --parents <FOLDER_ID>

# Create a Google Sheet
gws sheets spreadsheets create --title "Budget 2026" --json

# Download/export
gws drive files export <FILE_ID> --mime "application/pdf" --output report.pdf
```

### 共享设置

```bash
# Share with user
gws drive permissions create <FILE_ID> \
  --type user --role writer --emailAddress "colleague@company.com"

# Share with domain (view only)
gws drive permissions create <FILE_ID> \
  --type domain --role reader --domain "company.com"

# List who has access
gws drive permissions list <FILE_ID> --json
```

### 电子表格数据操作

```bash
# Read a range
gws sheets spreadsheets.values get <SHEET_ID> --range "Sheet1!A1:D10" --json

# Write data
gws sheets spreadsheets.values update <SHEET_ID> --range "Sheet1!A1" \
  --values '[["Name","Score"],["Alice",95],["Bob",87]]'

# Append rows
gws sheets spreadsheets.values append <SHEET_ID> --range "Sheet1!A1" \
  --values '[["Charlie",92]]'
```

---

## 工作流程 3：日历和会议

**目标：** 安排会议、查找可用时间以及生成每日站会报告。

### 事件管理

```bash
# Create an event
gws calendar events insert primary \
  --summary "Sprint Planning" \
  --start "2026-03-15T10:00:00" --end "2026-03-15T11:00:00" \
  --attendees "team@company.com" \
  --location "Conference Room A"

# List upcoming events
gws calendar events list primary --timeMin "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --maxResults 10 --json

# Quick event (natural language)
gws helpers quick-event "Lunch with Sarah tomorrow at noon"
```

### 查找可用时间

```bash
# Check free/busy for multiple people
gws helpers find-time \
  --attendees "alice@co.com,bob@co.com,charlie@co.com" \
  --duration 60 --within "2026-03-15,2026-03-19" --json
```

### 生成每日站会报告

```bash
# Generate daily standup from calendar + tasks
gws recipes standup-report --json \
  | python3 scripts/output_analyzer.py --format table

# Meeting prep (agenda + attendee info)
gws recipes meeting-prep --event-id <EVENT_ID>
```

---

## 工作流程 4：安全审计

**目标：** 审查 Google Workspace 的安全配置并生成相应的修复命令。

### 运行全面审计

```bash
# Full audit across all services
python3 scripts/workspace_audit.py --json

# Audit specific services
python3 scripts/workspace_audit.py --services gmail,drive,calendar

# Demo mode (no gws required)
python3 scripts/workspace_audit.py --demo
```

### 审计检查项

| 领域 | 检查内容 | 风险 |
|------|-------|------|
| Drive | 是否启用了外部共享 | 数据泄露风险 |
| Gmail | 自动转发规则 | 数据泄露风险 |
| Gmail | DMARC/SPF/DKIM 配置 | 邮件伪造风险 |
| 日历 | 默认共享设置 | 信息泄露风险 |
| OAuth | 第三方应用权限 | 未经授权的访问风险 |
| 管理员权限 | 管理员数量 | 权限升级风险 |
| 管理员设置 | 两步验证 | 账户被接管风险 |

### 审查与修复

```bash
# Review findings
python3 scripts/workspace_audit.py --json | python3 scripts/output_analyzer.py \
  --filter "status=FAIL" --select "area,check,remediation"

# Execute remediation (example: restrict external sharing)
gws drive about get --json  # Check current settings
# Follow remediation commands from audit output
```

---

## Python 工具

| 脚本 | 用途 | 使用方法 |
|--------|---------|-------|
| `gws_doctor.py` | 预运行诊断工具 | `python3 scripts/gws_doctor.py [--json] [--services gmail,drive]` |
| `auth_setup_guide.py` | 协助设置 OAuth 访问权限 | `python3 scripts/auth_setup_guide.py --guide oauth` |
| `gws_recipeRunner.py` | 工作流程模板管理工具 | `python3 scripts/gws_recipe_runner.py --list [--persona pm]` |
| `workspace_audit.py` | 安全配置审计工具 | `python3 scripts/workspace_audit.py [--json] [--demo]` |
| `output_analyzer.py` | JSON/NDJSON 数据分析工具 | `gws ... --json \| python3 scripts/output_analyzer.py --count` |

所有脚本均仅使用标准库编写，支持 `--json` 格式的输出，并提供包含示例数据的演示模式。

---

## 最佳实践

### 安全性

1. 仅请求每个工作流程所需的最小权限范围（使用 OAuth）。
2. 将令牌存储在系统密钥库中，切勿以明文形式保存。
3. 每 90 天轮换服务账户密钥。
4. 每季度审核第三方应用的 OAuth 权限授予情况。
5. 在执行批量破坏性操作前使用 `--dry-run` 选项进行测试。

### 自动化建议

1. 将 `--json` 格式的输出结果传递给 `output_analyzer.py` 进行过滤和汇总。
2. 使用工作流程模板（recipes）来执行多步骤操作，而非直接串联原始命令。
3. 根据自身角色选择相应的工作流程模板。
4. 对于大量数据输出，使用 NDJSON 格式（`--format ndjson`）。
5. 在 shell 配置文件中设置 `GWS_DEFAULT_FORMAT=json` 以支持脚本执行。

### 性能优化

1. 使用 `--fields` 选项仅请求所需字段，以减少数据传输量。
2. 在浏览数据时使用 `--limit` 限制返回结果数量。
3. 仅在需要完整数据集时使用 `--page-all` 选项。
4. 尽量使用工作流程模板（recipes）进行批量操作，而非单独调用 API。
5. 将频繁访问的数据（如标签 ID、文件夹 ID）缓存到变量中。

---

## 限制与注意事项

| 限制 | 影响 |
|------------|--------|
| OAuth 令牌有效期为 1 小时 | 长时间运行的脚本需要重新授权。 |
| API 使用频率限制（按用户和服务计） | 批量操作可能导致 429 错误。 |
| 不同服务的权限要求不同 | 验证时必须请求正确的权限范围。 |
| CLI 版本低于 1.0 的兼容性问题 | 新版本可能会引入兼容性问题。 |
| 需要 Google Cloud 项目 | 免费使用，但需在 Cloud Console 中进行配置。 |
| 管理员 API 需要管理员权限 | 部分审计功能需要管理员角色。 |

### 各服务所需的权限范围

```bash
# List scopes for specific services
python3 scripts/auth_setup_guide.py --scopes gmail,drive,calendar,sheets
```

| 服务 | 所需权限范围 |
|---------|-----------|
| Gmail | `gmail.modify`, `gmail.send`, `gmail.labels` |
| Drive | `drive.file`, `drive.metadata.readonly` |
| Sheets | `spreadsheets` |
| Calendar | `calendar`, `calendar.events` |
| Admin | `admin_directory.user.readonly`, `admin_directory.group` |
| Tasks | `tasks` |