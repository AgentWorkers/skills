---
name: clawback
description: Gmail安全代理，具备策略执行、审批工作流程和审计日志记录功能。适用于用户希望在阅读、搜索或发送Gmail邮件时增加安全保护的需求；某些发送操作在执行前可能需要人工审批。
homepage: https://clawback.sh
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["clawback"] },
        "install": [],
      },
  }
---
# clawback

`clawback` 是一个用于管理 Gmail 操作的工具，支持策略执行功能。所有操作都会通过一个服务器端代理进行，该代理负责执行策略并记录审计日志。某些操作可能需要人工审批。

**安装（如果尚未安装）：**

```bash
curl -fsSL https://clawback.sh/install | bash
```

**首次设置：**
- 执行 `clawback auth login`（设备端操作，会打开浏览器）
- 执行 `clawback auth status`（验证连接状态）

**常用命令：**
- **Gmail 搜索：**
  `clawback gmail search 'newer_than:7d' --max 10`
  `clawback gmail search 'from:boss@company.com' --all --json`
- **Gmail 获取邮件：**
  `clawback gmail get <messageId> --json`
- **Gmail 发送邮件：**
  `clawback gmail send --to a@b.com --subject "Hi" --body "Hello"`
  `clawback gmail send --to a@b.com --subject "Hi" --body-file ./message.txt`
  `clawback gmail send --to a@b.com --subject "Hi" --body-file -`
  `clawback gmail send --to a@b.com --subject "Hi" --body-html "<p>Hello</p>`
  `clawback gmail send --to a@b.com --subject "Hi" --body-html "<p>Hello</p>"`
  `clawback gmail send --to a@b.com --subject "Re: Hi" --body "Reply" --reply-to-message-id <msgId> --thread-id <threadId>`
  `clawback gmail send --to a@b.com --subject "Report" --body "See attached" --attach ./report.pdf`
- **Gmail 线程管理：**
  `clawback gmail thread list 'subject:meeting' --max 20`
  `clawback gmail thread get <threadId> --json`
  `clawback gmail thread modify <threadId> --add STARRED --remove UNREAD`
- **标签管理：**
  `clawback gmail labels list`
  `clawback gmail labels create --name "Important/Clients"`
  `clawback gmail labels modify <messageId> --add STARRED --remove UNREAD`
- **草稿管理：**
  `clawback gmail drafts list --json`
  `clawback gmail drafts create --to a@b.com --subject "Draft" --body "WIP"`
  `clawback gmail drafts send <draftId>`（可能触发审批流程，返回码为 8）
  `clawback gmail drafts delete <draftId>`
- **附件管理：**
  `clawback gmail attachment <messageId> <attachmentId> --out ./file.pdf`
- **邮件历史记录：**
  `clawback gmail history --since <historyId> --max 50`
- **批量操作：**
  `clawback gmail batch delete <id1> <id2> <id3>`
  `clawback gmail batch modify <id1> <id2> --add INBOX --remove SPAM`
- **其他设置：**
  `clawback gmail settings filters list --json`
  `clawback gmail settings send-as list`
  `clawback gmail settings vacation get`
  `clawback gmail settings forwarding list`
  `clawback gmail settings delegates list`
  `clawback gmail settings delegates list`
- **审批流程：**
  邮件发送可能会被 `approve_before_send` 策略拦截。在这种情况下：
    1. `clawback send` 命令会以返回码 **8** 结束执行，并显示审批 ID。
    2. 需要通过仪表板或电子邮件链接进行人工审批。
    3. 审批通过后，服务器会自动发送邮件。
    4. 如果审批被拒绝或过期，系统会通知用户。

**返回码说明：**
- **0**：操作成功
- **1**：发生意外错误
- **3**：没有找到结果（使用 `--fail-empty` 选项时）
- **4**：未认证——请执行 `clawback auth login`
- **6**：被策略阻止（仅允许读取）——通知用户
- **8**：审批待处理——持续查询 `clawback approvals get <approvalId>` 直到审批结果确定
- **130**：操作取消

**注意事项：**
- 可以通过设置 `CB_SERVER=https://your-server.example.com` 来覆盖默认服务器地址。
- 在脚本中使用 `--json`、`--no-input` 和 `--fail-empty` 选项可简化操作。
- `--connection <id>` 用于指定要使用的 Gmail 连接；如果已连接，则系统会自动选择合适的连接。
- `--all` 选项可自动分页显示搜索结果（适用于 `gmail search` 和 `clawback gmail thread list`）。
- `--select field1,field2` 可将 JSON 输出限制在特定字段内。
- `--results-only` 选项会去除邮件头部信息，仅返回数据内容。
- 在发送邮件前请务必确认结果。如果返回码为 8，请勿重试，等待人工审批。