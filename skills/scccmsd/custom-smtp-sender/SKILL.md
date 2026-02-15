---
name: custom-smtp-sender
description: **技能说明：**  
该技能用于发送包含 Markdown、HTML 文本及附件的电子邮件，同时利用 `/home/bb/.openclaw/smtp-config.json` 中配置的 SMTP 服务器进行发送。系统支持重试机制，并对发送过程进行日志记录。
---

# 自定义 SMTP 发送器

这是一个自定义技能，用于发送带有高级功能的电子邮件，包括 HTML/Markdown 转换、附件以及重试处理。该工具能够整合现有的配置，确保操作的安全性和可靠性。

## 主要功能
- **HTML/Markdown 支持**：使用 Markdown 编写邮件，并将其转换为 HTML 格式发送。
- **附件**：可以轻松添加一个或多个文件作为邮件附件。
- **重试机制**：在遇到临时故障时，会尝试重新发送邮件。
- **日志记录**：记录发送的邮件和出现的错误信息，以便进行审计。

## 先决条件
- **SMTP 配置文件**：`smtp-config.json`，位于 `/home/bb/.openclaw/` 目录下。

**示例代码：**
```json
{
  "server": "smtp.exmail.qq.com",
  "port": 465,
  "username": "your-email@example.com",
  "password": "your-password",
  "emailFrom": "your-email@example.com",
  "useTLS": true
}
```

请确保文件的权限设置安全（使用 `chmod 600` 命令）。

## 使用方法
- **发送普通邮件**：
```bash
custom-smtp-sender send --to "recipient@example.com" --subject "Hello" --body "你好"
```

- **发送带附件的 HTML 邮件**：
```bash
custom-smtp-sender send \
  --to "recipient@example.com" \
  --subject "Weekly Report" \
  --body "**Important updates inside.** See attached." \
  --html \
  --attachments path/to/file.pdf
```

## 错误处理
该工具在失败时会尝试最多 3 次重新发送，并详细记录每次尝试的情况。如果出现网络问题或身份验证问题，也会进行相应的日志记录。

## 未来扩展计划
- 支持抄送（CC）/密送（BCC）字段
- 邮件定时发送（与 cron 任务集成）
- 提供邮件模板

只需设置一次 SMTP 服务，您就可以将邮件发送功能集成到您的工作流程中！