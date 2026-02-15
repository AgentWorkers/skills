---
name: zoho
description: 与 Zoho CRM、Projects 和 Meeting 的 API 进行交互。适用于管理交易、联系人、潜在客户、任务、项目、里程碑、会议记录或任何 Zoho 工作区数据。当提到 Zoho、CRM、交易、项目、任务、里程碑、会议或会议记录时，该功能会触发相应的操作。
author: Zone 99 team
homepage: https://99.zone
repository: https://github.com/shreefentsar/clawdbot-zoho
---

# Zoho集成（CRM + 项目 + 会议）

由 [Zone 99](https://99.zone) 开发 · [GitHub](https://github.com/shreefentsar/clawdbot-zoho) 提供 · [欢迎贡献](https://github.com/shreefentsar/clawdbot-zoho/issues)

## 快速入门

使用 `zoho` CLI 工具包——它可自动处理 OAuth 令牌的刷新和缓存。

```bash
zoho help          # Show all commands
zoho token         # Print current access token (auto-refreshes)
```

## 认证设置

### 第1步：注册您的应用程序

1. 访问 [Zoho API 控制台](https://api-console.zoho.com/)
2. 点击 **添加客户端** → 选择 **基于服务器的应用程序**
3. 填写以下信息：
   - **客户端名称**：您的应用程序名称（例如：“Clawdbot Zoho Integration”）
   - **首页 URL**：您的域名或 `https://localhost`
   - **重定向 URI**：`https://localhost/callback`（或您控制的任何 URL——您只需获取一次该 URL 即可）
4. 点击 **创建**
5. 记下 **客户端 ID** 和 **客户端密钥**

### 第2步：生成授权码（获取令牌）

构建以下 URL 并在浏览器中打开它（请替换占位符）：

```
https://accounts.zoho.com/oauth/v2/auth
  ?response_type=code
  &client_id=YOUR_CLIENT_ID
  &scope=ZohoCRM.modules.ALL,ZohoCRM.settings.ALL,ZohoProjects.projects.ALL,ZohoProjects.tasks.ALL,ZohoMeeting.recording.READ,ZohoMeeting.meeting.READ,ZohoMeeting.meetinguds.READ,ZohoFiles.files.READ
  &redirect_uri=https://localhost/callback
  &access_type=offline
  &prompt=consent
```

> **注意：** 请使用与您的数据中心匹配的账户 URL：
> | 地区 | 账户 URL |
> |--------|-------------|
> | 美国 | `https://accounts.zoho.com` |
> | 欧盟 | `https://accounts.zoho.eu` |
> | 印度 | `https://accounts.zoho.in` |
> | 澳大利亚 | `https://accounts.zoho.com.au` |
> | 日本 | `https://accounts.zoho.jp` |
> | 英国 | `https://accounts.zoho.uk` |
> | 加拿大 | `https://accounts.zohocloud.ca` |
> | 南非 | `https://accounts.zoho.sa` |

授权成功后，系统会重定向到如下页面：
```
https://localhost/callback?code=1000.abc123...&location=us&accounts-server=https://accounts.zoho.com
```

复制 `code` 参数的值。**此代码的有效期为2分钟**——请立即进入第3步。

### 第3步：将授权码兑换为刷新令牌

运行以下 curl 命令（请替换占位符）：

```bash
curl -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=https://localhost/callback" \
  -d "code=PASTE_CODE_FROM_STEP_2"
```

响应结果：
```json
{
  "access_token": "1000.xxxx.yyyy",
  "refresh_token": "1000.xxxx.zzzz",
  "api_domain": "https://www.zohoapis.com",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

保存 **refresh_token**——这是您的长期有效凭证。访问令牌的有效期为1小时，但 CLI 会使用刷新令牌自动更新它。

### 第4步：获取您的组织 ID

**CRM/项目组织 ID：**
```bash
# After setting up .env with client_id, client_secret, refresh_token:
zoho raw GET /crm/v7/org | jq '.org[0].id'
```

**会议组织 ID：**
登录 [Zoho Meeting](https://meeting.zoho.com) → 进入管理设置 → 在 URL 或设置页面中查找组织 ID。该 ID 与 CRM 组织 ID 不同。

### 第5步：配置 `.env` 文件

在技能目录下创建一个 `.env` 文件：

```bash
ZOHO_CLIENT_ID=1000.XXXXXXXXXXXXXXXXXXXXXXXXX
ZOHO_CLIENT_SECRET=your_client_secret_here
ZOHO_REFRESH_TOKEN=1000.your_refresh_token_here
ZOHO_ORG_ID=123456789              # CRM/Projects org ID
ZOHO_MEETING_ORG_ID=987654321      # Meeting org ID (different from CRM)
ZOHO_CRM_DOMAIN=https://www.zohoapis.com
ZOHO_PROJECTS_DOMAIN=https://projectsapi.zoho.com/restapi
ZOHO_MEETING_DOMAIN=https://meeting.zoho.com
ZOHO_ACCOUNTS_URL=https://accounts.zoho.com
```

> 如果您使用的是非美国数据中心的服务器，请调整域名 URL（例如：`.eu`、`.in`、`.com.au`）。

### OAuth 权限范围参考

| 权限范围 | 用途 |
|-------|----------|
| `ZohoCRM.modules.ALL` | 读写 CRM 记录（交易、联系人、潜在客户等） |
| `ZohoCRM.settings.ALL` | 读取 CRM 字段定义和组织设置 |
| `ZohoProjects.projects.ALL` | 读写项目信息 |
| `ZohoProjects.tasks.ALL` | 读写任务、里程碑、错误和时间日志 |
| `ZohoMeeting.recording.READ` | 列出并访问会议记录 |
| `ZohoMeeting.meeting.READ` | 列出会议和会议详情 |
| `ZohoMeeting.meetinguds.READ` | 下载录制文件 |
| `ZohoFiles.files.READ` | 下载文件（录制文件、文字记录） |

如果您只需要使用 CRM 或会议功能，可以请求更少的权限范围。权限范围的参数之间用逗号分隔。

### 错误排查

- **"invalid_code"**：授权码已过期（有效期为2分钟）。请重新执行第2步。
- **"invalid_client"**：客户端 ID 错误，或使用的账户-服务器 URL 与数据中心不符。
- **"invalid_redirect_uri"**：curl 命令中的重定向 URI 必须与在 API 控制台中注册的完全一致。
- **令牌刷新失败**：刷新令牌可能会被撤销。请重新执行第2-3步以获取新的令牌。
- **"Given URL is wrong"**：您访问的 API 域名与数据中心不符。

## CRM 命令

```bash
# List records from any module
zoho crm list Deals
zoho crm list Deals "page=1&per_page=5&sort_by=Created_Time&sort_order=desc"
zoho crm list Contacts
zoho crm list Leads

# Get a specific record
zoho crm get Deals 1234567890

# Search with criteria
zoho crm search Deals "(Stage:equals:Closed Won)"
zoho crm search Contacts "(Email:contains:@acme.com)"
zoho crm search Leads "(Lead_Source:equals:Web)"

# Create a record
zoho crm create Contacts '{"data":[{"Last_Name":"Smith","First_Name":"John","Email":"j@co.com"}]}'
zoho crm create Deals '{"data":[{"Deal_Name":"New Project","Stage":"Qualification","Amount":50000}]}'

# Update a record
zoho crm update Deals 1234567890 '{"data":[{"Stage":"Closed Won"}]}'

# Delete a record
zoho crm delete Deals 1234567890
```

### CRM 模块
潜在客户、联系人、账户、交易、任务、事件、电话记录、备注、产品、报价单、销售订单、采购订单、发票

### 搜索操作符
等于（equals）、不等于（not_equal）、以……开头（starts_with）、包含（contains）、不包含（not_contains）、在……范围内（in）、不在……范围内（not_in）、介于……之间（between）、大于（greater_than）、小于（less_than）

## 项目命令

```bash
# List all projects
zoho proj list

# Get project details
zoho proj get 12345678

# Tasks
zoho proj tasks 12345678
zoho proj create-task 12345678 "name=Fix+login+bug&priority=High&start_date=01-27-2026"
zoho proj update-task 12345678 98765432 "percent_complete=50"

# Other
zoho proj milestones 12345678
zoho proj tasklists 12345678
zoho proj bugs 12345678
zoho proj timelogs 12345678
```

### 任务字段
名称（name）、开始日期（start_date，格式为 MM-DD-YYYY）、结束日期（end_date）、优先级（priority，可选值：None/Low/Medium/High）、负责人（owner）、描述（description）、任务列表 ID（tasklist_id）、完成百分比（percent_complete）

## 会议命令

```bash
# List all recordings
zoho meeting recordings
zoho meeting recordings | jq '[.recordings[] | {topic, sDate, sTime, durationInMins, erecordingId}]'

# Download a recording (use downloadUrl from recordings list)
zoho meeting download "https://files-accl.zohopublic.com/public?event-id=..." output.mp4

# List meetings/sessions
zoho meeting list
zoho meeting list "fromDate=2026-01-01T00:00:00Z&toDate=2026-01-31T23:59:59Z"

# Get meeting details
zoho meeting get 1066944216
```

### 会议记录字段
来自 `zoho meeting recordings` 的关键字段：
- `erecordingId` — 加密后的会议记录 ID（用于去重/追踪）
- `topic` — 会议主题
- `sDate`, `sTime` — 会议开始日期和时间（人类可读格式）
- `startTimeinMs` — 会议开始时间（以毫秒为单位）
- `durationInMins` — 会议时长
- `downloadUrl` / `publicDownloadUrl` — MP4 录制文件下载链接
- `transcriptionDownloadUrl` — Zoho 生成的文字记录链接（如有）
- `summaryDownloadUrl` — Zoho 生成的会议摘要链接（如有）
- `fileSize` / `fileSizeInMB` — 录制文件大小
- `status` — 例如：`UPLOADED`（表示文件已上传）
- `meetingKey` — 会议标识符
- `creatorName` — 录制会议的发起者

### 会议记录处理流程
用于自动化会议总结的脚本位于 `scripts/standup-summarizer.sh` 中。

## 原始 API 调用

对于未包含在子命令中的功能，请使用原始 API 调用。

## 使用示例

### 检查交易/项目进度
```bash
zoho crm list Deals "sort_by=Created_Time&sort_order=desc&per_page=10" | jq '.data[] | {Deal_Name, Stage, Amount, Closing_Date}'
```

### 检查项目进度
```bash
zoho proj list | jq '.projects[] | {name, status, id: .id_string}'
zoho proj tasks <project_id> | jq '.tasks[] | {name, status: .status.name, percent_complete, priority}'
```

### 从对话中创建任务
```bash
zoho proj create-task <project_id> "name=Task+description&priority=High&start_date=MM-DD-YYYY&end_date=MM-DD-YYYY"
```

### 总结会议记录
```bash
# Quick list of recent recordings
zoho meeting recordings | jq '[.recordings[:5] | .[] | {topic, sDate, sTime, durationInMins, fileSize}]'

# Download latest recording
URL=$(zoho meeting recordings | jq -r '.recordings[0].downloadUrl')
zoho meeting download "$URL" /tmp/latest.mp4
```

## 速率限制
- CRM：每分钟 100 次请求
- 项目：根据套餐不同而有所差异
- 会议：遵循标准 API 限制
- 令牌刷新：请按需调用（系统会自动缓存）

## 参考资料
- [CRM API 字段](references/crm-api.md)
- [项目 API 端点](references/projects-api.md)
- [会议 API 参考](references/meeting-api.md)