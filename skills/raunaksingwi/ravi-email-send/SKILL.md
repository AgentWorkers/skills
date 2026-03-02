---
name: ravi-email-send
description: 您可以发送、撰写、回复、全部回复或转发带有 HTML 格式和附件的电子邮件。请勿使用该功能来阅读收到的邮件（请使用 ravi-inbox），也不要用它来管理用户名和密码（请使用 ravi-passwords 或 ravi-vault）。
---
# Ravi Email — 发送邮件

您可以使用 Ravi 的电子邮件地址来撰写新邮件、回复现有邮件或转发邮件，并可选择附加文件。

> **邮件内容的撰写质量至关重要。** 在起草邮件内容之前，请参考 **ravi-email-writing** 技能文档，了解邮件主题行、HTML 格式、语气以及反垃圾邮件的最佳实践。

## 撰写新邮件

```bash
ravi email compose --to "recipient@example.com" --subject "Subject" --body "<p>HTML content</p>" --json
```

**参数说明：**
- `--to`（必选）：收件人电子邮件地址
- `--subject`（必选）：邮件主题行
- `--body`（必选）：邮件正文（支持 HTML 格式——可使用 `<p>`, `<h2>`, `<ul>` 等标签进行排版）
- `--cc`：抄送收件人（用逗号分隔）
- `--bcc`：密送收件人（用逗号分隔）
- `--attach`：附件文件路径（可重复输入以附加多个文件）

**示例（包含 HTML 格式和附件）：**
```bash
ravi email compose --to "user@example.com" --subject "Monthly Report" \
  --body "<h2>Monthly Report</h2><p>Key findings:</p><ul><li>Revenue up 15%</li><li>Churn down 3%</li></ul>" \
  --attach report.pdf --json
```

## 回复邮件

```bash
# Reply to sender only
ravi email reply <message_id> --subject "Re: Original Subject" --body "<p>Reply content</p>" --json

# Reply to all recipients
ravi email reply-all <message_id> --subject "Re: Original Subject" --body "<p>Reply content</p>" --json
```

**参数说明：**
- `--subject`（必选）：邮件主题行
- `--body`（必选）：邮件正文（支持 HTML 格式——可使用 `<p>`, `<h2>`, `<ul>` 等标签进行排版）
- `--cc`：抄送收件人（用逗号分隔）
- `--bcc`：密送收件人（用逗号分隔）
- `--attach`：附件文件路径（可重复输入以附加多个文件）

**示例（包含抄送功能）：**
```bash
ravi email reply <message_id> --subject "Re: Project Update" --body "<p>Adding the team.</p>" --cc "team@example.com" --json
```

**注意：** 由于邮件在服务器上进行端到端加密，因此必须提供邮件主题行。

## 转发邮件

```bash
ravi email forward <message_id> --to "recipient@example.com" --subject "Fwd: Original Subject" --body "<p>FYI — see below.</p>" --json
```

**参数说明：**
- `--to`（必选）：收件人电子邮件地址
- `--subject`（必选）：邮件主题行
- `--body`（必选）：邮件正文（支持 HTML 格式——可使用 `<p>`, `<h2>`, `<ul>` 等标签进行排版）
- `--cc`：抄送收件人（用逗号分隔）
- `--bcc`：密送收件人（用逗号分隔）
- `--attach`：附件文件路径（可重复输入以附加多个文件）

**注意：** 由于邮件在服务器上进行端到端加密，因此必须提供邮件主题行。

## 附件

当您使用 `--attach` 选项时，附件会自动上传。Ravi CLI 会：
1. 验证文件格式（如 `.exe` 等危险文件类型会被立即拒绝）
2. 从服务器获取预签名的上传 URL
3. 直接将文件上传到云存储
4. 在邮件中包含附件的 UUID（唯一标识符）

**禁止的文件类型：`.exe`, `.dll`, `.bat`, `.cmd`, `.msi`, `.iso`, `.dmg`, `.apk` 等**

**附件大小限制：** 每个附件的最大大小为 10 MB。

## 发送频率限制

每个用户账户的邮件发送频率受到限制：
- 每小时 60 封邮件
- 每天 500 封邮件
- 每小时最多上传 200 个附件

如果达到发送频率限制，系统会返回 429 错误，并显示 `retry_after_seconds` 值。请等待该时间后再尝试发送。

**操作建议：**
- 尽量避免频繁发送邮件——尽可能采用批量处理的方式
- 遇到 429 错误时，解析 `retry_after_seconds` 值，等待相应时间后再重试
- 在批量发送邮件时，每次发送之间请间隔 1-2 秒。

## 重要提示：
- **HTML 邮件正文：** `--body` 参数支持使用 HTML 格式。可以使用 `<p>`, `<h2>`, `<ul>`, `<a href="...">` 等标签进行排版。无需使用 `<html>` 或 `<body>` 标签。详情请参考 **ravi-email-writing** 文档中的模板和反垃圾邮件规则。
- **务必使用 `--json` 参数**：系统生成的输出格式为 JSON，不适合人工阅读。

## 相关技能：
- **ravi-email-writing**：邮件主题行、HTML 模板、语气设置及反垃圾邮件最佳实践
- **ravi-inbox**：在回复或转发邮件前查看收件箱中的邮件
- **ravi-identity**：获取您的电子邮件地址和身份名称用于签名
- **ravi-feedback**：报告邮件发送问题或提出改进建议