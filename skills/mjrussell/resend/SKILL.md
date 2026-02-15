---
name: resend
description: 通过 Resend API 管理收到的（入站）电子邮件及其附件。当用户询问他们的电子邮件、收到的消息或电子邮件附件时，可以使用此功能。
homepage: https://resend.com
metadata:
  clawdbot:
    emoji: "📧"
    requires:
      bins: ["resend"]
      env: ["RESEND_API_KEY"]
---

# 重新发送邮件（Resend Email）

这是一个用于重新发送邮件的命令行工具（CLI），它支持查询接收到的（入站）邮件及其附件。

## 安装

```bash
npm install -g @mjrussell/resend-cli
```

## 设置

1. 在 [resend.com](https://resend.com) 注册账号。
2. 为你的域名配置入站邮件路由。
3. 在“API Keys”页面创建API密钥（需要具备读取权限）。
4. 设置环境变量：`export RESEND_API_KEY="your_api_key"`。

## 命令

### 列出所有邮件

```bash
resend email list              # List recent emails (default 10)
resend email list -l 20        # List 20 emails
resend email list --json       # Output as JSON
```

### 查看邮件详情

```bash
resend email get <id>          # Show email details
resend email get <id> --json   # Output as JSON
```

### 查看邮件附件

```bash
resend email attachments <email_id>                    # List attachments
resend email attachment <email_id> <attachment_id>     # Get attachment metadata
resend email attachments <email_id> --json             # Output as JSON
```

### 查看已配置的域名

```bash
resend domain list             # List configured domains
resend domain get <id>         # Get domain details with DNS records
resend domain list --json      # Output as JSON
```

## 使用示例

**用户：“我有什么新邮件吗？”**
```bash
resend email list -l 5
```

**用户：“显示最新的邮件。”**
```bash
resend email list --json | jq -r '.data.data[0].id'  # Get ID
resend email get <id>
```

**用户：“那封邮件里有哪些附件？”**
```bash
resend email attachments <email_id>
```

**用户：“我配置了哪些域名？”**
```bash
resend domain list
```

**用户：“显示邮件X的完整内容。”**
```bash
resend email get <email_id>
```

## 注意事项

- 该CLI仅支持接收到的（入站）邮件，不支持发送邮件。
- 可使用 `--json` 标志并将输出结果通过管道（`|`）传递给 `jq` 工具进行脚本处理。
- 邮件ID以UUID的形式显示在列表中。