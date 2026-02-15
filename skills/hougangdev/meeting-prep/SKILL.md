---
name: meeting-prep
description: "自动化会议准备和每日提交总结功能：适用于在 Google 日历中查看即将召开的会议、根据 GitHub 的提交记录生成站立会议更新内容，或发送每日开发进度总结。该功能会从 GitHub 获取会议日程和提交历史记录，然后生成易于开发者阅读的详细更新信息。"
---

# 会议准备

为开发团队提供自动化的会议准备功能以及每日提交摘要。

## 功能

1. **会议准备**：检查 Google 日历中即将举行的会议（包含视频链接），通知相关用户，并根据提交记录生成会议更新信息。
2. **每日摘要**：汇总当天所有开发者的提交记录。

## 设置要求

### Google 日历 OAuth

在 Google Cloud Console 中创建 OAuth 凭据：

1. 启用 Google 日历 API。
2. 创建 OAuth 2.0 桌面应用程序凭据。
3. 将 `client_secret.json` 文件保存在 `credentials/` 目录下。
4. 授权访问权限：`https://www.googleapis.com/auth/calendar`。
5. 将生成的访问令牌保存在 `credentials/calendar_tokens.json` 文件中。
   （如使用多个账户，请为每个账户分别保存令牌文件。）

### GitHub 令牌

创建一个具有 `repo` 权限范围的经典个人访问令牌，并将其保存在 `credentials/github_token` 文件中。

## 工作流程

### 会议准备检查

触发条件：每 15 分钟或通过心跳事件触发。

1. 查询配置好的日历中接下来 45 分钟内的事件。
2. 过滤出包含 Google Meet 链接（`hangoutLink` 或 `conferenceData`）的事件。
3. 如果会议在 30–45 分钟后举行且用户尚未收到通知：
   - 询问用户：“[会议标题] 将在 X 分钟后举行。你上次更新是什么时候？我应该检查哪些仓库？”
   - 在状态文件中记录相关信息，以避免重复通知。
4. 如果会议在 10–20 分钟后举行：
   - 根据提交记录生成会议更新信息，并发送格式化的通知。

### 每日提交摘要

触发条件：每天结束时通过 Cron 任务触发。

1. 从配置好的仓库中获取当天的所有提交记录。
2. 包括所有开发者的提交信息。
3. 按仓库和子目录对提交记录进行分组。
4. 显示提交者的姓名。
5. 发送格式化的摘要信息。

## API 参考

### 检查日历

```bash
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
LATER=$(date -u -d "+45 minutes" +%Y-%m-%dT%H:%M:%SZ)
TOKEN=$(jq -r '.access_token' credentials/calendar_tokens.json)

curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=$NOW&timeMax=$LATER&singleEvents=true" \
  -H "Authorization: Bearer $TOKEN" | \
  jq '[.items[] | select(.hangoutLink != null or .conferenceData != null)]'

Refresh Token

CLIENT_ID=$(jq -r '.installed.client_id' credentials/client_secret.json)
CLIENT_SECRET=$(jq -r '.installed.client_secret' credentials/client_secret.json)
REFRESH_TOKEN=$(jq -r '.refresh_token' credentials/calendar_tokens.json)

curl -s -X POST https://oauth2.googleapis.com/token \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "refresh_token=$REFRESH_TOKEN" \
  -d "grant_type=refresh_token"

Fetch Commits

TOKEN=$(cat credentials/github_token)
SINCE=$(date -u -d "-7 days" +%Y-%m-%dT%H:%M:%SZ)

# List org repos
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/orgs/ORG_NAME/repos?per_page=50&sort=pushed"

# Get commits
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/ORG/REPO/commits?since=$SINCE&per_page=30"

Output Format

Plain text, no markdown, no emojis:

Update - [DATE]

[repo-name]

[subdirectory]
• Verbose description of change (Author)
• Another change (Author)

Today
• [user input]

Blockers
• None

Discussion
• None

Formatting Rules

• Group by repo, then subdirectory
• Summarize commits into meaningful descriptions
• Include author names
• Plain text only for easy copy-paste
State Management

Track state in data/meeting-prep-state.json:

{
  "notified": {},
  "config": {
    "repoFilter": "org-name/*"
  }
}
```