---
name: resend-email
description: 使用 Resend API 发送电子邮件。当用户无需配置 SMTP 服务器即可发送电子邮件时，可以使用该 API。支持发送纯文本邮件和 HTML 邮件，支持多个收件人、抄送（CC）和密送（BCC），以及批量发送功能。非常适合用于发送通知、警报、新闻通讯和自动化邮件工作流程。
---
# 重新发送邮件

通过 Resend API 发送邮件——无需配置 SMTP。

## 快速入门

### 1. 配置

在 `.env` 文件中设置环境变量：

```bash
RESEND_API_KEY=your_resend_api_key
RESEND_FROM=onboarding@resend.dev  # Optional, defaults to Resend test domain
```

在 https://resend.com 获取 API 密钥

### 2. 发送邮件

```bash
openclaw run resend-email \
  --to="recipient@example.com" \
  --subject="Hello" \
  --text="Plain text message"
```

## 使用方法

### 基本文本邮件

```bash
openclaw run resend-email \
  --to="user@example.com" \
  --subject="Notification" \
  --text="Your task is complete."
```

### HTML 邮件

```bash
openclaw run resend-email \
  --to="user@example.com" \
  --subject="Welcome" \
  --html="<h1>Welcome!</h1><p>Thanks for joining.</p>"
```

### 多个收件人

```bash
openclaw run resend-email \
  --to="user1@example.com,user2@example.com,user3@example.com" \
  --subject="Team Update" \
  --text="Meeting at 3 PM."
```

### 抄送 (CC) 和密送 (BCC)

```bash
openclaw run resend-email \
  --to="primary@example.com" \
  --cc="manager@example.com" \
  --bcc="archive@example.com" \
  --subject="Report" \
  --text="Please find the attached report."
```

### 通过代理发送邮件

当代理需要发送邮件时：

```bash
# Use exec to call the skill
exec openclaw run resend-email \
  --to="recipient@example.com" \
  --subject="Automated Notification" \
  --text="This email was sent automatically by the agent."
```

## 配置选项

| 变量 | 是否必填 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `RESEND_API_KEY` | 是 | - | 你的 Resend API 密钥 |
| `RESEND_FROM` | 否 | `onboarding@resend.dev` | 默认发件人地址 |

## 发件人地址

- **测试域名**: `onboarding@resend.dev`（默认，无需设置）
- **自定义域名**: `noreply@yourdomain.com`（需要在 Resend 控制面板中进行域名验证）

## 限制

- 不支持附件（Resend API 要求使用 base64 编码）
- 邮件发送频率受 Resend 计划限制
- 邮件大小受 Resend 文档中的规定限制

## 故障排除

**“RESEND_API_KEY 未配置”**
- 在 `.env` 文件或环境中设置 `RESEND_API_KEY`

**“发送邮件失败：未经授权”**
- 确认 API 密钥正确且有效
- 验证 API 密钥是否具有发送邮件的权限

**“发送邮件失败：请求错误”**
- 检查收件人电子邮件格式是否有效
- 验证发件人地址是否已通过验证（对于自定义域名）

## 资源

- `scripts/send_email.py` - 主要的邮件发送脚本