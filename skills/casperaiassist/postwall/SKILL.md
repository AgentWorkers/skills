---
name: postwall
description: 用于AI代理的安全电子邮件网关：在读取和发送电子邮件时需要人工审核（human-in-the-loop approval）。您可以在 [https://postwallapp.com](https://postwallapp.com) 获取API密钥。
homepage: https://postwallapp.com
user-invocable: true
metadata: {"version":"1.7.0","author":"postwallapp","license":"MIT","homepage":"https://postwallapp.com","repository":"https://github.com/postwallapp/postwall","openclaw":{"requires":{"bins":["postwall"],"env":["POSTWALL_API_KEY"]},"primaryEnv":"POSTWALL_API_KEY","install":[{"id":"npm","kind":"node","package":"postwall","bins":["postwall"],"label":"Install PostWall CLI (npm)"}]}}
---
# PostWall 邮件处理技能

PostWall 是一个位于 AI 代理与电子邮件系统之间的安全层。使用此技能，您可以执行以下操作：
- 阅读已获得人工审核的电子邮件
- 通过提交草稿的方式发送电子邮件（发送前需要人工审核）

## 设置

首先，使用您的 API 密钥进行身份验证（请从 PostWall 控制面板获取该密钥）：

```bash
postwall auth pw_your_api_key_here
```

## 命令

### 检查新邮件

返回未读且已获审核的邮件数量。适用于轮询操作。

```bash
postwall check              # Returns: 5
postwall check --json       # Returns: {"count": 5}
```

### 列出已审核的邮件

显示所有未读且已获审核的邮件。

```bash
postwall inbox              # Human-readable list
postwall inbox --json       # JSON format
postwall inbox --limit 10   # Limit results
```

### 阅读特定邮件

通过邮件 ID 读取邮件。**此操作会将邮件标记为已读**——该邮件将不再出现在后续的收件箱查询中。

```bash
postwall read <email-id>           # Shows email content
postwall read <email-id> --json    # JSON format
```

### 将邮件标记为已读（无需下载内容）

将一个或多个邮件标记为已读，而无需下载其内容。适用于批量处理或仅需要处理邮件元数据的情况。

```bash
postwall mark-read <id1>                  # Mark single email as read
postwall mark-read <id1> <id2> <id3>      # Mark multiple emails as read
postwall mark-read <id1> <id2> --json     # JSON format
```

**使用场景：**
- 在使用 `inbox --json` 获取邮件元数据后，将邮件标记为已处理
- 批量标记您已经处理过的邮件
- 跳过不需要完整阅读的邮件

**JSON 输出格式：**
```json
{
  "success": true,
  "marked": 3,
  "failed": 0,
  "results": [
    {"id": "abc123", "success": true},
    {"id": "def456", "success": true},
    {"id": "ghi789", "success": true}
  ]
}
```

### 发送电子邮件（提交草稿）

提交电子邮件草稿以供人工审核。邮件在控制面板获得批准之前不会被发送。

```bash
postwall draft --to "recipient@example.com" --subject "Hello" --body "Email content here"
postwall draft --to "user@example.com" --subject "Report" --body "..." --json
```

**返回一个审批 URL**，您可以将该 URL 分享给用户以便快速审批：

```
Draft submitted successfully!
Draft ID: abc123-uuid
Status: pending

Approval URL: https://www.postwallapp.com/dashboard/drafts/abc123-uuid
Share this URL with the user to approve the email.
```

**JSON 输出包含 `approveUrl`：**
```json
{
  "success": true,
  "draft": {
    "id": "abc123-uuid",
    "status": "pending",
    "created_at": "2024-02-12T10:30:00Z",
    "approveUrl": "https://www.postwallapp.com/dashboard/drafts/abc123-uuid"
  },
  "message": "Draft submitted for approval"
}
```

### 更新草稿

更新现有的待审核草稿。当用户要求在批准前对邮件进行修改时非常有用。

```bash
postwall update <draft-id> --subject "New subject"
postwall update <draft-id> --body "Updated email content"
postwall update <draft-id> --to "new-recipient@example.com" --subject "New subject" --body "New content"
postwall update <draft-id> --subject "Refined subject" --json
```

**注意：** 只能更新待审核的草稿。一旦草稿被发送或拒绝，就无法再修改。

**JSON 输出格式：**
```json
{
  "success": true,
  "draft": {
    "id": "abc123-uuid",
    "to": "recipient@example.com",
    "subject": "Refined subject",
    "body": "Updated content",
    "status": "pending",
    "createdAt": "2024-02-12T10:30:00Z",
    "updatedAt": "2024-02-12T11:00:00Z"
  },
  "message": "Draft updated successfully"
}
```

### 检查草稿状态

检查草稿的状态：等待审核、已批准或已发送。

```bash
postwall status <draft-id>         # Shows status
postwall status <draft-id> --json  # Returns: {"draft": {"id": "...", "status": "pending"}}
```

状态值：
- `pending`：等待人工审核
- `approved`：已批准，正在发送中
- `rejected`：被用户拒绝
- `sent`：已成功发送

### 列出草稿

列出所有草稿，并可添加状态过滤条件。

```bash
postwall drafts                    # All drafts
postwall drafts --status pending   # Only pending drafts
postwall drafts --json             # JSON format
```

## 常见工作流程

### 定期检查邮件

```bash
# Check if there are new emails
count=$(postwall check)
if [ "$count" -gt 0 ]; then
  # Process new emails
  postwall inbox --json | process_emails
fi
```

### 批量处理邮件（仅获取元数据）

当您只需要邮件的元数据（发件人、主题、日期）而不需要完整内容时：

```bash
# Get email list with metadata
emails=$(postwall inbox --json)

# Process metadata (e.g., filter by subject or sender)
ids=$(echo "$emails" | jq -r '.emails[] | select(.subject | contains("Report")) | .id')

# Mark processed emails as read without fetching content
postwall mark-read $ids
```

### 发送并跟踪邮件

```bash
# Submit draft
result=$(postwall draft --to "user@example.com" --subject "Hello" --body "Content" --json)
draft_id=$(echo "$result" | jq -r '.draft.id')
approve_url=$(echo "$result" | jq -r '.draft.approveUrl')

# Share the approval URL with the user
echo "Please approve this email: $approve_url"

# Check status later
postwall status "$draft_id"
```

### 根据用户反馈修改草稿

当用户在批准前要求对草稿进行修改时：

```bash
# User asks: "Make the subject line shorter and add a greeting"
postwall update "$draft_id" --subject "Q4 Report" --body "Hi Team,

Here is the quarterly report..."

# The draft is updated, user can now approve from the same URL
```

## 输出格式

所有命令都支持使用 `--json` 选项以获取结构化输出，便于脚本编写和自动化操作。

## 错误处理

命令执行失败时会返回代码 1。使用 `--json` 选项时，错误信息将以 JSON 格式返回：

```json
{"error": "Error message here"}
```

## 轮询新邮件

作为代理，您应定期检查是否有新的已审核邮件：
1. 运行 `postwall check` 以获取未读且已审核的邮件数量
2. 如果数量大于 0，则运行 `postwall inbox --json` 以获取邮件列表
3. 使用 `postwall read <id>` 处理每封邮件

**推荐的轮询频率：** 在活跃会话期间每 5-10 分钟检查一次，或在用户表示需要接收新邮件时进行检查。

**示例轮询工作流程：**
```bash
# Check if there are new emails
count=$(postwall check)
if [ "$count" -gt 0 ]; then
  # Fetch and process new emails
  postwall inbox --json
fi
```

## 注意事项：

- 电子邮件只有在获得 PostWall 控制面板的人工审核后才会显示
- 阅读邮件后，该邮件会被标记为已读——不会再出现在后续的收件箱查询中
- 草稿在发送前需要人工审核
- API 密钥存储在 `~/.postwall/config.json` 文件中