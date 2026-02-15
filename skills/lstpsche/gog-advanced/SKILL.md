---
name: gog-advanced
description: 可靠的 Google Workspace 命令行工具（gogcli）：  
- 日程查询默认使用所有日历；  
- 数据格式优先采用 JSON；  
- 写入操作安全可靠（数据不会被意外修改）。
metadata: {"clawdbot":{"emoji":"🗂️","requires":{"bins":["gog"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/gogcli","bins":["gog"],"label":"Install gogcli (brew)"}]}}
---

# gog-advanced

使用 `gog`（gogcli）来管理 Google Workspace 的各项服务：Gmail、日历、云端硬盘（Drive）、联系人（Contacts）、表格（Sheets）和文档（Docs）。

此技能旨在提升 **代理程序的可靠性**：
- 建议先使用 **列出/检查功能**，不要直接假设资源ID的正确性。
- 在解析数据时优先使用 `--json` 格式；如果数据格式不符合预期，可回退到手动处理表格数据。
- 对于关于“日程安排/今天/明天/本周”的查询，系统会默认在 **所有日历中搜索**。
- 在执行写入操作（发送邮件、创建/更新事件、修改云端硬盘/表格/文档）之前，务必 **确认操作意图** 并简要说明具体操作内容。

## 先决条件 / 设置（只需执行一次）

1) 存储 OAuth 客户端凭证：
   - `gog auth credentials /path/to/client_secret.json`

2) 添加需要使用的账户：
   - `gog auth add you@gmail.com --services gmail,calendar,drive,contacts,sheets,docs`

3) 将账户设置为默认值，以避免重复输入参数：
   - `export GOG_ACCOUNT=you@gmail.com`

**注意事项：**
- 可通过以下命令查看 `gog` 的使用帮助：`gog --help`、`gog calendar --help` 等。
- `gog` 支持多个账户，可以使用 `--account` 或 `GOG_ACCOUNT` 来指定账户。（建议使用环境变量。）

## 全局代理规则（不可更改）

1) **日历日程查询**
   - 如果用户询问“我今天的日程安排是什么？/明天是什么？/这周有什么安排？/接下来的N天有什么安排？”：
     - 执行命令：`gog calendar events --all --today|--tomorrow|--week|--days N --json`
     - 仅当结果为空时，才需要排查问题（如时区设置、账户信息或授权状态）。
   - 仅当用户明确要求查看特定日历时，才使用 `calendarId` 参数。

2) **日历识别**
   - 如果需要获取日历ID（因为用户指定了特定日历）：
     - 执行命令：`gog calendar calendars --json`
     - 根据日历名称或摘要来识别对应的日历ID。

3) **时区设置**
   - 在进行日期相关的查询时，尽可能使用 `--today/--tomorrow/--week/--days` 参数来指定时间范围。
   - 如果用户的时区设置影响查询结果，可以使用 `gog calendar time --timezone <IANA_TZ>` 来校验时区。
   - 如果 JSON 数据中包含本地化时间信息，建议返回用户所在时区的日期时间。

4) **写入操作需要确认**
   - 在执行以下操作之前，务必先获得用户确认：
     - `gog gmail send ...`
     - `gog calendar create ...`
     - `gog calendar update ...`
     - 任何对表格（Sheets）的更新、追加或清除操作
     - 在执行这些操作前，发送一条确认信息，内容包括接收者、主题、时间范围，并询问用户是否同意操作。

## 常用命令示例

### 日历：查询今天的日程安排
   - 默认查询所有日历：`gog calendar events --all --today --json`

   - 查询明天、本周或接下来3天的日程：`gog calendar events --all --tomorrow --json`
   - `gog calendar events --all --week --json`
   - `gog calendar events --all --days 3 --json`

   - 按关键词搜索日历事件：`gog calendar search "standup" --days 30 --json`
   - `gog calendar search "meeting" --from 2026-02-01T00:00:00Z --to 2026-03-01T00:00:00Z --max 50 --json`

   - （仅当用户要求时）查询特定日历的日程：`gog calendar calendars --json`（获取日历ID），然后使用 `gog calendar events <calendarId> --today --json` 查询该日历的日程。

### Gmail：搜索 + 阅读 + 发送（发送前需确认）
   - 搜索最近7天内的邮件：`gog gmail search 'newer_than:7d' --max 10 --json`
   - 搜索来自特定发件人的邮件（过去30天内）：`gog gmail search 'from:boss@example.com newer_than:30d' --max 20 --json`

   - 发送邮件（发送前需确认）：`gog gmail send --to a@b.com --subject "Hi" --body "Hello"`

### 云端硬盘（Drive）：查找文件
   - `gog drive search "invoice" --max 10 --json`

### 联系人（Contacts）：列出/搜索
   - `gog contacts list --max 50 --json`

### 表格（Sheets）：安全读写（写入前需确认）
   - 读取表格内容：`gog sheets get <sheetId> "Tab!A1:D10" --json`

   - 更新表格内容（写入前需确认）：`gog sheets update <sheetId> "Tab!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED`

   - 向表格中追加数据（写入前需确认）：`gog sheets append <sheetId> "Tab!A:C" --values-json '[["x","y","z"]]' --insert INSERT_ROWS`

   - 清空表格内容（写入前需确认）：`gog sheets clear <sheetId> "Tab!A2:Z"`

### 文档（Docs）：导出/查看内容
   - 导出文档内容：`gog docs export <docId> --format txt --out /tmp/doc.txt`
   - 查看文档内容：`gog docs cat <docId>`

## 故障排查步骤（快速解决）

如果日历查询结果不正确或为空，请按照以下步骤排查：
1) 确认账户信息：`gog auth status`
2) 列出所有可用的日历：`gog calendar calendars --json`
3) 确保查询时使用了所有可用的日历：`gog calendar events --all --today --json`
4) 如果问题仍然存在，检查时区设置是否正确：`gog calendar time --timezone <IANA_TZ>`